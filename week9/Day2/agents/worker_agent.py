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

def create_answer_agent():
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
        name="AnswerAgent",
        model_client=model_client,
        model_client_stream=True,
        system_message="""
        You are an ANSWER AGENT. Your ONLY job is to answer a user query by strictly following a structured plan.

        STRICT RULES:
        1. You MUST follow the plan's steps IN ORDER to frame your answer.
        2. Your answer must match the Expected Output described in the plan.
        3. Write in clear, well-structured paragraphs with appropriate headings.
        4. Do NOT add information beyond what the plan calls for.

        GOAL: Execute every step in the plan to produce a complete, structured answer to the user's query.
        """,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    return agent

BASE_DIR = Path(__file__).resolve().parents[1]
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUTS_DIR = BASE_DIR / "outputs"

def save_input(input, worker_id):
    INPUTS_DIR.mkdir(exist_ok=True)
    with open(INPUTS_DIR / f"worker{worker_id}.md", "w") as f:
        f.write(input)

def save_output(output, worker_id):
    OUTPUTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUTS_DIR / f"worker{worker_id}.md", "w") as f:
        f.write(output)

async def run_worker(query, plan, worker_id):
    agent = create_answer_agent()

    prompt = f"""# Plan structure to answer the query:\n\n\n{plan}\n\n\n
# answer this query using above plan:\n{query}
"""

    save_input(prompt, worker_id)
    print(f"[[[WorkerAgent {worker_id}]]] ==> Generating final answer...")

    output = ""
    buffer = ""
    async for event in agent.run_stream(task=prompt):
        if isinstance(event, ModelClientStreamingChunkEvent):
            buffer += event.content
            if "\n" in event.content:
                print(f"[[[WorkerAgent {worker_id}]]] ==> {buffer}")
                buffer = ""
            output += event.content
            
        elif isinstance(event, TaskResult):
            print(f"[[[WorkerAgent {worker_id}]]] ==> {buffer}")
            output = event.messages[-1].content

    save_output(output, worker_id)
    print(f"\n\n[[[WorkerAgent {worker_id}]]] ==> Answer generation complete.\n")
    return output