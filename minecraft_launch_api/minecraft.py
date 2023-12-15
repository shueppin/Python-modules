import requests


MINECRAFT_VERSIONS_URL = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'


def get_newest_version():
    response = requests.get(MINECRAFT_VERSIONS_URL)
    return response.json()['latest']['release']
