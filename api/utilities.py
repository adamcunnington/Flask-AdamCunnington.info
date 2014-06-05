#!/usr/bin/env python3

import hashlib
import time

import redis
import flask

from . import errors


class RateLimit(object):
    _redis = redis.Redis()
    _expiration_window = 10

    def __init__(self, key_prefix, limit, period):
        self.reset_time = ((int(time.time()) // period) * period) + period
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.period = period
        pipeline = self._redis.pipeline()
        pipeline.incr(self.key)
        pipeline.expireat(self.key, self.reset + self._expiration_window)
        self.current_requests = min(pipeline.execute()[0], limit)

    @property
    def remaining(self):
        return self.limit - self.current

    @property
    def over_limit(self):
        return self.current_requests >= self.limit


def implement_etag(return_value):
    assert (flask.request.method in ["HEAD", "GET"],
            "etag is only supported for GET requests")
    response = flask.make_response(return_value)
    etag = "\"" + hashlib.md5(response.get_data()).hexdigest() + "\""
    response.headers["ETag"] = etag
    if_match = flask.request.headers.get("If-Match")
    if_none_match = flask.request.headers.get("If-None-Match")
    if if_match:
        etag_list = [tag.strip() for tag in if_match.split(",")]
        if etag not in etag_list and "*" not in etag_list:
            response = errors.precondition_failed()
    elif if_none_match:
        etag_list = [tag.strip() for tag in if_none_match.split(",")]
        if etag in etag_list or "*" in etag_list:
            response = errors.not_modified()
    return response


def set_cache_control(return_value, *directives):
    response = flask.make_response(return_value)
    response.headers["Cache-Control"] = ", ".join(directives)
    return response


def paginate(query, item_function, page=1, max_per_page=10):
    page = flask.request.args.get("page", page)
    _max_per_page = flask.request.args.get("max_per_page", max_per_page)
    paginator = query.paginate(page, _max_per_page)
    if not page.isdigit() or page < 1 or page > paginator.pages:
        raise errors.InvalidQueryParameter("page '%s' is invalid" % page)
    elif page > paginator.pages:
        raise errors.LookupError("page '%s' does not exist; page '%s' is the "
                                 "last page" % (page, paginator.pages))
    if _max_per_page > max_per_page:
        raise errors.LookupError("the maximum number of items allowed per "
                                 "page is %s" % max_per_page)
    meta = {"page": page, "max_per_page": _max_per_page,
            "total": paginator.total, "meta": paginator.pages}
    if paginator.has_prev:
        meta["previous"] = flask.url_for(flask.request.endpoint,
                                         page=paginator.prev_num,
                                         max_per_page=_max_per_page)
    else:
        meta["previous"] = None
    if paginator.has_next:
        meta["next"] = flask.url_for(flask.request.endpoint,
                                     page=paginator.next_num,
                                     max_per_page=_max_per_page)
    else:
        meta["next"] = None
    meta["first"] = flask.url_for(flask.request.endpoint, page=1,
                                  max_per_page=_max_per_page)
    meta["last"] = flask.url_for(flask.request.endpoint, page=paginator.pages,
                                 max_per_page=_max_per_page)
    data = dict(item_function(paginator.items))
    data["meta"] = meta
    return flask.jsonify(data)


def rate_limit(limit=None, period=None):
    if limit is None:
        limit = flask.current_app.config["RATE_LIMIT"]
    if period is None:
        period = flask.current_app.config["RATE_LIMIT_PERIOD"]
    key = "rate-limit/%s/%s/" % (flask.request.endpoint,
                                 flask.request.remote_addr)
    rate_limiter = RateLimit(key, limit, period)
    flask.g.headers = {
        "X-RateLimit-Remaining": str(rate_limiter.remaining),
        "X-RateLimit-Limit": str(rate_limiter.limit),
        "X-RateLimit-ResetTime": str(rate_limiter.reset_time)
    }
    if rate_limiter.over_limit:
        return errors.too_many_requests("request rate exceeded")
