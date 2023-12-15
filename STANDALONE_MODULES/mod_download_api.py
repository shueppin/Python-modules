import requests


CURSEFORGE_BASE_URL = 'https://www.curseforge.com'
CURSEFORGE_API_BASE_URL = 'https://api.cfwidget.com'  # This is not the official API but instead an alternative which doesn't need an API key
CURSEFORGE_FILE_DOWNLOAD_BASE_URL = 'https://edge.forgecdn.net/files'

MODRINTH_BASE_URL = 'https://modrinth.com/mod'
MODRINTH_API_BASE_URL = 'https://api.modrinth.com/v2/project'


PROJECT_OWN_HEADERS = {
    'User-Agent': 'Mod-download-api'
}


class InvalidModBaseUrl(Exception):
    def __init__(self, url: str):
        message = f'The url "{url}" is not supported by this project. \nExamples for supported urls are: https://modrinth.com/mod/fabric-api or https://www.curseforge.com/minecraft/mc-mods/fabric-api'

        super().__init__(message)


class ModNotExisting(Exception):
    def __init__(self, upload_platform: str, mod_url: str):
        message = f'{upload_platform.capitalize()} does not have the mod from {mod_url}. Try using the project ID.'

        super().__init__(message)


class TryAgainLater(Exception):
    def __init__(self):
        message = 'The data on the API does not exist yet. Try again in a moment.'

        super().__init__(message)


class EmptyArguments(Exception):
    def __init__(self, variable_name: str, upload_platform: str):
        message = f'{upload_platform.capitalize()} needs a value for the variable "{variable_name}" but the passed value was empty.'

        super().__init__(message)


class APICooldown(Exception):
    def __init__(self, upload_platform):
        message = f'Requests to the {upload_platform} API is on cooldown. Try again in a moment.'

        super().__init__(message)


class NoFileAvailable(Exception):
    def __init__(self, mod_url: str, loader: str, version: str):
        message = f'On the url "{mod_url}" there is no version available for the loader "{loader}" and the version "{version}".'

        super().__init__(message)


def get_download_url(mod_url: str, game_version: str, mod_loader: str):
    if CURSEFORGE_BASE_URL in mod_url:
        return curseforge_download_url(mod_url, game_version, mod_loader)

    elif MODRINTH_BASE_URL in mod_url:
        return modrinth_download_url(mod_url, game_version, mod_loader)

    else:
        raise InvalidModBaseUrl(mod_url)


def curseforge_download_url(curseforge_url: str, game_version: str, mod_loader: str):
    url_for_version_data = CURSEFORGE_API_BASE_URL + curseforge_url[len(CURSEFORGE_BASE_URL):] + '?version=' + game_version + '&loader=' + mod_loader  # Remove the base curseforge url and add the api part and a version and a loader search

    website = requests.get(url_for_version_data)

    if website.status_code != 200:
        if website.status_code == 202:
            raise TryAgainLater

        else:
            raise ModNotExisting('curseforge', curseforge_url)

    version_data = website.json()

    try:
        file_data = version_data['download']
        project_id = str(file_data['id'])
        file_name = file_data['name']

        download_url = CURSEFORGE_FILE_DOWNLOAD_BASE_URL + '/' + project_id[:4] + '/' + project_id[4:] + '/' + file_name
        download_url = download_url.replace(' ', '%20')

        return download_url, file_name

    except KeyError:
        raise NoFileAvailable(curseforge_url, mod_loader, game_version)


def modrinth_download_url(modrinth_url: str, game_version: str, mod_loader: str):
    if not game_version:
        raise EmptyArguments('game_version', 'modrinth')

    if not mod_loader:
        raise EmptyArguments('mod_loader', 'modrinth')

    url_for_all_versions_data = MODRINTH_API_BASE_URL + modrinth_url[len(MODRINTH_BASE_URL):] + '/version'  # Remove the base modrinth url and add the api part

    website = requests.get(url_for_all_versions_data, headers=PROJECT_OWN_HEADERS)

    if int(website.headers['X-Ratelimit-Remaining']) < 1:
        raise APICooldown('modrinth')

    if website.status_code != 200:
        raise ModNotExisting('modrinth', modrinth_url)

    all_versions_data = website.json()

    for version_data in all_versions_data:
        if game_version in version_data['game_versions'] and mod_loader in version_data['loaders']:
            download_url = version_data['files'][0]['url']
            file_name = version_data['files'][0]['filename']

            return download_url, file_name

    raise NoFileAvailable(modrinth_url, mod_loader, game_version)


def _example():
    url = input('Enter url (from curseforge or modrinth): ')
    version = input('Enter game version (leave empty for most recent uploaded file on curseforge (snapshots included)): ')
    loader = input('Enter mod loader (fabric / forge / quilt): ')

    print(get_download_url(url, version, loader))


if __name__ == '__main__':
    _example()
