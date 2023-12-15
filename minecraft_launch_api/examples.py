import os

from minecraft_launch_api.picomc_api import LauncherAPI
from minecraft_launch_api.fabric import create_version as create_fabric


PICOMC_DIRECTORY = os.getenv('APPDATA') + '\\.picomc'


def example_launch():
    launcher = LauncherAPI()

    print('Accounts:', list(launcher.account_manager.list()))
    account_name = input("Enter the account name: ").strip()

    if not launcher.account_manager.exists(account_name):
        if not account_name:  # If the account name is empty
            print('Please enter an account name')
            return

        is_online_account = input("Should it be an ONLINE Account? Yes / No (Leave blank to exit): ").lower()

        if is_online_account == 'yes':
            launcher.create_account(account_name)

        elif is_online_account == 'no':
            launcher.create_account(account_name, online=False)

        else:
            return

    launcher.select_account(account_name)  # You can set authenticate=False if you don't want to check if the account is valid

    print('Instances:', list(launcher.instance_manager.list()))
    instance_name = input('Enter instance name (leave blank for default): ')
    if not instance_name:
        instance_name = 'default'

    if not launcher.instance_manager.exists(instance_name):
        version = input("Enter the Minecraft version (leave blank for latest): ")
        if not version:
            version = 'latest'

        launcher.instance_manager.create(instance_name, version)

    launcher.select_instance(instance_name, game_directory=PICOMC_DIRECTORY + '\\instances\\world\\')

    try:
        launcher.instance.launch(launcher.account, verify_hashes=True)
    except PermissionError:
        print('Had error')

    print('CLEANUP')


def example_fabric_download():
    create_fabric(PICOMC_DIRECTORY + '\\versions')


def example_remove_account():
    launcher = LauncherAPI()

    print('Accounts:', list(launcher.account_manager.list()))
    account_name = input("Enter the account name to delete: ").strip()

    if account_name:
        launcher.account_manager.remove(account_name)
        print(f'Removed account "{account_name}"')

    else:
        print('Removed no account')


if __name__ == '__main__':
    action = input('Launch (l) / Download Fabric (d) / Remove an account (r): ').lower()
    if action == 'l':
        example_launch()
    elif action == 'd':
        example_fabric_download()
    elif action == 'r':
        example_remove_account()
    else:
        print(f'Unrecognised action: {action}')
