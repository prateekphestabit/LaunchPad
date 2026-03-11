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

message = """
# You are an orchestrator agent.\n

Your job is NOT to solve tasks.
Your job is to decide:\n
1. Which agent should handle which task\n
2. In what order agents should be called\n

# Available agents:\n
    - code_agent: use when you need to write code to solve a task\n
    - db_agent: use when you need to interact with a database like read,write,update,delete data from a database\n
    - file_agent: use when you need to read/write files like .txt, .csv and .py\n

# Always respond in json format and don't include any markdown formatting in your response.:
{
    "tasks": [
        {"agent": <agent_name>,"task": <task_for_that_agent>},
        {"agent": <agent_name>,"task": <task_for_that_agent>},
        ...
}
"""

class PlannerAgent:
    def __init__(self):
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

        self.agent = AssistantAgent(
            name="PlannerAgent",
            model_client=model_client,
            model_client_stream=True,
            system_message=message,
            model_context=BufferedChatCompletionContext(buffer_size=50),
        )

    async def plan(self, query):
        output = ""
        buffer = ""
        async for event in self.agent.run_stream(task=query):
            if isinstance(event, ModelClientStreamingChunkEvent):
                buffer += event.content
                if "\n" in event.content:
                    print(f"[[[PlannerAgent]]] ==> {buffer}")
                    buffer = ""
                output += event.content
            elif isinstance(event, TaskResult):
                print(f"[[[PlannerAgent]]] ==> {buffer}")
                output = event.messages[-1].content
        return output

