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