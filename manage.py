#!/usr/bin/env python3

import getpass
import os

from flask.ext import script

from . import config
from api import models
import app

_app = app.app(config.config[os.getenv("AC_CONFIG") or "development"])
_manager = script.Manager(_app)

_env_file_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(_env_file_path):
    with open(_env_file_path) as f:
        for line in f:
            if "=" in line:
                os.putenv(*line.strip().split("=", 1))

# To Do: Implement Test Command (Nose inc. Converage)


@_manager.command
def addapiuser(username):
    while True:
        password = getpass.getpass(prompt="Enter Password: ")
        password2 = getpass.getpass(prompt="Confirm Password: ")
        if password == password2:
            break
        print("Passwords did not match. Please try again.")
    app.db.create_all()
    api_profile = models.APIProfile(username=username)
    api_profile.set_password(password)
    app.db.session.add(api_profile)
    app.db.session.commit()
    print("An API Profile was succesfully created for username, %s." %
          username)


def main():
    _manager.run()


if __name__ == "__main__":
    main()
