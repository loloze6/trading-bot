"""
CUL-265 (E-039): A8.5.1a episode-blocked significance, wired into
run_protocol.py's cross-window pooling as an ADDITIVE field.

Three things must hold, and each has a test below:

(a) LOCKSTEP -- the wired-in field must equal what calling
    episode_significance.compute_a851a_significance directly on the same pooled
    records produces. If these ever diverge, the wiring is feeding the function
    something other than what it claims to.
(b) ADDITIVE -- every pre-existing extended-summary field keeps its exact value.
    A8.5.1a is a second opinion, never a replacement for
    median_forecast_return_corr.
(c) NEVER FABRICATED -- when the statistic is not computable (no runs_root, no
    bars.csv), the field is None, not a number. This repo's own rule: a null
    result that was never measured must not be printed as though it were
    (see prescreen_signal._fmt_ic's "must never print as 0.0000").

Note on determinism: episode_block_bootstrap seeds random.Random(seed) with
seed=None by default (prescreen's own A8.5.1a call site does the same), so the
bootstrap path's p_value/ci are NOT reproducible run-to-run. The lockstep test
below therefore uses the DENSE fixture, whose dispatcher branch
(block_<n>_dense_fallback) is fully deterministic -- an exact-equality lockstep
on a genuinely deterministic path beats an approximate one on a random path.
"""
import sys
from pathlib import Path

import pandas as pd

TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402
import episode_significance as es  # noqa: E402


def _write_bars(run_dir: Path, forecasts, closes, freq="D"):
    run_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({
        "timestamp": pd.date_range("2020-01-01", periods=len(forecasts), freq=freq),
        "forecast": forecasts,
        "close": closes,
    }).to_csv(run_dir / "bars.csv", index=False)


def _rows(run_ids, corr=None):
    return [
        {"symbol": "BTCUSDT", "window": f"2020-{i + 1:02d}", "run_id": rid,
         "core": {"win_rate": 40.0, "forecast_return_corr": corr}}
        for i, rid in enumerate(run_ids)
    ]


# ---------------------------------------------------------------------------
# (a) Lockstep against the real function
# ---------------------------------------------------------------------------

def test_a851a_matches_direct_call_on_the_same_pooled_records(tmp_path):
    """The wired path and a direct compute_a851a_significance call on the same
    pooled records must agree exactly. Dense fixture -> deterministic dispatcher
    branch, so this is exact equality, not a tolerance."""
    runs_root = tmp_path / "results"
    # Every bar active -> density 100% >= 50% -> dense fallback, no bootstrap.
    _write_bars(runs_root / "run_a", forecasts=[5.0 + i % 7 for i in range(40)],
                closes=[100 + i * 0.1 for i in range(40)])
    rows = _rows(["run_a"])

    wired = rp._a851a_episode_significance(rows, str(runs_root), "1d")
    assert wired is not None

    records, _step, _all_ts = rp._assemble_pooled_symbol_records(rows, str(runs_root))
    direct = es.compute_a851a_significance(
        records,
        era_of=None,
        block_size=24 // 24,  # bars_per_day("1d") == 1
        expected_step=pd.Timedelta(seconds=86400),
    )

    assert wired["method"] == direct["method"] == "block_1_dense_fallback"
    assert wired["pooled_ic"] == direct["pooled_ic"]
    assert wired["p_value"] == direct["p_value"]
    assert wired["density_pct"] == direct["density_pct"] == 100.0
    assert wired["significant"] == direct["significant"]


def test_active_flag_uses_prescreens_own_threshold(tmp_path):
    """Episode identification is defined entirely in terms of "active", so the
    pooled records' active flag must mean the same shared threshold
    _assemble_pooled_symbol_records itself imports -- not a locally invented
    one (E-039 step 5: relocated from prescreen_signal.py to
    performance.signal_statistics.ACTIVE_THRESHOLD, same value)."""
    from performance.signal_statistics import ACTIVE_THRESHOLD
    runs_root = tmp_path / "results"
    below = ACTIVE_THRESHOLD / 2      # must read inactive
    above = ACTIVE_THRESHOLD * 10     # must read active
    _write_bars(runs_root / "run_a", forecasts=[above, below, above, below],
                closes=[100.0, 101.0, 102.0, 103.0])

    records, _s, _t = rp._assemble_pooled_symbol_records(_rows(["run_a"]), str(runs_root))
    # last bar is dropped (no next close), so 3 records
    assert [r["active"] for r in records] == [True, False, True]


# ---------------------------------------------------------------------------
# (b) Additive -- pre-existing fields unchanged
# ---------------------------------------------------------------------------

def test_preexisting_extended_summary_fields_are_unchanged(tmp_path):
    """A8.5.1a must not perturb median_forecast_return_corr or anything else
    that was already in the extended summary."""
    runs_root = tmp_path / "results"
    _write_bars(runs_root / "run_a", forecasts=[10.0] * 20 + [0.0] * 20,
                closes=[100 + i * 0.1 for i in range(40)])
    per_symbol = {"BTCUSDT": {"median_sharpe": -1.0}}
    rows = _rows(["run_a"])

    extended = rp._build_extended_summary(per_symbol, rows, str(runs_root), "1d")

    # The pre-existing contract, unchanged.
    assert extended["BTCUSDT"]["median_sharpe"] == -1.0
    assert extended["BTCUSDT"]["median_win_rate"] == 40.0
    assert "median_forecast_return_corr" in extended["BTCUSDT"]
    assert "median_forecast_return_corr_method" in extended["BTCUSDT"]
    # ... and the new fields sit alongside it, not in place of it.
    assert "episode_blocked_significance" in extended["BTCUSDT"]
    assert "episode_blocked_significance_method" in extended["BTCUSDT"]


def test_plain_median_path_is_untouched_by_a851a(tmp_path):
    """When per-window corrs exist, median_forecast_return_corr must still be
    the plain median -- A8.5.1a is computed alongside, never substituted in."""
    runs_root = tmp_path / "results"
    _write_bars(runs_root / "run_a", forecasts=[5.0] * 10,
                closes=[100 + i for i in range(10)])
    rows = [
        {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "run_a",
         "core": {"win_rate": 40.0, "forecast_return_corr": 0.05}},
        {"symbol": "BTCUSDT", "window": "2020-02", "run_id": "run_a",
         "core": {"win_rate": 40.0, "forecast_return_corr": 0.07}},
    ]
    extended = rp._build_extended_summary({"BTCUSDT": {}}, rows, str(runs_root), "1d")
    assert extended["BTCUSDT"]["median_forecast_return_corr"] == 0.06
    assert extended["BTCUSDT"]["median_forecast_return_corr_method"] == "per_window_median_pearson"


# ---------------------------------------------------------------------------
# (c) Never fabricated
# ---------------------------------------------------------------------------

def test_no_runs_root_yields_none_not_a_number():
    assert rp._a851a_episode_significance(_rows(["run_a"]), None, "1h") is None


def test_missing_bars_csv_yields_none_not_a_number():
    assert rp._a851a_episode_significance(
        _rows(["missing"]), "/nonexistent/path", "1h") is None


def test_extended_summary_carries_none_when_not_computable():
    """No runs_root at all: the key must be present (so its absence is never
    ambiguous) and must be None (so it is never mistaken for a measurement)."""
    rows = _rows(["run_a"], corr=0.05)
    extended = rp._build_extended_summary({"BTCUSDT": {}}, rows, None, "1h")
    assert extended["BTCUSDT"]["episode_blocked_significance"] is None
    assert extended["BTCUSDT"]["episode_blocked_significance_method"] is None


def test_insufficient_episodes_reports_no_p_value(tmp_path):
    """The <8-episode floor must yield the inconclusive disposition with
    p_value None -- "a bootstrap over 4 episodes is theater" (A8.5.1a spec).
    Sparse enough to take the episode path, too few episodes to claim anything."""
    runs_root = tmp_path / "results"
    # 2 short active bursts separated by a >48-bar inactive stretch: sparse
    # (density < 50%) so the dense fallback does not fire, but only 2 episodes.
    forecasts = [10.0] * 5 + [0.0] * 60 + [10.0] * 5 + [0.0] * 60
    closes = [100 + i * 0.1 for i in range(len(forecasts))]
    _write_bars(runs_root / "run_a", forecasts=forecasts, closes=closes)

    res = rp._a851a_episode_significance(_rows(["run_a"]), str(runs_root), "1d")
    assert res["method"] == "episode_bootstrap_insufficient_n"
    assert res["n_episodes"] == 2
    assert res["p_value"] is None, "must not report a p-value below the episode floor"
    assert res["significant"] is False
    assert res["disposition_note"] == "insufficient_sample_inconclusive"
