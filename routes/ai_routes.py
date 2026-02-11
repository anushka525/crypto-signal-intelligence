from flask import Blueprint, jsonify, request, current_app
from database import db, Signal, Asset, AIInsight
from services.ai_service import generate_insight

ai_bp = Blueprint("ai", __name__)

# This file manages the communication with Gemini.
# The /summary endpoint takes a signal ID and market data, retrieves the relevant signal and asset information from the database, 
# and then calls the generate_insight function to get an AI-generated summary and recommendation. The results are stored in the AIInsight table and returned as a JSON response.


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


def _asset_to_dict(asset: Asset) -> dict:
    return {
        "id": asset.id,
        "symbol": asset.symbol,
        "name": asset.name,
        "exchange": asset.exchange,
        "created_at": asset.created_at.isoformat(),
    }


@ai_bp.route("/summary", methods=["POST"])
def ai_summary():
    payload = request.get_json(silent=True) or {}
    signal_id = payload.get("signal_id")
    market = payload.get("market", {})

    if not signal_id:
        return jsonify({"error": "signal_id is required"}), 400

    signal = Signal.query.get_or_404(signal_id)
    asset = Asset.query.get_or_404(signal.asset_id)

    ai_payload = generate_insight(
        api_key=current_app.config.get("GEMINI_API_KEY", ""),
        model_name=current_app.config.get("GEMINI_MODEL", "gemini-1.5-flash"),
        signal=_signal_to_dict(signal),
        asset=_asset_to_dict(asset),
        market=market,
    )

    insight = AIInsight(
        signal_id=signal.id,
        provider="gemini",
        summary=ai_payload.get("summary", ""),
        recommendation=ai_payload.get("recommendation", ""),
    )
    db.session.add(insight)
    db.session.commit()

    return jsonify(
        {
            "signal_id": signal.id,
            "provider": insight.provider,
            "summary": insight.summary,
            "recommendation": insight.recommendation,
            "confidence": ai_payload.get("confidence", 0.0),
            "risks": ai_payload.get("risks", []),
        }
    )
