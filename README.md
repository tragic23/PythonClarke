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

## Deploying with Jenkins

The `Jenkinsfile` builds and deploys the bot on the Jenkins machine using Docker Compose.

1. Install Docker Engine and the Docker Compose plugin on the Jenkins machine. Ensure the Jenkins agent can run Docker commands; access to the Docker socket grants powerful host-level privileges.
2. In Jenkins, add a **Secret text** credential containing the Discord bot token with ID `discord-bot-token`.
3. Create a Pipeline job configured as **Pipeline script from SCM**, point it at this repository and deployment branch, and set the script path to `Jenkinsfile`.
4. Run the job. It validates the Compose configuration, builds the image, and starts or updates the `bot` service.

For local Compose runs, put `BOT_TOKEN=...` in an untracked `.env` file. Do not commit the token.