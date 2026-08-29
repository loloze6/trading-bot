"""
Tests for the window bound on build_daily_funding_series (#41).

The daily funding-cost series is read from the whole on-disk cache; #41 bounds that
read to the backtest window (normalized DAY, inclusive on both edges) so settlements
outside the loaded window -- the sealed holdout included -- never enter the returned
series. These tests pin:
  * the bound is applied and value-exact (T1);
  * boundary days are inclusive and DAY-normalized, not raw-timestamp cut (T2) -- the
    trap that would silently drop a day's later settlements;
  * sealed-side rows are provably excluded (T3);
  * the signature fails closed -- required params, degenerate inputs raise (T4);
  * the production call site derives the window from the loaded frames' extents (T5).

Fast: tmp_path CSV fixtures for T1-T4(a/b); a stubbed engine for T4(c)/T5.
"""

import logging
import sys
import types
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.backtester import BacktestEngine
from data.feed_registry import build_daily_funding_series

SYMBOL = "BTCUSDT"


def _write_funding_csv(data_dir, rows):
    """rows: list of (timestamp_str, funding_rate)."""
    df = pd.DataFrame(rows, columns=["timestamp", "funding_rate"])
    df["mark_price"] = ""
    path = Path(data_dir) / f"{SYMBOL}_funding_8h.csv"
    df.to_csv(path, index=False)
    return path


def test_bound_applied_keeps_only_in_window_days(tmp_path):
    """T1 -- only the in-window day survives, value-exact. Keys-equality (not `in`)
    makes an out-of-window day leaking through a failure, not a pass."""
    _write_funding_csv(
        tmp_path,
        [
            ("2024-01-01 00:00:00", 0.0001),
            ("2024-01-02 00:00:00", 0.0002),
            ("2024-01-02 08:00:00", 0.0004),
            ("2024-01-03 00:00:00", 0.0009),
        ],
    )
    series = build_daily_funding_series(
        [SYMBOL], str(tmp_path), "2024-01-02", "2024-01-02"
    )[SYMBOL]
    assert set(series.keys()) == {pd.Timestamp("2024-01-02")}
    assert series[pd.Timestamp("2024-01-02")] == pytest.approx(0.0002 + 0.0004)


def test_boundary_days_inclusive_day_normalized(tmp_path):
    """T2 -- the raw-timestamp trap. Bounds arrive as intra-day timestamps exactly as
    production produces them (a bar's open); the filter must normalize to DAY so a
    boundary day keeps ALL its settlements, not just those at/before the bound ts."""
    # End edge: a daily bar opens 00:00; that day's 08:00/16:00 settle AFTER the bound.
    end_dir = tmp_path / "end_edge"
    end_dir.mkdir()
    _write_funding_csv(
        end_dir,
        [
            ("2024-01-02 00:00:00", 0.0001),
            ("2024-01-02 08:00:00", 0.0002),
            ("2024-01-02 16:00:00", 0.0003),
        ],
    )
    end_series = build_daily_funding_series(
        [SYMBOL], str(end_dir), "2024-01-02 00:00:00", "2024-01-02 00:00:00"
    )[SYMBOL]
    assert end_series[pd.Timestamp("2024-01-02")] == pytest.approx(
        0.0001 + 0.0002 + 0.0003
    )

    # Start edge: a 1h-style last-bar open at 23:00; that day's earlier settlements
    # precede the bound and a raw `>=` cut would drop them.
    start_dir = tmp_path / "start_edge"
    start_dir.mkdir()
    _write_funding_csv(
        start_dir,
        [
            ("2024-01-01 00:00:00", 0.0005),
            ("2024-01-01 08:00:00", 0.0006),
            ("2024-01-01 16:00:00", 0.0007),
            ("2024-01-02 00:00:00", 0.0002),
        ],
    )
    start_series = build_daily_funding_series(
        [SYMBOL], str(start_dir), "2024-01-01 23:00:00", "2024-01-02 00:00:00"
    )[SYMBOL]
    assert start_series[pd.Timestamp("2024-01-01")] == pytest.approx(
        0.0005 + 0.0006 + 0.0007
    )


def test_sealed_side_rows_not_loaded(tmp_path):
    """T3 -- a settlement dated into the sealed window is provably excluded when the
    window ends before it. (Test fixtures may reference sealed dates -- see
    test_no_sealed_date_literals.py: "tests" is in EXCLUDED_PARTS.)"""
    _write_funding_csv(
        tmp_path,
        [
            ("2025-12-31 00:00:00", 0.0008),
            ("2026-01-02 00:00:00", 0.0011),
        ],
    )
    series = build_daily_funding_series(
        [SYMBOL], str(tmp_path), "2025-12-01", "2025-12-31"
    )[SYMBOL]
    assert set(series.keys()) == {pd.Timestamp("2025-12-31")}
    assert series[pd.Timestamp("2025-12-31")] == pytest.approx(0.0008)


def test_signature_fails_closed(tmp_path):
    """T4(a/b) -- required params (old 2-arg shape is a TypeError) and degenerate
    windows raise rather than silently reading unbounded or empty."""
    _write_funding_csv(tmp_path, [("2024-01-01 00:00:00", 0.0001)])
    with pytest.raises(TypeError):
        build_daily_funding_series([SYMBOL], str(tmp_path))
    with pytest.raises(ValueError):
        build_daily_funding_series([SYMBOL], str(tmp_path), None, None)
    with pytest.raises(ValueError):
        build_daily_funding_series([SYMBOL], str(tmp_path), "2024-01-05", "2024-01-01")


def _engine_with_frames(frames_by_symbol):
    """Minimal model_funding engine whose data_manager exposes the given frames."""
    dm = types.SimpleNamespace(historical_data=frames_by_symbol)
    return BacktestEngine(
        data_manager=dm,
        symbols=[SYMBOL],
        model_funding=True,
        candle_interval_seconds=86400,
        logger=logging.getLogger("test_funding_window_bound"),
    )


def test_call_site_degenerate_frames_raise_per_shape():
    """T4(c) -- the call site fails closed per frame shape: an empty frame WITH a
    timestamp column derives NaT bounds -> ValueError; the no-column empty frame the
    failed-fetch path returns -> KeyError. Neither falls through to an unbounded run."""
    engine_nat = _engine_with_frames(
        {SYMBOL: pd.DataFrame({"timestamp": pd.to_datetime([])})}
    )
    with pytest.raises(ValueError):
        engine_nat.simulate_on_loaded_data()

    engine_nocol = _engine_with_frames({SYMBOL: pd.DataFrame()})
    with pytest.raises(KeyError):
        engine_nocol.simulate_on_loaded_data()


def test_call_site_bounds_are_loaded_frame_extents(monkeypatch):
    """T5 -- the window passed to the builder is the loaded frames' (min, max)
    timestamp extents, not the request or a hardcode."""
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2024-02-01 00:00:00",
                    "2024-02-10 00:00:00",
                    "2024-02-05 00:00:00",
                ]
            ),
        }
    )
    engine = _engine_with_frames({SYMBOL: frame})

    captured = {}

    class _Captured(Exception):
        pass

    def _spy(symbols, data_dir, start, end):
        captured["start"] = start
        captured["end"] = end
        raise _Captured

    monkeypatch.setattr("core.backtester.build_daily_funding_series", _spy)
    with pytest.raises(_Captured):
        engine.simulate_on_loaded_data()

    assert captured["start"] == pd.Timestamp("2024-02-01 00:00:00")
    assert captured["end"] == pd.Timestamp("2024-02-10 00:00:00")


def test_call_site_bounds_reduce_across_multiple_frames(monkeypatch):
    """T6 -- the window is a TRUE cross-frame min/max, not a per-frame or
    first-frame-only reduction. Three frames whose extents interleave: the global
    earliest (2024-02-01) lives in the second frame and the global latest
    (2024-02-20) in the third, while the FIRST iterated frame is interior
    (2024-02-08..2024-02-12) and holds neither extreme. So the correct window
    (2024-02-01, 2024-02-20) is reachable only by reducing across all frames, and a
    first-frame-only min OR max gets a different answer for the right reason.

    Guards the single-symbol reduction (backtester.py: min/max over
    historical_data.values()), a no-op today because load_data populates one frame,
    but armed the moment the engine goes multi-symbol -- a documented trap."""
    interior = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2024-02-08 00:00:00", "2024-02-10 00:00:00", "2024-02-12 00:00:00"]
            )
        }
    )
    holds_min = pd.DataFrame(
        {"timestamp": pd.to_datetime(["2024-02-01 00:00:00", "2024-02-03 00:00:00"])}
    )
    holds_max = pd.DataFrame(
        {"timestamp": pd.to_datetime(["2024-02-18 00:00:00", "2024-02-20 00:00:00"])}
    )
    # Insertion order == iteration order: the interior frame is first.
    engine = _engine_with_frames(
        {
            "BTCUSDT": interior,
            "ETHUSDT": holds_min,
            "SOLUSDT": holds_max,
        }
    )

    captured = {}

    class _Captured(Exception):
        pass

    def _spy(symbols, data_dir, start, end):
        captured["start"] = start
        captured["end"] = end
        raise _Captured

    monkeypatch.setattr("core.backtester.build_daily_funding_series", _spy)
    with pytest.raises(_Captured):
        engine.simulate_on_loaded_data()

    assert captured["start"] == pd.Timestamp("2024-02-01 00:00:00")
    assert captured["end"] == pd.Timestamp("2024-02-20 00:00:00")
