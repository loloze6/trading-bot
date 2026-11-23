"""A trade's excursions (MAE, MFE) and its exit efficiency are read on the bars AFTER its entry bar, up to its exit bar:
the engine fills at the entry bar's close, so that bar's high and low come before the entry (2026-11-23, topic 47 of
the research workflow: a BTC trade entered at the close 43,410 had an MFE of 8.42 % from that bar's own high)."""
import csv, json
from pathlib import Path

from backtest.run_protocol import _compute_trade_records_for_window


def _window(tmp_path: Path, bars, trades):
    with open(tmp_path / "bars.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        w.writeheader()
        for b in bars:
            w.writerow({**b, "volume": 1.0})
    (tmp_path / "trades.json").write_text(json.dumps(trades), encoding="utf-8")
    return _compute_trade_records_for_window(tmp_path, "BTCUSD", "w1", bars[-1]["timestamp"], None)


BARS = [
    {"timestamp": "2024-01-01 00:00:00", "open": 100, "high": 110, "low": 90, "close": 100},   # the entry bar: before the entry
    {"timestamp": "2024-01-02 00:00:00", "open": 100, "high": 103, "low": 98, "close": 101},   # held: the exit at its close
    {"timestamp": "2024-01-03 00:00:00", "open": 101, "high": 101, "low": 101, "close": 101},
]


def _trade(side, entry_ts, exit_ts, entry, exit_):
    return {"trade_id": f"{side}-{entry_ts}", "side": side, "entry_price": entry, "exit_price": exit_,
            "entry_time": entry_ts, "exit_time": exit_ts, "entry_forecast": 10.0, "exit_forecast": 0.0}


def test_a_long_trade_reads_only_the_bars_after_its_entry(tmp_path):
    (r,) = _window(tmp_path, BARS, [_trade("LONG", "2024-01-01T00:00:00", "2024-01-02T00:00:00", 100.0, 101.0)])
    assert r["mfe"] == 3.0 and r["mae"] == 2.0                    # 103 and 98, not the entry bar's 110 and 90
    assert abs(r["exit_efficiency"] - 1 / 3) < 1e-3               # 1 % kept of the best 3 %
    assert r["holding_bars"] == 1


def test_a_short_trade_too(tmp_path):
    (r,) = _window(tmp_path, BARS, [_trade("SHORT", "2024-01-01T00:00:00", "2024-01-02T00:00:00", 100.0, 101.0)])
    assert r["mfe"] == 2.0 and r["mae"] == 3.0                    # its best: the low 98; its worst: the high 103
    assert r["exit_efficiency"] == -0.5                            # it lost 1 %, against a best of 2 %


def test_a_trade_opened_and_closed_on_one_bar_has_no_excursion(tmp_path):
    (r,) = _window(tmp_path, BARS, [_trade("LONG", "2024-01-02T00:00:00", "2024-01-02T00:00:00", 101.0, 101.0)])
    assert r["mfe"] == 0.0 and r["mae"] == 0.0 and r["exit_efficiency"] is None
