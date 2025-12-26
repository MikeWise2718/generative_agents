# Generative Agents (Mike's Fork)

## What This Is

A simulation where AI agents live in a virtual town called Smallville. Each agent has memories, daily routines, and can interact with other agents. Based on the Stanford paper "Generative Agents: Interactive Simulacra of Human Behavior".

## Changes Made

**Modernization:**
- Updated to work with `uv` package manager
- Replaced deprecated OpenAI models (`text-davinci-003`) with current ones (`gpt-4o-mini`, `gpt-4o`)
- Fixed deprecated `Completion` API → `ChatCompletion` API
- Added OpenRouter API support as alternative to direct OpenAI access
- Added token usage tracking with cost estimates after each run

**Bug Fixes:**
- Fixed crash when forking simulations (missing `movement` directory)
- Fixed "Please start backend first" error when navigating back to simulation
- Fixed camera starting in empty area instead of on characters
- Fixed GPT response parsing crashes (empty task strings, missing duration format)
- Added fail-safe returns when ChatGPT response validation fails
- Fixed prompt template typo (Sam Johnson example)

**UI Improvements:**
- Added numbered simulation selection menu (no more typing long names)
- Camera now starts centered on first character
- Unique character sprites for each persona (previously all identical)
- Character profile images in the detail cards below the map
- **New sidebar** on the right showing all characters with:
  - Initials badge and current action (one line per character)
  - Click any character to jump camera to their location
  - Tooltip shows full name on hover
- Base 3-agent simulation now starts at 8 AM instead of midnight

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

**Alternative: Using OpenRouter**

Instead of editing `utils.py`, you can use OpenRouter for more model flexibility:

```bash
export OPENROUTER_API_KEY="sk-or-your-key-here"
export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"  # optional, defaults to openai/gpt-4o-mini
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

**Basic:**
| Command | Description |
|---------|-------------|
| `run 100` | Run 100 steps (~17 min game time) |
| `save` | Save progress (important before stopping!) |
| `fin` | Save and exit |
| `exit` | Exit without saving |

**Inspect Characters:**
| Command | Description |
|---------|-------------|
| `print persona schedule <Name>` | Show daily schedule |
| `print all persona schedule` | Show all schedules |
| `print current time` | Game time and step count |
| `call -- analysis <Name>` | Chat with a character (stateless) |

## Cost

~$0.05-0.20 for 100 steps with 3 agents (using gpt-4o-mini).

After each `run` command, a usage summary is displayed showing:
- Total requests, input/output/embedding tokens
- Estimated cost based on current model pricing

## Documentation

See `wise_docs/` for detailed documentation on all changes.
