#!/usr/bin/env python3

import os

SECRET_KEY = os.environ.get("AC_SECRET_KEY") or os.urandom(24)
RATE_LIMIT = os.environ.get("AC_RATE_LIMIT")
RATE_LIMIT_PERIOD = os.environ.get("AC_RATE_LIMIT_PERIOD")
