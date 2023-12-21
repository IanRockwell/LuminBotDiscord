import discord
import asyncio
from data import data  # Assuming you have a data module

class LuminBotDiscord(discord.Client):
    """
    LuminBotDiscord class is a Discord bot built on the discord.py library.
    It extends the discord.Client class to handle events and interact with the Discord API.

    Attributes:
        token (str): The bot token used for authentication with the Discord API.

    Methods:
        __init__(self, token): Initializes the LuminBotDiscord instance with the provided bot token.
        on_ready(self): Event handler called when the bot has successfully connected to Discord.
        on_message(self, message): Event handler called when a message is received in a channel.
        change_bot_status(self): Updates the bot's presence with information about live streams.
        run_bot(self): Initiates the bot's connection to the Discord API and starts event processing.
    """

    def __init__(self, token):
        """
        Initializes the LuminBotDiscord instance.

        Parameters:
            token (str): The bot token used for authentication with the Discord API.
        """
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.token = token

    async def on_ready(self):
        """
        Event handler called when the bot has successfully connected to Discord.
        Displays a message in the console and updates the bot's status.
        """
        print(f'We have logged in as {self.user}')
        await self.change_bot_status()

    async def on_message(self, message):
        """
        Event handler called when a message is received in a channel.
        Responds to the '$hello' command with a 'Hello!' message.

        Parameters:
            message (discord.Message): The message object received.
        """
        if message.author == self.user:
            return

        #if message.content.startswith('$hello'):
        #    await message.channel.send('Hello!')

    async def change_bot_status(self):
        """
        Updates the bot's presence with information about live streams.
        Periodically retrieves stream data and sets the bot's activity to display the number
        of live streams and total viewers. Runs in a loop with a 60-second interval.
        """
        def get_total_viewcount(doc):
            """
            Helper function to calculate the total viewer count from stream data.

            Parameters:
                doc (dict): The stream data document.

            Returns:
                int: The total viewer count.
            """
            streams = doc.get("streams", [])
            total_viewcount = sum(stream.get("viewer_count", 0) for stream in streams)
            return total_viewcount

        while True:
            streams_data = data.get_data("streams")
            streams = streams_data["streams"]

            total_viewer_count = get_total_viewcount(streams_data)
            live_channels = len(streams)

            status = discord.Activity(type=discord.ActivityType.watching,
                                      name=f"{live_channels} streams | {total_viewer_count} viewers")
            await self.change_presence(activity=status)
            await asyncio.sleep(60)
    def run_bot(self):
        self.run(self.token)
