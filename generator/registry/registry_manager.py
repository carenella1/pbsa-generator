import json
from pathlib import Path
from datetime import datetime


REGISTRY_PATH = Path("generator/registry/entity_registry.json")


class EntityRegistry:

    def __init__(self):
        self.registry = self.load_registry()

    def load_registry(self):
        if not REGISTRY_PATH.exists():
            return {"entities": []}

        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)

    def save_registry(self):
        with open(REGISTRY_PATH, "w") as f:
            json.dump(self.registry, f, indent=2)

    def entity_exists(self, entity_id):
        for entity in self.registry["entities"]:
            if entity["entity_id"] == entity_id:
                return True
        return False

    def register_entity(self, entity_data):

        if self.entity_exists(entity_data["entity_id"]):
            raise ValueError("Entity already exists")

        entity_data["created_at"] = datetime.utcnow().isoformat()

        self.registry["entities"].append(entity_data)

        self.save_registry()

    def list_entities(self):
        return self.registry["entities"]