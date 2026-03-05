import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import ModelClientStreamingChunkEvent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_ext.models.ollama import OllamaChatCompletionClient

def create_answer_agent(LLM):
    model_client = OllamaChatCompletionClient(model=LLM)

    agent = AssistantAgent(
        name="AnswerAgent",
        model_client=model_client,
        model_client_stream=True,
        system_message="""
        You are an ANSWER AGENT. Your ONLY job is to craft the final, user-facing answer.

        STRICT RULES:
        1. You ONLY write the final answer. Never add new research or re-summarize.
        2. Use the provided summary to directly answer the original user question.
        3. Be clear, concise, and conversational — this goes directly to the user.
        4. Do NOT use technical headers or bullet-heavy formatting.
        5. Write in natural, flowing paragraphs.
        6. End your response with: ANSWER_COMPLETE

        GOAL: The user asked a question. Give them the best, most direct answer based on the summary.
        """,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    return agent


async def run_answer_agent(summary_text, original_query, LLM):
    agent = create_answer_agent(LLM)
    prompt = f"""
        Original user question: "{original_query}"

        Based on this summary, provide the final answer to the user:

        {summary_text}
        """

    print(f"[[[AnswerAgent]]] Generating final answer...")
    

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

    print("\n\n[[[AnswerAgent]]] Answer generation complete.\n")
    return output