import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ModelClientStreamingChunkEvent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.model_context import BufferedChatCompletionContext

def create_research_agent(LLM):
    model_client = OllamaChatCompletionClient(model=LLM)

    agent = AssistantAgent(
        name="ResearchAgent",
        model_client=model_client,
        model_client_stream=True, 
        system_message="""
            You are a RESEARCH AGENT. Your ONLY job is to gather detailed, factual information.

            STRICT RULES:
            1. You ONLY research. Never summarize. Never give final answers.
            2. Provide raw, detailed information with facts, data points, and context.
            3. Structure your research with clear sections using headers.
            4. Include multiple perspectives or aspects of the topic.
            5. When you have completed your research, end your response with exactly: RESEARCH_DONE

            FORMAT:
            ## Research Findings: [Topic]

            ### Key Facts
            - ...

            ### Background & Context
            ...

            ### Important Details
            ...

            ### Relevant Data Points
            ...

            RESEARCH_DONE
            """,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    return agent


async def run_research(query, LLM):
    agent = create_research_agent(LLM)
    print(f"[[[ResearchAgent]]] ==> Starting research on: '{query}'")

    output = ""

    async for event in agent.run_stream(task=query):
        if isinstance(event, ModelClientStreamingChunkEvent):
            #print(event.content, end="", flush=True) slow.........
            sys.stdout.write(event.content)
            if "\n" in event.content:  # flush only on newlines, not every token
                sys.stdout.flush()
            output += event.content
        elif isinstance(event, TaskResult):
            sys.stdout.flush()  # final flush before done
            # Final result — grab the last assistant message as the full output
            output = event.messages[-1].content

    print("\n\n[[[ResearchAgent]]] ==> Research complete.\n")

    return output