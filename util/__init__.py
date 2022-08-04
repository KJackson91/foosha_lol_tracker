import colorlog
import sys,random,string
from PIL import Image,ImageDraw,ImageFont


from util.league_rank import LoLRank



def get_numeric_division(division):
    if division == "IV":
        return 0
    elif division == "III":
        return 1
    elif division == "II":
        return 2
    elif division == "I":
        return 3

def get_numeric_tier(tier):
    if tier == "IRON":
        return 0
    elif tier == "BRONZE":
        return 1
    elif tier == "SILVER":
        return 2
    elif tier == "GOLD":
        return 3
    elif tier == "PLATINUM":
        return 4
    elif tier == "DIAMOND":
        return 5
    elif tier == "MASTER":
        return 6
    elif tier == "GRANDMASTER":
        return 7
    elif tier == "CHALLENGER":
        return 8


def was_win(game_a, game_b):
    
    game_a = game_a.to_dict()
    game_b = game_b.to_dict()


    if get_numeric_tier(game_b["tier"]) < get_numeric_tier(game_a["tier"]):
        return False
    elif get_numeric_division(game_b["rank"]) < get_numeric_division(game_a["rank"]):
        return False
    elif game_b["lp"] < game_a["lp"]:
        return False
    else:
        return True


def extract_remainder(message):
    text = message.content
    return " ".join(text.split()[1:])


def extract_command(message):
    return message.content.split()[0][1:]


def extract_queue_rank(obj, queue_name):
    for queue in obj:
        if queue["queueType"] == queue_name:
            return LoLRank(queue['tier'], queue['rank'], queue['leaguePoints'])



def get_logger(name: str) -> colorlog.log:
    handler = colorlog.StreamHandler(stream=sys.stdout)
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s[%(levelname)s][%(name)s]:%(message)s'))

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(colorlog.DEBUG)

    return logger


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



async def generateimage(values):
    RN = ImageFont.truetype("./assets/fonts/roman_font_7.ttf", 28, encoding="unic")
    img = Image.open('./assets/img/' + values.tier + ".png")
    width, height = img.size
    id = "./temp/" + id_generator() + ".png"
    img.save(id)
    return id