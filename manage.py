#!/usr/bin/env python3

import getpass
import os
import subprocess

from flask.ext import script
import flask

from . import config
from app import models
import app

_app = app.app_factory(config.config[os.getenv("AC_CONFIG") or "development"])
manager = script.Manager(_app)


class _AddAPIUser(script.Command):
    option_list = script.Option("username")

    def __init__(self, app):
        super(script.Command.__init__())
        self.app = app

    def run(self, username):
        while True:
            password = getpass.getpass(prompt="Enter Password: ")
            password2 = getpass.getpass(prompt="Confirm Password: ")
            if password == password2:
                break
            print("Passwords did not match. Please try again.")
        create_db()
        api_profile = models.APIProfile(username=username)
        api_profile.set_password(password)
        with app.app_context():
            flask.g.db.session.add(api_profile)
            flask.g.db.session.commit()
        print("An API Profile was succesfully created for username, %s." %
              username)


@manager.command("createdb")
def create_db():
    with app.app_context():
        flask.g.db.drop_all()
        flask.g.db.create_all()


@manager.command
def test():
    subprocess.call(["nosetests", "-v", "--with-coverage",
                     "--cover-package=api", "--cover-branches",
                     "--cover-erase", "--cover-html",
                     "--cover-html-dir=cover"])


def run():
    _env_file_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.isfile(_env_file_path):
        with open(_env_file_path) as f:
            for line in f:
                if "=" in line:
                    os.putenv(*line.strip().split("=", 1))
    if _app.CONFIG["USE_API"]:
        manager.add_command("addapiuser", _AddAPIUser(_app))
    manager.run()


if __name__ == "__main__":
    run()
