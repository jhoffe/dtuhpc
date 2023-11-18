"""Connection module.

This module defines the connection to the DTU HPC server.
"""
from typing import Optional

from fabric import Connection, Result


class HPCConnection:
    """Class for connecting and running commands on DTU HPC server.

    Attributes:
        _conn (Connection): Connection object from the fabric library.
        cwd (Optional[str]): Current working directory.
        hide (bool): Hide the output of the command.
    """

    conn: Connection
    cwd: Optional[str]
    hide: bool

    def __init__(
        self,
        user: str,
        host: str,
        key_filename: str,
        password: Optional[str] = None,
        hide: bool = False,
        cwd: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the connection with the required parameters.

        Args:
            user (str): Username for the DTU HPC server.
            host (str): Hostname for the DTU HPC server.
            password (str, optional): Password for the DTU HPC server. Defaults to None.
            hide (bool, optional): Hide the output of the command. Defaults to False.
            cwd (Optional[str], optional): Current working directory. Defaults to None.
            **kwargs: Additional arguments parsed directly into Paramikos Client.
        """
        connect_kwargs = {"key_filename": key_filename}

        if password is not None:
            connect_kwargs["password"] = password

        self.hide = hide
        self.cwd = cwd
        self.conn = Connection(
            user=user,
            host=host,
            connect_kwargs=connect_kwargs,
            **kwargs,
        )

    def run(self, command: str) -> Result:
        """Run a command on the DTU HPC server.

        Args:
            command (str): Command to run.

        Returns:
            Result: Result object from the fabric library.
        """

        if self.cwd is not None:
            with self.conn.cd(self.cwd):
                return self.conn.run(f"bash -l -c '{command}'", hide=self.hide)

        return self.conn.run(f"bash -l -c '{command}'", hide=self.hide)

    def open_shell(self) -> None:
        """Open a shell on the DTU HPC server."""
        self.conn.shell()

    def close(self):
        """Close the connection to the DTU HPC server."""
        self.conn.close()
