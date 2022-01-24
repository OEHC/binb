# Adding tracks to the database

This directory contains different scripts to add tracks to the `redis` database.
A pre-filled database is required to running the server.

## `load_sample_tracks.js` by lpinca

Loads sample tracks for defined artists in `artist-ids.js` into the database. Usage:
```console
$ npm run import-data
```

## `billboard-tracks.py`

Fetches _Billboard Year-End Hot 100 singles_ list for one or more given year(s), and stores the tracks as a `.csv`file.
This `.csv` file can then be used by `fetch-track-csv.py` to fetch information from the iTunes API.
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

## `fetch-track-csv.py`

Reads a `.csv` containing track names in the first column and artist names in the second column, and fetches required information from the iTunes API for these tracks.
It uses the [iTunes Search API](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/). Because results are ambiguos sometimes, the user will be asked to manually resolve problems after the fetching is done.
The results are stored in a `.json`file, and can be inserted into the database via `load-tracks.py`.
Important Note: This scripts expect a semicolon (;) as a separator in the `.csv` file.
Usage:
```console
$ py fetch-track-csv.py
usage: fetch-track-csv.py [-h] [-o, --output OUTPUT] csv

positional arguments:
  csv                  Source .csv file, containing track information.

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output file name.
```

## `load-tracks.py`

Loads the contents of a `.json` file into the `redis` database.
The `json` file must have the following structure:
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
$ py load-tracks.py -h
usage: load-tracks.py [-h] json room_name

positional arguments:
  json        Input .json file
  room_name   Stores track information for this room

options:
  -h, --help  show this help message and exit
 ```
Note: The script **does not** check if the given room name exist. Make sure to edit `config.json` in the root directory!