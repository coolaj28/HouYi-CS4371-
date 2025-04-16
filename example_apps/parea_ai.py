from dotenv import load_dotenv
import os
import dataclasses
from parea import Parea
from parea.schemas import Completion, LLMInputs, Message, ModelParams, Role
from constant.prompt_injection import PromptInjection
from harness.base_harness import Harness


load_dotenv()
api_key = os.getenv("PAREA_API_KEY")

@dataclasses.dataclass
class PareaHarness(Harness):
    name: str = "parea_ai"
    site_url: str = ""
    application_document: str = "Parea AI is a developer-first observability and evaluation platform designed to streamline the development, monitoring, and improvement of LLM-powered applications. It provides tooling to manage prompts, track model behavior, and evaluate completions across different models and parameters. Parea integrates seamlessly with OpenAI-compatible APIs and supports advanced features like prompt versioning, real-time debugging, cost tracking, and token usage analytics. Ideal for teams building production-grade AI applications, Parea empowers developers to test, iterate, and deploy LLM workflows with confidence."

    def __post_init__(self):
        self.parea = Parea(api_key=api_key) 

    def run_harness(self, prompt_injection: PromptInjection):
        # Initialize client if not done already
        if not hasattr(self, "parea"):
            self.parea = Parea(api_key=api_key)

        message = Message(
            role=Role.user,
            content=prompt_injection.get_attack_prompt()
        )

        llm_inputs = LLMInputs(
            model="gpt-3.5-turbo",
            model_params=ModelParams(temp=0.7),
            messages=[message]
        )

        completion = Completion(llm_configuration=llm_inputs)

        try:
            response = self.parea.completion(completion)
            print(f"[{self.name}] Response: {response.content}")
            return response.content
        except Exception as e:
            print(f"[{self.name}] Error during prompt injection: {e}")
            return None