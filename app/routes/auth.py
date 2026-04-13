from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signin")
def signin():
    return render_template("auth/sign_in.html")


@auth_bp.route("/signup")
def signup():
    return render_template("auth/sign_up.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("movie.home"))


@auth_bp.route("/user", methods=["POST"])
def user():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email, ),
    ).fetchone()

    if user and check_password_hash(user["password"],password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("movie.userindex"))
    else:
        flash("Sai tài khoản hoặc mật khẩu. Vui lòng thử lại", "error")
        return redirect(url_for("auth.signin"))


@auth_bp.route("/add_user", methods=["POST"])
def adduser():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    passwordHash = generate_password_hash(password)

    conn = get_db()
    cursor = conn.cursor()
    ans = cursor.execute("SELECT * FROM users WHERE email=%s", (email,)).fetchall()

    if len(ans) > 0:
        flash("Email đã tồn tại vui lòng thử email khác", "error")
        return redirect(url_for("auth.signup"))
    else:
        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)",
            (username, email, passwordHash),
        )
        conn.commit()
        return redirect(url_for("auth.signin"))
