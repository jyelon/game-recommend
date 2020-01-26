"Fetch data from steam in JSON format."

import urllib.parse
from util import jfetch, jget

joshkey="C786B33A0649B58DEB8DC04692A6A658"
joshid="76561198141326535"

class SteamError(Exception):
    pass



def games():
    "Returns a list of all steam games, including only appid and name."
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
    result = jfetch(url)
    return jget(jget(result, 'applist'), 'apps')


def owned(steamid):
    "Gets a list of the games owned by the specified person, including play time."
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={joshkey}&steamid={steamid}&format=json'
    result = jfetch(url)
    response = jget(result, 'response')
    response['steamid'] = steamid
    return response

def reviews_raw(appid, cursor):
    ucursor = urllib.parse.quote(cursor)
    url = f'https://store.steampowered.com/appreviews/{appid}?filter=recent&num_per_page=100&json=1&cursor={ucursor}'
    return jfetch(url)
        
def reviews(appid, cursor):
    "Get the reviews for a game, starting at a specified cursor position."
    result = reviews_raw(appid, cursor)
    result["appid"] = appid
    result.pop('query_summary', None)
    success = jget(result, 'success')
    if success != 1:
        raise SteamException("Steam should have returned success")
    result["precursor"] = cursor
    for r in jget(result, "reviews"):
        author = jget(r, "author")
        r.update(author)
        del r["author"]
        r["appid"] = appid
    return result

def apptype(appid):
    "Get the app type for the specified appid."
    assert(isinstance(appid, int))
    url = f'https://store.steampowered.com/api/appdetails/?appids={appid}&filters=basic'
    result = jfetch(url)
    appresult = jget(result, str(appid))
    success = jget(appresult, "success")
    if success == True:
        return jget(jget(appresult, "data"), "type")
    else:
        return "junk"
