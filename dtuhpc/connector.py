from typing import Optional

from fabric import Connection


class HPCConnection:
    _conn: Connection
    cwd: Optional[str]
    hide: bool

    def __init__(
        self,
        user: str,
        host: str,
        password: str = None,
        hide: bool = True,
        cwd: Optional[str] = None,
        **kwargs,
    ):
        connect_kwargs = {"password": password} if password is not None else None
        self.hide = hide
        self.cwd = cwd
        self._conn = Connection(
            user=user, host=host, connect_kwargs=connect_kwargs, **kwargs
        )

    def run(self, command: str):
        if self.cwd is not None:
            with self._conn.cd(self.cwd):
                return self._conn.run(f"bash -l -c '{command}'", hide=self.hide)

        return self._conn.run(f"bash -l -c '{command}'", hide=self.hide)

    def open_shell(self) -> None:
        self._conn.shell()

    def close(self):
        self._conn.close()
