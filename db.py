import mysql.connector

cnx = mysql.connector.connect(user='admin', password='monkeynopants', host='127.0.0.1', database='steam')
cursor = cnx.cursor(dictionary=True)


def store_game_names(games):
    "Store a list of game names.  Input must be a list of records containing appid and name."
    for g in games:
        command = "INSERT IGNORE INTO games (name, appid) VALUES (%(name)s, %(appid)s)"
        cursor.execute(command, g)
        command = "UPDATE games SET name=%(name)s WHERE appid=%(appid)s"
        cursor.execute(command, g)
    cnx.commit()


def store_reviews(reviews):
    "Store a bunch of reviews"
    for r in reviews:
        command = ("REPLACE INTO usergames (appid, steamid, steam_purchase, received_for_free, playtime_forever, voted_up, review) "
                   "VALUES (%(appid)s, %(steamid)s, %(steam_purchase)s, %(received_for_free)s, %(playtime_forever)s, %(voted_up)s, %(review)s) ")
        cursor.execute(command, r)
    cnx.commit()

def store_game_metadata(info):
    "Store metadata about a game"
    command = ("UPDATE games SET type=%(type)s, "
                                 "reviews_fetched=%(reviews_fetched)s, "
                                 "reviews_cursor=%(reviews_cursor)s, "
                                 "reviews_done=%(reviews_done)s "
               "WHERE appid = %(appid)s")
    cursor.execute(command, info)
    cnx.commit()

def list_games_with_more_reviews(n):
    "Get a list of games that still need to have their reviews fetched"
    data = {"limit": n}
    command = ("SELECT appid, name, type, reviews_fetched, reviews_cursor FROM games "
                "WHERE reviews_done=0 ORDER BY reviews_fetched ASC limit %(limit)s")
    cursor.execute(command, data)
    results = cursor.fetchall()
    return results

