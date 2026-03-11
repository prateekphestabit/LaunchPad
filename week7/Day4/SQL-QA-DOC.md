# How to run this project 
1. make a postgresql database on which we want to run our queries  
    |=> run postgresql on docker using <docker compose up -d>
    |=> access psql on docker using <psql -U prateek -d week7Day4>
    |=> insert tables using <postgresql/seed_db.py>   
    |=> see schema using <\dt> describe tables
    
# flow

## Main.py => send queery to sql_piplines.py  

## sql_pipline
1. generate sql <generator/sql_generator.py>
2. validation <utils/query_validatior.py>
3. execution <utils/safe_execution.py>
4. sumarize using llm <utils/result_summarizer.py>

