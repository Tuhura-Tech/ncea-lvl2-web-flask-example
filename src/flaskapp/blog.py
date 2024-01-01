"""Blog routes."""
from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskapp.db import get_db

bp = Blueprint("blog", __name__)


def get_post(id):
    """Get a blog post.

    Args:
        id (int): the id of the post to get.

    Returns:
        the post if found otherwise redirects the user to a 404.
    """
    post = (
        get_db()
        .execute(
            "SELECT id, title, body, created FROM post WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post


def get_comments(id):
    """Gets all comments on a post.

    Args:
        id (int): the id of the post to get.

    Returns:
        A list of all comments if found.
    """
    post = (
        get_db()
        .execute(
            "SELECT id, body, created FROM comment WHERE post_id = ?",
            (id,),
        )
        .fetchall()
    )

    return post


@bp.route("/create", methods=("GET", "POST"))
def create():
    """Create post page."""
    error = None
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        if not title:
            error = "Title is required."

        if error is None:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body) VALUES (?, ?)",
                (title, body),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html", error=error)


@bp.route("/")
def index():
    """Main view page."""
    db = get_db()
    posts = db.execute(
        "SELECT post.id, post.title, SUBSTR(post.body, 1, 400) AS body, post.created, "
        "count(comment.id) AS comment_amount FROM post LEFT JOIN comment ON "
        "comment.post_id=post.id group by post.id ORDER BY post.created DESC",
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/<int:id>/post", methods=("GET", "POST"))
def post(id):
    """Post page with comments and the ability to add comments."""
    error = None
    if request.method == "POST":
        body = request.form["body"]

        if len(body) < 10:
            error = "Comment is too short"

        if error is None:
            db = get_db()
            db.execute(
                "INSERT INTO comment (body, post_id) VALUES (?, ?)",
                (
                    body,
                    id,
                ),
            )
            db.commit()
            return redirect(f"/{id}/post")
    post = get_post(id)
    comments = get_comments(id)
    return render_template(
        "blog/post.html",
        post=post,
        comments=comments,
        error=error,
    )


@bp.route("/search")
def search():
    """Search page."""
    query = request.args.get("query")
    db = get_db()
    results = db.execute(
        (
            "SELECT id, title, SUBSTR(body, 1, 400) AS body, created FROM post "
            "WHERE title LIKE ? OR body LIKE ?"
        ),
        (f"%{query}%", f"%{query}%"),
    ).fetchall()
    return render_template("blog/search.html", posts=results, query=query)
