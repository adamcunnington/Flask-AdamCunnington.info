#!/usr/bin/env python3

from werkzeug import security
import flask
import itsdangerous


class APIProfile(flask.g.database.Model):
    __tablename__ = "api_profiles"
    id = flask.g.database.Column(flask.g.database.Integer, primary_key=True)
    username = flask.g.database.Column(flask.g.database.String(64), index=True,
                                       unique=True)
    password = flask.g.database.Column(flask.g.database.String(128))

    def generate_auth_token(self, expires_in=None):
        # Stop referencing literal string, SECRET_KEY
        serialiser = itsdangerous.TimedJSONWebSignatureSerializer(
            flask.current_app["SECRET_KEY"], expires_in=expires_in)
        return serialiser.dumps({"id": self.id}).decode("UTF-8")

    def set_password(self, password):
        self.password = security.generate_password_hash(password)

    @staticmethod
    def verify_auth_token(token):
        # Stop referencing literal string, SECRET_KEY
        serialiser = itsdangerous.TimedJSONWebSignatureSerializer(
            flask.current_app["SECRET_KEY"])
        try:
            data = serialiser.loads(token)
        except itsdangerous.BadSignature, itsdangerous.SignatureExpired:
            return None
        return APIProfile.query.get(data["id"])

    def verify_password(self, password):
        return security.check_password_hash(self.password, password)
