# PySpoty
This is a project to show how integrate API Spotify using #Python+sqlite3+Pandas DataFrame+SqlAlchemy#

/*
  Getting data from Spotify.
  1) Get Token from API Spotify
  2) Format this to JSON
  3) Use tool to read JSON Content or use debugger of Python to browser the content using method keys of an array  
  
*/
  
  
  engine = sqlalchemy.create_engine(DATABASE_LOCATION)
  ...
  
  
  r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers)
    data = r.json()
    
  ...

  # save using Pandas Dataframe
    song_df = pd.DataFrame(song_dict, columns=["artists", "songs_name", "played_at", "timestamp"])


