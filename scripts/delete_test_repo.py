import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from deployment.github_client import GitHubClient


repo_name = "pbsa-test-pbsa_generator"


client = GitHubClient()

repo = client.user.get_repo(repo_name)

repo.delete()

print(f"{repo_name} deleted successfully.")