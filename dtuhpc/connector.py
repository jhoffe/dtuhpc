from fabric import Connection


class HPCConnection:
    _conn: Connection

    def __init__(self, user: str, host: str, password: str = None, **kwargs):
        connect_kwargs = {"password": password} if password is not None else None

        self._conn = Connection(
            user=user, host=host, connect_kwargs=connect_kwargs, **kwargs
        )

    def run(self, command: str, hide: bool = False):
        return self._conn.run(f"bash -l -c '{command}'", hide=hide)

    def close(self):
        self._conn.close()
