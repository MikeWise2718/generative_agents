# Generative Agents Setup Plan

## Prerequisites
- uv package manager (https://docs.astral.sh/uv/)
- OpenAI API key

## Initial Setup (one time)

### 1. Install Dependencies
```bash
cd D:\python\generative_agents
uv sync
```

### 2. Configure API Key
Create `reverie/backend_server/utils.py` with your OpenAI API key:

```python
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

Note: This file is in `.gitignore` and won't be committed.

## Running the Simulation

### Terminal 1 - Start Frontend Server
```bash
cd D:\python\generative_agents
uv run python environment/frontend_server/manage.py runserver
```
Verify at http://localhost:8000/

### Terminal 2 - Start Simulation Server
```bash
cd D:\python\generative_agents/reverie/backend_server
uv run python reverie.py
```

When prompted:
- Forked simulation: `base_the_ville_isabella_maria_klaus`
- New simulation name: any name (e.g., `my-first-run`)

### Run the Simulation
1. Open http://localhost:8000/simulator_home in browser
2. In Terminal 2, type: `run 100`
3. Watch agents move on the map

## Commands Reference
| Command | Description |
|---------|-------------|
| `run <steps>` | Run N steps (each step = 10 game seconds) |
| `save` | Save progress |
| `fin` | Save and exit |
| `exit` | Exit without saving |
| `print persona schedule <Name>` | View agent's daily schedule |
| `print current time` | Show simulation time |
| `call -- analysis <Name>` | Chat with an agent |

## Cost Estimate
- 3 agents, 100 steps: ~$0.05-0.20
- 3 agents, full day: ~$0.50-2.00
- Start small to verify everything works!

## Troubleshooting
- API rate limits may cause hangs - save often
- If you need to reinstall: `uv sync`

## Related Documentation
- `02_UV_SETUP.md` - Details on uv configuration
- `03_MODEL_UPDATES.md` - OpenAI model changes and cost breakdown
- `04_BUG_FIXES.md` - Bug fixes and UI improvements
