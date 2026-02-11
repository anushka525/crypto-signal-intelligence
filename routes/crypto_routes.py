from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from database import db, Asset

crypto_bp = Blueprint("assets", __name__)


def _asset_to_dict(asset: Asset) -> dict:
    return {
        "id": asset.id,
        "symbol": asset.symbol,
        "name": asset.name,
        "exchange": asset.exchange,
        "created_at": asset.created_at.isoformat(),
    }


@crypto_bp.route("/", methods=["POST"])
def create_asset():
    payload = request.get_json(silent=True) or {}
    symbol = payload.get("symbol")
    name = payload.get("name")
    exchange = payload.get("exchange", "binance")

    if not symbol or not name:
        return jsonify({"error": "symbol and name are required"}), 400

    asset = Asset(symbol=symbol.upper(), name=name, exchange=exchange)
    db.session.add(asset)
    try:
        db.session.commit()   # executes the SQL command INSERT INTO assets
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "symbol already exists"}), 409

    return jsonify(_asset_to_dict(asset)), 201


@crypto_bp.route("/", methods=["GET"])
def list_assets():
    assets = Asset.query.all()
    return jsonify([_asset_to_dict(asset) for asset in assets])


@crypto_bp.route("/<int:asset_id>", methods=["GET"])
def get_asset(asset_id: int):
    asset = Asset.query.get_or_404(asset_id)
    return jsonify(_asset_to_dict(asset))


@crypto_bp.route("/<int:asset_id>", methods=["PUT", "PATCH"])
def update_asset(asset_id: int):
    asset = Asset.query.get_or_404(asset_id)
    payload = request.get_json(silent=True) or {}

    if "symbol" in payload:
        asset.symbol = payload["symbol"].upper()
    if "name" in payload:
        asset.name = payload["name"]
    if "exchange" in payload:
        asset.exchange = payload["exchange"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "symbol already exists"}), 409

    return jsonify(_asset_to_dict(asset))


@crypto_bp.route("/<int:asset_id>", methods=["DELETE"])
def delete_asset(asset_id: int):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({"status": "deleted"})
