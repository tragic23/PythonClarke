# PythonClarke

A personal Discord bot project written in Python using `discord.py`.

## Version 1

- Check messages and reactions for non-Clarke emojis using a regex.
- Time out users for one minute when they use a non-Clarke emoji in a message or reaction.

## Version 2
- Welcome new members in a configured server channel.
- Add timestamped server logs for bot activity and moderation outcomes.
- Add a Dockerfile to run the bot in a container.

## Version 3
- Detect non-Clarke emojis added when a message is edited and time out the author.
- Handle reaction additions with the raw reaction event and fetch the server member before timing them out.
- Rename the emoji-checking function to `check_clarke_nonEmoji`.
- Log message edits, reactions, and timeout outcomes.

## Edge cases to fix

- Some places where objcet would return null or None are not handled
- Custom emojis are not catch in `check_clarke_nonEmoji`

## To do

- Run a quarterly mayor poll and change the winner's nickname to Mayor of Clarke Town.
- Make the bot join a voice chat when at least 2 people are present and play cat meow audio clips.
- Make happy meows sounds in voice chat when a new member joins chat, and sad meow when member leaves
- add Commands