import discord
import asyncio
import os
from data import data
from dotenv import load_dotenv

load_dotenv()

PROMOTION_CHANNEL_ID = os.getenv("PROMOTION_CHANNEL_ID")


class LuminBotDiscord(discord.Client):
    """
    Main class for the discord bot.
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

        # if message.content.startswith('$hello'):
        #    await message.channel.send('Hello!')

    async def change_bot_status(self):
        """
        Updates the bot's presence with information about live streams.
        Periodically retrieves stream data and sets the bot's activity to display the number
        of live streams and total viewers. Runs in a loop with a 60-second interval.
        """
        previous_stream_ids = set()

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

            current_stream_ids = {stream["id"] for stream in streams}

            # Check for new streams
            new_streams = current_stream_ids - previous_stream_ids
            for stream_id in new_streams:
                stream_info = next((stream for stream in streams if stream["id"] == stream_id), None)
                if stream_info:
                    await self.send_go_live_message(stream_info)

            total_viewer_count = get_total_viewcount(streams_data)
            live_channels = len(streams)

            status = discord.Activity(type=discord.ActivityType.watching,
                                      name=f"{live_channels} streams | {total_viewer_count} viewers")
            await self.change_presence(activity=status)

            previous_stream_ids = current_stream_ids
            await asyncio.sleep(60)

    async def send_go_live_message(self, stream_info):
        """
        Sends a message when a streamer goes live.

        Parameters:
            stream_info (dict): Information about the live stream.
        """
        channel_id = int(PROMOTION_CHANNEL_ID)
        channel = self.get_channel(channel_id)

        if channel:
            await channel.send(f"{stream_info['user']['name']} has gone live using **LuminBot**! Watch here: https://twitch.tv/{stream_info['user']['name']}")

    def run_bot(self):
        self.run(self.token)
