import json
from pathlib import Path

TEMPLATE_DIR = Path("generator/architecture_templates")

def load_architecture(entity_type):

    template_path = TEMPLATE_DIR / f"{entity_type}.json"

    if not template_path.exists():
        raise Exception(f"No architecture template for {entity_type}")

    with open(template_path) as f:
        template = json.load(f)

    return template