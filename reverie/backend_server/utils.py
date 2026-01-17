# Configuration for the Generative Agents simulation backend
#
# API Key Configuration:
# ----------------------
# API keys are now configured via environment variables (not in this file).
# Set one of the following before running the simulation:
#
#   Option 1 - OpenRouter (recommended, supports multiple models):
#     export OPENROUTER_API_KEY="sk-or-your-key-here"
#     export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"  # optional
#
#   Option 2 - OpenAI direct:
#     export OPENAI_API_KEY="sk-your-key-here"
#
# See llm_config.py for the API initialization logic.

# Owner name (for logging/identification purposes)
key_owner = "User"

# Path configuration (relative to reverie/backend_server/)
maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

collision_block_id = "32125"

# Verbose debugging output
debug = True
