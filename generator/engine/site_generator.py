import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from generator.architecture_loader import load_architecture
from generator.registry.registry_manager import EntityRegistry


class PBSASiteGenerator:

    def __init__(self, config_path):

        self.config_path = Path(config_path)

        with open(self.config_path) as f:
            self.config = json.load(f)

        self.templates_dir = Path("generator/templates")

        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir)
        )

    def build(self):

        entity_id = self.config["entity_id"]

        # Register entity in ecosystem registry
        registry = EntityRegistry()
        registry.register_entity(
            entity_id=entity_id,
            entity_type=self.config.get("entity_type", "unknown")
        )

        output_dir = Path("output/builds") / entity_id

        if output_dir.exists():
            shutil.rmtree(output_dir)

        output_dir.mkdir(parents=True)

        print(f"Building PBSA site for {entity_id}")

        entity_type = self.config.get("entity_type", "personal_brand")

        architecture = load_architecture(entity_type)

        pillars = architecture["pillars"]

        # Navigation structure
        navigation = [{"name": "Home", "url": "/"}]

        for pillar in pillars:
            navigation.append({
                "name": pillar.title(),
                "url": f"/{pillar}/"
            })

        # Copy static assets
        self.copy_assets(output_dir)

        # Build homepage
        self.build_homepage(output_dir, navigation)

        # Build pillar pages
        self.build_pillars(output_dir, pillars, navigation)

        # Generate sitemap
        self.build_sitemap(output_dir, pillars)

        # Generate robots.txt
        self.build_robots(output_dir)

        print(f"Site generated at {output_dir}")

    def build_homepage(self, site_dir, navigation):

        template = self.env.get_template("pages/index.html")

        entity = {
            "site_name": self.config["entity_id"].replace("_", " ").title()
        }

        rendered = template.render(
            entity=entity,
            config=self.config,
            navigation=navigation
        )

        with open(site_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(rendered)

        print("Homepage generated")

    def build_pillars(self, site_dir, pillars, navigation):

        for pillar in pillars:

            pillar_dir = site_dir / pillar
            pillar_dir.mkdir(exist_ok=True)

            template = self.env.get_template("pages/pillar.html")

            entity = {
                "site_name": self.config["entity_id"].replace("_", " ").title()
            }

            rendered = template.render(
                pillar=pillar,
                entity=entity,
                config=self.config,
                navigation=navigation
            )

            with open(pillar_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"Pillar generated: {pillar}")

    def copy_assets(self, site_dir):

        static_dir = Path("generator/static")

        if not static_dir.exists():
            return

        dest = site_dir / "assets"

        shutil.copytree(static_dir, dest)

        print("Assets copied")

    def build_sitemap(self, site_dir, pillars):

        urls = []

        urls.append("<url><loc>/</loc></url>")

        for pillar in pillars:
            urls.append(f"<url><loc>/{pillar}/</loc></url>")

        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>
"""

        with open(site_dir / "sitemap.xml", "w") as f:
            f.write(content)

        print("Sitemap generated")

    def build_robots(self, site_dir):

        robots = """
User-agent: *
Allow: /

Sitemap: /sitemap.xml
"""

        with open(site_dir / "robots.txt", "w") as f:
            f.write(robots)

        print("robots.txt generated")