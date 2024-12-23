from bs4 import BeautifulSoup, NavigableString
from os import scandir, path, makedirs
from natsort import os_sorted
import csv
import requests
from constants import regionFallback, metaProperties, gamelistsFolder

systems = scandir("matches")
systems = [path.splitext(system.name)[0] for system in systems]
systems = os_sorted(systems)

def parseWebpage(page, preferredRegion):
    soup = BeautifulSoup(page, 'html.parser')

    def findTableByTitle(title):
        tds = soup.find_all("td")
        gameNameTd = [td for td in tds if td.string == title][0]
        
        try:
            table = gameNameTd.parent.parent.parent.parent.parent.parent
            table = table.contents[3].contents[1].contents[1]
            return table
        
        except:
            return soup.new_tag("table")

    titlesTable = findTableByTitle("Game name (by Region)")
    titles = []
    for child in titlesTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 9:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        src = hasFlag["src"]
        region = src[len("images/flags/"):-len(".png")]
        title = "\n".join(child.contents[5].stripped_strings)

        if title:
            titles += [{"region": region, "value": title}]

    

    if len(titles) == 0:
        internalTitleTable = findTableByTitle("Game Name (internal ScreenScraper)")
        title = "\n".join(internalTitleTable.contents[3].contents[3].stripped_strings)
        titles += [{"region": "ss", "value": title}]
            
        


    descriptionTable = findTableByTitle("Synopsis")
    description = None
    for child in descriptionTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 9:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        src = hasFlag["src"]
        lang = src[len("images/flags/"):-len(".png")]

        if lang == "en":
            description = "\n".join(child.contents[5].stripped_strings)
            break

    playersTable = findTableByTitle("Number of Players")
    playerCount = None
    for child in playersTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 7:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        playerCount = child.contents[3].contents[1].contents[1].contents[5].string.strip()


   


    ratingTable = findTableByTitle("Rating")
    rating = None
    for child in ratingTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 7:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        rating = child.contents[3].contents[1].contents[1].contents[5].string.strip()
        [up, down] = rating.split("/")
        rating = int(up) / int(down)

   

    releaseDatesTable = findTableByTitle("Release date(s)")
    releaseDates = []
    for child in releaseDatesTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 9:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        src = hasFlag["src"]
        region = src[len("images/flags/"):-len(".png")]
        releaseDate = "\n".join(child.contents[5].stripped_strings)

        if len(releaseDate) == 4:
            releaseDate = f"{releaseDate}0101T000000"
            releaseDates += [{"region": region, "value": releaseDate}]


        if len(releaseDate) == 10:
            [day, month, year] = releaseDate.split("/")
            releaseDate = f"{year}{month}{day}T000000"
            releaseDates += [{"region": region, "value": releaseDate}]

        
    


    genreTable = findTableByTitle("Genre(s)")
    genre = None
    for child in genreTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 7:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        genre = child.contents[3].contents[1].contents[1].contents[5].string.strip()
        break
        


   


    publisherTable = findTableByTitle("Publisher")
    publisher = None
    for child in publisherTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 7:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        publisher = child.contents[3].contents[1].contents[1]["title"]

   

    developerTable = findTableByTitle("Developer")
    developer = None
    for child in developerTable.contents:
        if isinstance(child, NavigableString) or len(child.contents) != 7:
            continue

        hasFlag = child.contents[3].find("img")
        if not hasFlag:
            continue

        developer = child.contents[3].contents[1].contents[1]["title"]


    
    def getBestMatchingString(options):
        if len(options) == 0:
            return
        
        for region in regionFallback[preferredRegion]:
            for option in options:
                if option["region"] == region:
                    return option["value"]
        
        return options[0]["value"]
    
    return {
        "name": getBestMatchingString(titles),
        "desc": description,
        "rating": rating,
        "releasedate": getBestMatchingString(releaseDates),
        "developer": developer,
        "publisher": publisher,
        "genre": genre,
        "players": playerCount
    }



for system in systems:
    if not path.exists(f"{gamelistsFolder}/{system}"):
        makedirs(f"{gamelistsFolder}/{system}")

    matchFilePath = "matches/" + system + ".csv"
    matchFileFields = ["path", "ssName", "ssRegion", "ssId", "confidence"]

    # Read the existing rows
    rows = []
    with open(matchFilePath, 'r') as matchFile:
        matchReader = csv.DictReader(matchFile, fieldnames=matchFileFields)
        rows = list(matchReader)[1:]

    if not path.exists(f"{gamelistsFolder}/{system}/gamelist.xml"):
        with open(f"{gamelistsFolder}/{system}/gamelist.xml", "w+") as f:
            f.write("""<?xml version="1.0"?>""")

    with open(f"{gamelistsFolder}/{system}/gamelist.xml", "r") as f:
        gamelist = BeautifulSoup(f.read(), 'xml')
        
        if not gamelist.gameList:
            gamelist.append(gamelist.new_tag("gameList"))


    def getGameInGamelist(gamePath):
        result = [e for e in gamelist.gameList.contents if not isinstance(e, NavigableString) and e.path.string == gamePath]
        return result[0] if len(result) > 0 else gamelist.new_tag("game")

    def getMissingProperties(game):
        return [prop for prop in metaProperties if not game.find(prop)]


    def saveChanges():
        with open(f"{gamelistsFolder}/{system}/gamelist.xml", "w+") as f:
            f.write(str(gamelist))

    
    for row in rows:
        gameName = path.splitext(row["path"])[0]
        gameId = row["ssId"]

        if gameId == "":
            continue
            
        game = getGameInGamelist("./" + row["path"])

        if game.find("name"):
            continue
        
        if not game.find("path"):
            newProperty = gamelist.new_tag("path")
            newProperty.append("./" + row["path"])
            game.append(newProperty)
        
        missingProps = getMissingProperties(game)
        if len(missingProps) > 0:
            print(f"[{system}] [{gameId}] {gameName} has some missing props")

            url = f"https://www.screenscraper.fr/gameinfos.php?gameid={gameId}&langue=en"

            try:
                response = requests.get(url)
                if not response.ok:
                    print(f"[{system}] [{gameId}] {gameName}'s download failed", url)
                    continue
            except:
                print(f"[{system}] [{gameId}] {gameName}'s download crashed", url)
                continue

            props = parseWebpage(response.text, row["ssRegion"])

            for prop in missingProps:
                if props[prop] != None:
                    newProperty = gamelist.new_tag(prop)
                    newProperty.append(str(props[prop]))
                    game.append(newProperty)
                    print(f"[{system}] [{gameId}] {gameName}'s {prop} was found!")
                else:
                    print(f"[{system}] [{gameId}] {gameName}'s {prop} is not available on ss. Skipping")
        
        gamelist.gameList.append(game)
        saveChanges()


        