#!/usr/bin/env python3
import spotipy, argparse, os, json, sys, logging
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
from spotipy.exceptions import SpotifyException

"""
    This script generates a .csv file containing the track title and artist name for all from a Spotify playlist. Since the Spotify API requires authentication, you must supply a client id and secret, either by commandline option or environment variables (SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET).
    Take a look at:
    https://developer.spotify.com/documentation/web-api/quick-start/
"""

TRACK_FETCH_LIMIT = 100

if __name__ == "__main__":

    # cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=str, help="Spotify Playlist ID")
    parser.add_argument("--client-id", dest="client_id", type=str, help="Spotify client ID. Can also be set via environment variable SPOTIPY_CLIENT_ID")
    parser.add_argument("--client-secret", dest="client_secret", type=str, help="Spotify client secret. Can also be set via environment variable SPOTIPY_CLIENT_SECRET")
    parser.add_argument("-o", "--output", dest="output", type=str, help="Output .csv file")
    args = parser.parse_args()

    # Logging
    logging.basicConfig(format="\033[33m%(levelname)s\033[0m :: %(message)s", level = logging.INFO)

    # Load supplied options
    if args.client_id != None:
        os.environ["SPOTIPY_CLIENT_ID"] = args.client_id

    if args.client_secret != None:
        os.environ["SPOTIPY_CLIENT_SECRET"] = args.client_secret

    if args.output != None:
        output = args.output
        if not output.endswith(".csv"):
            logging.error("Output file must be of type .csv")
            sys.exit()
    else:
        output = f"spotify_playlist{args.id}.csv"

    # Authorize
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    except SpotifyOauthError as e:
        sys.exit(e)

    # Fetch tracks
    items = []
    playlist_name = "Unknown"

    try:
        playlist_info = sp.playlist(args.id, fields="name")
        playlist_name = playlist_info["name"]
    except SpotifyException as e:
        sys.exit(e)

    try:
        offset = 0
        while True:
            playlist = sp.playlist_tracks(args.id, limit=TRACK_FETCH_LIMIT, offset=offset)
            items += playlist["items"]
            offset += TRACK_FETCH_LIMIT
            if offset > playlist["total"]:
                break

    except SpotifyException as e:
        sys.exit(e)

    # Check for empty tracks where item["track"] == None
    empty = [ index + 1 for index, item in enumerate(items) if item["track"] == None]
    if len(empty) != 0:
        logging.warning(f"No data for track(s) at the following position(s): {empty}")

    # Write required information to file
    tracks = [ (item["track"]["name"], item["track"]["artists"][0]["name"]) for item in items if item["track"] != None ]

    logging.info(f"Fetched {len(tracks)} tracks from playlist '{playlist_name}'.")

    with open(output, "w", encoding="utf8") as outfile:
        for trackName, artistName in tracks:
            outfile.write(f"{trackName};{artistName}\n")
