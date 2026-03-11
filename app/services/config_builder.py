from pathlib import Path
import json

CONFIG_OUTPUT = Path("examples/pbsa-config.json")


def build_config(data):

    config = {
        "entity_id": data["entity_id"],
        "site_name": data["site_name"],
        "tagline": data["tagline"],
        "description": data["description"],
        "projects": []
    }

    for project in data.get("projects", []):
        config["projects"].append({
            "name": project["name"],
            "url": project["url"]
        })

    with open(CONFIG_OUTPUT, "w") as f:
        json.dump(config, f, indent=2)

    return config