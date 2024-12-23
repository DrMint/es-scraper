from bs4 import BeautifulSoup
from os import scandir, path
import requests
import csv
from thefuzz import fuzz
from natsort import os_sorted
from constants import regionMatching, romsFolder
import re

# CONFIGURATION

blacklistRomsFolderFile = ["cloud.conf", "readme.txt", "systeminfo.txt", "Disc Games Can Be Put Here For Automatic Detection.txt", "keys.txt", "log.txt", "metadata.txt"]
blacklistSystem = ["3ds", "gamecube", "emulators"]

overwriteSystemRomFolders = {"wiiu": "/roms", "model2": "/roms", "xbox360": "/roms"}

# END CONFIGURATION

def matchSortFn(e):
    return e["confidence"]

romSystems = scandir(romsFolder)
romSystems = [system for system in romSystems if system.is_dir()]
romSystems = [system.name for system in romSystems]
romSystems = [system for system in romSystems if system not in blacklistSystem]
romSystems = os_sorted(romSystems)

gameCount = 0
systemCount = 0

def getRegionFromName(name: str) -> str:
    for region in regionMatching:
        if region["criteria"] in name:
            return region["ssRegion"]
    return ""

for system in romSystems:

    # Generate path to rom folder
    systemRomFolderPath = romsFolder + "/" + system
    if system in overwriteSystemRomFolders:
        systemRomFolderPath += overwriteSystemRomFolders[system]
    
    # Scan list of roms in system's rom folder
    roms = scandir(systemRomFolderPath)
    roms = [file for file in roms if file.is_file(follow_symlinks=False)]
    roms = [file.name for file in roms]
    roms = [file for file in roms if file not in blacklistRomsFolderFile]
    roms = os_sorted(roms)

    # Skip folders with no roms in them
    if len(roms) == 0:
        continue

    systemCount += 1

    ssGameIdList = []
    with open("local-cache/" + system + ".csv") as cacheFile:
        reader = csv.DictReader(cacheFile, delimiter=";")
        ssGameIdList = list(reader)

    matchFilePath = "matches/" + system + ".csv"
    matchFileFields = ["path", "ssName", "ssRegion", "ssId", "confidence"]

    # Read the existing rows
    existingRows = []
    if path.exists(matchFilePath):
        with open(matchFilePath, 'r') as cacheFile:
            matchReader = csv.DictReader(cacheFile, fieldnames=matchFileFields)
            existingRows = list(matchReader)[1:]

    with open(matchFilePath, 'w', newline='') as cacheFile:
        matchWriter = csv.DictWriter(cacheFile, fieldnames=matchFileFields)
        matchWriter.writeheader()

        for row in existingRows:
            rowPath = row["path"]
            # Only keep existing rows where the rom file exists
            if (row["path"] in roms):
                matchWriter.writerow(row)
                gameCount += 1
            else:
                print(f"[{system}] Removing {rowPath} as it no longer exists in the roms folder")

        existingRowsPaths = [row["path"] for row in existingRows]

        # For each new rom file, create a row
        unmatchedRoms = [rom for rom in roms if rom not in existingRowsPaths]
        for rom in unmatchedRoms:
            nameWithoutParenthesis = path.splitext(rom)[0]
            nameWithoutParenthesis = re.sub(r"\(([^\)]+)\)", "", nameWithoutParenthesis)
            matches = [{"path": rom, "ssId": row["Game ID"], "ssName": row["Game Name"], "confidence": fuzz.ratio(nameWithoutParenthesis, row["Game Name"]), "ssRegion": getRegionFromName(rom) } for row in ssGameIdList]
            matches.sort(key=matchSortFn, reverse=True)
            newRow = matches[0] if len(matches) > 0 else {"path": rom, "match": 0} 
            matchWriter.writerow(newRow)
            newRowPath = newRow["path"]
            print(f"[{system}] Adding {nameWithoutParenthesis}")
            gameCount += 1


print(f"Done auto-matching {gameCount} games for {systemCount} systems")