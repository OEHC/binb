import argparse, requests, pandas
from bs4 import BeautifulSoup
from http.client import responses

"""
    This script generates a .csv file containing a list of all tracks
    on the "Billboard Year-End Hot 100 singles" list for the given year(s).
"""

if __name__ == "__main__":

    # cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("years", type=int, nargs="+", help="One or more year, for which tracks should be fetched.")
    parser.add_argument("-o, --output", dest="output", type=str, help="Output .csv file.")
    args = parser.parse_args()

    output = args.output if args.output != None else f"billboard-hot{'_'.join([str(y) for y in args.years])}.csv"
    base_url = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_"
    tracks = []

    # Load tracks for each year into a list
    for year in args.years:

        # Fetch wikipedia page
        url = f"{base_url}{year}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Could not load list for year {year}: {responses[response.status_code]}")
            continue

        # Parse response
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class" : "wikitable"})
        df = pandas.read_html(str(table))

        # Add track to list
        for _, _, trackName, artistName in df[0].itertuples():
            tracks.append([trackName.strip('"'), artistName])

    # Save list to file
    with open(output, "w", encoding="utf8") as outfile:
        for trackName, artistName in tracks:
            outfile.write(f"{trackName};{artistName}\n")