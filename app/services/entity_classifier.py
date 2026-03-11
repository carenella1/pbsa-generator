import os
from openai import OpenAI


class EntityClassifier:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def classify(self, description: str) -> str:

        prompt = f"""
You are an architecture classifier for a website generator.

Your job is to classify a user's project into ONE of the following entity types:

personal_brand
creator
artist
developer
project
company
research

Return ONLY the classification word.

User description:
{description}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You classify website architectures."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip().lower()

        return result