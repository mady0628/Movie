from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """Decorator kiểm tra user đã đăng nhập chưa."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Vui lòng đăng nhập để tiếp tục", "error")
            return redirect(url_for("auth.signin"))
        return f(*args, **kwargs)
    return decorated_function
