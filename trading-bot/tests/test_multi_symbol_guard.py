"""Phase 0 multi-symbol guard.

TradingBot loads and trades symbols[0] only and marks every asset at that one
symbol's close, so a config with more than one symbol used to complete with
silently corrupted economics and no error. The guard in TradingBot.__init__
refuses len(symbols) > 1 loudly instead.

Cache-free by construction: TradingBot() stores its collaborators and never
touches market data at construction (data_manager=None -> candle_builder=None),
so this runs on a cache-less CI. No skipif -- a skipped guard is an unguarded
engine.
"""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.trading_bot import TradingBot  # noqa: E402


def test_two_symbols_raise():
    with pytest.raises(ValueError) as exc_info:
        TradingBot(symbols=["BTCUSDT", "ETHUSDT"])
    message = str(exc_info.value)
    assert "BTCUSDT" in message
    assert "ETHUSDT" in message


def test_single_symbol_constructs():
    bot = TradingBot(symbols=["BTCUSDT"])
    assert bot.symbols == ["BTCUSDT"]
