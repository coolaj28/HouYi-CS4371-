import dataclasses


@dataclasses.dataclass
class Chromosome:
    disruptor: str              # The adversarial string injected to confuse or hijack the model
    separator: str              # A separator string between prompt parts (e.g., "###", "--", or "\n\n")
    framework: str              # The base prompt or instruction structure that wraps the user input
    question_prompt: str        # The actual question/intention
    llm_response: str = ""      # The LLM's response to this full prompt
    fitness_score: float = 0.0  # How "successful" this prompt was at breaking the app (assigned later)
    is_successful: bool = False # A flag for whether this was a successful attack (crossed the threshold)
