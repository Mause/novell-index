import os
import tempfile

import pytest
from main import app
import responses


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    yield client


@responses.activate
def test_simple(client):
    url = "https://api.cloudflare.com/client/v4/zones"

    responses.add(
        "GET",
        url,
        json={"success": True, "result": [{"id": "QQQQ", "name": "mause.me"}]},
    )
    responses.add(
        "GET",
        url + "/QQQQ/dns_records",
        json={"success": True, "result": [{"name": "concourse.novell.mause.me"}]},
    )

    response = client.get("/")

    assert response.status == '200 OK'


def main():
    test_simple(client().__next__())


if __name__ == "__main__":
    main()
