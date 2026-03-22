from flask import Blueprint, render_template,request,redirect,url_for,session
from database import get_db
import requests
import os

MOVIES_API_KEY = os.getenv("MOVIES_API_KEY")

router = Blueprint("router", __name__)


@router.route("/")
def home():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={MOVIES_API_KEY}"
    res = requests.get(url)
    data = res.json()
    movies = data["results"]
    logged = "user_id" in session
    return render_template("index.html", movies=movies,logged=logged)


@router.route("/signin")
def signin():
    return render_template("sign_in.html")


@router.route("/signup")
def signup():
    return render_template("sign_up.html")

@router.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("router.home"))

@router.route("/user_index")
def userindex():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={MOVIES_API_KEY}"
    res = requests.get(url)
    data = res.json()
    movies = data["results"]

    userID = session["user_id"]
    username = session["username"]
    conn = get_db()
    cursor = conn.cursor()
    favo = cursor.execute("SELECT movie_id FROM favorites WHERE user_id=?",(userID,)).fetchall()
    favorites = [int(f["movie_id"]) for f in favo]
    conn.close()

    logged = "user_id" in session

    return render_template("user_index.html", username=username, movies=movies, logged=logged, favorites=favorites,show_home = False)

@router.route("/user", methods = ['POST'])
def user():
    email = request.form.get('email')
    password = request.form.get('password')
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password)).fetchone()
    conn.close()
    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for('router.userindex'))
    else:
        return redirect(url_for('router.signin'))

@router.route("/add_user", methods = ["POST"])
def adduser():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    conn = get_db()
    cursor = conn.cursor()
    ans = cursor.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password)).fetchall()
    if len(ans) >0:
        conn.close()
        return redirect(url_for('router.signup'))
    else:
        cursor.execute("INSERT INTO users(username,email,password)values(?,?,?)",(username,email,password))
        conn.commit()
        conn.close()
        return redirect(url_for('router.signin'))
    
@router.route("/add_favorite", methods = ['POST'])
def addfavorite():
    movieID = int(request.form.get('movie_id'))
    conn = get_db()
    cursor = conn.cursor()
    userID = session["user_id"]
    exist = cursor.execute(
        "SELECT 1 FROM favorites WHERE user_id=? AND movie_id=?",
        (userID, movieID)
    ).fetchone()

    if not exist:
        cursor.execute(
            "INSERT INTO favorites(user_id,movie_id) VALUES (?,?)",
            (userID, movieID)
        )
        conn.commit()
    else:
        cursor.execute(
            "DELETE FROM favorites WHERE user_id=? AND movie_id=?",
            (userID,movieID)
        )
        conn.commit()
    conn.close()
    return redirect(request.referrer)

@router.route('/favorites')
def favorite():
    userID = session["user_id"]
    username = session["username"]
    conn = get_db()
    cursor = conn.cursor()
    favo = cursor.execute("SELECT movie_id FROM favorites WHERE user_id=?",(userID,)).fetchall()
    favorites = [int(f["movie_id"]) for f in favo]
    conn.close()
    logged = "user_id" in session
    movie = []
    for i in favorites:
        url = f"https://api.themoviedb.org/3/movie/{i}?api_key={MOVIES_API_KEY}"
        res = requests.get(url)
        data = res.json()
        movie.append(data)
    
    return render_template("favorites.html", username=username, movies = movie, favorites=favorites, logged=logged, show_home=True)

@router.route('/detail/<int:id>')
def movie_detail(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key={MOVIES_API_KEY}"
    res = requests.get(url)
    movie = res.json()
    logged = "user_id" in session
    favorites = []
    comment = []
    conn = get_db()
    cursor = conn.cursor()
    if logged:
        userID = session["user_id"]
        
        favo = cursor.execute("SELECT movie_id FROM favorites WHERE user_id=?",(userID,)).fetchall()
        favorites = [int(f["movie_id"]) for f in favo]
    comment = cursor.execute("SELECT * from comments WHERE movie_id=?",(id,)).fetchall()
    conn.close()
    return render_template("detail.html",movie=movie,logged=logged,favorites=favorites,comment=comment)

@router.route('/comment', methods = ['POST'])
def comment():
    content = request.form.get('content')
    anonymous = request.form.get('anonymous')
    movieID = request.form.get('movie_id')
    userName = session['username']
    if anonymous:
        anonymous = 1
    else:
        anonymous = 0
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments(movie_id,user_name,anonymous,contents) VALUES(?,?,?,?)",
        (movieID,userName,anonymous,content)
    )
    conn.commit()
    conn.close()
    return redirect(request.referrer)