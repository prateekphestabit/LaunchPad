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

def create_reflector_agent():
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
        name="ReflectorAgent",
        model_client=model_client,
        model_client_stream=True,
        system_message="""
        You are a REFLECTOR AGENT. Your job is to critically review a draft answer and produce an improved version.

        You will be given:
        - The original user query
        - A structured plan that the answer should follow
        - A draft answer written by a worker agent

        YOUR TASKS:
        1. IDENTIFY ERRORS: Find factual inaccuracies, logical mistakes, missing steps from the plan, or unclear reasoning.
        2. CHECK ALIGNMENT: Verify the answer addresses the query and follows all steps in the plan.
        3. IMPROVE: Rewrite the answer to fix all identified issues, fill in missing information, and improve clarity.

        STRICT RULES:
        - Do NOT skip the reflection step. Always list issues found before rewriting.
        - If the answer is already perfect, state why and return it unchanged.
        - Your final output must contain two clearly labeled sections:

        ## Reflection
        (List all errors, gaps, or improvements identified. If none, state "No issues found.")
        Reflection format:
        - Issue 1: Description of the issue and where it is in the answer.
        - Issue 2: Description of the issue and where it is in the answer.

        ## Improved Answer
        (The fully rewritten and corrected answer.)
        """,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    return agent

BASE_DIR = Path(__file__).resolve().parents[1]
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUTS_DIR = BASE_DIR / "outputs"

def save_input(input, reflector_id):
    INPUTS_DIR.mkdir(exist_ok=True)
    with open(INPUTS_DIR / f"reflector{reflector_id}.md", "w") as f:
        f.write(input)

def save_output(output, reflector_id):
    OUTPUTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUTS_DIR / f"reflector{reflector_id}.md", "w") as f:
        f.write(output)

async def run_reflector_agent(query, plan, answer, reflector_id):
    agent = create_reflector_agent()

    prompt1 = f"""# Original user query:\n## {query}\n\n
# Structured plan that the answer should follow:\n\n{plan}\n\n
# review this answer:\n\n{answer}\n\n
# List only the issues in the answer\n\n"""

    print(f"[[[ReflectorAgent {reflector_id}]]] ==> Reflecting on answer...")

    reflection = ""
    buffer = ""
    async for event in agent.run_stream(task=prompt1):
        if isinstance(event, ModelClientStreamingChunkEvent):
            buffer += event.content
            if "\n" in event.content:
                print(f"[[[ReflectorAgent {reflector_id}]]] ==> {buffer}")
                buffer = ""
            reflection += event.content

        elif isinstance(event, TaskResult):
            print(f"[[[ReflectorAgent {reflector_id}]]] ==> {buffer}")
            reflection = event.messages[-1].content
            buffer = ""

    prompt2 = f"""{reflection}\n\n
# Now, using this reflection, rewrite the answer to fix all issues and improve it. Provide only the rewritten answer without any explanations.\n\n"""
    
    all_inputs = prompt1 + prompt2
    save_input(all_inputs, reflector_id)

    answer = ""
    async for event in agent.run_stream(task=prompt2):
        if isinstance(event, ModelClientStreamingChunkEvent):
            buffer += event.content
            if "\n" in event.content:
                print(f"[[[ReflectorAgent {reflector_id}]]] ==> {buffer}")
                buffer = ""
            answer += event.content

        elif isinstance(event, TaskResult):
            print(f"[[[ReflectorAgent {reflector_id}]]] ==> {buffer}")
            answer = event.messages[-1].content
            buffer = ""
    print(f"\n\n[[[ReflectorAgent {reflector_id}]]] ==> Reflection complete.\n")
    
    save_output(answer, reflector_id)
    return answer