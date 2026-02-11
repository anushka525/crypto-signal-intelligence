import os
from flask import Flask, render_template
from dotenv import load_dotenv

from config import get_config
from logging_config import configure_logging
from error_handlers import register_error_handlers
from database import init_db
from routes.crypto_routes import crypto_bp
from routes.signal_routes import signal_bp
from routes.ai_routes import ai_bp
from routes.market_routes import market_bp


def create_app() -> Flask:
    load_dotenv(override=True)
    app = Flask(__name__)
    app.config.update(get_config())   #It jumps to config.py, resolves the absolute path for crypto_intel.db, and stores these settings in the Flask app.config object.

    configure_logging(app)  #This sets up logging for the app, so you can easily track what's happening and debug issues.

    init_db(app)  #It jumps to database.py, uses SQLAlchemy to check if crypto_intel.db exists, and runs db.create_all() to build the tables (Users, Assets, Signals, AIInsights).

    # The cursor registers the Blueprints. This maps URL prefixes (like /api/assets) to their respective route files.
    app.register_blueprint(crypto_bp, url_prefix="/api/assets")
    app.register_blueprint(signal_bp, url_prefix="/api/signals")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(market_bp, url_prefix="/api/market")

    register_error_handlers(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

# './instance/crypto_intel.db'
app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
