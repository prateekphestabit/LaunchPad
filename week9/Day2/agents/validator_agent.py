import re
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ModelClientStreamingChunkEvent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import ModelInfo, ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

def create_validator_agent():
    model_client = OpenAIChatCompletionClient(
        model=os.environ.get("GROQ_MODEL"),
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY"),
        model_info=ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family=ModelFamily.LLAMA_3_3_70B,
            structured_output=False,
        ),
        include_name_in_message=False,  # Groq does not support the 'name' field
    )

    agent = AssistantAgent(
        name="ValidatorAgent",
        model_client=model_client,
        model_client_stream=True,
        system_message="""
        You are a VALIDATOR AGENT. Your ONLY job is to critically evaluate a final answer against the original plan and assign a score out of 10.

        You will be given:
        - The original user query
        - The structured plan that was meant to guide the answer
        - The final answer to be evaluated

        YOUR TASKS:
        1. PLAN ADHERENCE: Check if every step in the plan is addressed in the answer.
        2. COMPLETENESS: Verify that no critical information from the plan is missing.
        3. ACCURACY: Assess whether the content is factually correct and logically sound.
        4. CLARITY: Evaluate whether the answer is well-structured, clear, and easy to understand.
        5. RELEVANCE: Confirm the answer directly addresses the original user query.

        SCORING GUIDE:
        - 9-10: Exceptional. All plan steps covered, accurate, clear, and complete.
        - 7-8:  Good. Most plan steps covered with minor gaps or clarity issues.
        - 5-6:  Average. Some plan steps missing or answer is partially unclear/inaccurate.
        - 3-4:  Poor. Significant gaps, inaccuracies, or plan steps largely ignored.
        - 1-2:  Very Poor. Answer barely follows the plan and is mostly incorrect or irrelevant.

        STRICT OUTPUT FORMAT:
        ## Evaluation

        ### Plan Adherence
        (Describe which plan steps are covered and which are missing.)

        ### Completeness
        (Describe what information is present and what is missing.)

        ### Accuracy
        (Comment on factual correctness and logical soundness.)

        ### Clarity
        (Comment on structure, readability, and presentation.)

        ### Relevance
        (Confirm whether the answer addresses the user query.)

        ## Final Score: X/10
        (Replace X with a whole number from 1 to 10. This line must appear exactly as shown.)
        """,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    return agent


BASE_DIR = Path(__file__).resolve().parents[1]
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUTS_DIR = BASE_DIR / "outputs"


def save_input(input_text, validator_id):
    INPUTS_DIR.mkdir(exist_ok=True)
    with open(INPUTS_DIR / f"validator{validator_id}.md", "w") as f:
        f.write(input_text)


def save_output(output_text, validator_id):
    OUTPUTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUTS_DIR / f"validator{validator_id}.md", "w") as f:
        f.write(output_text)


def extract_score(text: str) -> int | None:
    """Extract the numeric score from '## Final Score: X/10' line."""
    match = re.search(r"##\s*Final Score:\s*(\d+)\s*/\s*10", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


async def run_validator(query, plan, answer, validator_id):
    agent = create_validator_agent()

    prompt = f"""# Original user query:\n\n{query}\n\n
# Structured plan that the answer should follow:\n\n{plan}\n\n
# Final answer to evaluate:\n\n{answer}\n\n
# Evaluate the answer against the plan and assign a score out of 10.
"""

    save_input(prompt, validator_id)
    print(f"[[[ValidatorAgent {validator_id}]]] ==> Evaluating answer...")

    output = ""
    buffer = ""
    async for event in agent.run_stream(task=prompt):
        if isinstance(event, ModelClientStreamingChunkEvent):
            buffer += event.content
            if "\n" in event.content:
                print(f"[[[ValidatorAgent {validator_id}]]] ==> {buffer}")
                buffer = ""
            output += event.content

        elif isinstance(event, TaskResult):
            print(f"[[[ValidatorAgent {validator_id}]]] ==> {buffer}")
            output = event.messages[-1].content
            buffer = ""

    save_output(output, validator_id)

    score = extract_score(output)
    print(f"\n\n[[[ValidatorAgent {validator_id}]]] ==> Validation complete. Score: {score}/10\n")
    return score
