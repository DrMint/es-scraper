from os import scandir, path, makedirs
from natsort import os_sorted
import csv
import requests
from constants import listSystem, medias, regionFallback, downloadedMediaFolder
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qsl


systems = scandir("matches")
systems = [path.splitext(system.name)[0] for system in systems]
systems = os_sorted(systems)

skipRom = True

for system in systems:
    systemId = [e["id"] for e in listSystem if e["name"] == system][0]
    
    with open(f"matches/{system}.csv", 'r') as cacheFile:
        matchReader = csv.DictReader(cacheFile)

        for row in matchReader:
            gameName = path.splitext(row["path"])[0]

            gameId = row["ssId"]
            if gameId == "":
                continue

            if gameId == "78686":
                skipRom = False

            if skipRom:
                continue

            def getMissingMedias():
                missingMedias = []
                for media in medias:
                    esMediaType = media["esMediaType"]
                    fileExtension = ".mp4" if esMediaType == "videos" else ".png"
                    mediaPath = f"{downloadedMediaFolder}/{system}/{esMediaType}/{gameName}{fileExtension}"

                    if not path.exists(mediaPath):
                        missingMedias += [media]
                return missingMedias

            missingMedia = getMissingMedias()
            if len(missingMedia) > 0:
                print(f"[{system}] [{gameId}] {gameName} has some missing medias")

                mediaPageUrl = f"https://www.screenscraper.fr/gameinfos.php?gameid={gameId}&action=onglet&zone=gameinfosmedias"
                response = requests.get(mediaPageUrl)

                soup = BeautifulSoup(response.text, 'html.parser')

                allImages = soup.find_all("img")

                for media in missingMedia:
                    esMediaType = media["esMediaType"]
                    ssMediaType = media["ssMediaType"]

                    fileExtension = ".mp4" if esMediaType == "videos" else ".png"
                    mediaPath = f"{downloadedMediaFolder}/{system}/{esMediaType}/{gameName}{fileExtension}"

                    if path.exists(mediaPath):
                        continue

                    def getVideoUrl():
                        allVideos = soup.find_all("source")
                        normalizedVideo = [e for e in allVideos if "src" in e.attrs.keys() and "video-normalized" in e["src"]]
                        
                        if len(normalizedVideo) == 0:
                            return

                        print(f"[{system}] [{gameId}] {gameName}'s {esMediaType} found")
                        videoUrl = normalizedVideo[0]["src"]
                        return f"https://www.screenscraper.fr/{videoUrl}"

                    def getImageUrl():
                        availableImages = [e for e in allImages if "src" in e.attrs.keys() and f"&media={ssMediaType}&" in e["src"]]
                        
                        availableRegions = []
                        for e in availableImages:
                            parseUrl = urlparse(e["src"])
                            parsedQuery = parse_qsl(parseUrl.query)

                            numPart = [e for e in parsedQuery if e[0] == "num"]
                            num = ""
                            if len(numPart) != 0:
                                num = numPart[0][1]

                            versionPart = [e for e in parsedQuery if e[0] == "version"]
                            version = ""
                            if len(versionPart) != 0:
                                version = versionPart[0][1]

                            availableRegions += [{
                                "region": e["id"][len(ssMediaType) + 1:],
                                "hd": "1" if "hd=1" in e["src"] else "0",
                                "num": num,
                                "version": version
                            }]

                        availableRegionsCodes = [e["region"] for e in availableRegions]

                        if len(availableRegions) == 0:
                            return

                        def findBestMatchingRegion():
                            for region in regionFallback[row["ssRegion"]]:
                                if region in availableRegionsCodes:
                                    return region
                            return availableRegionsCodes[0]

                        bestMatchingRegion = findBestMatchingRegion()
                        idealRegion = regionFallback[row["ssRegion"]][0]
                        if bestMatchingRegion == idealRegion:
                            print(f"[{system}] [{gameId}] {gameName}'s {esMediaType} found in the ideal region")
                        else:
                            print(f"[{system}] [{gameId}] {gameName}'s {esMediaType} not found in the {idealRegion} region. Falling back to {bestMatchingRegion}")
                        
                        bestMatchingMedia = [e for e in availableRegions if e["region"] == bestMatchingRegion][0]
                        hd = bestMatchingMedia["hd"]
                        num = bestMatchingMedia["num"]
                        version = bestMatchingMedia["version"]
                        return f"https://www.screenscraper.fr/image.php?gameid={gameId}&media={ssMediaType}&hd={hd}&region={bestMatchingRegion}&num={num}&version={version}&maxwidth=1024&maxheight=1024"

                    
                    if esMediaType == "videos":
                        mediaUrl = getVideoUrl()

                        if mediaUrl == None:
                            print(f"[{system}] [{gameId}] {gameName}'s {esMediaType} is not available on ss. Falling back to screenshot")
                            missingMedia += [{"esMediaType": "screenshots", "ssMediaType": "ss"}]
                            continue

                    else:
                        mediaUrl = getImageUrl()

                        if mediaUrl == None:
                            print(f"[{system}] [{gameId}] {gameName}'s {esMediaType} is not available on ss. Skipping")
                            if esMediaType == "screenshots":
                                missingMedia += [{"esMediaType": "titlescreens", "ssMediaType": "sstitle"}]
                            elif esMediaType == "titlescreens":
                                missingMedia += [{"esMediaType": "fanart", "ssMediaType": "fanart"}]
                            continue

                    try:
                        response = requests.get(mediaUrl, headers={"Referer": "https://www.screenscraper.fr"})

                        if not response.ok:
                            print(f"[{system}] [{gameId}] {gameName}'s {esMediaType} download failed", mediaUrl)
                            continue
                    except:
                        print(f"[{system}] [{gameId}] {gameName}'s {esMediaType} download crashed", mediaUrl)
                        continue
                    
                    if not path.exists(f"{downloadedMediaFolder}/{system}"):
                        makedirs(f"{downloadedMediaFolder}/{system}")

                    if not path.exists(f"{downloadedMediaFolder}/{system}/{esMediaType}"):
                        makedirs(f"{downloadedMediaFolder}/{system}/{esMediaType}")

                    with open(mediaPath, mode="wb") as file:
                        file.write(response.content)