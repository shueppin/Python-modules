import os

import requests

from .minecraft import get_newest_version as newest_minecraft_version


FABRIC_VERSIONS_URL = 'https://meta.fabricmc.net/v2/versions/loader'
JSON_FILE_URL = 'https://meta.fabricmc.net/v2/versions/loader/{minecraft_version}/{fabric_version}/profile/json'
JAR_FILE_URL = 'https://maven.fabricmc.net/net/fabricmc/fabric-loader/{fabric_version}/fabric.py-loader-{fabric_version}.jar'


def get_newest_version():  # Get the newest stable fabric.py version
    response = requests.get(FABRIC_VERSIONS_URL)
    for version_json in response.json():
        if version_json['stable']:
            return version_json['version']


def get_json_file(minecraft_version, fabric_version):
    json_file_url = JSON_FILE_URL.format(minecraft_version=minecraft_version, fabric_version=fabric_version)
    json_response = requests.get(json_file_url)
    json_file_content = json_response.content

    return json_file_content


def get_jar_file(fabric_version):
    jar_file_url = JAR_FILE_URL.format(fabric_version=fabric_version)
    jar_response = requests.get(jar_file_url)
    jar_file_content = jar_response.content

    return jar_file_content


def create_version(versions_directory, minecraft_version='', fabric_version=''):
    if not minecraft_version:
        minecraft_version = newest_minecraft_version()

    if not fabric_version:
        fabric_version = get_newest_version()

    version_name = f'/fabric-loader-{fabric_version}-{minecraft_version}'
    directory_path = versions_directory + version_name

    try:
        os.mkdir(directory_path)
    except FileExistsError:
        pass

    jar_file_content = get_jar_file(fabric_version)
    json_file_content = get_json_file(minecraft_version, fabric_version)

    jar_file_path = directory_path + '/' + version_name + '.jar'
    json_file_path = directory_path + '/' + version_name + '.json'

    try:
        with open(jar_file_path, 'wb') as file:
            file.write(jar_file_content)
    except FileExistsError:
        pass

    try:
        with open(json_file_path, 'wb') as file:
            file.write(json_file_content)
    except FileExistsError:
        pass

    print(minecraft_version, fabric_version)
    print(str(jar_file_content[:50]) + '...')
    print(str(json_file_content))

    return version_name

    # TODO: Create the files. It needs the config in the directory in the instances and the json and the jar in the versions
