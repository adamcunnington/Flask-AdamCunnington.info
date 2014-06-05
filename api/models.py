#!/usr/bin/env python3

from werkzeug import security
import flask
import itsdangerous


class APIProfile(flask.g.db.Model):
    __tablename__ = "api_profiles"
    id = flask.g.db.Column(flask.g.db.Integer, primary_key=True)
    username = flask.g.db.Column(flask.g.db.String(64), index=True,
                                 nullable=False, unique=True)
    password = flask.g.db.Column(flask.g.db.String(128))

    def generate_auth_token(self, expires_in=None):
        serialiser = itsdangerous.TimedJSONWebSignatureSerializer(
            flask.current_app.secret_key, expires_in=expires_in)
        return serialiser.dumps({"id": self.id}).decode("UTF-8")

    def set_password(self, password):
        self.password = security.generate_password_hash(password)

    @staticmethod
    def verify_auth_token(token):
        serialiser = itsdangerous.TimedJSONWebSignatureSerializer(
            flask.current_app.secret_key)
        try:
            data = serialiser.loads(token)
        except itsdangerous.BadSignature, itsdangerous.SignatureExpired:
            return None
        return APIProfile.query.get(data["id"])

    def verify_password(self, password):
        return security.check_password_hash(self.password, password)
