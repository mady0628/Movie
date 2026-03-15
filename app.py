from flask import Flask
from routers.router import router
from database import init_db
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

app = Flask(__name__)

app.register_blueprint(router)

init_db()

if __name__ == "__main__":
    app.run(debug=True)