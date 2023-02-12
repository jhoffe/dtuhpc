import base64
import json
import os
from pathlib import Path
from typing import Optional

import click
import tomli
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from git import Repo
from github import Github

from dtuhpc.connector import HPCConnection
from dtuhpc.console import console


class CLIConfig:
    config_path: Path
    hide: bool
    config: Optional[dict] = None
    auth: dict = {}
    cwd: Optional[str]

    def __init__(
        self,
        config_path: Optional[str] = None,
        hide: bool = True,
        cwd: Optional[str] = None,
    ):
        self.config_path = (
            Path(config_path) if config_path is not None else self._get_config_path()
        )
        self.hide = hide
        self.cwd = cwd

    @staticmethod
    def _get_global_config_path() -> Path:
        return Path(os.path.join(Path.home(), ".config", ".dtuhpc.toml"))

    @staticmethod
    def get_global_auth_path() -> Path:
        return Path(os.path.join(Path.home(), ".config", "dtuhpc", "auth.json"))

    @staticmethod
    def _get_local_config_path() -> Path:
        return Path(os.path.join(Path.cwd(), ".dtuhpc.toml"))

    def _get_config_path(self) -> Path:
        local_path = self._get_local_config_path()
        if local_path.exists():
            return local_path

        global_path = self._get_global_config_path()
        if global_path.exists():
            return global_path

        console.error("Could not find any config file.")
        os.sys.exit(1)

    def load_config(self):
        with open(self.config_path, "rb") as config_file:
            config = tomli.load(config_file)

        self.config = config
        self.cwd = self.cwd if self.cwd is not None else config["ssh"]["default_cwd"]

    def _load_auth(self) -> dict:
        if not os.path.exists(self.get_global_auth_path()):
            console.error("Could not find auth file. Please call 'dtuhpc auth' first.")
            os.sys.exit(1)

        with open(self.get_global_auth_path(), "rb") as auth_file:
            auth = json.load(auth_file)

        encryption_key = bytes(click.prompt("Encryption key", hide_input=True), "utf-8")

        salt = base64.urlsafe_b64decode(auth["salt"].encode("utf-8"))
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(encryption_key))

        f = Fernet(key)

        auth["password"] = f.decrypt(bytes(auth["password"], "utf-8")).decode("utf-8")

        return auth

    def connection(self) -> HPCConnection:
        self.auth = self._load_auth()
        console.primary("Connecting...")
        conn = HPCConnection(
            user=self.auth["username"],
            host=self.config["ssh"]["host"],
            password=self.auth["password"],
            hide=self.hide,
            cwd=self.cwd,
        )
        console.success("Connected!")
        return conn

    def git_repo(self) -> Repo:
        return Repo(os.getcwd())

    def github(self) -> Github:
        return Github(self.config["github"]["access_token"])
