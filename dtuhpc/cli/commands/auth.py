import base64
import json
import os

import click
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from dtuhpc.cli.cli_context import CLIContext
from dtuhpc.console import console


@click.command()
def auth():
    """Authenticate with the DTU HPC cluster."""
    auth_path = CLIContext.get_global_auth_path()

    if auth_path.exists():
        click.confirm(
            f"Auth file already exists at {auth_path}. Do you want to overwrite it?",
            abort=True,
        )

    username = click.prompt("Username")
    ssh_password = bytes(click.prompt("Password", hide_input=True), "utf-8")

    console.primary(
        "You will now be asked to enter an encryption key, \
        for encrypting your password."
    )
    encryption_key = bytes(click.prompt("Encryption key", hide_input=True), "utf-8")

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(encryption_key))

    f = Fernet(key)

    auth_conf = {
        "username": username,
        "password": f.encrypt(ssh_password).decode("utf-8"),
        "salt": base64.urlsafe_b64encode(salt).decode("utf-8"),
    }
    auth_path.parent.mkdir(parents=True, exist_ok=True)

    with open(auth_path, "w") as auth_file:
        json.dump(auth_conf, auth_file)

    console.success(f"Successfully saved auth file to {auth_path}")
