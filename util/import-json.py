#!/usr/bin/env python3

import json, argparse, os, redis, logging, uuid

"""
    This script reads track data from a .json file filled with
    iTunes API responses, and inserts the tracks into the redis database.
"""

if __name__ == "__main__":

    # cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("json", type=str, help="Input .json file")
    parser.add_argument("room_name", type=str, help="Stores track information for this room")
    parser.add_argument("-p", "--port", dest="port", type=int, help="Port of the redis database (default: 6379")
    parser.add_argument("-h", "--host", dest="host", type=str, help="Host of the redis database (default: localhost")
    args = parser.parse_args()

    # Logging
    logging.basicConfig(format="\033[33m%(levelname)s\033[0m :: %(message)s", level = logging.INFO)

    host = args.host if args.host != None else "localhost"
    port = args.port if args.port != None else 6379

    # Check file types
    if not args.json.endswith(".json"):
        logging.error("Input file must be of type .json")
        exit()

    # Load json
    with open(args.json, "r", encoding="utf8") as json_file:
        data = json.load(json_file)

    # Check basic json structure
    if "tracks" not in data:
        logging.error('Root element "tracks" not found in json file.')
        exit()

    tracks = data["tracks"]

    # Connect to the database
    try:
        rc = redis.Redis(host=host, port=port)
    except Exception as e:
        logging.error(f"Could not connect to the redis db: {e}")
        exit()

    """
        > How are songs stored in the database?
        For each title, the following fields are stored via `hset`:
            * artistName
            * trackName
            * trackViewUrl
            * previewUrl
            * artworkUrl60
            * artworkUrl100
        This dictionary is stored for the key "song:<songId>", with songId being the unique identifier.

        > How is room membership stored for each song?
        Each room consists of a sorted set of (songId, score) pairs.
        It seems like the score of the song is used to fetch new songs in a round, so that they don't repeat.
        # TODO: Check if that is the case
        I am using a score that is incremented by 1 for each song.
    """

    # Iterate over tracks and insert them into the database
    for score, track in enumerate(tracks, start=1):

        # Add the song
        mapping = {
            "artistName" : track["artistName"],
            "trackName" : track["trackName"],
            "trackViewUrl" : track["trackViewUrl"],
            "previewUrl" : track["previewUrl"],
            "artworkUrl60" : track["artworkUrl60"],
            "artworkUrl100" : track["artworkUrl100"]
        }
        # use iTunes trackId to avoid multiple entries for same track
        song_id = str(track["trackId"]) if "trackId" in track else str(uuid.uuid4())
        name = f"song:{song_id}"
        rc.hset(name, mapping=mapping)

        # Add song to room
        rc.zadd(args.room_name, { song_id : score })