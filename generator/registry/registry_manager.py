import json
from pathlib import Path
from datetime import datetime

REGISTRY_PATH = Path("generator/registry/entity_registry.json")


class EntityRegistry:

    def __init__(self):

        if not REGISTRY_PATH.exists():
            REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(REGISTRY_PATH, "w") as f:
                json.dump({"entities": [], "relationships": []}, f, indent=2)

        with open(REGISTRY_PATH) as f:
            self.data = json.load(f)

    def save(self):

        with open(REGISTRY_PATH, "w") as f:
            json.dump(self.data, f, indent=2)

    def register_entity(self, entity_id, entity_type):

        for entity in self.data["entities"]:
            if entity["entity_id"] == entity_id:
                return

        entity = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "created": datetime.utcnow().isoformat()
        }

        self.data["entities"].append(entity)

        self.save()

        print(f"Registered entity: {entity_id}")

    def add_relationship(self, parent, child, relation_type="related"):

        relationship = {
            "parent": parent,
            "child": child,
            "type": relation_type
        }

        self.data["relationships"].append(relationship)

        self.save()

        print(f"Linked {parent} → {child}")

    def get_related_entities(self, entity_id):

        related = []

        for rel in self.data["relationships"]:

            if rel["parent"] == entity_id:
                related.append(rel["child"])

            if rel["child"] == entity_id:
                related.append(rel["parent"])

        return related