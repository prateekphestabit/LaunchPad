from pathlib import Path
from orchestrator.planner import plan_steps
from agents.worker_agent import run_worker
from agents.refelector_agent import run_reflector_agent
from agents.validator_agent import run_validator
import asyncio

BASE_DIR = Path(__file__).resolve().parents[0]
OUTPUTS_DIR = BASE_DIR / "outputs"

async def run_pipeline(query, try_num):
    if(try_num > 2):
        print("Maximum retry attempts reached. Ending pipeline.")
        return "llm was not able to generate a valid answer after multiple attempts. Please try again later."
    # print(f"USER QUERY: {query}\n")

    # # ─── STAGE 1: Orchestrator ───────────────────────────────────────
    # print("[[[PlannerAgent]]] ==> creating Plan")
    # plan_output = await plan_steps(query)

    # # ─── STAGE 2: worker ──────────────────────────────────────
    # print("[[[WorkerAgent]]] ==> working on plan to answer the query")
    # output1, output2 = await asyncio.gather(
    #     run_worker(query, plan_output, 1),
    #     run_worker(query, plan_output, 2),
    # )

    # # ─── STAGE 3: Reflector ─────────────────────────────────────────
    # print("[[[ReflectorAgent]]] ==> Reflecting and improving answers")
    # reflectedOutput1, reflectedOutput2 = await asyncio.gather(
    #     run_reflector_agent(query, plan_output, output1, 1),
    #     run_reflector_agent(query, plan_output, output2, 2),
    # )

    # ─── Load saved outputs ──────────────────────────────────────────
    plan_output       = (OUTPUTS_DIR / "Planner.md").read_text()
    reflectedOutput1  = (OUTPUTS_DIR / "reflector1.md").read_text()
    reflectedOutput2  = (OUTPUTS_DIR / "reflector2.md").read_text()

    # ─── STAGE 4: Validator ─────────────────────────────────────────
    print("[[[ValidatorAgent]]] ==> Validating reflected answers")
    score1, score2 = await asyncio.gather(
        run_validator(query, plan_output, reflectedOutput1, 1),
        run_validator(query, plan_output, reflectedOutput2, 2),
    )

    print(f"[[[ValidatorAgent]]] ==> Final Scores:\nAnswer 1: {score1}/10\nAnswer 2: {score2}/10")

    if score1 >= 5 and score2 >= 5:
        if score1 >= score2:
            return reflectedOutput1
        else:
            return reflectedOutput2
    else:
        return run_pipeline(query, try_num + 1)


def save_output(output_text):
    OUTPUTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUTS_DIR / f"finalAnswer.md", "w") as f:
        f.write(output_text)

if __name__ == "__main__":
    query = "What is machine learning and how is it used in healthcare?"
    final_answer = asyncio.run(run_pipeline(query, 1)) 
    save_output(final_answer)