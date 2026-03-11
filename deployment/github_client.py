from github import Github
import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()


class GitHubClient:

    def __init__(self):

        token = os.getenv("GITHUB_TOKEN")

        if not token:
            raise ValueError("Missing GITHUB_TOKEN in environment")

        self.github = Github(token)
        self.user = self.github.get_user()

    def create_repo(self, repo_name, private=False):

        repo = self.user.create_repo(
            name=repo_name,
            private=private
        )

        return repo