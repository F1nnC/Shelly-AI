# Shelly Surf AI 🐚
- San Diego AI Surf App (Could be scaled to the rest of the world)
- Uses the spots I love to go to
- Way to show my knowledge of DB, JWT, DOCKER, and learn LLMs

# How to run it locally
> easy method
1. Download Docker 🐋
2. Run this in the terminal `docker-compose up --build`
    - This step may take a while because it has to download the lite version of the AI
3. Access the website at this link `http://127.0.0.1:8012`

# Alternate run locally no Docker
> Basically what the Dockerfile does, if I miss anything look there for help
1. Download [Ollama](https://ollama.com/download) for your respective os
2. Run this command in the terminal after `ollama pull llama3.2:1b`
3. Change Directories into the repo
4. Start Virtual ENV `python -m venv venv`
5. Download the dependencies `pip install -r requirements.txt`
6. Access the website at this link `http://127.0.0.1:8012`
