from agents.research_agent import run_research
from agents.summarizer_agent import run_summarizer
from agents.answer_agent import run_answer_agent
import asyncio

LLM = "phi3"  # can also use "mistral"
async def run_pipeline(query):

    print(f"USER QUERY: {query}\n")

    # ─── STAGE 1: Research ───────────────────────────────────────
    print("[[[ResearchAgent]]] ==> Gathering information")
    research_output = await run_research(query, LLM)

    # ─── STAGE 2: Summarize ──────────────────────────────────────
    print("[[[SummarizerAgent]]] ==> Condensing research")
    summary_output = await run_summarizer(research_output, LLM)

    # # ─── STAGE 3: Answer ─────────────────────────────────────────
    print("[[[AnswerAgent]]] ==> Crafting final answer")
    await run_answer_agent(summary_output, query, LLM)


if __name__ == "__main__":
    asyncio.run(run_pipeline("What is machine learning and how is it used in healthcare?")) 