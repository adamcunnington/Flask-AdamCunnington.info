#!/usr/bin/env python3

import hashlib

import flask

from . import errors


def implement_etag(return_value):
    assert (flask.request.method in ["HEAD", "GET"],
            "etag is only supported for GET requests")
    return_value = flask.make_response(return_value)
    etag = "\"" + hashlib.md5(return_value.get_data()).hexdigest() + "\""
    return_value.headers["ETag"] = etag
    if_match = flask.request.headers.get("If-Match")
    if_none_match = flask.request.headers.get("If-None-Match")
    if if_match:
        etag_list = [tag.strip() for tag in if_match.split(",")]
        if etag not in etag_list and "*" not in etag_list:
            return_value = errors.precondition_failed()
    elif if_none_match:
        etag_list = [tag.strip() for tag in if_none_match.split(",")]
        if etag in etag_list or "*" in etag_list:
            return_value = errors.not_modified()
    return return_value


def modify_cache_control(return_value, *directives):
    return_value = flask.make_response(return_value)
    return_value.headers["Cache-Control"] = ", ".join(directives)
    return return_value

# TODO: paginate
# TODO: limit_rate; use flask-limiter?
