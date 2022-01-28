import argparse, logging, json, requests
from os import path
from http.client import responses
from time import sleep
from difflib import SequenceMatcher

"""
    This script reads a .csv file of tracks, with track names in the first column and
    artist names in the second. It then uses the iTunes API to fetch required information
    such as previewUrl or artworkUrls, and generates a json file that can then be loaded
    into the redis database.
    Important Note: The expected separation character is a semicolon (;).
"""

ITUNES_API_URL = "https://itunes.apple.com/search?"
SEARCH_ITEM_LIMIT = 100 # number of items for each search query

# Returns true if the trackNames a and b match
def match_trackName(a, b):
    a = b.lower()
    b = a.lower()
    return a == b or a in b

# Returns true if the artistNames a and b match
def match_artistName(a, b):
    a = a.lower()
    b = b.lower()
    ratio = SequenceMatcher(None, a, b).ratio()
    return a == b or ratio > 0.7

# Asks the user for a decision. Returns the index of the chosen option,
# and None if no option was chosen.
def user_decision(question, options):
    if len(options) == 0:
        logging.debug("user_decision() called without options.")
        return None

    logging.info(question)
    options.append("None of the above")

    # Print options
    for index, option in enumerate(options):
        print(f"[{index}] {option}")

    # Get user response
    while True:
        x = input(f"Please enter a number between 0 and {len(options) - 1}:  ")
        try:
            x = int(x)
            if not (0 <= x < len(options)):
                raise ValueError()
            break
        except ValueError:
            pass

    return x if x != len(options) - 1 else None

if __name__ == "__main__":

    # cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=str, help="Source .csv file, containing track information.")
    parser.add_argument("-o", "--output", dest="output", type=str, help="Output file name.")
    args = parser.parse_args()

    # Logging
    logging.basicConfig(format="\033[33m%(levelname)s\033[0m :: %(message)s", level = logging.INFO)

    output = args.output if args.output != None else path.splitext(args.csv)[0] + ".json"

    # Check file types
    if not output.endswith(".json"):
        logging.error("Output file must be of type .json")
        exit()

    if not args.csv.endswith(".csv"):
        logging.error("Input file must be of type .csv")
        exit()

    # Load track information
    with open(args.csv, "r", encoding="utf8") as csv_file:
        lines = csv_file.readlines()

    tracks = [ line.strip().split(";") for line in lines if line.strip() != "" ]

    logging.info(f"Found {len(tracks)} tracks in .csv file.")

    # Store data in this dictionary
    data = { "tracks" : [] }

    # If no result was found, ask the user after fetching all tracks
    unclear = []

    # Fetch information for each track
    url = "https://itunes.apple.com/search?"
    for trackName, artistName in tracks:

        # Sleep for 2 seconds to avoid timeout by the API (limited to roughly 20 calls per minute)
        sleep(2)

        # Wikipedia sometimes includes "featuring" in the artists name, which leads to problems
        artistName = artistName.split("featuring")[0].strip()

        # Send search request
        params = {
            "term" : f"{trackName} {artistName}",
            "entity" : "song",
            "limit" : 100
        }
        response = requests.get(ITUNES_API_URL, params = params)
        if response.status_code != 200:
            logging.warning(f"Could not fetch information for '{trackName}' by {artistName}: {responses[response.status_code]}")
            continue
        elif response.json()["resultCount"] == 0:
            logging.warning(f"No results found for '{trackName}' by {artistName}.")
            continue

        results = response.json()["results"]
        
        # Check if any of the results matches the requested song
        found = False
        for result in results:
            if match_trackName(trackName, result["trackName"]) and match_artistName(artistName, result["artistName"]):
                data["tracks"].append(result)
                found = True
                break

        if found:
            logging.info(f"Successfully fetched information for '{trackName}' by {artistName}")
        else:
            logging.info(f"Could not reliably determine information for '{trackName}' by {artistName}. Postponing ...")
            unclear.append((trackName, artistName, results))


    # Resolve unclear tracks manually, if possible
    for trackName, artistName, results in unclear:

        # If the track was not found, ask the user which song matches
        top5_results = results[0:5]
        top5_options = [ f"'{t['trackName']}' by {t['artistName']}" for t in top5_results ]

        question = f"No matching information was found for '{trackName}' by {artistName}. Please select manually:"
        decision = user_decision(question, top5_options)

        if decision == None: # none of the chosen options
            continue
        else:
            data["tracks"].append(top5_results[decision])

    # Store dictionary in json file
    with open(output, "w", encoding="utf8") as json_file:
        json.dump(data, json_file, indent=4)

