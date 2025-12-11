# OpenAI Model Updates

This document describes the changes made to `reverie/backend_server/persona/prompt_template/gpt_structure.py` to update deprecated OpenAI models.

## Problem

The original code used deprecated OpenAI models and APIs:
- `text-davinci-002` and `text-davinci-003` (shut down by OpenAI)
- `openai.Completion.create()` API (deprecated, replaced by Chat Completions)

This caused "TOKEN LIMIT EXCEEDED" errors because the API calls were failing silently.

## Changes Made

### Model Replacements

| Function | Old Model | New Model | Purpose |
|----------|-----------|-----------|---------|
| `ChatGPT_single_request` | `gpt-3.5-turbo` | `gpt-4o-mini` | Simple single requests |
| `ChatGPT_request` | `gpt-3.5-turbo` | `gpt-4o-mini` | General chat completions |
| `GPT4_request` | `gpt-4` | `gpt-4o` | Complex reasoning tasks |
| `GPT_request` | `text-davinci-002/003` | `gpt-4o-mini` | Legacy prompt completions |
| `get_embedding` | `text-embedding-ada-002` | `text-embedding-3-small` | Text embeddings |

### API Changes

The `GPT_request` function was converted from the deprecated Completions API to Chat Completions API:

**Before (broken):**
```python
response = openai.Completion.create(
    model=gpt_parameter["engine"],
    prompt=prompt,
    ...
)
return response.choices[0].text
```

**After (working):**
```python
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    ...
)
return response["choices"][0]["message"]["content"]
```

### Error Handling

Improved error messages to show actual exceptions instead of generic "TOKEN LIMIT EXCEEDED":
```python
except Exception as e:
    print(f"GPT REQUEST ERROR: {e}")
```

## Cost Expectations

### Model Pricing (as of December 2024)

| Model | Input Cost | Output Cost |
|-------|------------|-------------|
| `gpt-4o-mini` | $0.15 / 1M tokens | $0.60 / 1M tokens |
| `gpt-4o` | $2.50 / 1M tokens | $10.00 / 1M tokens |
| `text-embedding-3-small` | $0.02 / 1M tokens | - |

### Estimated Simulation Costs

| Scenario | Estimated Cost |
|----------|----------------|
| 3 agents, 100 steps (~17 min game time) | $0.05 - $0.20 |
| 3 agents, 1 game day (~8,640 steps) | $0.50 - $2.00 |
| 25 agents, 1 game day | $5 - $15 |
| 25 agents, 2 game days (full paper reproduction) | $10 - $30 |

### Cost Comparison with Original Paper

The original paper (early 2023) used GPT-4 at ~$0.03/1K input tokens. Current pricing:
- `gpt-4o-mini` is ~200x cheaper than original GPT-4 pricing
- `gpt-4o` is ~12x cheaper than original GPT-4 pricing

A simulation that cost $100+ in 2023 now costs under $10.

## Model Selection Rationale

### gpt-4o-mini (default for most tasks)
- Extremely cost-effective
- Sufficient for: schedule generation, action planning, location decisions, event descriptions
- 128K context window

### gpt-4o (complex reasoning only)
- Used only in `GPT4_request` for tasks requiring deeper reasoning
- Better for: reflection, complex conversation generation
- Higher cost but more capable

### text-embedding-3-small
- Newer and cheaper than ada-002
- Better performance on benchmarks
- Used for memory retrieval similarity searches
