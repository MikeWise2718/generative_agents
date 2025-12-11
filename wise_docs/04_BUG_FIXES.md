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
