"""Test blog routes."""
from flaskapp.db import get_db


def test_index(client):
    """Test index page."""
    response = client.get("/")
    assert b"Our Blog" in response.data

    assert b"POST 1" in response.data
    assert b"Continue reading..." in response.data


def test_post(client):
    """Test post page."""
    response = client.get("/1/post")

    assert b"POST 1" in response.data
    assert (
        b"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        b"tempor incididunt ut labore et dolore magna aliqua. Aliquam faucibus purus "
        b"in massa tempor nec feugiat nisl. Diam quis enim lobortis scelerisque "
        b"fermentum dui. Maecenas sed enim ut sem viverra. Urna condimentum mattis "
        b"pellentesque id nibh tortor id aliquet. Dignissim sodales ut eu sem integer "
        b"vitae justo eget magna. Nisi est sit amet facilisis. Aenean euismod "
        b"elementum nisi quis eleifend. Urna condimentum mattis pellentesque id nibh "
        b"tortor id aliquet lectus. Urna porttitor rhoncus dolor purus non enim "
        b"praesent elementum facilisis. Convallis tellus id interdum velit laoreet id "
        b"donec ultrices. Sed enim ut sem viverra aliquet eget. Mattis enim ut tellus "
        b"elementum sagittis vitae et leo. In metus vulputate eu scelerisque felis "
        b"imperdiet. Amet facilisis magna etiam tempor orci." in response.data
    )


def test_invalid_post(client):
    """Test invalid route for a post."""
    assert client.get("/6/post").status_code == 404


def test_create(client, app):
    """Test creating a post."""
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": "testing"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 6

        post = db.execute("SELECT * FROM post WHERE id=6").fetchone()
        assert post["title"] == "created"
        assert post["body"] == "testing"


def test_invalid_create(client, app):
    """Test invalid create post with no title."""
    assert client.get("/create").status_code == 200
    post = client.post("/create", data={"title": "", "body": "testing"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 5

    assert b"Title is required." in post.data


def test_comment(client, app):
    """Test comment view and creation."""
    response = client.get("/1/post")

    assert b"comment 1..." in response.data
    client.post("/1/post", data={"body": "testing comment"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM comment").fetchone()[0]
        assert count == 5

        post = db.execute("SELECT * FROM comment WHERE id=5").fetchone()
        assert post["body"] == "testing comment"


def test_invalid_comment(client, app):
    """Test invalid comment creation with too short of a body."""
    post = client.post("/1/post", data={"body": "short"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM comment").fetchone()[0]
        assert count == 4

    assert b"Comment is too short" in post.data


def test_search(client):
    """Test searching for a post."""
    response = client.get("/search?query=1")

    assert b"POST 1" in response.data
