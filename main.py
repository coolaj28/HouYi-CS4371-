import json
import pathlib

import loguru
import openai

from iterative_prompt_optimization import IterativePromptOptimizer
from constant.chromosome import Chromosome
from harness.base_harness import Harness

#intentions are the malicious prompt objective used for testing.
from intention.base_intention import Intention
from intention.content_manipulation import ContentManipulation 
from intention.information_gathering import InformationGathering
from intention.prompt_leakage import PromptLeakage
from intention.spam_generation import SpamGeneration
from intention.write_code import WriteCode

#example_apps are the LLM services or application harnesses used for testing.
from example_apps.open_ai import OpenAIHarness
from example_apps.write_sonic import WriteSonicHarness
from example_apps.forefront_ai import ForefrontHarness
from example_apps.parea_ai import PareaHarness

logger = loguru.logger

# Define constants for optimization process
max_iteration = 50
max_crossover = 0.1
max_mutation = 0.5
max_population = 10


def inject(intention: Intention, application_harness: Harness) -> Chromosome:
    # Create and run an IterativePromptOptimizer instance to optimize prompts
    iterative_prompt_optimizer = IterativePromptOptimizer(
        intention,
        application_harness,
        max_iteration,
        max_crossover,
        max_mutation,
        max_population,
    )
    iterative_prompt_optimizer.optimize()
    return iterative_prompt_optimizer.best_chromosome


def main():
    # Initialize prompt injection intention and harness
    content_manipulation = ContentManipulation()
    application_harness = OpenAIHarness()

    # Begin the prompt injection process
    chromosome = inject(content_manipulation, application_harness)

    logger.info("Finish injection")
    if chromosome is None:
        logger.error("Failed to inject prompt, please check the log for more details")

    # Log the results of the injection
    if chromosome.is_successful:
        logger.info(
            f"Success! Injected prompt: {chromosome.framework}{chromosome.separator}{chromosome.disruptor}"
        )
    else:
        logger.info(
            f"Failed! Injected prompt: {chromosome.framework}{chromosome.separator}{chromosome.disruptor}"
        )
    logger.info(f"Fitness Score: {chromosome.fitness_score}")
    logger.info(f"Response: {chromosome.llm_response}")


if __name__ == "__main__":
    main()
