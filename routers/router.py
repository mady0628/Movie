from flask import Blueprint, render_template,request,redirect,url_for
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
    return render_template("index.html", movies=movies)


@router.route("/signin")
def signin():
    return render_template("sign_in.html")


@router.route("/signup")
def signup():
    return render_template("sign_up.html")

@router.route("/user_index/<user>")
def userindex(user):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={MOVIES_API_KEY}"
    res = requests.get(url)
    data = res.json()
    movies = data["results"]
    return render_template("user_index.html", username=user, movies=movies)

@router.route("/user", methods = ['POST'])
def user():
    email = request.form.get('email')
    password = request.form.get('password')
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password)).fetchone()
    if user:
        return redirect(url_for('router.userindex', user=user["username"]))
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