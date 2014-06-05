#!/usr/bin/env python3

import functools

from . import utilities


def etag(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        return utilities.implement_etag(function(*args, **kwargs))
    return wrapped


def control_cache(*directives):
    def decorator(function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            return utilities.set_cache_control(function(*args, **kwargs))
        return wrapped
    return decorator


def no_cache(function):
    return control_cache("no-cache", "no-store", "max-age=0")(function)
