import json
import pathlib
import os
import loguru
import openai

from constant.chromosome import Chromosome
from harness.base_harness import Harness
from example_apps.write_sonic import WriteSonicHarness
from intention.write_code import WriteCode
from intention.base_intention import Intention
from intention.content_manipulation import ContentManipulation
from iterative_prompt_optimization import IterativePromptOptimizer

logger = loguru.logger

#openai.api_key = os.getenv('')

# Define constants for optimization process
max_iteration = 1
max_crossover = 0.1
max_mutation = 0.5
max_population = 1


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
    content_manipulation = WriteCode()
    application_harness = WriteSonicHarness()

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