# Shelly Surf AI 🐚
- San Diego AI Surf App (Could be scaled to the rest of the world)
- Uses the spots I love to go to
- Way to show my knowledge of DB, JWT, DOCKER, and learn LLMs

# How to run it locally
> easy method
1. Download Docker 🐋
2. Run this in the terminal `docker-compose up --build`
    - This step may take a while because it has to download the lite version of the AI
    - Depends how fast ur wifi is
3. Access the website at this link `http://127.0.0.1:8012`

# Documentation

- [DB](https://github.com/F1nnC/Shelly-AI/edit/main/README.md#db)
  1. [User](https://github.com/F1nnC/Shelly-AI/edit/main/README.md#user)
  2. [spot_id](https://github.com/F1nnC/Shelly-AI/edit/main/README.md#spot_id)
  3. [spot_forecast](https://github.com/F1nnC/Shelly-AI/edit/main/README.md#spot-forecast)

## DB
> What are the db tables
1. user
   - id (int)
   - username (string)
   - email (string)
   - favorite_spots (json data, holds the name and spot id for that spot)
   - password (hashed)
2. spot_forecast
   - id (int)
   - spot_id (string)
   - spot_name (string)
   - time (DateTime obj)
   - surf_min (int)
   - surf_max (int)
   - wave_height (double, avg of the min and max)
   - wind_speed (double)
   - wind_direction (double used for finding onshore, and offshore wind)
   - surf_optimial (value given by surfline)
3. spot_id
   - id (int)
   - name (string)
   - spot_id (string)

## user
> General Info to know
- Uses JWT
- All Api methods are found in `auth.py`
- Contains pretty much every neccesary CRUD method inside for the app

## spot_id
> pretty self explantory
- Only hold the spot names and *surfline spot id*
- the reason the surfline spot id is so important is because it used to fetch the data from surfline
- using the data direct and stored in the spot_forecast
- All Api methods are found in `spot.py`
- Currently the only way to add spots is through postman
- The reason I have so little amount of spots is because I dont want my computer to take to long
- + you have to manualy find the spot ids, [refrence](https://giocaizzi.github.io/pysurfline/examples/SpotForecasts.html)

## spot_forecast
> This one is a bit more complicated than user
- How does it work?
1. Every time the server starts it runs a script on all the spots found inside the spot_id table
2. This script is found in the data directorty
3. All the relevant information is then compiled into the directory
4. It takes the surf in 3 hour increments
5. Most of the time only the most recent data is fetched through the date time feature
- Improvement that could be made, delete old info, i havent decide whether or not im going to use it, but i might not




















# What this project means to me
> No need to read just some my thoughts

- When I first started coding I absolutely hated working in the backend. I thought website design was more of my thing and I stuck to just updating the front end on most of my school projects
- I didn't start to enjoy backend code until my junior year of computer science, by that time the backend that we used in class was made with java springboot.
- However, in my sophomore year in high school, the year of mainly frontend work, I never fully understood the Python Flask backend we used.
- This project was not only something that I wanted to put on my resume that had to do with AI, but it was also to prove I could use Flask at a high level.
- At the end of my high school year I had mostly mastered every aspect of full-stack development, but not knowing how Flask worked always ate at me.
- This project proves to me that I can code flask repos, and that I have mastered all the tools I used in my high school career.
- This is a good confidence boost for me as I enter the next computer science chapter, most likely college. I most likely will be learning react/typescript on my next project cause coding everything in HTML, JS, and CSS is annoying af. Plus I got a couple of cool ideas for it.
