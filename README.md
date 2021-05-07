# personal_website_bot
A simple bot to answer questions on my personal website. (In development)

# Frontend deployment options

Discussed & prioritized on stream March 19, 2021.

## Rasa X + Digital ocean deploy
- create a droplet (tutorial vid: https://www.youtube.com/watch?v=E9-s_49pw_8&ab_channel=Rasa)
- install Rasa X
- while installing, add notice that convos will be seen publically during CDD on the livestream
- create rasa x instance
- add our assistant to our server via github integration
- quick test
- create an image of our action server & add to dockerhub (using manual install)
- add action server to our rasa x instance
- added database to our action server image
- update action server image w/ new version of database
- TODO: 
    - NLU insights
    - share bot & get user data & do CDD

## possibilities for first deployment
- 1st: Rasa X (server, digital ocean?): share using chatbot sharing feature for early CDD & link where appropraite
    - pro: good proof of concpet, can use for inital softlaunch/early CDD, link from my website, need to set up Rasa X anyway for CDD/annotation/model management
    - con: kicks the can on the front end integration problem, already done it on livestream (double dipping :P)
- 2nd: twitter - pref. is for convos in the dms, [which is definintely possible](https://www.freecodecamp.org/news/how-to-create-your-own-auto-direct-message-twitter-bot-for-free-e851265ce730/)
    - pro: a reasonable place to put the assistant, meeting people who ask ?s where they are, needing an account might help prevent abuse
    - con: people need to have a Twitter account (but can add other channels that don't need an account later), need to handle twitter API & TOS; not sure how bots are handleded by that
- 3rd: Website: host on a new, v. simple webpage
    - pro: good proof of concpet, can use for inital softlaunch/early CDD, link from my website, show integration with front end in simple html
    - con: kicks the can on the front end integration problem, why build myself when Rasa X will already do this?
- 4th: Website: Add jekyll plugin (?) to my existing website
    - pro: can use w/ existing website, lots of people want to do something similar (but not necessarily w/ jekyll), if i can find a plugin i don't have to do any front end work myself (besides maybe adjusting color) 
    - con: haven't found a suitable plug in yet, may spend a lot of time searching only the find there's nothing that I can use


## not happening
- Website: Add webchat as raw html to my current website (no idea where that would go??)
     - don't know jekyll well enough & don't really want to spend a bunch of time learning
- Website: rebuild website from scratch in a framework I know better (blogdown?) so I add a chat window
    - not an efficent use of time
- Website: shiny somehow + rserver??? will take a lot of custom work but could be useful to other people as well
    - would take a lot of futzing, maybe in the future, haven't found anything similar 
- discord - would have to make one... can provide a widget w/ htm/json widget?
    - don't have an existing discord, widget integration is the same as the first website option above 
- slack - contributor slack?
    - rasa contribs probably don't need answers to the questions my assistant can answer



# backlog
- TODONE: how to add image to docker-compose (rather than helm)
    - /etc/rasa add image path (on dockerhub) to docker-compose or docker-compose.override.yaml
    - to check running dockers = docker ps
    - to check logs = docker logs [continer id, get from ps list]
- TODO: figure out where your sqlite database is
    - to do: host database in different image?
    - from chat (ty!): app needs DNS translation (add translation in etc/hosts as localhost). copy sentence in dockerfile when you build the image has to moe the db file inside the image
    - from chat: digital ocena managed database? 
- TODO: add error message if database file not found   
- TODO: update rasa in docker compose
- TODO: write doc strings for our Python functions
- TODO: add chitchat to handle polite turns (thank you, goodbye, etc.)
- TODO: a way to handle when the bot has no response