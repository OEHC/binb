# Adding tracks to the database

## Introduction

Besides the `load_sample_track.js` script by [lpinca](https://github.com/lpinca), this fork contains multiple scripts that makes adding tracks to the database so much easier.
These scripts follow a 3-step to loading new tracks:

  1. Create a `.csv` file containing track title and artist name
  2. Read a `.csv` file, fetch required iTunes data from the iTunes API into a `.json` file
  3. Import such a `.json` file into the database

With this structure, it is very easy to add own scripts or even hand-made files at various points in the process. For example, if you find or manually create a `.csv` file containing the required basic information, you can feed this information right into `fetch-csv.py`.
Another example is the output of `fetch-csv.py`: Because running this script might take some time (since the iTunes-API only allows for around 20 requests / minute), you don't want to run it multiple times, and instead store the generated `.json` file.

The following sections show the options provided by the different scripts.

### `load_sample_tracks.js` by lpinca

Loads sample tracks for defined artists in `artist-ids.js` into the database. Usage:
```console
$ npm run import-data
```

## Creating `.csv` files

If you don't want to create your `.csv` files manually, take a look at the following scripts.
`.csv` files generated here can then be used by `fetch-track-csv.py` to fetch information from the iTunes API.

### `billboard-tracks.py`

Fetches _Billboard Year-End Hot 100 singles_ list from Wikipedia (Example: [2000](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2000)) for one or more given year(s), and stores the tracks as a `.csv` file.
Usage:
```console
$ py billboard-tracks.py -h
usage: billboard-tracks.py [-h] [-o, --output OUTPUT] years [years ...]

positional arguments:
  years                One or more year, for which tracks should be fetched.

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output .csv file.
```

### `spotify-playlist-tracks.py`

Fetches tracks from a Spotify playlist and stores them in a `.csv` file.
Since the Spotify API requires authentification, you need to provide a client id and secret, either using the options `--client-id` / `--client-secret` or environment variables `SPOTIPY_CLIENT_ID` / `SPOTIPY_CLIENT_SECRET`. If both are specified, options take precedence.
Usage:
```console
$ py spotify-playlist-tracks.py -h
usage: spotify-playlist-tracks.py [-h] [--client-id CLIENT_ID] [--client-secret CLIENT_SECRET] [-o OUTPUT] id

positional arguments:
  id                    Spotify Playlist ID

optional arguments:
  -h, --help            show this help message and exit
  --client-id CLIENT_ID
                        Spotify client ID. Can also be set via environment variable SPOTIPY_CLIENT_ID        
  --client-secret CLIENT_SECRET
                        Spotify client secret. Can also be set via environment variable SPOTIPY_CLIENT_SECRET
  -o OUTPUT, --output OUTPUT
                        Output .csv file
```

## Creating `.json` files from `.csv` files

### `fetch-csv.py`

Reads a `.csv` containing track names in the first column and artist names in the second column, and fetches required information from the iTunes API for these tracks.
It uses the [iTunes Search API](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/). Because results are ambiguos sometimes, the user will be asked to manually resolve problems after the fetching is done.
The results are stored in a `.json`file, and can be inserted into the database via `import-json.py`.
Important Note: This scripts expect a semicolon (;) as a separator in the `.csv` file.
Usage:
```console
$ py fetch-csv.py
usage: fetch-csv.py [-h] [-o, --output OUTPUT] csv

positional arguments:
  csv                  Source .csv file, containing track information.

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output file name.
```

## Importing `.json` files into the database

## `import-json.py`

Loads the contents of a `.json` file into the `redis` database.
The `json` file must contain the following data:
```json
{
  "tracks" : [
    {
      "artistName" : "...",
      "trackName" : "...",
      "trackViewUrl" : "...",
      "previewUrl" : "...",
      "artworkUrl60" : "...",
      "artworkUrl100" : "..."
    }
  ]
}
```
The order of keys for each track is not important, and each track entry can contain more key-value pairs (which will be ignored).
Requires a running `redis` server. The URL and port are by default `"localhost"` and `6379`, but these values can be overridden using the environment variables `REDIS_URL` and `REDIS_PORT`.
Usage:
```console
$ py import-json.py -h
usage: import-json.py [-h] json room_name

positional arguments:
  json        Input .json file
  room_name   Stores track information for this room

options:
  -h, --help  show this help message and exit
 ```
Note: The script **does not** check if the given room name exist. Make sure to edit `config.json` in the root directory!

## Example

This example shows the process of importing the tracks of a spotify playlist into the database.
First, pick a playlist. I will be using [this playlist](https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U) for this example.

As discussed, we now need to create a `.csv` file using `spotify-playlist-tracks.py`. I have already set up my client id and secret using environment variables, and extracted the playlist id `37i9dQZF1DWXRqgorJj26U` from the URL.

```console
$ py spotify-playlist-tracks.py 37i9dQZF1DWXRqgorJj26U
INFO :: Fetched 175 tracks from playlist 'Rock Classics'.
```

You can double check if the number of tracks and the playlist track matches if you want.
Next, we want to create a `.json` file using our created `.csv` file using `fetch-csv.py`. If you don't choose a specific output file name, it will be called `spotify_playlist<PLAYLIST_ID>.csv`.

```console
$ py fetch-csv.py spotify_playlist37i9dQZF1DWXRqgorJj26U.csv
INFO :: Found 175 tracks in .csv file.
INFO :: Successfully fetched information for 'Paradise City' by Guns N' Roses
WARNING :: No results found for 'Another One Bites The Dust - Remastered 2011' by Queen.
INFO :: Successfully fetched information for 'Highway to Hell' by AC/DC
INFO :: Successfully fetched information for 'Should I Stay or Should I Go - Remastered' by The Clash
INFO :: Successfully fetched information for 'I Love Rock 'N Roll' by Joan Jett & The Blackhearts
WARNING :: No results found for 'Whole Lotta Love - 1990 Remaster' by Led Zeppelin.
INFO :: Successfully fetched information for 'Dreams - 2004 Remaster' by Fleetwood Mac
...
```

As you can see, some of the tracks had to be manually selected, and other tracks were not even found. This happens, because the script can only search for the name/artist combination and pick the most fitting result. In our example, no results were found for 'Another One Bites The Dust - Remastered 2011' by Queen. The reason for this might be the additional " - Remastered 2011" in the search query, which could be fixed manually in the `.csv` file if required.
After a few minutes (remember the rate limit on the iTunes API) the script should be done and you will be asked to manually evaluate uncertain cases.

```console
$ py fetch-csv.py spotify_playlist37i9dQZF1DWXRqgorJj26U.csv
INFO :: Found 175 tracks in .csv file.
...
INFO :: No matching information was found for 'We Will Rock You - Remastered 2011' by Queen. Please select manually:
[0] 'We Will Rock You (2020 Remaster)' by Nickelback
[1] None of the above
Please enter a number between 0 and 1:  1
```

Just select the matching track and the script should terminate, leaving you with `spotify_playlist37i9dQZF1DWXRqgorJj26U.json` (again, you can change this output file with the `-o` option).

As a last step, make sure the redis server is running and import the `.json` file into a room (called `rock` in this example):

```console
$ py import-json.py spotify_playlist37i9dQZF1DWXRqgorJj26U.json rock
```