# Generative Agents (Mike's Fork)

## What This Is

A simulation where AI agents live in a virtual town called Smallville. Each agent has memories, daily routines, and can interact with other agents. Based on the Stanford paper "Generative Agents: Interactive Simulacra of Human Behavior".

## Changes Made

**Modernization:**
- Updated to work with `uv` package manager
- Replaced deprecated OpenAI models (`text-davinci-003`) with current ones (`gpt-4o-mini`, `gpt-4o`)
- Fixed deprecated `Completion` API → `ChatCompletion` API

**Bug Fixes:**
- Fixed crash when forking simulations (missing `movement` directory)
- Fixed "Please start backend first" error when navigating back to simulation
- Fixed camera starting in empty area instead of on characters

**UI Improvements:**
- Added numbered simulation selection menu (no more typing long names)
- Camera now starts centered on first character

## Installation

```bash
# Clone and enter directory
git clone https://github.com/MikeWise2718/generative_agents.git
cd generative_agents

# Install dependencies (requires uv)
uv sync

# Create API key config
# Edit reverie/backend_server/utils.py with your OpenAI key:
```

```python
# reverie/backend_server/utils.py
openai_api_key = "sk-your-key-here"
key_owner = "YourName"

maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

collision_block_id = "32125"
debug = True
```

## Running

**Terminal 1 - Frontend:**
```bash
cd environment/frontend_server
uv run python manage.py runserver
```

**Terminal 2 - Backend:**
```bash
cd reverie/backend_server
uv run python reverie.py
```

Select simulation (e.g., `1` for base 3-agent sim), enter a name for your run.

**Browser:**
1. Open http://localhost:8000/simulator_home
2. Type `run 100` in Terminal 2
3. Use arrow keys to pan camera

## Commands

| Command | Description |
|---------|-------------|
| `run 100` | Run 100 steps (~17 min game time) |
| `save` | Save progress |
| `fin` | Save and exit |
| `exit` | Exit without saving |

## Cost

~$0.05-0.20 for 100 steps with 3 agents (using gpt-4o-mini).

## Documentation

See `wise_docs/` for detailed documentation on all changes.
