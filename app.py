from flask import Flask
from routers.router import router
from database import init_db
app = Flask(__name__)

app.register_blueprint(router)

init_db()

if __name__ == "__main__":
    app.run(debug=True)