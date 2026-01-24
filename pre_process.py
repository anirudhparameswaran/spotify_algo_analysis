# %%
import pandas as pd
import json
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pd.options.display.max_columns = None

## Function to extract artist names
# text: str - string representation of list of dicts of length equal to number of artists
def get_artist(text):
    artists = ast.literal_eval(text)  # list (artists) containing (artists) dictionaries

    return ", ".join(artist['name'] for artist in artists)

# %%
# example to test
get_artist("[{'external_urls': {'spotify': 'https://open.spotify.com/artist/1Cs0zKBU1kc0i8ypK3B9ai'}, 'href': 'https://api.spotify.com/v1/artists/1Cs0zKBU1kc0i8ypK3B9ai', 'id': '1Cs0zKBU1kc0i8ypK3B9ai', 'name': 'David Guetta', 'type': 'artist', 'uri': 'spotify:artist:1Cs0zKBU1kc0i8ypK3B9ai'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/64M6ah0SkkRsnPGtGiRAbb'}, 'href': 'https://api.spotify.com/v1/artists/64M6ah0SkkRsnPGtGiRAbb', 'id': '64M6ah0SkkRsnPGtGiRAbb', 'name': 'Bebe Rexha', 'type': 'artist', 'uri': 'spotify:artist:64M6ah0SkkRsnPGtGiRAbb'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1vyhD5VmyZ7KMfW5gqLgo5'}, 'href': 'https://api.spotify.com/v1/artists/1vyhD5VmyZ7KMfW5gqLgo5', 'id': '1vyhD5VmyZ7KMfW5gqLgo5', 'name': 'J Balvin', 'type': 'artist', 'uri': 'spotify:artist:1vyhD5VmyZ7KMfW5gqLgo5'}]")

# %%
## Load and clean the data
# index_col=0 : consider first column as index
# sort by position in ascending order and reset index
df = pd.read_csv('played_out.csv', index_col=0).sort_values(by='position', ascending=True).reset_index(drop=True)

# track.type : always same value 'track'
# track.is_local : always same value 'local'
# track.track_number : position on its original album (not relevant for our analysis)
df.drop(columns = ['track.type', 'track.is_local', 'track.track_number'], inplace=True)

# extract artist names from 'track.artists' column
df['artist'] = df['track.artists'].apply(get_artist)

# drop the original 'track.artists' column
df.drop(columns = ['track.artists'], inplace=True)

df.rename(columns={'track.duration_ms':'duration_ms', 'track.explicit':'explicit', 'track.id':'track_id', 'track.name':'track_name', 'track.popularity':'popularity',
                'accousticness':'acousticness'}, inplace=True)
df.to_csv('played_out_cleaned.csv')
df.head()

# %%
print(df['position'].value_counts().sort_index() )

# positions where it does not have count as 89
for pos in range(df['position'].nunique()):
    if df['position'].value_counts().sort_index().iloc[pos] != 89:
        print("count not as 89 :-",'position :', pos,',','count :', df['position'].value_counts().sort_index().iloc[pos])


# %%
# should we remove these two rows ??
# or remove the first two rows (songs) of the corresponding users


