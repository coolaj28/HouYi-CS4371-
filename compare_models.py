import json
import pathlib
from loguru import logger
from constant.chromosome import Chromosome
from harness.model_comparison import ModelComparisonHarness
from intention.basic_injections import OverrideInstructions
from iterative_prompt_optimization import IterativePromptOptimizer

# Load config file
config_file_path = pathlib.Path("./config.json")
config = json.load(open(config_file_path))

# Initialize OpenAI API key
import openai
openai.api_key = config["openai_key"]

# Optimization parameters
max_iteration = 3
max_crossover = 0.1
max_mutation = 0.5
max_population = 2

def run_model_test(model_version, intention):
    """Run optimized test for a single model"""
    harness = ModelComparisonHarness(model_version=model_version)
    optimizer = IterativePromptOptimizer(
        intention,
        harness,
        max_iteration,
        max_crossover,
        max_mutation,
        max_population,
    )
    optimizer.optimize()
    return optimizer.best_chromosome

def compare_models():
    """Compare models and display results"""
    intention = OverrideInstructions()
    results = {}
    
    for model in ["gpt-3.5-turbo", "gpt-4"]:
        logger.info(f"\nTesting {model}...")
        results[model] = run_model_test(model, intention)
    
    # Display comparison
    logger.info("\n\n=== MODEL COMPARISON RESULTS ===")
    for model, chromosome in results.items():
        logger.info(f"\nModel: {model}")
        if chromosome:
            logger.info(f"Most successful prompt: {chromosome.framework}")
            logger.info(f"Response: {chromosome.llm_response[:200]}...")
            logger.info(f"Fitness score: {chromosome.fitness_score}")
        else:
            logger.warning("No successful injection found")
    
    # Key differences analysis
    logger.info("\n=== KEY DIFFERENCES ===")
    if results["gpt-3.5-turbo"] and results["gpt-4"]:
        gpt3_score = results["gpt-3.5-turbo"].fitness_score
        gpt4_score = results["gpt-4"].fitness_score
        
        logger.info(f"GPT-3.5 vulnerability score: {gpt3_score}")
        logger.info(f"GPT-4 vulnerability score: {gpt4_score}")
        logger.info(f"Difference: {abs(gpt3_score - gpt4_score)}")
        
        if gpt3_score > gpt4_score:
            logger.info("GPT-3.5 was more vulnerable to injections")
        else:
            logger.info("GPT-4 was more vulnerable to injections")
    else:
        logger.warning("Incomplete data for full comparison")

if __name__ == "__main__":
    compare_models()