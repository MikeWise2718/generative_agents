# Next Steps to Get Lois Lane Working

## Problem

Lois Lane is stuck sleeping and won't wake up, even though her `lifestyle` says she wakes at 6am.

## Root Cause

Lois Lane's `spatial_memory.json` was missing her own home location. Her `living_area` is set to `"the Ville:Isabella Rodriguez's apartment:main room"`, but that location wasn't in her spatial memory.

When the planning module tries to generate her daily schedule (wake up, get ready, make breakfast, etc.), it can't find valid locations in her spatial memory for home-based activities. So she defaults to sleeping indefinitely.

## Fix Applied

Added `"Isabella Rodriguez's apartment"` to Lois Lane's `spatial_memory.json` in `trial_em_03`:

```json
"Isabella Rodriguez's apartment": {
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
}
```

## Remaining Steps

1. **Restart the simulation** - The running simulation has already loaded the old spatial memory into memory. You need to restart from the base simulation for the fix to take effect.

2. **Fix the base simulation** - Update the spatial memory in the base simulation so future forks inherit the fix:
   ```
   environment/frontend_server/storage/base_the_ville_isabella_maria_klaus/personas/Lois Lane/bootstrap_memory/spatial_memory.json
   ```

3. **Verify after restart** - Run the simulation and confirm Lois Lane wakes up at ~6am and starts her daily routine (walking around town, going to the library, visiting Hobbs Cafe).

## Files Modified

- `environment/frontend_server/storage/trial_em_03/personas/Lois Lane/bootstrap_memory/spatial_memory.json` - Added Isabella Rodriguez's apartment

## Files to Update (base simulation)

- `environment/frontend_server/storage/base_the_ville_isabella_maria_klaus/personas/Lois Lane/bootstrap_memory/spatial_memory.json` - Same fix needed here
