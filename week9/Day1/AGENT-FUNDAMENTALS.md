## How to Run:

1. install ollama to pull phi3(3.8 B) modle locally <curl -fsSL https://ollama.com/install.sh | sh>
2. ollama pull phi3
3. python -m pip install "autogen-agentchat>=0.4" "autogen-ext[ollama]"
4. <ollama serve> ollama servers started at port 11434 <http://localhost:11434>


# flow => main.py => research agent => summarizer agent => answer agent 

run using <python Day1/main.py>