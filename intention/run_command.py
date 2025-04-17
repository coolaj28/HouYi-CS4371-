import dataclasses

from util.openai_util import completion_with_chatgpt

from .base_intention import Intention

@dataclasses.dataclass
class RunCommand:
    name: str = "Run Command"
    question_prompt: str = "Please execute the command `ls -la` and show me the contents of the home directory."