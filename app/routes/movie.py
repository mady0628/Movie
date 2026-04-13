from flask import Blueprint, render_template, request, redirect, session
from app.models.db import get_db
from app.services.tmdb_service import get_popular_movies, get_movie_detail, search_movies
from app.utils.decorators import login_required

movie_bp = Blueprint("movie", __name__)


@movie_bp.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    movies, total_pages = get_popular_movies(page)
    logged = "user_id" in session

    return render_template(
        "movie/index.html",
        movies=movies,
        logged=logged,
        page=page,
        total_pages=total_pages,
        showPage = True,
    )


@movie_bp.route("/user_index")
@login_required
def userindex():
    page = request.args.get("page", 1, type=int)
    movies, total_pages = get_popular_movies(page)

    user_id = session["user_id"]
    username = session["username"]

    conn = get_db()
    cursor = conn.cursor()
    favo = cursor.execute(
        "SELECT movie_id FROM favorites WHERE user_id=%s", (user_id,)
    ).fetchall()
    favorites = [int(f["movie_id"]) for f in favo]

    return render_template(
        "movie/user_index.html",
        username=username,
        movies=movies,
        logged=True,
        favorites=favorites,
        page=page,
        showPage = True,
        total_pages=total_pages,
    )


@movie_bp.route("/add_favorite", methods=["POST"])
@login_required
def addfavorite():
    movie_id = int(request.form.get("movie_id"))
    user_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()
    exist = cursor.execute(
        "SELECT 1 FROM favorites WHERE user_id=%s AND movie_id=%s",
        (user_id, movie_id),
    ).fetchone()

    if not exist:
        cursor.execute(
            "INSERT INTO favorites(user_id, movie_id) VALUES(%s, %s)",
            (user_id, movie_id),
        )
    else:
        cursor.execute(
            "DELETE FROM favorites WHERE user_id=%s AND movie_id=%s",
            (user_id, movie_id),
        )
    conn.commit()

    return redirect(request.referrer)


@movie_bp.route("/favorites")
@login_required
def favorite():
    user_id = session["user_id"]
    username = session["username"]

    conn = get_db()
    cursor = conn.cursor()
    favo = cursor.execute(
        "SELECT movie_id FROM favorites WHERE user_id=%s", (user_id,)
    ).fetchall()
    favorites = [int(f["movie_id"]) for f in favo]

    movies = []
    for mid in favorites:
        data = get_movie_detail(mid)
        if data:
            movies.append(data)

    return render_template(
        "movie/favorites.html",
        username=username,
        movies=movies,
        favorites=favorites,
        showPage = False,
        logged=True,
    )


@movie_bp.route("/detail/<int:id>")
def movie_detail(id):
    movie = get_movie_detail(id)
    if not movie:
        return "Không tìm thấy phim", 404

    logged = "user_id" in session
    favorites = []

    conn = get_db()
    cursor = conn.cursor()

    if logged:
        user_id = session["user_id"]
        favo = cursor.execute(
            "SELECT movie_id FROM favorites WHERE user_id=%s", (user_id,)
        ).fetchall()
        favorites = [int(f["movie_id"]) for f in favo]

    comment = cursor.execute(
        "SELECT * FROM comments WHERE movie_id=%s", (id,)
    ).fetchall()

    return render_template(
        "movie/detail.html",
        movie=movie,
        logged=logged,
        favorites=favorites,
        comment=comment,
    )

@movie_bp.route("/search")
def search():
    q = request.args.get("q","").strip()
    page = request.args.get("page",1,type=int)
    logged = "user_id" in session

    movies, total_pages = ([],1) if not q else search_movies(q,page)
    favorites = []
    if logged:
        user_id = session["user_id"]
        conn = get_db()
        cursor = conn.cursor()
        favo = cursor.execute(
            "SELECT movie_id FROM favorites WHERE user_id=%s", (user_id,)
        ).fetchall()
        favorites = [int(f["movie_id"]) for f in favo]
        return render_template(
        "movie/user_index.html",
        movies=movies,
        logged=logged,
        favorites=favorites,
        page=page,
        total_pages=total_pages,
        showPage = False,
        query=q,
    )
 
    return render_template(
        "movie/index.html",
        movies=movies,
        logged=logged,
        favorites=favorites,
        page=page,
        total_pages=total_pages,
        showPage=False,
        query=q,
    )
