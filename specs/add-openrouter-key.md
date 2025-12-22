# Add OpenRouter API Support

## Overview

Add support for OpenRouter as an alternative to direct OpenAI API access, providing flexibility to use different models and providers through a unified interface.

## Requirements

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | No | If set, use OpenRouter instead of OpenAI |
| `OPENROUTER_MODEL` | No | Override default model (default: `openai/gpt-4o-mini`) |
| `OPENAI_API_KEY` | No | Fallback if no OpenRouter key (can also use `utils.py`) |

### Behavior

1. **Startup Detection**: At the beginning of execution (`reverie.py`), check for `OPENROUTER_API_KEY` in environment
   - If found: Print `"Using OpenRouter API (model: <model_name>)"`
   - If not found: Fall back to OpenAI API key from `utils.py` or `OPENAI_API_KEY` env var

2. **Model Mapping**: Default OpenRouter models should match current OpenAI models:
   | Current OpenAI Model | OpenRouter Equivalent |
   |---------------------|----------------------|
   | `gpt-4o-mini` | `openai/gpt-4o-mini` |
   | `gpt-4o` | `openai/gpt-4o` |
   | `text-embedding-3-small` | `openai/text-embedding-3-small` |

3. **Model Override**: If `OPENROUTER_MODEL` is set, use it for all chat completions (not embeddings)

4. **Usage Tracking**: Track and display at end of each `run <N>` command:
   - Total input tokens
   - Total output tokens
   - Estimated cost (based on model pricing)

## Implementation Plan

### Phase 1: Create API Abstraction Layer

**File: `reverie/backend_server/persona/prompt_template/llm_config.py`** (new file)

```python
"""
LLM Configuration and API abstraction layer.
Supports OpenAI direct and OpenRouter APIs.
"""
import os
import openai

# Token tracking
_usage_stats = {
    "input_tokens": 0,
    "output_tokens": 0,
    "embedding_tokens": 0,
    "requests": 0
}

def init_llm_api():
    """
    Initialize LLM API based on environment variables.
    Returns tuple: (api_type, model_name)
    """
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")

    if openrouter_key:
        openai.api_key = openrouter_key
        openai.api_base = "https://openrouter.ai/api/v1"
        model = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        print(f"Using OpenRouter API (model: {model})")
        return ("openrouter", model)
    else:
        # Fall back to OpenAI
        from utils import openai_api_key
        openai.api_key = openai_api_key
        print("Using OpenAI API (model: gpt-4o-mini)")
        return ("openai", "gpt-4o-mini")

def get_model_name(base_model):
    """
    Get the appropriate model name based on API type.
    """
    # If using OpenRouter with custom model, use that for chat models
    if _api_type == "openrouter" and _custom_model:
        if "embedding" not in base_model:
            return _custom_model

    # Map to OpenRouter format if needed
    if _api_type == "openrouter":
        model_map = {
            "gpt-4o-mini": "openai/gpt-4o-mini",
            "gpt-4o": "openai/gpt-4o",
            "text-embedding-3-small": "openai/text-embedding-3-small"
        }
        return model_map.get(base_model, f"openai/{base_model}")

    return base_model

def track_usage(response):
    """
    Track token usage from API response.
    """
    if hasattr(response, 'usage'):
        _usage_stats["input_tokens"] += response.usage.get("prompt_tokens", 0)
        _usage_stats["output_tokens"] += response.usage.get("completion_tokens", 0)
        _usage_stats["requests"] += 1

def get_usage_stats():
    """Return current usage statistics."""
    return _usage_stats.copy()

def reset_usage_stats():
    """Reset usage statistics."""
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

    # Pricing per 1M tokens (as of Dec 2024)
    pricing = {
        "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "openai/gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
    }

    model_pricing = pricing.get(_current_model, pricing["gpt-4o-mini"])
    input_cost = (stats["input_tokens"] / 1_000_000) * model_pricing["input"]
    output_cost = (stats["output_tokens"] / 1_000_000) * model_pricing["output"]
    total_cost = input_cost + output_cost

    print("\n" + "="*50)
    print("LLM Usage Summary")
    print("="*50)
    print(f"  Requests:      {stats['requests']}")
    print(f"  Input tokens:  {stats['input_tokens']:,}")
    print(f"  Output tokens: {stats['output_tokens']:,}")
    print(f"  Est. cost:     ${total_cost:.4f}")
    print("="*50 + "\n")
```

### Phase 2: Modify gpt_structure.py

**File: `reverie/backend_server/persona/prompt_template/gpt_structure.py`**

Changes needed:
1. Import `llm_config` module
2. Remove hardcoded `openai.api_key = openai_api_key`
3. Use `llm_config.get_model_name()` for model selection
4. Add `llm_config.track_usage(response)` after each API call
5. Add OpenRouter headers if needed

Key modifications:

```python
# At top of file
from . import llm_config

# Replace hardcoded API key setup
# OLD: openai.api_key = openai_api_key
# NEW: (handled by llm_config.init_llm_api() called from reverie.py)

# In each API call function, add usage tracking:
def ChatGPT_request(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model=llm_config.get_model_name("gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            headers=llm_config.get_headers()  # For OpenRouter
        )
        llm_config.track_usage(completion)  # Track tokens
        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"ChatGPT ERROR: {e}")
        return "ChatGPT ERROR"
```

### Phase 3: Modify reverie.py

**File: `reverie/backend_server/reverie.py`**

Changes needed:
1. Import and initialize LLM config at startup
2. Print usage summary after each `run` command completes

```python
# At top, after imports
from persona.prompt_template import llm_config

# In open_server(), before main loop
llm_config.init_llm_api()

# After rs.start_server(int_count) completes in the "run" command handler
elif sim_command[:3].lower() == "run":
    int_count = int(sim_command.split()[-1])
    llm_config.reset_usage_stats()  # Reset before run
    rs.start_server(int_count)
    llm_config.print_usage_summary()  # Print after run
```

### Phase 4: OpenRouter-Specific Headers

OpenRouter requires/recommends additional headers:

```python
def get_headers():
    """Get headers for API requests."""
    if _api_type == "openrouter":
        return {
            "HTTP-Referer": "https://github.com/joonspk-research/generative_agents",
            "X-Title": "Generative Agents Simulation"
        }
    return {}
```

## Files to Modify

| File | Changes |
|------|---------|
| `reverie/backend_server/persona/prompt_template/llm_config.py` | **NEW** - API abstraction layer |
| `reverie/backend_server/persona/prompt_template/gpt_structure.py` | Use llm_config, track usage |
| `reverie/backend_server/reverie.py` | Init API, print usage after run |
| `reverie/backend_server/persona/prompt_template/__init__.py` | May need to create/update for imports |

## Testing Plan

1. **OpenAI fallback**: Run without `OPENROUTER_API_KEY` set, verify uses OpenAI
2. **OpenRouter basic**: Set `OPENROUTER_API_KEY`, verify startup message and API calls work
3. **Custom model**: Set `OPENROUTER_MODEL=anthropic/claude-3-haiku`, verify model is used
4. **Usage tracking**: Run `run 10`, verify usage summary prints with reasonable numbers
5. **Cost estimation**: Verify cost calculation matches expected based on token counts

## Example Usage

```bash
# Use OpenRouter with default model (gpt-4o-mini via OpenRouter)
export OPENROUTER_API_KEY="sk-or-..."
cd reverie/backend_server
python reverie.py

# Use OpenRouter with Claude
export OPENROUTER_API_KEY="sk-or-..."
export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"
python reverie.py

# Use direct OpenAI (no env vars, uses utils.py)
python reverie.py
```

## Expected Output

```
$ python reverie.py
Using OpenRouter API (model: openai/gpt-4o-mini)

Enter the name of the forked simulation: 1
Enter the name of the new simulation: test
Enter option: run 100

[... simulation runs ...]

==================================================
LLM Usage Summary
==================================================
  Requests:      47
  Input tokens:  12,345
  Output tokens: 3,456
  Est. cost:     $0.0039
==================================================

Enter option:
```

## Notes

- OpenRouter uses the same API format as OpenAI, so minimal code changes needed
- Embeddings should continue to use OpenAI models even with OpenRouter (or use OpenRouter's embedding endpoints)
- Consider adding retry logic for OpenRouter rate limits
- Token tracking relies on API responses including usage data (both OpenAI and OpenRouter provide this)
