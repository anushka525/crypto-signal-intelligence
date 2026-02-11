from flask import Blueprint, jsonify, request
from database import db, Signal, Asset
from services.market_service import fetch_market_snapshot, generate_auto_signal

signal_bp = Blueprint("signals", __name__)


def _signal_to_dict(signal: Signal) -> dict:
    return {
        "id": signal.id,
        "asset_id": signal.asset_id,
        "side": signal.side,
        "timeframe": signal.timeframe,
        "confidence": signal.confidence,
        "entry_price": signal.entry_price,
        "stop_loss": signal.stop_loss,
        "take_profit": signal.take_profit,
        "created_at": signal.created_at.isoformat(),
    }


@signal_bp.route("/auto", methods=["POST"])
def create_auto_signal():
    payload = request.get_json(silent=True) or {}
    asset_id = payload.get("asset_id")
    timeframe = payload.get("timeframe", "5m")

    if not asset_id:
        return jsonify({"error": "asset_id is required"}), 400

    asset = Asset.query.get_or_404(asset_id)
    snapshot = fetch_market_snapshot(asset.symbol, timeframe)
    auto_fields = generate_auto_signal(snapshot)

    signal = Signal(
        asset_id=asset_id,
        side=auto_fields["side"],
        timeframe=auto_fields["timeframe"],
        confidence=auto_fields["confidence"],
        entry_price=auto_fields["entry_price"],
        stop_loss=auto_fields["stop_loss"],
        take_profit=auto_fields["take_profit"],
    )
    db.session.add(signal)
    db.session.commit()

    return jsonify({"signal": _signal_to_dict(signal), "market": snapshot.to_dict()}), 201


@signal_bp.route("/", methods=["GET"])
def list_signals():
    signals = Signal.query.order_by(Signal.created_at.desc()).all()
    return jsonify([_signal_to_dict(signal) for signal in signals])


@signal_bp.route("/<int:signal_id>", methods=["GET"])
def get_signal(signal_id: int):
    signal = Signal.query.get_or_404(signal_id)
    return jsonify(_signal_to_dict(signal))


@signal_bp.route("/<int:signal_id>", methods=["PUT", "PATCH"])
def update_signal(signal_id: int):
    signal = Signal.query.get_or_404(signal_id)
    payload = request.get_json(silent=True) or {}

    if "side" in payload:
        signal.side = payload["side"]
    if "timeframe" in payload:
        signal.timeframe = payload["timeframe"]
    if "confidence" in payload:
        signal.confidence = payload["confidence"]
    if "entry_price" in payload:
        signal.entry_price = payload["entry_price"]
    if "stop_loss" in payload:
        signal.stop_loss = payload["stop_loss"]
    if "take_profit" in payload:
        signal.take_profit = payload["take_profit"]

    db.session.commit()
    return jsonify(_signal_to_dict(signal))


@signal_bp.route("/<int:signal_id>", methods=["DELETE"])
def delete_signal(signal_id: int):
    signal = Signal.query.get_or_404(signal_id)
    db.session.delete(signal)
    db.session.commit()
    return jsonify({"status": "deleted"})
