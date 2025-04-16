import dataclasses
import json
import os
from dotenv import load_dotenv

import requests

from constant.prompt_injection import PromptInjection
from harness.base_harness import Harness
import uuid

load_dotenv()

@dataclasses.dataclass
class WriteSonicHarness(Harness):
    name: str = "write_sonic"
    site_url: str = "https://app.writesonic.com/"
    application_document: str = "Writesonic is an AI writer that creates SEO-friendly content for blogs, Facebook ads, Google ads, and Shopify for free."

    def run_harness(self, prompt_injection: PromptInjection):
        url = "https://api-azure.botsonic.ai/v1/botsonic/generate"

        headers = {
            "accept": "application/json",
            "token": os.getenv("BOTSONIC_API_KEY"),
            "User-Agent": "python-requests/2.28.1",
            "Connection": "keep-alive"
        }

        json_data = {
            "input_text": prompt_injection.get_attack_prompt(),
            "chat_id": str(uuid.uuid4())  # Random chat ID per request
        }

        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code != 200:
            print(f"[!] Botsonic API Error {response.status_code}: {response.text}")
            return ""

        try:
            return response.json().get("answer", "")
        except Exception as e:
            print(f"[!] Failed to parse Botsonic response: {e}")
            return ""