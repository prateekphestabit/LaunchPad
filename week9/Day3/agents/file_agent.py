import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

sys.path.append(str(Path(__file__).resolve().parent))
from tools.file_tool import create_file, create_folder, read_file, list_files, list_directories, get_current_directory

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult, Response
from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage, ToolCallRequestEvent, ToolCallExecutionEvent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import ModelInfo, ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken

message = """
You are a FILE AGENT.
Your only job is to read, write, create files/folders and explain your thinking.

MANDATORY FIRST STEP: For EVERY task, you MUST call get_current_directory() as your FIRST tool call before doing anything else.

RULES:
- ALWAYS start with get_current_directory() — no exceptions.
- After getting the directory, call the appropriate tool to complete the task.
- NEVER write tool call syntax as text. ONLY use the actual tools provided.
- To create a folder: call create_folder(folder_name="name").
- To create a file: call create_file(filename="name.ext", content="...").
- Do not pass extra arguments beyond what is required.
- Do not modify or delete files unless explicitly asked.
- After every tool call, briefly explain what you did.
"""

class FileAgent:
    def __init__(self):
        self.history = []
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
            parallel_tool_calls=False,  
        )

        self.agent = AssistantAgent(
            name="FileAgent",
            model_client=model_client,
            model_client_stream=True,
            system_message=message,
            tools=[create_file, create_folder, read_file, list_files, list_directories, get_current_directory],
            model_context=BufferedChatCompletionContext(buffer_size=50),
            max_tool_iterations=5,
        )

    async def chat(self, query):
        prefixed_query = f"Step 1: Call get_current_directory() right now. Step 2: {query}"
        self.history.append(TextMessage(content=prefixed_query, source="user"))
        output = ""
        buffer = ""
        try:
            async for event in self.agent.on_messages_stream(
                messages=self.history,
                cancellation_token=CancellationToken()
                ):
                
                if isinstance(event, ToolCallRequestEvent):
                    for tool_call in event.content:
                        print(f"[[[FileAgent]]]  Calling tool: {tool_call.name}")
                        print(f"[[[FileAgent]]]  Arguments: {tool_call.arguments}")

                elif isinstance(event, ToolCallExecutionEvent):
                    for result in event.content:
                        print(f"[[[FileAgent]]] Tool result [{result.call_id}]: {result.content}")

                elif isinstance(event, Response):
                    if buffer:
                        print(f"[[[FileAgent]]] ==> {buffer}", flush=True)
                    output += event.chat_message.content

                    self.history.append(event.chat_message)

        except Exception as e:
            print(f"\n ERROR TYPE: {type(e).__name__}")
            print(f" ERROR MESSAGE: {str(e)}")
            
            # Groq puts the failed generation in e.body
            if hasattr(e, 'body') and e.body:
                print(f" FAILED GENERATION:\n{e.body}")
            if hasattr(e, 'response') and e.response:
                print(f" RAW RESPONSE:\n{e.response.text}")

            self.history.pop()
        return output