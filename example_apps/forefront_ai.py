import dataclasses
import os
import requests
from dotenv import load_dotenv

from constant.prompt_injection import PromptInjection
from harness.base_harness import Harness

# Load environment variables from .env file
load_dotenv()

@dataclasses.dataclass
class ForefrontHarness(Harness):
    name: str = "forefront"
    site_url: str = "https://www.forefront.ai/"
    application_document: str = (
        "Forefront is a platform that offers access to various language models "
        "including GPT-4 and Claude with API integration for custom LLM applications."
    )

    def run_harness(self, prompt_injection: PromptInjection) -> str:
        """Send a prompt injection attack to Forefront.ai and return the response."""
        url = "https://api.forefront.ai/v1/chat/completions"
        api_key = os.getenv("FOREFRONT_API_KEY")
        model_id = "Artples/L-MChat-7b"
        if not api_key:
            print("[!] FOREFRONT_API_KEY not found in environment variables.")
            return ""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_id,
            "messages": [
                {"role": "user", "content": prompt_injection.get_attack_prompt()}
            ],
            "max_tokens": 128,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
        except requests.RequestException as e:
            print(f"[!] Network error while contacting Forefront API: {e}")
            return ""

        if response.status_code != 200:
            print(f"[!] Forefront API Error {response.status_code}: {response.text}")
            return ""

        try:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except (ValueError, KeyError) as e:
            print(f"[!] Failed to parse Forefront response: {e}")
            return ""