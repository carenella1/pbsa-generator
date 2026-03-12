import json
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from generator.engine.site_generator import PBSASiteGenerator
from app.services.entity_classifier import EntityClassifier

app = FastAPI()

app.mount("/ui", StaticFiles(directory="app/ui"), name="ui")


class EntityInput(BaseModel):
    name: str
    description: str


class ConfigInput(BaseModel):
    entity_name: str
    entity_description: str


# -----------------------------
# CREATE CONFIG
# -----------------------------

@app.post("/create-config")
def create_config(data: ConfigInput):

    print("Creating PBSA config...")

    classifier = EntityClassifier()

    entity_type = classifier.classify(
        data.entity_name,
        data.entity_description
    )

    config = {
        "entity_id": data.entity_name.lower().replace(" ", "_"),
        "entity_name": data.entity_name,
        "description": data.entity_description,
        "entity_type": entity_type
    }

    os.makedirs("examples", exist_ok=True)

    config_path = f"examples/{config['entity_id']}_config.json"

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("Config created:", config_path)

    return JSONResponse({
        "status": "success",
        "config_path": config_path,
        "config": config
    })


# -----------------------------
# GENERATE SITE
# -----------------------------

@app.post("/generate")
def generate_site(payload: dict):

    print("Generating PBSA site...")

    config = payload.get("config")

    if not config:
        return JSONResponse(
            {"status": "error", "message": "No config provided"},
            status_code=400
        )

    generator = PBSASiteGenerator(config)

    generator.build()

    print("Site generation finished.")

    return JSONResponse({
        "status": "success",
        "message": "Site generated successfully."
    })