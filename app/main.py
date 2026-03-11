from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import FileResponse
from app.services.config_builder import build_config
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from generator.engine.site_generator import PBSASiteGenerator
from deployment.deploy_site import GitHubDeployer
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/ui", StaticFiles(directory="app/ui"), name="ui")

@app.get("/")
def root():
    return {"message": "PBSA Generator API running"}

@app.post("/create-config")
def create_config(data: dict):

    config = build_config(data)

    return {
        "status": "config created",
        "config": config
    }

@app.post("/generate")
def generate_site():

    config_path = ROOT / "examples/pbsa-config.json"

    generator = PBSASiteGenerator(config_path)
    generator.build()

    return {"status": "site generated"}


import json
from pathlib import Path

CONFIG_PATH = Path("examples/pbsa-config.json")

@app.post("/deploy")
def deploy_site():

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    entity_id = config["entity_id"]

    deployer = GitHubDeployer()
    deployer.deploy(entity_id)

    return {"status": f"site deployed for {entity_id}"}

@app.get("/app")
def load_ui():
    return FileResponse("app/ui/index.html")

