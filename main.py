import asyncio
import configparser

import discord

from riot_api import RiotAPI
from util import get_logger, extract_queue_rank, extract_remainder, was_win
from discord_bot import DiscordBot


log = get_logger(__name__)


class FooshaLoLTracker:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read("config.ini")
        self._tracked_users = []
        self._ranked_stats = {}

        self._discord_bot = DiscordBot(self._config.get("discord", "api_key"))
        self._riot_api = RiotAPI(self._config.get("riot", "api_key"))

        asyncio.ensure_future(self.check_tracked_users())

    async def start(self):
        log.info("Starting Foosha LoL tracker!")
        asyncio.ensure_future(self._discord_bot.start())
        await self._discord_bot.add_callback("add", self.add_tracked_user)
        await self._riot_api.start()

    async def check_tracked_users(self):

        log.info("Starting check_tracked_users")

        while True:
            temp_rs = {}
            for name in self._tracked_users:
                rs = extract_queue_rank(await self._riot_api.get_ranked_stats_by_name(name),
                                        self._config.get("foosha", "queue_name"))
                temp_rs[name] = rs

            for name in temp_rs.keys():
                if name in self._ranked_stats:
                    if self._ranked_stats[name] != temp_rs[name]:

                        result = was_win(game_a=self._ranked_stats[name], game_b=temp_rs[name])

                        embed = discord.Embed(
                            title="Game result",
                            description=f"{name} {['lost', 'won'][result]} their game!",
                            colour=[0xFF0000, 0x00FF00][result]
                        )

                        embed.add_field(name="Previous rank", value=self._ranked_stats[name].to_str(), inline=True)
                        embed.add_field(name="Current rank", value=temp_rs[name].to_str(), inline=True)

                        await self._discord_bot.announce(stats=embed)

            self._ranked_stats = temp_rs

            await asyncio.sleep(30)

    async def add_tracked_user(self, message):

        name = extract_remainder(message)

        if name not in self._tracked_users:
            self._tracked_users.append(name)
            log.info(f"Added {name} to tracked users")


if __name__ == '__main__':
    flt = FooshaLoLTracker()
    asyncio.ensure_future(flt.start())
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        log.info(f"Shutting down Foosha LoL tracker")