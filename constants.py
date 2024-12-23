listSystem = [
    {"id": 18, "name": "wiiu"},
    {"id": 3, "name": "nes"},
    {"id": 31, "name": "tg16"},
    {"id": 82, "name": "ngpc"},
    {"id": 25, "name": "ngp"},
    {"id": 26, "name": "atari2600"},
    {"id": 1, "name": "megadrive"},
    {"id": 9, "name": "gb"},
    {"id": 10, "name": "gbc"},
    {"id": 12, "name": "gba"},
    {"id": 45, "name": "wonderswan"},
    {"id": 46, "name": "wonderswancolor"},
    {"id": 21, "name": "gamegear"},
    {"id": 66, "name": "c64"},
    {"id": 16, "name": "wii"},
    {"id": 58, "name": "ps2"},
    {"id": 13, "name": "gc"},
    {"id": 80, "name": "channelf"},
    {"id": 59, "name": "ps3"},
    {"id": 73, "name": "vic20"},
    {"id": 105, "name": "supergrafx"},
    {"id": 99, "name": "plus4"},
    {"id": 23, "name": "dreamcast"},
    {"id": 2, "name": "mastersystem"},
    {"id": 28, "name": "atarilynx"},
    {"id": 11, "name": "virtualboy"},
    {"id": 41, "name": "atari7800"},
    {"id": 62, "name": "psvita"},
    {"id": 4, "name": "snes"},
    {"id": 40, "name": "atari5200"},
    {"id": 61, "name": "psp"},
    {"id": 225, "name": "switch"},
    {"id": 57, "name": "psx"},
    {"id": 102, "name": "vectrex"},
    {"id": 14, "name": "n64"},
    {"id": 15, "name": "nds"},
    {"id": 17, "name": "n3ds"}
]

medias = [
    {"esMediaType": "3dboxes", "ssMediaType": "box-3D" },
    {"esMediaType": "physicalmedia", "ssMediaType": "support-2D"},
    {"esMediaType": "marquees", "ssMediaType": "wheel"},
    {"esMediaType": "videos", "ssMediaType": "video-normalized"}
]

regionMatching = [
        {"criteria": "(US)", "ssRegion": "us"},
        {"criteria": "(USA)", "ssRegion": "us"},
        {"criteria": "(Europe)", "ssRegion": "eu"},
        {"criteria": "(EU)", "ssRegion": "eu"},
        {"criteria": "(Brazil)", "ssRegion": "br"},
        {"criteria": "(France)", "ssRegion": "fr"},
        {"criteria": "(Australia)", "ssRegion": "au"},
        {"criteria": "(Germany)", "ssRegion": "de"},
        {"criteria": "(Canada)", "ssRegion": "ca"},
        {"criteria": "(Japan, USA)", "ssRegion": "us,jp"},
        {"criteria": "(USA, Europe)", "ssRegion": "us,eu"},
        {"criteria": "(Japan)", "ssRegion": "jp"},
        {"criteria": "(Sweden)", "ssRegion": "se"},
        {"criteria": "(Europe, Australia)", "ssRegion": "eu,au"},
        {"criteria": "(Asia)", "ssRegion": "asi"},
        {"criteria": "(World)", "ssRegion": "wor"}
    ]

regionFallback = {
    "us": ["us", "wor", "ca", "eu"],
    "eu": ["eu", "wor", "us"],
    "br": ["br", "wor", "us"],
    "au": ["au", "wor", "us"],
    "de": ["de", "eu", "wor", "us"],
    "fr": ["fr", "eu", "wor", "us"],
    "se": ["se", "eu", "wor", "us"],
    "us,jp": ["us", "jp", "wor", "ca"],
    "us,eu": ["us", "eu", "ca", "wor"],
    "eu,au": ["eu", "au", "wor", "us"],
    "jp": ["jp", "asi", "wor", "us", "eu"],
    "ca": ["ca", "us", "wor", "eu"],
    "asi": ["asi", "jp", "wor", "us", "eu"],
    "wor": ["wor", "eu", "us"],
    "": ["wor", "us", "eu"]
}

metaProperties = [
    "name",
    "desc",
    "rating",
    "releasedate",
    "developer",
    "publisher",
    "genre",
    "players"
]

gamelistsFolder = "/home/deck/.emulationstation/gamelists"
downloadedMediaFolder = "/run/media/deck/7e3b832e-4cca-42ee-8fbf-636001f1dcd6/Emulation/tools/downloaded_media"
romsFolder = "/run/media/deck/7e3b832e-4cca-42ee-8fbf-636001f1dcd6/Emulation/roms"