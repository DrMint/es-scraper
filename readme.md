# EmulationStation Scapper

## Update local cache

Instead of querying screenscraper for each rom we are trying to match, we download a local cache.
This cache is a list of rom names and screenscraper game ids, one file for each system.

Run
```sh
python3 update-local-cache.py
```

You can rerun that command from time to time to keep the local cache updated (most useful for newer system where new games are added).

### After updating the local cache, one of my system is missing. What do I do?
Right now, not all systems have been mapped out. You can add additional system by:
- going to a system's page on screenscraper
- finding the `SystemId` in the url
    - e.g: for the ps2, the url is https://www.screenscraper.fr/systemeinfos.php?plateforme=58&alpha=0&numpage=0
    - the `SystemId` is right next to "plateforme=", so 58 in this case.
- add a line in `update-local-cache.py` -> `listSystem`
    - the line should look like:
      `{"id": 58, "name": "ps2"},` where the id is the `SystemId` we retrieved on the previous step, and name is the name of the folder in emulationstation rom folder.
- rerun `python3 update-local-cache.py` to download the missing local cache file.


## Run the auto-matching

During the auto-matching step, the program will list of the roms in given system folder. For each, it will try to match the filename with one of the game in the local cache data. The name that match best will be selected and the `GameId` will be saved in the `matches` folder.

To run the matching, run
```sh
python3 matching.py
```

The resulting csv can be opened in your favorite editor (e.g: LibreOffice Calc). The columns are:
- path: the name of the rom file in the system's rom folder
- name: the matched name
- id: the game id. This is what will be used for the next step
- match: auto-match confidence rating (in %). 100 means the auto-match was very confident, a value bellow 50 is likely to be wrong. Even with a high rating, the match can still be wrong because during the auto-match process, if there are multiple matches with high rating, only the highest is selected.

After running the auto-matching, you should open the resulting csv file  to review the matching. When a match seems off, you can open the csv file in `local-cache` (of the same system) and manually search for a game there.

As explained in the section bellow, you can manually change the name, id, and match columns of an existing row. It is not recommended to change the path of a row, or to manually add/remove rows.

### Rerunning the auto-matching

For each rom file:
- If the rom file is already matched, nothing is changed
- If the rom file is no longer present, the match is deleted
- If a new rom file is detected, a new match is added

This means that if you manually change the match for a specific game, your changes will be preserved if you rerun the auto-matching.

### I've added more games in my rom folders. What do I do?

- Update the local cache if you haven't done it in a while
- Rerun the auto-matching script (you will see what has been added/removed for each system in the terminal)
- Manually review the new matches (which will be at the very bottom of the csv file)

## Fetch the medias

Once you are certain of the quality of the matching, you can start fetching medias. Simply run
```sh
python3 fetch-medias.py
```

By default, it downloads:
- Marquee
- Video
- 3D box
- Physical media.

There is a fallback behavior if the video is not available. It will try downloading the first media available in this order:
- Screenshot
- Titlescreen
- Fanart

## Fetch the metadata

```sh
python3 fetch-meta.py
```

By default, it retrieves:
- name
- description
- rating
- release date
- developer
- publisher
- genre
- players
