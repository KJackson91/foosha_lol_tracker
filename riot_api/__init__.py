from riotwatcher import LolWatcher, ApiError

from util import get_logger

log = get_logger(__name__)


class RiotAPI:
    def __init__(self, api_key, region='na1'):
        self._api_key = api_key
        self._lol_watcher = None
        self._region = region

    async def start(self):
        log.info("Starting Riot API")
        self._lol_watcher = LolWatcher(self._api_key)
        log.info("Started Riot API")

    async def get_puuid_by_name(self, name):
        log.info(f"Fetching player: {name}")
        return self._lol_watcher.summoner.by_name(self._region, name)

    async def get_ranked_stats_by_name(self, name):
        log.info(f"Fetching ranked stats for player: {name}")

        return self._lol_watcher.league.by_summoner(self._region, name)
