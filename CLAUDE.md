# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the research implementation for "Generative Agents: Interactive Simulacra of Human Behavior" - a simulation framework where AI agents (personas) exhibit believable human behaviors in a virtual town called Smallville. The system uses LLMs to generate agent behaviors based on memory, perception, and planning.

This fork has been modernized to use `uv` package manager and current OpenAI APIs (gpt-4o-mini, gpt-4o instead of deprecated text-davinci models).

## Running the Simulation

**Prerequisites:**
- Python 3.9.x (requires-python = ">=3.9,<3.10")
- `uv` package manager
- OpenAI API key configured in `reverie/backend_server/utils.py`

**Install dependencies:**
```bash
uv sync
```

**Start the environment server (Django frontend):**
```bash
cd environment/frontend_server
uv run python manage.py runserver
# Access at http://localhost:8000/
```

**Start the simulation server (in separate terminal):**
```bash
cd reverie/backend_server
uv run python reverie.py
# Select simulation by number from menu, then enter new simulation name
```

**Simulation commands (at "Enter option:" prompt):**
- `run <steps>` - Run simulation for N steps (each step = 10 game seconds)
- `save` - Save current progress
- `fin` - Save and exit
- `exit` - Exit without saving
- `print persona schedule <Name>` - View agent's daily schedule
- `print current time` - Show simulation time
- `call -- analysis <Name>` - Interactive chat with agent
- `call -- load history the_ville/<history_file>.csv` - Load agent memory history

**Browser URLs:**
- `http://localhost:8000/simulator_home` - Live simulation view
- `http://localhost:8000/replay/<sim-name>/<step>` - Replay saved simulation
- `http://localhost:8000/demo/<sim-name>/<step>/<speed>` - Demo with character sprites (1-5 speed)

## Architecture

### Two-Server Architecture
1. **Frontend Server** (`environment/frontend_server/`) - Django server rendering the Smallville map and handling visualization. Browser displays agent movements in real-time.
2. **Backend Server** (`reverie/backend_server/`) - Core simulation engine. The `ReverieServer` class orchestrates the simulation loop, managing personas and the maze world.

### Core Components

**ReverieServer** (`reverie/backend_server/reverie.py`):
- Main simulation controller
- Manages game time, step progression, and persona coordination
- Communicates with frontend via JSON files in `storage/` directories

**Persona** (`reverie/backend_server/persona/persona.py`):
- Represents a generative agent
- Contains three memory systems and invokes cognitive modules
- Main cognitive loop: `perceive() -> retrieve() -> plan() -> reflect() -> execute()`

**Maze** (`reverie/backend_server/maze.py`):
- 2D tile-based world representation
- Manages collision detection, events, and spatial addressing
- Tiles contain world/sector/arena/game_object hierarchy

### Persona Memory Systems

1. **Spatial Memory** (`memory_structures/spatial_memory.py`) - Tree structure of known locations
2. **Associative Memory** (`memory_structures/associative_memory.py`) - Long-term memory stream storing events, thoughts, and chats as `ConceptNode` objects with embeddings
3. **Scratch** (`memory_structures/scratch.py`) - Short-term working memory for current state

### Cognitive Modules (`persona/cognitive_modules/`)

- **perceive.py** - Filters nearby events based on attention bandwidth and retention
- **retrieve.py** - Queries associative memory for relevant context using embeddings
- **plan.py** - Generates daily schedules and decomposes into actions (largest module)
- **reflect.py** - Creates higher-level thoughts from accumulated experiences
- **converse.py** - Handles agent-to-agent conversations
- **execute.py** - Converts plans to concrete tile movements

### LLM Integration (`persona/prompt_template/`)

- **gpt_structure.py** - OpenAI API wrapper functions (uses ChatCompletion API)
- **run_gpt_prompt.py** - Prompt templates for all cognitive functions

**Model usage:**
- `gpt-4o-mini` - Default for most tasks (schedules, actions, locations)
- `gpt-4o` - Complex reasoning (reflection, conversations)
- `text-embedding-3-small` - Memory retrieval embeddings

## Data Flow

1. Frontend sends environment state to `storage/<sim>/environment/<step>.json`
2. Backend reads environment, runs each persona's cognitive loop
3. Backend writes movements to `storage/<sim>/movement/<step>.json`
4. Frontend animates agent movements on the map

## Key Paths

- `environment/frontend_server/storage/` - Simulation save data
- `environment/frontend_server/static_dirs/assets/the_ville/` - Map assets and history files
- `environment/frontend_server/compressed_storage/` - Demo-ready compressed simulations
- `reverie/compress_sim_storage.py` - Utility to compress simulations for demos

## Base Simulations

- `base_the_ville_isabella_maria_klaus` - 3 agents (Isabella Rodriguez, Maria Lopez, Klaus Mueller)
- `base_the_ville_n25` - 25 agents

## Cost Estimates

- 3 agents, 100 steps (~17 min game time): $0.05-0.20
- 3 agents, 1 game day (~8,640 steps): $0.50-2.00
- 25 agents, 1 game day: $5-15

## Customization

**History files** for initializing agent memories are in `environment/frontend_server/static_dirs/assets/the_ville/`:
- `agent_history_init_n25.csv` - For 25-agent sim
- `agent_history_init_n3.csv` - For 3-agent sim

**Creating new base simulations:** Copy an existing base simulation folder and edit using the [Tiled](https://www.mapeditor.org/) map editor if changing agents or map layout.
