import json
from pathlib import Path
from orchestrator.planner import PlannerAgent
from agents.file_agent import FileAgent
# from agents.refelector_agent import run_reflector_agent
# from agents.validator_agent import run_validator
import asyncio

BASE_DIR = Path(__file__).resolve().parents[0]
OUTPUTS_DIR = BASE_DIR / "outputs"

def save_output(output_text, filename):
    OUTPUTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUTS_DIR / filename, "w") as f:
        f.write(output_text)


async def run_pipeline(query):

    # ─── STAGE 0: Load All agents ───────────────────────────────────
    code_agent = None
    db_agent = None
    file_agent = FileAgent()
    planner_agent = PlannerAgent()
    print(f"USER QUERY: {query}\n")

    # ─── STAGE 1: Orchestrator ───────────────────────────────────────
    print("[[[PlannerAgent]]] ==> creating Plan...")
    plan = await planner_agent.plan(query)
    save_output(plan, "tasks.json")
    print("\n\n[[[PlannerAgent]]] ==> Plan ready.\n")

    # ─── STAGE 2: executing tasks in order ─────────────────────────────
    tasks = json.loads(plan)["tasks"] 
    for t in tasks:
        agent = t["agent"]
        task_desc = t["task"]
        
        if(agent == "code_agent"):
            print(f"Executing task using code_agent.py: {task_desc}")
            # result = await run_worker(task_desc, agent="code_agent.py")
            # print(f"Result: {result}\n\n")
        elif(agent == "db_agent"):
            print(f"Executing task using db_agent.py: {task_desc}")
            # result = await run_worker(task_desc, agent="db_agent.py")
            # print(f"Result: {result}\n\n")
        elif(agent == "file_agent"):
            print(f"Executing task using file_agent.py: {task_desc}")
            await file_agent.chat(task_desc)
            # result = await run_worker(task_desc, agent="file_agent.py")
            # print(f"Result: {result}\n\n")
        else:
            print(f"Unknown agent specified: {agent}")
            return

if __name__ == "__main__":
    query = "write a python script to print numbers from 1 to 10"
    asyncio.run(run_pipeline(query)) 
    # save_output(final_answer)