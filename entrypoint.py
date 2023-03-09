#!/usr/bin/env python3

import argparse, os, json, sys


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rooms", dest="rooms", type=str, help="Room names, separated by commas")
    parser.add_argument("-p", "--port", dest="port", type=int, help="Port to run on")
    parser.add_argument("--games-with-no-repeats", dest="gameswithnorepeats", type=int, help="Number of games with no repeats")
    parser.add_argument("--songs-in-a-run", type=int, dest="songsinarun", help="Number of songs in a run")
    args = parser.parse_args()

    # Load configuration file
    with open("config.json", "r", encoding="utf8") as config_file:
            config = json.load(config_file)

    # Room configuration
    if args.rooms != None:
        rooms = args.rooms.split(",")
        if any([" " in room for room in rooms]):
            sys.exit("Room names must not contain whitespace.")

        config["rooms"] = rooms

    # Port configuration
    if args.port != None:
        config["port"] = args.port

    # Games with no repeats
    if args.gameswithnorepeats:
        config["gameswithnorepeats"] = args.gameswithnorepeats

    # Songs in a run
    if args.songsinarun:
        config["songsinarun"] = args.songsinarun

    # Print configuration
    print("Running binb with the following configuration:", flush=True)
    print(json.dumps(config, indent=4), flush=True)

    # Save configuration file
    with open("config.json", "w", encoding="utf8") as config_file:
        json.dump(config, config_file, indent=4)

    # Run `npm start`
    os.execvp("npm", ["npm", "start"])
