# Welcome to Poyo Bot! 

The reason I made this bot is because I wanted to create a new experience for my Discord server.  
This bot is currently a work in progress and I am actively working on adding more functionality.  

---

## Features (so far)
- `!poyoball [question]` → Asks the bot a yes/no question and it responds in different ways based on emotion.
- `!ego [leave blank for yourself or mention another user]` → Measures how big your or another users ego is as a joke 
- `!insult [leave blank for yourself or mention another user]` → Utilizing an insult api, this command allows you to insult yourself or other users
- `!play_cope` → The bot joins and plays a prerecorded audio clip jokingly stating ("I knew the [NFL team here] were bad") , I thought this would be fun to add since my friends are huge NFL fans and to demonstrate the audio integration feature for Discord bots
- `!hack [mention another user]` → Lets you "hack" other users (NOTE: Does not really hack)
- `!tldr [reply to a persons long message with this command]` → Utilizing the Hugging Face transformer model, the bot will generate a concise summary of a replied message. 
- `!warnconfig [add/remove <trigger word>]` → Utilizing SQLite you can add/remove trigger words that the bot will use to automatically punish rule breakers
- `!warnuser [mention a user]` → Allows you to manually warn a user for breaking certain rules
- `!whitelist [add/remove roles]` → Utilizing SQLite you can add/remove roles who are immune to manual and bot warns
- `!quote [sarcastic, valley-girl, genz] (leave blank for normal style)` → The bot quotes a user after you reply to one of their posts with !quote [optional action here]
---

## Planned Features
- More interactive commands  
- Fun games
- Moderation:
    - Spam prevention
    - Channel slow mode
    - Managing roles
    - Allow users to select roles in Roles channel
 
## How to add to your server via Ubuntu VPS
- Run the following
    - ```bash
      sudo apt update && sudo apt install -y docker.io docker-compose git
- Verify Docker installed
    - docker --version
      docker compose version
      git --version
- Clone the the repositiory
  - I added it to /opt so cd into that direcotry
    ```bash
      cd /opt
      sudo git clone https://github.com/<your-github-username>/Poyo-Bot.git
- Add the .env file to /opt/
  ```bash
  sudo nano .env
  ```
  - Edit the file like so
    ```bash
      DISCORD_TOKEN=your_discord_token_here
      DB_PATH=/opt/databases  #You'll need to create the databases folder
      FFMPEG_LOCATION=/usr/bin/ffmpeg
      AUDIO_PATH=/opt/resources/audio_file_goes_here #You'll need to create the resources folder
      
- Update the docker-compose.yml file
  ```bash
  version: '3.9'

    services:
      poyobot:
        container_name: poyobot
        build:
          context: ./Poyo-Bot
        env_file: /opt/.env
        volumes:
          - ./Poyo-Bot/resources:/opt/resources
          - /opt/databases:/opt/databases
        restart: unless-stopped
- Build and run the bot
  - Run the following
    ```bash
    docker compose up -d --build
