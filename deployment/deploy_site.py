import subprocess
from pathlib import Path
from deployment.github_client import GitHubClient


class GitHubDeployer:

    def __init__(self):

        self.client = GitHubClient()

    def deploy(self, entity_id):

        site_dir = Path("output/builds") / entity_id
        repo_name = f"pbsa-test-{entity_id}"

        repo = self.client.create_repo(repo_name)

        # initialize git
        subprocess.run(["git", "init"], cwd=site_dir)
        subprocess.run(["git", "add", "."], cwd=site_dir)

        subprocess.run(
            ["git", "commit", "-m", "Initial PBSA site"],
            cwd=site_dir
        )

        remote_url = repo.clone_url

        subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            cwd=site_dir
        )

        subprocess.run(
            ["git", "branch", "-M", "main"],
            cwd=site_dir
        )

        subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=site_dir
        )

        print(f"Repo created: {remote_url}")
        print(f"Site will deploy to: https://{self.client.user.login}.github.io/{repo_name}")