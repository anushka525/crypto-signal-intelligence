from flask import Blueprint, jsonify, request
from database import Asset
from services.market_service import fetch_market_snapshot

market_bp = Blueprint("market", __name__)


@market_bp.route("/snapshot", methods=["POST"])
def market_snapshot():
    payload = request.get_json(silent=True) or {}
    asset_id = payload.get("asset_id")
    timeframe = payload.get("timeframe", "5m")

    if not asset_id:
        return jsonify({"error": "asset_id is required"}), 400

    asset = Asset.query.get_or_404(asset_id)
    symbol = asset.symbol

    snapshot = fetch_market_snapshot(symbol, timeframe)
    return jsonify(snapshot.to_dict())
