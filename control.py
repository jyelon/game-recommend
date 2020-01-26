import db
import steam
import random
from util import jget, pp

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
    
def get_game_list():
    gl = steam.games()
    for idx, chunk in enumerate(chunks(gl, 1000)):
        print(f"Inserting chunk {idx}...")
        db.store_game_names(chunk)

def get_game_type(appid):
    gtype = steam.apptype(appid)
    db.store_game_type({"appid":appid, "type":gtype})


def get_more_info(game):
    appid = jget(game, "appid")
    gtype = jget(game, "type")
    if gtype == "":
        gtype = steam.apptype(appid)
        print(f"Steam says appid {appid} is {gtype}")
        done = 1
        if gtype == "game": done = 0
        db.store_game_metadata({"appid":appid, "type":gtype, "reviews_fetched":0, "reviews_cursor":"", "reviews_done":done})
        return True
    if gtype != "game":
        return False
    precursor = jget(game, "reviews_cursor")
    fetched = jget(game, "reviews_fetched")
    rl = steam.reviews(appid, precursor)
    reviews = jget(rl, "reviews")
    print(f"Steam reported {len(reviews)} reviews for appid {appid}")
    db.store_reviews(reviews)
    fetched += len(reviews)
    cursor = jget(rl, "cursor")
    done=0
    if cursor == "*" or cursor == precursor:
        done=1
        cursor="*"
    status = {"appid": appid, "type":gtype, "reviews_fetched":fetched, "reviews_done":done, "reviews_cursor":cursor}
    db.store_game_metadata(status)
    return True

def auto_get_info():
    "Find someplace where game info is lacking, and get more info"
    options = db.list_games_with_more_reviews(10)
    if len(options) == 0:
        return False
    pick = random.choice(options)
    print(f"Pick:{pick}")
    return get_more_info(pick)
