# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import sqlite3

import pandas as pd
import requests
import sqlalchemy

USER_ID = "12141073735"
TOKEN = "BQAsUJ6X5SrRGne5vN7VbMpiFtGJKdyCSCZI7wFuUnh8HK34xKVqgJiyWwBcJdu3fL7eYixdvbQ6w0a-gK8-c-3NKTFL2dk3k-Wp8X8DfLCSM4N82JQ3vjOlVQr4WnPprQ8D7C-9ZGyZYbruWl7B_PMig98V88qbofzGvrxaGkMlCci6yRykBEc"
DATABASE_LOCATION = "sqlite:///d:\\my_played_track.db"


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # check whether exists or not data
    if df.empty:
        print("None songs downloaded")
        return False
    # check primary key
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary key check is violated")
    if df.isnull().values.any():
        raise Exception("Null value found")



    # check tha all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    # timestamps = df["timestamp"].tolist()
    # for timestamp in timestamps:
    #     if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
    #         raise Exception("At leas one of the returned songs does not come from within the last 24 hours")

    return True


if __name__ == '__main__':
    # create_a_connection()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers)
    data = r.json()
    # print(data)

    # msg = "this is our message of {name}".format(name = "jorge nizama")
    # print(msg)

    artists = []
    songs_name = []
    played_at = []
    timestamps = []
    for item in data["items"]:
        song_name = item["track"]["album"]["name"]
        artist = item["track"]["album"]["artists"][0]["name"]
        play_at = item["played_at"]
        timestamp = item["played_at"][0:10]
        artists.append(artist)
        songs_name.append(song_name)
        played_at.append(play_at)
        timestamps.append(timestamp)

    song_dict = {
        "artists": artists,
        "songs_name": songs_name,
        "played_at": played_at,
        "timestamp": timestamps
    }

    # save using Pandas Dataframe
    song_df = pd.DataFrame(song_dict, columns=["artists", "songs_name", "played_at", "timestamp"])

    if check_if_valid_data(song_df):
        print(song_df)


        engine = sqlalchemy.create_engine(DATABASE_LOCATION)
        conn = sqlite3.connect('my_played_track.sqlite')
        cursor = conn.cursor()

        sql_query = """
        CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY(played_at)
        )
        """
        cursor.execute(sql_query)
        print("Opened database successfully")

        try:
            song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
        except:
            print("Data already in the database")
        conn.close()
        print("Close database successfully")
