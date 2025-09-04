from pathlib import Path
import json

# Define the paths to check
trial_files = [
    "data/trials/egfr.json",
    "data/trials/pd-l1.json",
    "data/trials/kras_g12c.json",
    "data/trials/combo.json",
    "data/trials/early_stage.json"
]

# Try to load and parse each JSON file
results = {}

for file in trial_files:
    path = Path(file)
    if not path.exists():
        results[file] = "File not found"
        continue
    try:
        with open(path, "r") as f:
            data = json.load(f)
        # Check for required keys
        if "title" in data and "criteria" in data:
            results[file] = "Valid"
        else:
            results[file] = "Missing keys"
    except json.JSONDecodeError as e:
        results[file] = f"JSON error: {e}"
    except Exception as e:
        results[file] = f"Other error: {e}"

# Print results
for file, status in results.items():
    print(f"{file}: {status}")

