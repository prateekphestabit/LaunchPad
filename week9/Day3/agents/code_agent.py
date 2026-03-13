import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

sys.path.append(str(Path(__file__).resolve().parent))
from tools.file_tool import read_file, list_files, get_current_directory
from tools.code_tool import execute_python_file

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage, ToolCallRequestEvent, ToolCallExecutionEvent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import ModelInfo, ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken

message = """
You are a CODE AGENT.
Your ONLY job is to execute existing Python (.py) files and report the output.
You do NOT create, write, or modify files.

MANDATORY FIRST STEP: For EVERY task, call get_current_directory() FIRST.

RULES:
- ALWAYS start with get_current_directory() — no exceptions.
- Use list_files(path) to find .py files if needed.
- Use read_file(filename) to inspect a file before running it if needed.
- Use execute_python_file(filepath) to run the Python file.
- NEVER create or modify files. You only execute.
- After every tool call, briefly explain the result.
"""

class CodeAgent:
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
            name="CodeAgent",
            model_client=model_client,
            model_client_stream=True,
            system_message=message,
            tools=[execute_python_file, read_file, list_files, get_current_directory],
            model_context=BufferedChatCompletionContext(buffer_size=50),
            max_tool_iterations=5,
        )

    async def chat(self, query, previous_output=None):
        if previous_output:
            query = f"{query}\n\nPrevious Output:\n{previous_output}"
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
                        print(f"[[[CodeAgent]]]  Calling tool: {tool_call.name}")
                        print(f"[[[CodeAgent]]]  Arguments: {tool_call.arguments}")

                elif isinstance(event, ToolCallExecutionEvent):
                    for result in event.content:
                        print(f"[[[CodeAgent]]] Tool result [{result.call_id}]: {result.content}")

                elif isinstance(event, Response):
                    if buffer:
                        print(f"[[[CodeAgent]]] ==> {buffer}", flush=True)
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