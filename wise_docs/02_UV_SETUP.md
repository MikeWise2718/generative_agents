# UV Environment Setup

This document describes the changes made to enable running the project with `uv` instead of traditional pip/venv.

## Files Created

### pyproject.toml

Created a `pyproject.toml` in the project root to define the project and dependencies for uv:

```toml
[project]
name = "generative-agents"
version = "1.0.0"
description = "Generative Agents: Interactive Simulacra of Human Behavior"
requires-python = ">=3.9,<3.10"
dependencies = [
    # ... all dependencies listed
]
```

**Key decisions:**
- Python version pinned to 3.9.x (`>=3.9,<3.10`) because newer Python versions (3.10+) have compatibility issues with some dependencies
- Removed `psycopg2-binary` (requires PostgreSQL installation, not needed for file-based storage)
- Removed `sklearn==0.0` meta-package (just use `scikit-learn` directly)
- Loosened version constraints to allow uv to resolve compatible versions

### requirements-local.txt

Created as a fallback for pip-based installation without PostgreSQL:
- Same as original `requirements.txt` but without `psycopg2-binary`

## Setup Process

### Initial Setup (one time)
```bash
cd D:\python\generative_agents
uv sync
```

This:
1. Downloads Python 3.9 if not available
2. Creates `.venv` directory
3. Installs all dependencies

### Running Commands

No need to activate the virtual environment. Use `uv run` prefix:

```bash
# Start frontend server
uv run python environment/frontend_server/manage.py runserver

# Start simulation server
cd reverie/backend_server
uv run python reverie.py
```

### Reinstalling Dependencies

If dependencies get corrupted or you need to refresh:
```bash
uv sync
```

## Why uv?

1. **Faster** - uv is written in Rust, 10-100x faster than pip
2. **No activation needed** - `uv run` handles the venv automatically
3. **Better dependency resolution** - Catches conflicts before installation
4. **Automatic Python management** - Downloads correct Python version if needed

## Dependency Changes from Original

| Original | Change | Reason |
|----------|--------|--------|
| `gensim==3.8.0` | `gensim>=4.0.0` | 3.8.0 required numpy<=1.16.1, incompatible with other deps |
| `psycopg2-binary==2.9.5` | Removed | Requires PostgreSQL, not needed |
| `sklearn==0.0` | Removed | Meta-package, scikit-learn is sufficient |
| Pinned versions | Loosened to `>=` | Allow uv to find compatible versions |

## Troubleshooting

### "No solution found when resolving dependencies"
Run `uv sync` again or check `pyproject.toml` for version conflicts.

### Python version issues
Ensure Python 3.9 is being used:
```bash
uv run python --version
# Should show Python 3.9.x
```

### Missing dependencies
```bash
uv sync --refresh
```
