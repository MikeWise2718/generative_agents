"""
LLM Configuration and API abstraction layer.
Supports OpenAI direct and OpenRouter APIs.

Usage:
    Set OPENROUTER_API_KEY env var to use OpenRouter.
    Optionally set OPENROUTER_MODEL to override the default model.
    If no OpenRouter key, falls back to OpenAI via utils.py.
"""
import os
import openai

# Global state
_api_type = "openai"  # "openai" or "openrouter"
_current_model = "gpt-4o-mini"
_custom_model = None
_initialized = False

# Token tracking
_usage_stats = {
    "input_tokens": 0,
    "output_tokens": 0,
    "embedding_tokens": 0,
    "requests": 0
}

# Model pricing per 1M tokens (as of Dec 2024)
MODEL_PRICING = {
    # OpenAI models
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
    # OpenRouter format
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "openai/gpt-4o": {"input": 2.50, "output": 10.00},
    "openai/text-embedding-3-small": {"input": 0.02, "output": 0.0},
    # Anthropic models (via OpenRouter)
    "anthropic/claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "anthropic/claude-3-haiku": {"input": 0.25, "output": 1.25},
    # Default fallback
    "default": {"input": 0.50, "output": 2.00},
}


def init_llm_api():
    """
    Initialize LLM API based on environment variables.
    Call this once at startup.

    Returns tuple: (api_type, model_name)
    """
    global _api_type, _current_model, _custom_model, _initialized

    if _initialized:
        return (_api_type, _current_model)

    openrouter_key = os.environ.get("OPENROUTER_API_KEY")

    if openrouter_key:
        openai.api_key = openrouter_key
        openai.api_base = "https://openrouter.ai/api/v1"
        _api_type = "openrouter"

        # Check for custom model override
        custom_model = os.environ.get("OPENROUTER_MODEL")
        if custom_model:
            _custom_model = custom_model
            _current_model = custom_model
        else:
            _current_model = "openai/gpt-4o-mini"

        print(f"Using OpenRouter API (model: {_current_model})")
    else:
        # Fall back to OpenAI
        _api_type = "openai"
        _current_model = "gpt-4o-mini"

        # Try environment variable first, then utils.py
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            openai.api_key = openai_key
        else:
            try:
                from utils import openai_api_key
                openai.api_key = openai_api_key
            except ImportError:
                print("WARNING: No API key found. Set OPENROUTER_API_KEY or OPENAI_API_KEY")

        print(f"Using OpenAI API (model: {_current_model})")

    _initialized = True
    return (_api_type, _current_model)


def get_api_type():
    """Get the current API type ('openai' or 'openrouter')."""
    return _api_type


def get_model_name(base_model):
    """
    Get the appropriate model name based on API type.

    Args:
        base_model: The base model name (e.g., "gpt-4o-mini")

    Returns:
        The model name formatted for the current API
    """
    # If using OpenRouter with custom model, use that for chat models
    if _api_type == "openrouter" and _custom_model:
        # Don't override embedding models
        if "embedding" not in base_model.lower():
            return _custom_model

    # Map to OpenRouter format if needed
    if _api_type == "openrouter":
        # If already in OpenRouter format, return as-is
        if "/" in base_model:
            return base_model
        # Map OpenAI model names to OpenRouter format
        model_map = {
            "gpt-4o-mini": "openai/gpt-4o-mini",
            "gpt-4o": "openai/gpt-4o",
            "text-embedding-3-small": "openai/text-embedding-3-small",
        }
        return model_map.get(base_model, f"openai/{base_model}")

    return base_model


def get_headers():
    """
    Get extra headers for API requests.
    OpenRouter requires/recommends additional headers.
    """
    if _api_type == "openrouter":
        return {
            "HTTP-Referer": "https://github.com/joonspk-research/generative_agents",
            "X-Title": "Generative Agents Simulation"
        }
    return {}


def track_usage(response):
    """
    Track token usage from API response.

    Args:
        response: The API response object (dict or OpenAI response)
    """
    global _usage_stats

    try:
        # Handle dict response
        if isinstance(response, dict):
            usage = response.get("usage", {})
        else:
            # Handle OpenAI response object
            usage = getattr(response, "usage", {})
            if hasattr(usage, "_asdict"):
                usage = usage._asdict()
            elif hasattr(usage, "__dict__"):
                usage = usage.__dict__

        if usage:
            _usage_stats["input_tokens"] += usage.get("prompt_tokens", 0)
            _usage_stats["output_tokens"] += usage.get("completion_tokens", 0)
            _usage_stats["requests"] += 1
    except Exception as e:
        # Don't crash on tracking errors
        pass


def track_embedding_usage(response):
    """
    Track token usage from embedding API response.
    """
    global _usage_stats

    try:
        if isinstance(response, dict):
            usage = response.get("usage", {})
        else:
            usage = getattr(response, "usage", {})
            if hasattr(usage, "__dict__"):
                usage = usage.__dict__

        if usage:
            _usage_stats["embedding_tokens"] += usage.get("total_tokens", 0)
            _usage_stats["requests"] += 1
    except Exception:
        pass


def get_usage_stats():
    """Return current usage statistics."""
    return _usage_stats.copy()


def reset_usage_stats():
    """Reset usage statistics for a new run."""
    global _usage_stats
    _usage_stats = {
        "input_tokens": 0,
        "output_tokens": 0,
        "embedding_tokens": 0,
        "requests": 0
    }


def print_usage_summary():
    """Print usage summary with cost estimate."""
    stats = _usage_stats

    # Get pricing for current model
    model_pricing = MODEL_PRICING.get(_current_model, MODEL_PRICING["default"])
    embedding_pricing = MODEL_PRICING.get("text-embedding-3-small", {"input": 0.02})

    # Calculate costs
    input_cost = (stats["input_tokens"] / 1_000_000) * model_pricing["input"]
    output_cost = (stats["output_tokens"] / 1_000_000) * model_pricing["output"]
    embedding_cost = (stats["embedding_tokens"] / 1_000_000) * embedding_pricing["input"]
    total_cost = input_cost + output_cost + embedding_cost

    total_tokens = stats["input_tokens"] + stats["output_tokens"] + stats["embedding_tokens"]

    print("\n" + "=" * 50)
    print("LLM Usage Summary")
    print("=" * 50)
    print(f"  Model:           {_current_model}")
    print(f"  API:             {_api_type}")
    print(f"  Requests:        {stats['requests']}")
    print(f"  Input tokens:    {stats['input_tokens']:,}")
    print(f"  Output tokens:   {stats['output_tokens']:,}")
    print(f"  Embedding tokens:{stats['embedding_tokens']:,}")
    print(f"  Total tokens:    {total_tokens:,}")
    print(f"  Est. cost:       ${total_cost:.4f}")
    print("=" * 50 + "\n")
