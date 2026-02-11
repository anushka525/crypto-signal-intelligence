from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import math
import statistics

try:
    import ccxt
except ImportError:  # pragma: no cover - handled at runtime
    ccxt = None


@dataclass
class MarketSnapshot:
    symbol: str
    timeframe: str
    last_price: float
    rsi: float
    macd: float
    signal: float
    volatility: float

    def to_dict(self) -> Dict[str, float | str]:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "last_price": self.last_price,
            "rsi": self.rsi,
            "macd": self.macd,
            "signal": self.signal,
            "volatility": self.volatility,
        }


def _ema(values: List[float], period: int) -> List[float]:
    if not values:
        return []
    k = 2 / (period + 1)
    ema_values = [values[0]]
    for price in values[1:]:
        ema_values.append(price * k + ema_values[-1] * (1 - k))
    return ema_values


def _rsi(values: List[float], period: int = 14) -> float:
    if len(values) < period + 1:
        return 50.0
    gains = []
    losses = []
    for i in range(1, period + 1):
        change = values[-i] - values[-i - 1]
        if change >= 0:
            gains.append(change)
        else:
            losses.append(abs(change))
    average_gain = sum(gains) / period if gains else 0.0
    average_loss = sum(losses) / period if losses else 0.0
    if average_loss == 0:
        return 100.0
    rs = average_gain / average_loss
    return 100 - (100 / (1 + rs))


def _volatility(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    returns = []
    for i in range(1, len(values)):
        if values[i - 1] == 0:
            continue
        returns.append((values[i] - values[i - 1]) / values[i - 1])
    if len(returns) < 2:
        return 0.0
    return float(statistics.pstdev(returns))


def fetch_market_snapshot(symbol: str, timeframe: str = "5m") -> MarketSnapshot:
    if ccxt is None:
        raise RuntimeError("ccxt is not installed")

    symbol = _normalize_symbol(symbol)

    exchange = ccxt.binance({"enableRateLimit": True})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    closes = [candle[4] for candle in ohlcv]
    if not closes:
        raise RuntimeError("No market data returned")

    ema_fast = _ema(closes, 12)
    ema_slow = _ema(closes, 26)
    macd_series = [f - s for f, s in zip(ema_fast[-len(ema_slow):], ema_slow)]
    signal_series = _ema(macd_series, 9) if macd_series else [0.0]

    macd = macd_series[-1] if macd_series else 0.0
    signal = signal_series[-1] if signal_series else 0.0

    snapshot = MarketSnapshot(
        symbol=symbol,
        timeframe=timeframe,
        last_price=closes[-1],
        rsi=_rsi(closes, 14),
        macd=macd,
        signal=signal,
        volatility=_volatility(closes),
    )
    return snapshot


def _normalize_symbol(symbol: str) -> str:
    if "/" in symbol:
        return symbol
    upper = symbol.upper()
    if upper.endswith("USDT") and len(upper) > 4:
        return f"{upper[:-4]}/USDT"
    return upper


def generate_auto_signal(snapshot: MarketSnapshot) -> Dict[str, float | str]:
    side = "hold"
    if snapshot.rsi < 45 and snapshot.macd > snapshot.signal:
        side = "buy"
    elif snapshot.rsi > 55 and snapshot.macd < snapshot.signal:
        side = "sell"

    confidence = min(1.0, max(0.1, abs(snapshot.rsi - 50) / 50 + abs(snapshot.macd) / 10))

    entry_price = snapshot.last_price
    vol = max(snapshot.volatility, 0.005)
    if side == "buy":
        stop_loss = entry_price * (1 - 2 * vol)
        take_profit = entry_price * (1 + 3 * vol)
    elif side == "sell":
        stop_loss = entry_price * (1 + 2 * vol)
        take_profit = entry_price * (1 - 3 * vol)
    else:
        stop_loss = None
        take_profit = None

    return {
        "side": side,
        "timeframe": snapshot.timeframe,
        "confidence": round(confidence, 3),
        "entry_price": round(entry_price, 4),
        "stop_loss": round(stop_loss, 4) if stop_loss else None,
        "take_profit": round(take_profit, 4) if take_profit else None,
    }
