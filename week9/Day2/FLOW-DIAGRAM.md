## problem 1
- workers will not work parallely because of ollama default configuration 

## solution 
- stop the server <sudo systemctl stop ollama>
- Restart with parallel requests enabled
- <OLLAMA_NUM_PARALLEL=2 ollama serve>

## problem 2
- local llm was very slow for again and again debugging 
- there for using grq api for llm part

## saved inputs and outpus for each agent for better debugging as debugging using console for parallel outputs caused many errors and confussion 

## problem 3
- api limit exceded 5 debug session almost costed 55 calls 
- solution freze the above layers and take input from the md files

## complete flow mentioned in the main file 

## env file format 
GROQ_API_KEY=key
GROQ_MODEL=llama-3.3-70b-versatile