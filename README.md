# PythonClarke

A personal Discord bot project written in Python using `discord.py`.

## Version 1

- Time out users for sending messages that contain non-Clarke emojis.
- Time out users for reacting with non-Clarke emojis.

## Version 2
- Implement a welcome message for new members.
- Add server log messages.
- Containerized; now works in a Docker container


## Edge cases to fix

- Messages edited to include non-Clarke emojis are not detected. (?)
- Reactions to messages sent before the bot starts may not be detected. (?)

## To do

- Detect non-Clarke emojis in edited messages.
- Run a quarterly mayor poll and change the winner's nickname to Mayor of Clarke Town.
- Make the bot join a voice chat when at least four people are present and play cat meow clips.
