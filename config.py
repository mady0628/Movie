import os
from dotenv import load_dotenv

load_dotenv()


def build_database_url():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    required_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = [name for name in required_vars if not os.getenv(name)]
    if missing_vars:
        raise RuntimeError(
            "Missing database configuration. Set DATABASE_URL or these variables: "
            + ", ".join(missing_vars)
        )

    return (
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')} "
        f"host={os.getenv('DB_HOST', 'localhost')} "
        f"port={os.getenv('DB_PORT', '5432')}"
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MOVIES_API_KEY = os.getenv("MOVIES_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = build_database_url()
