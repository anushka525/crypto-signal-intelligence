import os


def get_config() -> dict:
    db_path = os.getenv("DATABASE_PATH", "./instance/crypto_intel.db")
    db_path = os.path.abspath(db_path)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        database_url = f"sqlite:///{db_path}"
    return {
        "ENV": os.getenv("FLASK_ENV", "development"),
        "DEBUG": os.getenv("FLASK_DEBUG", "1") == "1",
        "DATABASE_PATH": db_path,
        "SQLALCHEMY_DATABASE_URI": database_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "AI_PROVIDER": os.getenv("AI_PROVIDER", "gemini"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
        "GEMINI_MODEL": os.getenv("GEMINI_MODEL", "gemini-1.5-flash-002"),
        "BINANCE_BASE_URL": os.getenv("BINANCE_BASE_URL", "https://api.binance.com"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        "LOG_FILE": os.getenv("LOG_FILE", "./logs/app.log"),
    }
