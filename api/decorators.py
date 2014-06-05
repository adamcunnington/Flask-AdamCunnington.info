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


def paginator(item_function, page=1, max_per_page=10):
    def decorator(function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            return utilities.paginator(function(*args, **kwargs),
                                       item_function, page, max_per_page)
        return wrapped
    return decorator


def rate_limit(limit=None, period=None):
    def decorator(function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            too_many_requests_error = utilities.rate_limit(limit, period)
            if too_many_requests_error is None:
                return function(*args, **kwargs)
            return too_many_requests_error
        return wrapped
    return decorator
