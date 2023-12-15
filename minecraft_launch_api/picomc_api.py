from pathlib import Path
from contextlib import ExitStack
import atexit

from picomc.launcher import Launcher
from picomc.account import AccountManager, OfflineAccount, MicrosoftAccount
from picomc.instance import InstanceManager, Instance, InstanceNotFoundError


class LauncherAPI:
    def __init__(self):
        self.launcher = Launcher(ExitStack())

        self.account_manager = AccountManager(self.launcher)
        self.instance_manager = InstanceManager(self.launcher)
        self.root = self.launcher.root

        self.account = None
        self.instance = None

        """
        if root_path:
            path_object = Path(root_path)
            self.launcher = Launcher.new(root=path_object)
        else:
            self.launcher = Launcher.new()

        with self.launcher as launcher_context_manager:
            self.account_manager = AccountManager(launcher_context_manager)
            self.instance_manager = InstanceManager(launcher_context_manager)

            self.root = launcher_context_manager.root
        """

        atexit.register(self.close)

    def play(self, account_name, instance_name, verify_hashes=True):
        self.select_account(account_name)
        self.select_instance(instance_name)
        self.instance.launch(account_name, verify_hashes=verify_hashes)

    def select_instance(self, instance_name, game_directory=''):
        if game_directory:
            if not self.instance_manager.exists(instance_name):
                raise InstanceNotFoundError(instance_name)
            self.instance = Instance(self.launcher, Path(game_directory), instance_name)

        else:
            self.instance = self.instance_manager.get(instance_name)

    def select_account(self, username, authenticate=True):
        self.account = self.account_manager.get(username)

        if authenticate and type(self.account) == MicrosoftAccount:
            self.account.authenticate()

    def create_account(self, username, online=True):
        if online:
            account = MicrosoftAccount.new(self.account_manager, username)
        else:
            account = OfflineAccount.new(self.account_manager, username)

        self.account_manager.add(account)

    def authenticate_microsoft_account(self):
        self.account.authenticate()

    def close(self):
        print('closed')
        self.launcher.exit_stack.close()
