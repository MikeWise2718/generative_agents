# Bug Fixes and UI Improvements

This document describes bug fixes and usability improvements made to the original codebase.

## 1. Fixed "Please start the backend first" Navigation Bug

**File:** `environment/frontend_server/translator/views.py`

**Problem:** The frontend deleted `temp_storage/curr_step.json` after first reading it (line 120). This caused any subsequent navigation to `/simulator_home` (like clicking "back to simulation") to fail with "Please start the backend first" error.

**Fix:** Commented out the file deletion:
```python
# Don't delete - allows navigation back to simulation
# os.remove(f_curr_step)
```

## 2. Added Simulation Selection Menu

**File:** `reverie/backend_server/reverie.py`

**Problem:** Users had to manually type long simulation names like `base_the_ville_isabella_maria_klaus` every time they started the backend.

**Fix:** Added interactive menu that lists all available simulations:
```
Available simulations:
----------------------------------------
  1. base_the_ville_isabella_maria_klaus
  2. base_the_ville_n25
  3. July1_the_ville_isabella_maria_klaus-step-3-1
  ...
----------------------------------------
Enter a number to select, or type a name directly.

Fork from simulation: 1
```

**Features:**
- Base simulations (`base_*`) are listed first
- Enter a number for quick selection
- Can still type full name if preferred

**Functions added:**
- `list_simulations()` - Scans storage directory, returns base sims first
- `select_simulation()` - Interactive menu for selection

## 3. Fixed Missing Movement Directory

**File:** `reverie/backend_server/reverie.py`

**Problem:** When forking a new simulation from a base simulation, the `movement` directory was not created. This caused a `FileNotFoundError` when the simulation tried to write movement data.

**Fix:** Added directory creation in `ReverieServer.__init__()`:
```python
# Ensure movement directory exists
movement_folder = f"{sim_folder}/movement"
if not os.path.exists(movement_folder):
    os.makedirs(movement_folder)
```

## 4. Fixed Camera Starting Position

**File:** `environment/frontend_server/templates/home/main_script.html`

**Problem:** The game camera started at an arbitrary position (800, 288) which was far from any characters. Users saw an empty map and didn't know to use arrow keys to navigate.

**Fix:** Camera now starts centered on the first persona's spawn location:
```javascript
// Start camera at first persona's location instead of arbitrary position
let first_persona_name = Object.keys(spawn_tile_loc)[0];
let camera_start_x = spawn_tile_loc[first_persona_name][0] * tile_width;
let camera_start_y = spawn_tile_loc[first_persona_name][1] * tile_width;

player = this.physics.add.
              sprite(camera_start_x, camera_start_y, "atlas", "misa-front")...
```

**Note:** Use arrow keys to pan the camera around the map to see other characters.
