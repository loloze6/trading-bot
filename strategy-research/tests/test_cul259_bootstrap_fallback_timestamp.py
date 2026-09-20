"""
CUL-259: run_protocol._pooled_ic_with_bootstrap_fallback now threads a
"timestamp" column through into the records it hands to
_stationary_block_bootstrap_ic_significance, deriving expected_step from the
first window's own first two consecutive bars -- so the degenerate-active-
forecast fallback path (the family the committed production strategy
belongs to, per CUL-259's own description) is no longer gap-unaware even
after CUL-20 made the underlying bootstrap gap-aware.

Depends on PR #137 (CUL-15/CUL-20/CUL-21/CUL-34): builds on top of that
branch, since expected_step_by_symbol does not exist on
_stationary_block_bootstrap_ic_significance until it merges.

Two things this file proves, neither exercised by PR #137's own
test_bootstrap_end_to_end_via_run_protocol_fallback (whose synthetic
bars.csv fixture has no "timestamp" column at all, so it never engages the
new path -- it stays valid unchanged, proving the fix is backward
compatible with a bars.csv that genuinely lacks the column):

1. When bars.csv DOES carry "timestamp", the derived expected_step is
   actually passed through to the bootstrap (spied, not inferred from the
   IC value, which is randomized by the resampling seed and gap placement).
2. A bars.csv missing "timestamp" on ANY pooled window still falls back to
   expected_step_by_symbol=None -- the fail-loud missing-timestamp KeyError
   in _contiguous_segments must never surface here; a data-availability gap
   in an older run is not the "real time gap" C-H5 is guarding against.
"""
import csv
import sys
from pathlib import Path

import pytest

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))

import run_protocol as rp  # noqa: E402


def _write_bars_csv(path, n, with_timestamp, start="2024-01-01", freq_hours=1):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        if with_timestamp:
            w.writerow(["timestamp", "forecast", "close"])
        else:
            w.writerow(["forecast", "close"])
        import pandas as pd
        ts = pd.date_range(start, periods=n, freq=f"{freq_hours}h")
        for i in range(n):
            row = [10.0 if i % 2 else -10.0, 100.0 + i]  # degenerate active forecast
            if with_timestamp:
                row = [ts[i].isoformat()] + row
            w.writerow(row)


def test_expected_step_is_derived_and_passed_through_when_timestamp_present(tmp_path, monkeypatch):
    run_dir = tmp_path / "r1"
    run_dir.mkdir()
    _write_bars_csv(run_dir / "bars.csv", n=30, with_timestamp=True, freq_hours=1)
    rows = [
        {"window": "w1", "run_id": "r1", "symbol": "SYM", "core": {"forecast_return_corr": None}}
    ]

    captured = {}
    from performance import signal_statistics as pss

    real_bootstrap = pss.stationary_block_bootstrap_ic_significance

    def _spy(*args, **kwargs):
        captured["expected_step_by_symbol"] = kwargs.get("expected_step_by_symbol")
        return real_bootstrap(*args, **kwargs)

    monkeypatch.setattr(pss, "stationary_block_bootstrap_ic_significance", _spy)

    rp._pooled_ic_with_bootstrap_fallback(rows, str(tmp_path))

    assert captured["expected_step_by_symbol"] is not None, (
        "a bars.csv with a real timestamp column must derive and pass a real "
        "expected_step -- CUL-259's fix has regressed to the old None-always path"
    )
    step = captured["expected_step_by_symbol"]["SYM"]
    import pandas as pd
    assert step == pd.Timedelta(hours=1), f"expected a 1h step from the fixture's cadence, got {step}"


def test_missing_timestamp_on_any_window_falls_back_to_none_not_a_crash(tmp_path, monkeypatch):
    """Two pooled windows for the same symbol; the second lacks 'timestamp'.
    Must not raise, and must not silently derive a step from only the first
    window while feeding the bootstrap heterogeneous records (some with the
    key, some without) -- CUL-259's fix gates on ALL windows carrying it."""
    run_dir1 = tmp_path / "r1"
    run_dir1.mkdir()
    _write_bars_csv(run_dir1 / "bars.csv", n=20, with_timestamp=True)

    run_dir2 = tmp_path / "r2"
    run_dir2.mkdir()
    _write_bars_csv(run_dir2 / "bars.csv", n=20, with_timestamp=False)

    rows = [
        {"window": "w1", "run_id": "r1", "symbol": "SYM", "core": {"forecast_return_corr": None}},
        {"window": "w2", "run_id": "r2", "symbol": "SYM", "core": {"forecast_return_corr": None}},
    ]

    from performance import signal_statistics as pss
    captured = {}
    real_bootstrap = pss.stationary_block_bootstrap_ic_significance

    def _spy(*args, **kwargs):
        captured["expected_step_by_symbol"] = kwargs.get("expected_step_by_symbol")
        return real_bootstrap(*args, **kwargs)

    monkeypatch.setattr(pss, "stationary_block_bootstrap_ic_significance", _spy)

    _pooled_ic, method = rp._pooled_ic_with_bootstrap_fallback(rows, str(tmp_path))

    assert method == "block_bootstrap_all_bars_v1"
    assert captured["expected_step_by_symbol"] is None, (
        "one window missing 'timestamp' must fall back to expected_step_by_symbol=None "
        "for the whole pooled symbol, not a partially-derived step feeding heterogeneous records"
    )
