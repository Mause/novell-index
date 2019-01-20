import os
from functools import wraps
from flask import Flask, render_template
from CloudFlare import CloudFlare
from dotenv import load_dotenv

load_dotenv()

PREFIX = ".novell.mause.me"
app = Flask(__name__)


class Context:
    def __init__(self):
        self._cache = {}

    def cached(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func in self._cache:
                return self._cache[func]
            value = func(*args, **kwargs)
            self._cache[func] = value
            return value

        return wrapper

    def reset():
        self._cache.clear()


context = Context()


@context.cached
def get_cf() -> CloudFlare:
    return CloudFlare("me@mause.me", os.environ.get("CF_KEY"))


@context.cached
def get_zone() -> str:
    return next(
        zone["id"] for zone in get_cf().zones.get() if zone["name"] == "mause.me"
    )


@app.route("/")
def index():
    records = get_cf().zones.dns_records.get(get_zone())
    records = [record["name"] for record in records]
    records = {
        record.replace(PREFIX, ""): record
        for record in records
        if record.endswith(PREFIX)
    }
    return render_template("index.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
