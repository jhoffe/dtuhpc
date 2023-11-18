import base64
import json
import os
import sys
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


class CLIContext:
    _hide: bool = False
    _config: Optional[dict] = None
    _auth: Optional[dict] = None
    _github: Optional[Github] = None
    _conn: Optional[HPCConnection] = None
    _config_path: Optional[str] = None
    _cwd: Optional[str] = None

    def __init__(
        self,
        config_path: Optional[str] = None,
        hide: bool = False,
        cwd: Optional[str] = None,
    ):
        self.hide = hide
        self._config_path = config_path
        self._cwd = cwd

    @staticmethod
    def _get_global_config_dir() -> Path:
        return Path(os.path.join(Path.home(), ".config", "dtuhpc"))

    @staticmethod
    def _get_local_config_path() -> Path:
        return Path(os.path.join(Path.cwd(), ".dtuhpc.toml"))

    @staticmethod
    def _get_global_config_path() -> Path:
        return CLIContext._get_global_config_dir() / ".dtuhpc.toml"

    @staticmethod
    def get_global_auth_path() -> Path:
        return CLIContext._get_global_config_dir() / "auth.json"

    @property
    def config_path(self) -> Path:
        if self._config_path is not None:
            return Path(self._config_path)

        local_path = self._get_local_config_path()
        if local_path.exists():
            return local_path

        global_path = self._get_global_config_path()
        if global_path.exists():
            return global_path

        console.error("Could not find any config file.")
        sys.exit(1)

    @property
    def config(self):
        if self._config is None:
            self._load_config()

        return self._config

    def _load_config(self) -> "CLIContext":
        with open(self.config_path, "rb") as config_file:
            config = tomli.load(config_file)

        self._config = config
        self._cwd = self._cwd if self.cwd is not None else config["ssh"]["default_cwd"]

        return self

    @property
    def cwd(self) -> str:
        if self._cwd is None:
            return self.config["ssh"]["default_cwd"]

        return self._cwd

    @cwd.setter
    def cwd(self, cwd: str):
        self._cwd = cwd

    @property
    def auth(self):
        if self._auth is None:
            self._load_auth()

        return self._auth

    def _load_auth(self) -> "CLIContext":
        if not os.path.exists(self.get_global_auth_path()):
            console.error("Could not find auth file. Please call 'dtuhpc auth' first.")
            sys.exit(1)

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

        self._auth = auth

        return self

    @property
    def connection(self) -> HPCConnection:
        if self._conn is None:
            console.primary("Connecting...")
            self._conn = HPCConnection(
                user=self.auth["username"],
                host=self.config["ssh"]["host"],
                key_filename=self.config["ssh"]["key_filename"],
                password=self.auth["password"],
                hide=self.hide,
                cwd=self.cwd,
            )
            console.success("Connected!")

        return self._conn

    @property
    def git_repo(self) -> Repo:
        return Repo(os.getcwd())

    @property
    def github(self) -> Github:
        if self._github is None:
            self._github = Github(self.config["github"]["access_token"])

        return self._github
