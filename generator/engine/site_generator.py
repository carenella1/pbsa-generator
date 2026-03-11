import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = Path("generator/templates")
OUTPUT_DIR = Path("output/builds")


class PBSASiteGenerator:

    def __init__(self, config_path):

        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.entity_id = self.config["entity_id"]

        self.env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR)
        )

    def build(self):

        site_dir = OUTPUT_DIR / self.entity_id
        site_dir.mkdir(parents=True, exist_ok=True)

        self.build_homepage(site_dir)

        print(f"Site generated at {site_dir}")

    def build_homepage(self, site_dir):

        template = self.env.get_template("pages/index.html")

        output = template.render(
            entity=self.config
        )

        with open(site_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(output)