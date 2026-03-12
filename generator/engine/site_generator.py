import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PBSASiteGenerator:

    def __init__(self, config):

        # Accept either a config dictionary or a path to a config file
        if isinstance(config, dict):
            self.config = config
        else:
            with open(config, "r", encoding="utf-8") as f:
                self.config = json.load(f)

        self.env = Environment(
            loader=FileSystemLoader("generator/templates")
        )

    # -----------------------------
    # MAIN BUILD
    # -----------------------------

    def build(self):

        entity_id = self.config.get("entity_id", "pbsa_site")

        output_dir = Path("output/builds") / entity_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Building PBSA site for: {entity_id}")

        self.build_homepage(output_dir)
        self.build_architecture_pages(output_dir)

        print("PBSA build complete.")

    # -----------------------------
    # HOMEPAGE
    # -----------------------------

    def build_homepage(self, output_dir):

        template = self.env.get_template("pages/index.html")

        entity = {
            "site_name": self.config.get("entity_name", self.config.get("entity_id", "PBSA Site")),
            "description": self.config.get("description", ""),
            "entity_type": self.config.get("entity_type", "personal_brand"),
        }

        rendered = template.render(
            entity=entity,
            pillars=self.get_pillars()
        )

        with open(output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(rendered)

    # -----------------------------
    # ARCHITECTURE PAGES
    # -----------------------------

    def build_architecture_pages(self, output_dir):

        architecture = self.load_architecture()

        entity = {
            "site_name": self.config.get("entity_name", self.config.get("entity_id", "PBSA Site")),
            "description": self.config.get("description", ""),
            "entity_type": self.config.get("entity_type", "personal_brand"),
        }

        for page in architecture["pages"]:

            template = self.env.get_template("pages/generic_page.html")

            rendered = template.render(
                entity=entity,
                page=page,
                pillars=self.get_pillars()
            )

            filename = f"{page['name']}.html"

            with open(output_dir / filename, "w", encoding="utf-8") as f:
                f.write(rendered)

    # -----------------------------
    # LOAD ARCHITECTURE TEMPLATE
    # -----------------------------

    def load_architecture(self):

        entity_type = self.config.get("entity_type", "personal_brand")

        architecture_path = Path("generator/architectures") / f"{entity_type}.json"

        if not architecture_path.exists():
            print(f"Architecture '{entity_type}' not found. Using fallback.")
            architecture_path = Path("generator/architectures/personal_brand.json")

        with open(architecture_path, "r", encoding="utf-8") as f:
            architecture = json.load(f)

        return architecture

    # -----------------------------
    # PILLARS
    # -----------------------------

    def get_pillars(self):

        architecture = self.load_architecture()
        return architecture["pages"]