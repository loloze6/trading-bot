"""
run_protocol.py exit-reason classifier: `_bar_idx_at` / `_infer_exit_reason`.

The defect these pin (Notion `3b31d1fb05a281b1b0dacd644023ebae`, pointed at
from `engineering/roadmap/E-017/EPIC.md`): run_054's `trade_diagnostics.json`
reported `end_of_window_pct: 0.85` (1 trade of 117) while 16 of its 30
walk-forward windows demonstrably ended with the position still open. Two
independent silent-failure paths were measured in the classifier's inputs:

  1. `_bar_idx_at` compared bars.csv and trades.json timestamp strings RAW.
     Since the CandleBuilder._align local-timezone fix (2529f5b), 1d bars land
     on midnight UTC and pandas writes bars.csv date-only ('2019-12-01'), while
     trades.json keeps the full ISO form ('2019-12-01T00:00:00'). Every lookup
     in such a run returned -1 -- measured on run_059: 699 of 699 trades, all
     MAE/MFE 0.0, all efficiencies and post-exit returns null.

  2. `_infer_exit_reason`'s last-bar test was `exit_idx == len(bars) - 1`.
     Every backtest that ended holding a position wrote a DUPLICATE final row
     in bars.csv (fixed forward in c5b1dc6, but every existing artifact still
     carries it), so first-match `_bar_idx_at` returns len(bars)-2 for a trade
     that did exit on the last bar, the index test misses, and the trade lands
     on the `signal_flip` default. This is what produced run_054's 0.85%: the
     one correctly-classified window was the only held-to-end window whose
     bars.csv had no duplicate row.

The nominal `window_end` check cannot substitute for either: the engine's last
bar routinely falls days short of the protocol's declared boundary (run_054:
last bar 2018-09-28 vs window_end 2018-10-01), so `exit_date >= window_end_date`
is False for every held-to-end trade.

These tests run on committed artifacts and in-memory fixtures only -- no
network, no engine, no caches.
"""

import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402 -- also puts trading-bot/ on sys.path


# ---------------------------------------------------------------------------
# Fixture helpers: the smallest bars.csv / trades.json pair the classifier reads
# ---------------------------------------------------------------------------

_BAR_FIELDS = ["timestamp", "open", "high", "low", "close"]


def _write_run_dir(tmp_path, timestamps, trades, duplicate_final_bar=False):
    """Write a minimal run artifact directory and return its Path."""
    run_dir = tmp_path / "run"
    run_dir.mkdir(exist_ok=True)
    rows = [
        {"timestamp": ts, "open": 100.0 + i, "high": 101.0 + i, "low": 99.0 + i, "close": 100.5 + i}
        for i, ts in enumerate(timestamps)
    ]
    if duplicate_final_bar:
        # Exactly the shape _close_all_positions_at_end used to produce: the
        # same instant recorded twice, pre-close then post-close.
        rows.append(dict(rows[-1]))
    with open(run_dir / "bars.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=_BAR_FIELDS)
        w.writeheader()
        w.writerows(rows)
    (run_dir / "trades.json").write_text(json.dumps(trades), encoding="utf-8")
    return run_dir


def _trade(entry_time, exit_time, exit_forecast=0.0, side="LONG"):
    return {
        "trade_id": f"BTCUSDT-{entry_time}-{exit_time}",
        "symbol": "BTCUSDT",
        "side": side,
        "entry_price": 100.0,
        "exit_price": 110.0,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "duration_minutes": 1440.0,
        "profit_loss_percent": 10.0,
        "net_portfolio_profit_loss_percent": 9.8,
        "profitable_net": True,
        "exit_forecast": exit_forecast,
        "total_commission_percent": 0.2,
    }


_HOURLY = [f"2024-01-0{d} 0{h}:00:00" for d in (1, 2, 3) for h in range(3)]


# ---------------------------------------------------------------------------
# Cause 2 -- duplicated final bar row (the run_054 discrepancy)
# ---------------------------------------------------------------------------


def test_exit_on_final_bar_is_end_of_window_despite_duplicate_final_row(tmp_path):
    """The regression itself: last bar recorded twice, trade exits on it.

    Under the old `exit_idx == len(bars) - 1` test this returned "signal_flip".
    """
    run_dir = _write_run_dir(
        tmp_path,
        _HOURLY,
        [_trade("2024-01-01T00:00:00", "2024-01-03T02:00:00")],
        duplicate_final_bar=True,
    )
    recs = rp._compute_trade_records_for_window(run_dir, "BTCUSDT", "2024-01", "2024-01-04", cost_model=None)
    assert [r["exit_reason"] for r in recs] == ["end_of_window"]


def test_exit_on_final_bar_is_end_of_window_without_duplicate_row(tmp_path):
    """Control: the un-duplicated shape classified correctly before and after."""
    run_dir = _write_run_dir(
        tmp_path,
        _HOURLY,
        [_trade("2024-01-01T00:00:00", "2024-01-03T02:00:00")],
    )
    recs = rp._compute_trade_records_for_window(run_dir, "BTCUSDT", "2024-01", "2024-01-04", cost_model=None)
    assert [r["exit_reason"] for r in recs] == ["end_of_window"]


def test_nominal_window_end_beyond_last_bar_does_not_rescue_the_classification(tmp_path):
    """window_end is the protocol's DECLARED boundary, not the engine's last bar.

    With the last bar three days short of window_end (run_054's real shape), the
    `exit_date >= window_end_date` branch is False, so the last-bar test is the
    only thing standing between a held-to-end trade and the signal_flip default.
    """
    bars = [{"timestamp": ts} for ts in _HOURLY]
    assert rp._infer_exit_reason("LONG", 5.0, bars, exit_idx=len(bars) - 1, window_end="2024-01-06") == "end_of_window"


def test_mid_window_exit_is_still_signal_flip(tmp_path):
    """Negative control: the fix must not relabel ordinary exits."""
    run_dir = _write_run_dir(
        tmp_path,
        _HOURLY,
        [_trade("2024-01-01T00:00:00", "2024-01-02T00:00:00")],
        duplicate_final_bar=True,
    )
    recs = rp._compute_trade_records_for_window(run_dir, "BTCUSDT", "2024-01", "2024-01-04", cost_model=None)
    assert [r["exit_reason"] for r in recs] == ["signal_flip"]


# ---------------------------------------------------------------------------
# Cause 1 -- date-only bars.csv timestamps vs full-ISO trade timestamps
# ---------------------------------------------------------------------------


def test_date_only_bar_timestamps_match_midnight_trade_timestamps():
    bars = [{"timestamp": "2019-12-01"}, {"timestamp": "2019-12-02"}, {"timestamp": "2019-12-03"}]
    assert rp._bar_idx_at(bars, rp._ts_normalize("2019-12-02T00:00:00")) == 1
    assert rp._bar_idx_at(bars, rp._ts_normalize("2019-12-03T00:00:00")) == 2
    # A day that is genuinely absent must still miss.
    assert rp._bar_idx_at(bars, rp._ts_normalize("2019-12-09T00:00:00")) == -1


def test_daily_run_diagnostics_are_not_degenerate(tmp_path):
    """run_059's exact shape: date-only bars, full-ISO trades.

    Before the fix every field derived from bar position collapsed (MAE/MFE
    0.0, efficiencies and post-exit returns None, holding_bars back-computed
    from duration_minutes as if bars were hourly -- 72 for a 3-day trade).
    """
    run_dir = _write_run_dir(
        tmp_path,
        [f"2019-12-0{d}" for d in range(1, 10)],
        [_trade("2019-12-01T00:00:00", "2019-12-04T00:00:00")],
    )
    (rec,) = rp._compute_trade_records_for_window(run_dir, "BTCUSDT", "2019-12", "2019-12-31", cost_model=None)
    assert rec["holding_bars"] == 3  # not 72
    assert rec["mae"] > 0.0 and rec["mfe"] > 0.0
    assert rec["exit_efficiency"] is not None
    assert rec["entry_efficiency"] is not None
    assert rec["post_exit_return_5bars"] is not None


def test_unresolvable_timestamp_warns_instead_of_passing_silently(tmp_path, capsys):
    """A lookup that cannot be resolved is a data-integrity signal, not a
    normal outcome -- it must leave a trace on stderr."""
    run_dir = _write_run_dir(
        tmp_path,
        _HOURLY,
        [_trade("2024-01-01T00:00:00", "2024-06-30T02:00:00")],
    )
    recs = rp._compute_trade_records_for_window(run_dir, "BTCUSDT", "2024-01", "2024-01-04", cost_model=None)
    assert len(recs) == 1
    err = capsys.readouterr().err
    assert "WARNING" in err
    assert "2024-06-30 02:00:00" in err


# ---------------------------------------------------------------------------
# Real-artifact regression: run_054, the run named in the ticket
# ---------------------------------------------------------------------------

_RUN_054 = ROOT / "runs" / "run_054"


def _run_054_windows():
    summary = json.loads((_RUN_054 / "protocol_summary.json").read_text(encoding="utf-8"))
    protocol = json.loads((ROOT / "protocols" / "ts_trend_daily_v1.json").read_text(encoding="utf-8"))
    window_end = {w["label"]: w["test"]["end"] for w in protocol["windows"]}
    out = []
    for r in summary["results"]:
        rd = _RUN_054 / "results" / r["run_id"]
        if not (rd / "bars.csv").exists() or not (rd / "trades.json").exists():
            return None
        out.append((rd, r["symbol"], r["window"], window_end[r["window"]]))
    return out


@pytest.mark.real_repo_readonly
def test_run_054_end_of_window_matches_the_windows_that_actually_ended_held():
    """Reproduces and pins the ticket's number on the committed artifacts.

    Measured: 16 of run_054's 30 windows have a final trade whose exit_time is
    the last bar of that window's bars.csv. Pre-fix the classifier found 1 of
    them (117 trades -> end_of_window_pct 0.85); 15 were swallowed by the
    duplicate-final-row path.
    """
    windows = _run_054_windows()
    if windows is None:
        pytest.skip("run_054 backtest artifacts not present in this checkout")

    reasons, held, held_misclassified = [], 0, 0
    for run_dir, symbol, label, window_end in windows:
        recs = rp._compute_trade_records_for_window(run_dir, symbol, label, window_end, cost_model=None)
        reasons.extend(r["exit_reason"] for r in recs)
        bars = rp._load_bars(run_dir)
        trades = rp._load_trades(run_dir)
        if not trades or not bars:
            continue
        last_exit = rp._ts_key(rp._ts_normalize(trades[-1]["exit_time"]))
        if last_exit == rp._ts_key(bars[-1]["timestamp"]):
            held += 1
            if recs[-1]["exit_reason"] != "end_of_window":
                held_misclassified += 1

    assert len(reasons) == 117, "run_054's trade count moved; re-derive the pin"
    assert held == 16
    assert held_misclassified == 0
    n_eow = reasons.count("end_of_window")
    assert n_eow == 16
    assert round(n_eow / len(reasons) * 100, 2) == 13.68  # was 0.85
