import os
import dataclasses
from dotenv import load_dotenv
from typing import Any
import openai
from openai import OpenAI
from harness.base_harness import Harness
from constant.prompt_injection import PromptInjection

# Load environment variables
load_dotenv()

@dataclasses.dataclass
class OpenAIHarness(Harness):
    model: str = "gpt-4o"
    temperature: float = 0.7
    api_key: str = None

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided or found in environment.")

        self.client = OpenAI(api_key=self.api_key)

    def send_message(self, user_message: str) -> Any:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                temperature=self.temperature
            )
            return response
        except Exception as e:
            print(f"[OpenAIHarness] Error during API call: {e}")
            return {"error": str(e)}

    def run_harness(self, prompt_injection: PromptInjection) -> str:
        attack_prompt = prompt_injection.get_attack_prompt()
        response = self.send_message(attack_prompt)

        if "error" in response:
            print(f"[OpenAIHarness] API Error: {response['error']}")
            return None

        message_content = response.choices[0].message.content
        print(f"Model response: {message_content}")
        return message_content