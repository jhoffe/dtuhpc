import os
from pathlib import Path
from typing import Optional

import tomli
from git import Repo
from github import Github

from dtuhpc.connector import HPCConnection
from dtuhpc.console import console


class CLIConfig:
    config_path: Path
    hide: bool
    config: dict = {}
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
        self.config = self._load_config()
        self.hide = hide
        self.cwd = cwd if cwd is not None else self.config["ssh"]["default_cwd"]

    @staticmethod
    def _get_global_config_path() -> Path:
        return Path(os.path.join(Path.home(), ".config", ".dtuhpc.toml"))

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

        console.print("[bold red]Could not find any config file.[/bold red]")
        os.sys.exit(1)

    def _load_config(self) -> dict:
        with open(self.config_path, "rb") as config_file:
            config = tomli.load(config_file)

        return config

    def connection(self) -> HPCConnection:
        console.print("[bold green]Connecting...[/bold green]")
        return HPCConnection(
            user=self.config["ssh"]["user"],
            host=self.config["ssh"]["host"],
            password=self.config["ssh"]["password"],
            hide=self.hide,
            cwd=self.cwd,
        )

    def git_repo(self) -> Repo:
        return Repo(os.getcwd())

    def github(self) -> Github:
        return Github(self.config["github"]["access_token"])
