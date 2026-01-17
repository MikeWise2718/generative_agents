# Complete Guide: Adding a New Character to Smallville

This document covers every step required to add a new character (persona) with custom pixel art to the generative agents simulation.

---

## Overview

Adding a new character requires modifications to:
1. Sprite assets (pixel art)
2. Persona data files (memory, identity)
3. Simulation configuration (registration, spawn point)
4. Optional: History/memory initialization

---

## 1. Create Pixel Art Sprites

### Main Character Sprite

**Location:** `environment/frontend_server/static_dirs/assets/characters/`

**Requirements:**
- **Dimensions:** 32x128 pixels (width × height)
- **Format:** PNG with transparency
- **Filename:** `FirstName_LastName.png` (spaces replaced with underscores)

**Sprite Layout (4 rows × 5 columns, each frame 32x32px):**
```
Row 0 (y=0):   down-walk.000, down-walk.001, down-walk.002, down-walk.003, down (idle)
Row 1 (y=32):  left-walk.000, left-walk.001, left-walk.002, left-walk.003, left (idle)
Row 2 (y=64):  right-walk.000, right-walk.001, right-walk.002, right-walk.003, right (idle)
Row 3 (y=96):  up-walk.000, up-walk.001, up-walk.002, up-walk.003, up (idle)
```

Each row contains 4 walking animation frames + 1 idle frame for that direction.

### Profile Picture

**Location:** `environment/frontend_server/static_dirs/assets/characters/profile/`

**Requirements:**
- **Filename:** Same as sprite (`FirstName_LastName.png`)
- **Size:** Variable (typically square, used in UI)

### Atlas File (Usually No Changes Needed)

**Location:** `environment/frontend_server/static_dirs/assets/characters/atlas.json`

The atlas defines frame coordinates. All characters share the same layout, so no changes needed unless using a non-standard sprite sheet.

---

## 2. Create Persona Data Folder

### Folder Structure

Create the following structure in your base simulation:
```
environment/frontend_server/storage/base_the_ville_*/personas/
└── Full Name/
    └── bootstrap_memory/
        ├── scratch.json
        ├── spatial_memory.json
        └── associative_memory/
            ├── nodes.json
            ├── embeddings.json
            └── kw_strength.json
```

### scratch.json (Identity & State)

This defines the character's identity, personality, and runtime state variables.

```json
{
  "vision_r": 8,
  "att_bandwidth": 8,
  "retention": 8,
  "curr_time": null,
  "curr_tile": null,
  "daily_plan_req": "Description of character's typical daily activities and routines.",
  "name": "Full Name",
  "first_name": "First",
  "last_name": "Last",
  "age": 28,
  "innate": "trait1, trait2, trait3",
  "learned": "Longer description of the character's background, skills, personality, and history.",
  "currently": "What the character is currently focused on or working towards.",
  "lifestyle": "Character goes to bed around 11pm, wakes up around 6am, eats lunch around noon.",
  "living_area": "the Ville:Location Name:room name",
  "concept_forget": 100,
  "daily_reflection_time": 180,
  "daily_reflection_size": 5,
  "overlap_reflect_th": 4,
  "kw_strg_event_reflect_th": 10,
  "kw_strg_thought_reflect_th": 9,
  "recency_w": 1,
  "relevance_w": 1,
  "importance_w": 1,
  "recency_decay": 0.995,
  "importance_trigger_max": 150,
  "importance_trigger_curr": 150,
  "importance_ele_n": 0,
  "thought_count": 5,
  "daily_req": [],
  "f_daily_schedule": [],
  "f_daily_schedule_hourly_org": [],
  "act_address": null,
  "act_start_time": null,
  "act_duration": null,
  "act_description": null,
  "act_pronunciatio": null,
  "act_event": ["Full Name", null, null],
  "act_obj_description": null,
  "act_obj_pronunciatio": null,
  "act_obj_event": [null, null, null],
  "chatting_with": null,
  "chat": null,
  "chatting_with_buffer": {},
  "chatting_end_time": null,
  "act_path_set": false,
  "planned_path": []
}
```

**Key Fields to Customize:**
| Field | Description |
|-------|-------------|
| `name`, `first_name`, `last_name` | Character's full name |
| `age` | Character's age |
| `innate` | Core personality traits (comma-separated adjectives) |
| `learned` | Background, skills, history (paragraph) |
| `currently` | Current goals or situation |
| `daily_plan_req` | Typical daily routine description |
| `lifestyle` | Sleep/wake times, meal times |
| `living_area` | Home location (must match spatial_memory!) |
| `act_event` | Initialize with `["Full Name", null, null]` |

### spatial_memory.json (Known Locations)

**CRITICAL:** Must include the character's `living_area` location!

```json
{
  "the Ville": {
    "Character's Home Location": {
      "main room": [
        "bed",
        "desk",
        "refrigerator",
        "closet",
        "shelf"
      ],
      "bathroom": [
        "shower"
      ]
    },
    "Hobbs Cafe": {
      "cafe": [
        "refrigerator",
        "cafe customer seating",
        "cooking area",
        "kitchen sink",
        "behind the cafe counter",
        "piano"
      ]
    },
    "Oak Hill College": {
      "library": [
        "library sofa",
        "library table",
        "bookshelf"
      ],
      "classroom": [
        "blackboard",
        "classroom student seating",
        "classroom podium"
      ]
    },
    "Johnson Park": {
      "park": [
        "park garden"
      ]
    }
  }
}
```

**Important:**
- The `living_area` in scratch.json MUST exist in spatial_memory.json
- Include locations the character would reasonably know about
- Copy from an existing character and modify as needed

### associative_memory/ Files

**nodes.json:** Start empty
```json
{}
```

**embeddings.json:** Start empty
```json
{}
```

**kw_strength.json:**
```json
{
  "kw_strength_event": {},
  "kw_strength_thought": {}
}
```

---

## 3. Register in Simulation Configuration

### meta.json (Persona List)

**Location:** `environment/frontend_server/storage/base_the_ville_*/reverie/meta.json`

Add the character's full name to the `persona_names` array:

```json
{
  "fork_sim_code": "base_the_ville_isabella_maria_klaus",
  "start_date": "February 13, 2023",
  "curr_time": "February 13, 2023, 08:00:00",
  "sec_per_step": 10,
  "maze_name": "the_ville",
  "persona_names": [
    "Isabella Rodriguez",
    "Maria Lopez",
    "Klaus Mueller",
    "New Character Name"
  ],
  "step": 0
}
```

### environment/0.json (Spawn Position)

**Location:** `environment/frontend_server/storage/base_the_ville_*/environment/0.json`

Add spawn coordinates (x, y tile position):

```json
{
  "Isabella Rodriguez": {
    "maze": "the_ville",
    "x": 72,
    "y": 14
  },
  "New Character Name": {
    "maze": "the_ville",
    "x": 75,
    "y": 19
  }
}
```

**Finding Valid Coordinates:**
- Look at existing characters' spawn points
- Spawn should be inside the character's living_area
- Check the map visually at `http://localhost:8000/simulator_home`

---

## 4. Optional: Initialize Character Memories

### History CSV Files

**Location:** `environment/frontend_server/static_dirs/assets/the_ville/`

Files:
- `agent_history_init_n3.csv` - For 3-agent simulations
- `agent_history_init_n25.csv` - For 25-agent simulations

**Format:**
```csv
Name,Whisper
"Character Name","Fact 1; Fact 2; Relationship info; Background detail"
```

**Example:**
```csv
"Lois Lane","You are an investigative reporter who recently moved to the Ville; Isabella Rodriguez runs Hobbs Cafe which is a great place to meet locals; You enjoy talking to people and learning their stories"
```

**Loading History:** Use the simulation command:
```
call -- load history the_ville/agent_history_init_n3.csv
```

---

## 5. Validation Checklist

Before running the simulation, verify:

- [ ] **Sprite exists:** `static_dirs/assets/characters/FirstName_LastName.png`
- [ ] **Sprite dimensions:** 32x128 pixels, PNG format
- [ ] **Profile picture:** `static_dirs/assets/characters/profile/FirstName_LastName.png`
- [ ] **Persona folder:** `storage/base_*/personas/Full Name/` exists
- [ ] **scratch.json:** All required fields filled, `act_event[0]` matches name
- [ ] **spatial_memory.json:** Contains the `living_area` location
- [ ] **associative_memory/:** All 3 files exist (can be empty `{}`)
- [ ] **meta.json:** Name added to `persona_names` array
- [ ] **environment/0.json:** Spawn coordinates added
- [ ] **Name consistency:** Folder name = scratch.json name = meta.json name

---

## 6. Common Issues & Fixes

### Character Won't Wake Up / Stuck Sleeping
**Cause:** `living_area` not in `spatial_memory.json`
**Fix:** Add the home location to spatial_memory.json

### Character Not Appearing
**Cause:** Name mismatch between files or missing from meta.json
**Fix:** Ensure exact name match across all files (case-sensitive, including spaces)

### Sprite Not Loading
**Cause:** Filename doesn't match expected format
**Fix:** Use `FirstName_LastName.png` with underscores, matching the name in meta.json

### Character Can't Navigate
**Cause:** Spatial memory missing required locations
**Fix:** Add relevant locations the character needs to visit

---

## 7. File Reference Table

| Purpose | Path (relative to `environment/frontend_server/`) |
|---------|---------------------------------------------------|
| Character Sprite | `static_dirs/assets/characters/FirstName_LastName.png` |
| Profile Picture | `static_dirs/assets/characters/profile/FirstName_LastName.png` |
| Sprite Atlas | `static_dirs/assets/characters/atlas.json` |
| Persona Folder | `storage/base_*/personas/Full Name/` |
| Identity (scratch) | `personas/Full Name/bootstrap_memory/scratch.json` |
| Known Locations | `personas/Full Name/bootstrap_memory/spatial_memory.json` |
| Memory Nodes | `personas/Full Name/bootstrap_memory/associative_memory/nodes.json` |
| Embeddings | `personas/Full Name/bootstrap_memory/associative_memory/embeddings.json` |
| Keyword Strength | `personas/Full Name/bootstrap_memory/associative_memory/kw_strength.json` |
| Persona List | `storage/base_*/reverie/meta.json` |
| Spawn Positions | `storage/base_*/environment/0.json` |
| History Init | `static_dirs/assets/the_ville/agent_history_init_n*.csv` |

---

## 8. Quick Start Template

To add a character quickly, copy an existing character's folder and modify:

```bash
# Copy existing character as template
cp -r "storage/base_the_ville_isabella_maria_klaus/personas/Isabella Rodriguez" \
      "storage/base_the_ville_isabella_maria_klaus/personas/New Character"

# Then edit:
# 1. bootstrap_memory/scratch.json - Update all identity fields
# 2. bootstrap_memory/spatial_memory.json - Update known locations
# 3. reverie/meta.json - Add name to persona_names
# 4. environment/0.json - Add spawn coordinates
# 5. Add sprite PNG files to assets/characters/
```

---

## 9. Testing

1. Start the frontend server:
   ```bash
   cd environment/frontend_server
   uv run python manage.py runserver
   ```

2. Start the backend server:
   ```bash
   cd reverie/backend_server
   uv run python reverie.py
   ```

3. Select your base simulation and create a new fork

4. Run a few steps:
   ```
   run 100
   ```

5. Check `http://localhost:8000/simulator_home` to see the character

6. Verify the character wakes up and follows their daily routine
