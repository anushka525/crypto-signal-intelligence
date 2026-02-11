from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # This creates the main database object that you will use to define models and execute queries.


def init_db(app) -> None:     # a helper function to initialize the database with the Flask app context. This is where you will create tables and link the db object to your app.  
    """Initialize SQLAlchemy and create tables."""
    db_path = app.config.get("DATABASE_PATH", "./instance/crypto_intel.db")
    db_path = os.path.abspath(db_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db.init_app(app)          # Links db object to our specific flask application
    with app.app_context():
        db.create_all()       # This "magic" command reads all the classes below and automatically creates the tables in SQLite if they don't exist yet.


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    exchange = db.Column(db.String(50), default="binance", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    signals = db.relationship("Signal", back_populates="asset", cascade="all, delete")


class Signal(db.Model):
    __tablename__ = "signals"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    side = db.Column(db.String(10), nullable=False)  # buy/sell/hold
    timeframe = db.Column(db.String(20), default="5m", nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    entry_price = db.Column(db.Float)
    stop_loss = db.Column(db.Float)
    take_profit = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    asset = db.relationship("Asset", back_populates="signals")
    insight = db.relationship(
        "AIInsight", back_populates="signal", uselist=False, cascade="all, delete"
    )


class AIInsight(db.Model):
    __tablename__ = "ai_insights"

    id = db.Column(db.Integer, primary_key=True)
    signal_id = db.Column(db.Integer, db.ForeignKey("signals.id"), nullable=False)
    provider = db.Column(db.String(20), default="gemini", nullable=False)
    summary = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    signal = db.relationship("Signal", back_populates="insight")
