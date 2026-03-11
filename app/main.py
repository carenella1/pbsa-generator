import os
import json

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from app.services.entity_classifier import EntityClassifier
from generator.engine.site_generator import PBSASiteGenerator
from deployment.deploy_site import GitHubDeployer


# load environment variables
load_dotenv()

app = FastAPI()


# -----------------------------
# UI STATIC FILES
# -----------------------------

UI_DIR = os.path.join(os.getcwd(), "ui")

app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")


@app.get("/")
def root():
    return FileResponse("ui/index.html")


# -----------------------------
# CREATE CONFIG
# -----------------------------

@app.post("/create-config")
def create_config(data: dict):

    entity_name = data.get("entity_name")
    entity_id = data.get("entity_id")
    description = data.get("description")

    classifier = EntityClassifier()

    entity_type = classifier.classify(description)

    config = {
        "version": "1.0",
        "entity_id": entity_id,
        "entity_name": entity_name,
        "description": description,
        "entity_type": entity_type,
        "site": {
            "domain": "",
            "tagline": ""
        },
        "relationships": [],
        "metadata": {
            "created_by": "pbsa_generator"
        }
    }

    os.makedirs("examples", exist_ok=True)

    with open("examples/pbsa-config.json", "w") as f:
        json.dump(config, f, indent=4)

    return {
        "status": "config created",
        "entity_type": entity_type
    }


# -----------------------------
# GENERATE SITE
# -----------------------------

@app.post("/generate")
def generate_site():

    config_path = "examples/pbsa-config.json"

    if not os.path.exists(config_path):
        return {"error": "No config found. Create config first."}

    with open(config_path) as f:
        config = json.load(f)

    generator = PBSASiteGenerator(config_path)

    generator.build()

    return {
        "status": "site generated",
        "entity_id": config["entity_id"]
    }


# -----------------------------
# DEPLOY SITE
# -----------------------------

@app.post("/deploy")
def deploy_site():

    config_path = "examples/pbsa-config.json"

    if not os.path.exists(config_path):
        return {"error": "No config found"}

    with open(config_path) as f:
        config = json.load(f)

    entity_id = config["entity_id"]

    deployer = GitHubDeployer()

    deployer.deploy(entity_id)

    return {
        "status": "deployment started",
        "repo": entity_id
    }