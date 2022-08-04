import discord

from util import get_logger, extract_command

log = get_logger(__name__)


class DiscordBot(discord.Client):
    def __init__(self, api_key, cmd_prefix="!", **options):
        super().__init__(**options)
        self._api_key = api_key
        self._callbacks = {}
        self._cmd_prefix = cmd_prefix
        self._announce_channels = []

    async def start(self):
        log.info("Starting Discord Bot")
        await super().start(self._api_key)
        log.info("Started Discord Bot")

    async def on_ready(self):
        await self.add_callback("watch", self.add_announce_channel)
        log.info(f"{self.user} connected!")
        log.info("Discord Bot ready")

    async def add_announce_channel(self, message):
        chan_id = message.channel.id

        if chan_id not in self._announce_channels:
            log.info(f"Adding {chan_id} to announce channels")
            self._announce_channels.append(chan_id)

    async def announce(self,file,stats):
        for channel in self._announce_channels:
            chan = self.get_channel(channel)
            await chan.send(file=file,embed=stats)

    async def on_message(self, message):

        text = message.content

        if text.startswith(self._cmd_prefix):
            cmd = extract_command(message)
            if cmd in self._callbacks:
                await self._callbacks[cmd](message)

    async def add_callback(self, command, callback):
        log.info(f"Adding callback for command: {command}")
        self._callbacks[command] = callback
        log.info(self._callbacks)