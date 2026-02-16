## preparations to run this project 

1. make a postgresql database on which we want to run our queries  
    |=> run postgresql on docker using <docker compose up -d>
    |=> access psql on docker using <psql -U prateek -d week7Day4>
    |=> insert tables using <seed_db.py>   
    |=> see schema using <\dt> describe tables
    
## Main.py => send queery to sql_piplines.py  
    1. schema loader loads the schema
    2. generate sql(question , schema)
    3. validate sql 
    4. execute sql
    5. provide summary(question, sql, result)

