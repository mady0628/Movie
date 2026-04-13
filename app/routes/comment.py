from flask import Blueprint, request, redirect, url_for, session
from app.models.db import get_db
from app.utils.decorators import login_required

comment_bp = Blueprint("comment", __name__)


@comment_bp.route("/comment", methods=["POST"])
@login_required
def add_comment():
    content = request.form.get("content")
    anonymous = request.form.get("anonymous")
    movie_id = request.form.get("movie_id")
    user_name = session["username"]

    if anonymous:
        anonymous = 1
    else:
        anonymous = 0

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments(movie_id, user_name, anonymous, contents) VALUES(%s, %s, %s, %s)",
        (movie_id, user_name, anonymous, content),
    )
    conn.commit()

    return redirect(url_for("movie.movie_detail", id=movie_id))
