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

def create_planner_agent():
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
        name="PlannerAgent",
        model_client=model_client,
        model_client_stream=True,
        system_message="""
            You are a PLANNER AGENT. Your ONLY job is to produce a clear, structured, step-by-step plan for answering any given query.

            STRICT RULES:
            1. You ONLY plan. Never execute steps. Never provide the actual answer.
            2. Break the query down into logical, sequential steps.
            3. Each step must be actionable and specific.
            4. Keep steps concise — one clear action per step.
            5. Number every step.

            OUTPUT FORMAT:
            ## Objective (1 sentence)
            ...

            ## Steps
            1. ...
            2. ...
            3. ...
            (add as many steps as needed)

            ## Expected Output
            Briefly describe what the final answer should look like.
            """,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    return agent

BASE_DIR = Path(__file__).resolve().parents[1]
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUTS_DIR = BASE_DIR / "outputs"

def save_input(query):
    INPUTS_DIR.mkdir(exist_ok=True)
    with open(INPUTS_DIR / "planner.md", "w") as f:
        f.write(query)

def save_output(output):
    OUTPUTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUTS_DIR / "Planner.md", "w") as f:
        f.write(output)

async def plan_steps(query):
    agent = create_planner_agent()
    print(f"[[[PlannerAgent]]] ==> Starting planning...")

    save_input(query)

    prompt = query

    output = ""
    buffer = ""
    async for event in agent.run_stream(task=prompt):
        if isinstance(event, ModelClientStreamingChunkEvent):
            buffer += event.content
            if "\n" in event.content:
                print(f"[[[PlannerAgent]]] ==> {buffer}")
                buffer = ""
            output += event.content
        elif isinstance(event, TaskResult):
            print(f"[[[PlannerAgent]]] ==> {buffer}")
            output = event.messages[-1].content

    save_output(output)
    print("\n\n[[[PlannerAgent]]] ==> Plan ready.\n")
    return output