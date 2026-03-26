from flask import Flask
from routers.router import router
from database import init_db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = "lojav"

app.register_blueprint(router)

init_db()

if __name__ == "__main__":
    app.run(debug=True)