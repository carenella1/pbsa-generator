import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from deployment.deploy_site import GitHubDeployer


entity_id = "pbsa_generator"

deployer = GitHubDeployer()

deployer.deploy(entity_id)