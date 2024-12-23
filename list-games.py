from bs4 import BeautifulSoup, NavigableString
from os import scandir, path
from natsort import os_sorted
import csv
from constants import gamelistsFolder, downloadedMediaFolder

systems = scandir("matches")
systems = [path.splitext(system.name)[0] for system in systems]
systems = os_sorted(systems)

fieldnames = [
    "system",
    "path",
    "name",
    "ssId",
    "region",
    "desc",
    "rating",
    "releasedate",
    "developer",
    "publisher",
    "genre",
    "players",
    "3dboxes",
    "physicalmedia",
    "marquees",
    "videos",
    "screenshots",
    "titlescreens",
    "fanarts"
]

with open("output.csv", "w+") as csvFile:
    outputWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    outputWriter.writeheader()

    for system in systems:
        matchFilePath = "matches/" + system + ".csv"
        print(system)

        with open(matchFilePath, 'r') as matchFile:
            matchFileFields = ["path", "ssName", "ssRegion", "ssId", "confidence"]
            matchReader = csv.DictReader(matchFile, fieldnames=matchFileFields)
            matches = list(matchReader)[1:]

        with open(f"{gamelistsFolder}/{system}/gamelist.xml", "r") as f:
            gamelist = BeautifulSoup(f.read(), 'xml')

        def getGameInGamelist(gamePath):
            result = [e for e in gamelist.gameList.contents if not isinstance(e, NavigableString) and e.path.string == gamePath]
            return result[0] if len(result) > 0 else gamelist.new_tag("game")

        for match in matches:
            gameName = path.splitext(match["path"])[0]
            gameId = match["ssId"]
            game = getGameInGamelist("./" + match["path"])

            boxExists = path.exists(f"{downloadedMediaFolder}/{system}/3dboxes/{gameName}.png")
            physicalmediaExists = path.exists(f"{downloadedMediaFolder}/{system}/physicalmedia/{gameName}.png")
            marqueesExists = path.exists(f"{downloadedMediaFolder}/{system}/marquees/{gameName}.png")
            videosExists = path.exists(f"{downloadedMediaFolder}/{system}/videos/{gameName}.mp4")
            screenshotsExists = path.exists(f"{downloadedMediaFolder}/{system}/screenshots/{gameName}.png")
            titlescreensExists = path.exists(f"{downloadedMediaFolder}/{system}/titlescreens/{gameName}.png")
            fanartsExists = path.exists(f"{downloadedMediaFolder}/{system}/fanarts/{gameName}.png")

            outputWriter.writerow({
                "system": system,
                "path": match["path"],
                "region": match["ssRegion"],
                "ssId": match["ssId"],
                "name": "Yes" if game.find("name") else "",
                "desc": "Yes" if game.find("desc") else "",
                "rating": "Yes" if game.find("rating") else "",
                "releasedate": "Yes" if game.find("releasedate") else "",
                "developer": "Yes" if game.find("developer") else "",
                "publisher": "Yes" if game.find("publisher") else "",
                "genre": "Yes" if game.find("genre") else "",
                "players": "Yes" if game.find("players") else "",
                "3dboxes": "Yes" if boxExists else "",
                "physicalmedia": "Yes" if physicalmediaExists else "",
                "marquees": "Yes" if marqueesExists else "",
                "videos": "Yes" if videosExists else "",
                "screenshots": "Yes" if screenshotsExists else "",
                "titlescreens": "Yes" if titlescreensExists else "",
                "fanarts": "Yes" if fanartsExists else "",
            })


        