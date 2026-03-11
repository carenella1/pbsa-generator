import sys
from pathlib import Path

# add project root to python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from generator.engine.site_generator import PBSASiteGenerator


config_path = ROOT / "examples/pbsa-config.json"

generator = PBSASiteGenerator(config_path)

generator.build()