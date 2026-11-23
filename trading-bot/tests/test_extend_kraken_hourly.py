"""Checks of tools/extend_kraken_hourly.py on made-up answers (no network)."""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import extend_kraken_hourly as e  # noqa: E402


def test_row_is_the_cache_format():
    r = e.row(1767222000, "87584.2", "87584.2", "87500.1", "87500.1", "14.09024435", 1299)
    assert ",".join(r) == ("2025-12-31 23:00:00,87584.2,87584.2,87500.1,87500.1,14.09024435,2025-12-31 23:59:59.999,"
                           "1232897.789649435,1299,,,0")


def test_trade_bars_counts_a_trade_repeated_across_pages_once(monkeypatch):
    h = 1790755200  # an hour start
    pages = [
        {"error": [], "result": {"XXMRZUSD": [["10.0", "1.0", h + 1, "b", "l", "", 1], ["12.0", "2.0", h + 5, "s", "l", "", 2]], "last": "2"}},
        {"error": [], "result": {"XXMRZUSD": [["12.0", "2.0", h + 5, "s", "l", "", 2], ["9.0", "0.5", h + 3600 + 1, "b", "m", "", 3]], "last": "3"}},
        {"error": [], "result": {"XXMRZUSD": [["11.0", "1.0", h + 7200, "b", "m", "", 4]], "last": "4"}},
    ]
    calls = iter(pages)
    monkeypatch.setattr(e, "get", lambda url, headers=None: json.dumps(next(calls)).encode())
    monkeypatch.setattr(e.time, "sleep", lambda s: None)
    bars, n = e.trade_bars("XMR", h, h + 7200, lambda s: None)
    assert n == 3
    o, hi, lo, c, v, k = bars[h]
    assert (float(o), float(hi), float(lo), float(c), float(v), k) == (10.0, 12.0, 10.0, 12.0, 3.0, 2)
    assert float(bars[h + 3600][4]) == 0.5 and bars[h + 3600][5] == 1
    assert h + 7200 not in bars          # the end is excluded


def test_same_compares_prices_volume_and_count():
    a = ("537.4", "541.04", "537.32", "541.04", "133.08818629", "116")
    assert e.same(a, ("537.40000000", "541.04000000", "537.32000000", "541.04000000", "133.08818629", 116))
    assert not e.same(a, ("537.40000000", "541.04000000", "537.32000000", "541.04000000", "133.09818629", 117))
    assert not e.same(a, ("537.41", "541.04", "537.32", "541.04", "133.08818629", 116))
