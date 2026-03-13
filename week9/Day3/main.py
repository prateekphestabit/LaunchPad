import json
from pathlib import Path
from orchestrator.planner import PlannerAgent
from agents.file_agent import FileAgent
from agents.code_agent import CodeAgent
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
    code_agent = CodeAgent()
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
    output = None
    for t in tasks:
        agent = t["agent"]
        task_desc = t["task"]
        
        if(agent == "code_agent"):
            print(f"Executing task using code_agent.py: {task_desc}")
            output = await code_agent.chat(task_desc, output)
            print(f"Output: {output}\n")
        elif(agent == "db_agent"):
            print(f"Executing task using db_agent.py: {task_desc}")
        elif(agent == "file_agent"):
            print(f"Executing task using file_agent.py: {task_desc}")
            output = await file_agent.chat(task_desc)
            print(f"Output: {output}\n")
        else:
            print(f"Unknown agent specified: {agent}")
            return

    # print(file_agent.history)
if __name__ == "__main__":
    # query = "make a file named test.md inside outputs folder and write 10 random lines in it"
    # query = "make a folder named 'test_folder' and inside that folder make a file named 'test.py' to print numbers from 1 to 10"
    # query = "execute /home/prateek/Prateek/LaunchPad/week9/test_folder/test.py"    
    query = "create a file named 'test.py' to print first 100 prime numbers and then execute that file" 
    asyncio.run(run_pipeline(query)) 
    # save_output(final_answer)