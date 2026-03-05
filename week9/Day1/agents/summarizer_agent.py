import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ModelClientStreamingChunkEvent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_ext.models.ollama import OllamaChatCompletionClient

def create_summarizer_agent(research_text, LLM):
    model_client = OllamaChatCompletionClient(model=LLM) # can also use "mistral"

    agent = AssistantAgent(
        name="SummarizerAgent",
        model_client=model_client,
        model_client_stream=True,
        system_message="""
            You are a SUMMARIZER AGENT. Your ONLY job is to condense raw research into a clean summary.

            STRICT RULES:
            1. You ONLY summarize. Never add new information. Never give recommendations.
            2. Extract the most important points from the research provided.
            3. Remove redundancy. Keep it concise but complete.
            4. Preserve all key facts and data points.
            5. When done, end with exactly: SUMMARY_DONE

            OUTPUT FORMAT:
            ## Summary

            ### Core Topic (1-2 sentences)
            ...

            ### Key Takeaways (bullet points, max 5)
            - ...
            - ...

            ### Critical Data Points
            - ...

            SUMMARY_DONE
            """,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    return agent

async def run_summarizer(research_text, LLM):
    agent = create_summarizer_agent(research_text, LLM)
    print(f"[[[SummarizerAgent]]] Starting summarization...")

    prompt = f"""Please summarize the following research output: {research_text}"""

    output = ""

    async for event in agent.run_stream(task=prompt):
        if isinstance(event, ModelClientStreamingChunkEvent):
            sys.stdout.write(event.content)
            if "\n" in event.content:
                sys.stdout.flush()
            output += event.content
        elif isinstance(event, TaskResult):
            sys.stdout.flush()
            output = event.messages[-1].content

    print("\n\n[[[SummarizerAgent]]] Summarization complete.\n")
    return output