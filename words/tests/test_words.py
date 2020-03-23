import pytest

import json

from ..app import create_app


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


def test_get_word(client):

    resp = client.get("/api/v1/words/")
    assert resp.status_code == 404


def test_post_word(client):

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "input_type": "text",
        "data": "bob avi bob avi avi bob bob"
    }

    response = client.post("/api/v1/words", data=json.dumps(data), headers=headers)

    assert response.content_type == mimetype
    assert response.status_code == 201



