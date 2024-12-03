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
3. Change the Directory to the repo `cd Shelly-AI`
4. Start Virtual ENV `python -m venv venv`
5. Activate VENV `source venv/bin/activate`
6. Download the dependencies `pip install -r requirements.txt`
7. Run app.py `app.py inside the python folder`
8. Access the website at this link `http://127.0.0.1:8012`

# What this project means to me
> No need to read just some my thoughts

When I first started coding I absolutely hated working in the backend. I thought website design was more of my thing and I stuck to just updating the front end on most of my school projects. I didn't start to enjoy backend code until my junior year of computer science, by that time the backend that we used in class was made with java springboot. However, in my sophomore year in high school, the year of mainly frontend work, I never fully understood the Python Flask backend we used. This project was not only something that I wanted to put on my resume that had to do with AI, but it was also to prove I could use Flask at a high level. At the end of my high school year I had mostly mastered every aspect of full-stack development, but not knowing how Flask worked always ate at me. This project proves to me that I can code flask repos, and that I have mastered all the tools I used in my high school career. This is a good confidence boost for me as I enter the next computer science chapter, most likely college. I most likely will be learning react/typescript on my next project cause coding everything in HTML, JS, and CSS is annoying af. Plus I got a couple of cool ideas for it.
