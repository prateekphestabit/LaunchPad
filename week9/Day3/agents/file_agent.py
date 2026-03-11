import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

sys.path.append(str(Path(__file__).resolve().parent))
from tools.file_tool import create_file, read_file, list_files

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ModelClientStreamingChunkEvent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import ModelInfo, ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

message = """
You are a FILE AGENT.
your only job is to read, write and create files .
Follow the instructions carefully and strictly.
"""

class FileAgent:
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
            include_name_in_message=False,  
        )

        self.agent = AssistantAgent(
            name="FileAgent",
            model_client=model_client,
            model_client_stream=True,
            system_message=message,
            tools=[create_file, read_file, list_files],
            model_context=BufferedChatCompletionContext(buffer_size=50),
        )

    async def chat(self, query):
        output = ""
        buffer = ""
        async for event in self.agent.run_stream(task=query):
            if isinstance(event, ModelClientStreamingChunkEvent):
                buffer += event.content
                if "\n" in event.content:
                    print(f"[[[FileAgent]]] ==> {buffer}")
                    buffer = ""
                output += event.content
            elif isinstance(event, TaskResult):
                print(f"[[[FileAgent]]] ==> {buffer}")
                output = event.messages[-1].content
        return output