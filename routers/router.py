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
    return render_template("index.html", movies=movies,show_favorite=False)


@router.route("/signin")
def signin():
    return render_template("sign_in.html")


@router.route("/signup")
def signup():
    return render_template("sign_up.html")

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

    return render_template("user_index.html", username=username, movies=movies, show_favorite=True, favorites=favorites,show_home = False )

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
    print(username, email, password)
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
    
    movie = []

    for i in favorites:
        url = f"https://api.themoviedb.org/3/movie/{i}?api_key={MOVIES_API_KEY}"
        res = requests.get(url)
        data = res.json()
        movie.append(data)
    
    return render_template("favorites.html", username=username, movies = movie, favorites=favorites, show_favorite=True, show_home=True)