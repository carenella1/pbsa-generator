from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from pathlib import Path
import json

# --------------------------------
# App Initialization
# --------------------------------

app = FastAPI(title="PBSA Generator")

print("MAIN.PY LOADED")

# --------------------------------
# Paths
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

UI_DIR = BASE_DIR / "ui"
ARCH_DIR = PROJECT_ROOT / "generator" / "architectures"
OUTPUT_DIR = PROJECT_ROOT / "output"

print("UI_DIR:", UI_DIR)
print("UI exists:", UI_DIR.exists())

# --------------------------------
# Static UI Mount
# --------------------------------

app.mount(
    "/ui",
    StaticFiles(directory=str(UI_DIR)),
    name="ui"
)

# --------------------------------
# Root Redirect
# --------------------------------

@app.get("/")
def root():
    return RedirectResponse("/ui/index.html")

# --------------------------------
# Health Check
# --------------------------------

@app.get("/health")
def health():
    return {"status": "running"}

# --------------------------------
# PBSA Site Generation
# --------------------------------

@app.post("/generate")
def generate_site(config: dict):

    try:

        entity_type = config.get("entity_type", "personal_brand")

        architecture_path = ARCH_DIR / f"{entity_type}.json"

        if not architecture_path.exists():
            architecture_path = ARCH_DIR / "personal_brand.json"

        with open(architecture_path) as f:
            architecture = json.load(f)

        site_name = config.get("site_name", "pbsa-site")

        build_dir = OUTPUT_DIR / f"builds/{site_name}"
        build_dir.mkdir(parents=True, exist_ok=True)

        index_html = f"""
        <html>
        <head>
            <title>{site_name}</title>
        </head>
        <body>
            <h1>{site_name}</h1>
            <p>PBSA site generated successfully.</p>
        </body>
        </html>
        """

        with open(build_dir / "index.html", "w") as f:
            f.write(index_html)

        return {
            "status": "success",
            "build_location": str(build_dir)
        }

    except Exception as e:

        print("GENERATION ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )