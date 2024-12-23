import json
import requests
import os
from constants import listSystem


for system in listSystem:
    url = "https://www.screenscraper.fr/medias/" + str(system["id"]) + "/gameslist.csv"
    response = requests.get(url)

    if not response.ok:
        print("Request failed", url)
        exit()

    with open("local-cache/" + system["name"] + ".csv", mode="wb") as file:
        file.write(response.content)
