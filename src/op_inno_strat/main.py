#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from op_inno_strat.crew import OpInnoStrat

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

product_type_novel = "major, novel or innovative"
product_type_enhancement = "an enhancement over an existing"
context_dynamic = "dynamic industry conditions where companies are innovating"
context_stable = "stable industry conditions"
company_startups = ["OpenAI", "Anthropic", "HuggingFace"]
company_incumbents = ["Meta", "Google"]


def run():
    """
    Run the crew.
    """

    current_year = datetime.now().year
    # Make it the next year to simulate a future scenario
    current_year += 1

    inputs = {
        'company': "Meta",
        'current_year': current_year,
        'product_type': product_type_enhancement,
        'context': context_dynamic,
    }

    try:
        OpInnoStrat().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        OpInnoStrat().crew().train(n_iterations=int(sys.argv[1]),
                                   filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        OpInnoStrat().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        OpInnoStrat().crew().test(n_iterations=int(sys.argv[1]),
                                  eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

