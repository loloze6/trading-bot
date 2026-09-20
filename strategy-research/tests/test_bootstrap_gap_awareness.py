"""
Gap-awareness tests for performance.signal_statistics.stationary_block_bootstrap_ic_significance
(CUL-20 / GH#63, the #50 family; relocated from prescreen_signal.py, E-039 step
5, 2026-09-12). Pre-registered in
docs/analysis-reports/PRESCREEN_GAP_BOOTSTRAP_POLICY.md.

The stationary block bootstrap must draw each block from within a single
contiguous segment and wrap circularly within that segment only, so no block
straddles a data hole (nor wraps series-end to series-start across one).
`expected_step_by_symbol=None` reproduces the pre-gap-aware global-wrap
resampling byte-for-byte.
"""

import inspect
import random
import sys
from pathlib import Path

import pandas as pd

TRADING_BOT_ROOT = Path(__file__).parent.parent.parent / "trading-bot"
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))
TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

from performance import signal_statistics as pss
from performance.signal_statistics import spearman_correlation, stationary_block_bootstrap_ic_significance

_STEP = pd.Timedelta(1, unit="h")
_BASE = pd.Timestamp("2020-01-01 00:00:00")
_B, _R, _SEED = 3, 4, 0  # small block_size / n_resamples for fast, deterministic runs


def _recs(forecasts, returns, hole_after=None):
    """Records at a 1h step; `hole_after` inserts a 2h jump (one missing bar)
    after that index, so a gap falls between it and the next record."""
    recs, h = [], 0
    for i, (f, r) in enumerate(zip(forecasts, returns, strict=True)):
        recs.append({"forecast": float(f), "next_return_bps": float(r), "timestamp": _BASE + pd.Timedelta(h, unit="h")})
        h += 2 if i == hole_after else 1
    return recs


def _ref_positional_bootstrap(records_by_symbol, block_size, n_resamples, seed):
    """Independent reimplementation of the PRE-#63 global-wrap algorithm (blocks
    over the whole positional series, circular at the series end). The gap-aware
    function with expected_step=None must equal this byte-for-byte."""
    symbol_arrays, obs_f, obs_r = {}, [], []
    for sym, recs in records_by_symbol.items():
        f = [x["forecast"] for x in recs]
        ret = [x["next_return_bps"] for x in recs]
        symbol_arrays[sym] = (f, ret)
        obs_f.extend(f)
        obs_r.extend(ret)
    observed_ic = spearman_correlation(obs_f, obs_r)
    base = {"method": "block_bootstrap_all_bars_v1", "block_size": block_size, "n_resamples": n_resamples}
    if observed_ic is None:
        return {**base, "pooled_ic": None, "p_value": 1.0, "significant": False, "n_bootstrap_valid": 0}
    rng = random.Random(seed)
    boot = []
    for _ in range(n_resamples):
        rf, rr = [], []
        for f, ret in symbol_arrays.values():
            n = len(f)
            if n == 0:
                continue
            nb = (n + block_size - 1) // block_size
            for _b in range(nb):
                start = rng.randrange(0, n)
                for k in range(block_size):
                    idx = (start + k) % n
                    rf.append(f[idx])
                    rr.append(ret[idx])
        ic = spearman_correlation(rf, rr)
        if ic is not None:
            boot.append(ic)
    if not boot:
        return {
            **base,
            "pooled_ic": round(observed_ic, 6),
            "p_value": 1.0,
            "significant": False,
            "n_bootstrap_valid": 0,
        }
    fl = sum(1 for v in boot if v <= 0) / len(boot)
    fg = sum(1 for v in boot if v >= 0) / len(boot)
    p = min(1.0, 2.0 * min(fl, fg))
    return {
        **base,
        "pooled_ic": round(observed_ic, 6),
        "p_value": round(p, 4),
        "significant": bool(p < pss._SIG_THRESHOLD),
        "n_bootstrap_valid": len(boot),
    }


def _capture_blocks(monkeypatch, records_by_symbol, expected_step_by_symbol, block_size=_B, n_resamples=_R):
    """Run the bootstrap with spearman_correlation spied so we recover the exact
    sampled return-markers per resample; returns the list of per-resample marker
    lists (excluding the first, which is the observed-IC call)."""
    captured = []

    def _spy(f_arg, r_arg):
        captured.append(list(r_arg))
        return 0.5  # fixed non-None IC so every resample is valid

    monkeypatch.setattr(pss, "spearman_correlation", _spy)
    pss.stationary_block_bootstrap_ic_significance(
        records_by_symbol,
        block_size=block_size,
        n_resamples=n_resamples,
        seed=_SEED,
        expected_step_by_symbol=expected_step_by_symbol,
    )
    return captured[1:]  # drop the observed-IC call


# ---------------------------------------------------------------------------
# Bit-identity (None default reproduces the global-wrap algorithm exactly)
# ---------------------------------------------------------------------------


def test_bootstrap_no_expected_step_is_byte_identical():
    """On a GAPPY fixture, expected_step_by_symbol=None must equal the
    independent global-wrap reimplementation byte-for-byte (same seed) -- the
    hole is invisible to the None path. n=9 == 3*block_size so the per-segment
    block count is exercised exactly (an off-by-one there changes the draw
    count and breaks this equality)."""
    fc = [1.0, 2.0, 1.0, 3.0, 2.0, 1.0, 4.0, 2.0, 3.0]
    rt = [10.0, -5.0, 3.0, 8.0, -2.0, 6.0, -4.0, 1.0, 7.0]
    rbs = {"SYNTH": _recs(fc, rt, hole_after=4)}

    got = stationary_block_bootstrap_ic_significance(
        rbs, block_size=_B, n_resamples=_R, seed=_SEED
    )  # expected_step defaults None
    assert got == _ref_positional_bootstrap(rbs, _B, _R, _SEED)


def test_bootstrap_gapfree_unchanged():
    """On a gap-free single symbol (one segment either way) the result is
    identical with and without expected_step."""
    fc = [1.0, 2.0, 1.0, 3.0, 2.0, 1.0, 4.0, 2.0]
    rt = [10.0, -5.0, 3.0, 8.0, -2.0, 6.0, -4.0, 1.0]
    rbs = {"SYNTH": _recs(fc, rt)}  # contiguous, no hole

    with_step = stationary_block_bootstrap_ic_significance(
        rbs, block_size=_B, n_resamples=_R, seed=_SEED, expected_step_by_symbol={"SYNTH": _STEP}
    )
    without = stationary_block_bootstrap_ic_significance(rbs, block_size=_B, n_resamples=_R, seed=_SEED)
    assert with_step == without == _ref_positional_bootstrap(rbs, _B, _R, _SEED)


# ---------------------------------------------------------------------------
# Segment confinement (no block spans a gap; no series-end wrap across one)
# ---------------------------------------------------------------------------


def test_bootstrap_block_never_spans_gap(monkeypatch):
    """With a hole after index 4 (segments [0,5) and [5,10)), every emitted
    block of block_size markers lies entirely within ONE segment."""
    fc = [1.0] * 10
    rt = list(range(10))  # each bar's return == its index, so rr recovers indices
    rbs = {"SYNTH": _recs(fc, rt, hole_after=4)}

    resamples = _capture_blocks(monkeypatch, rbs, {"SYNTH": _STEP})
    assert resamples  # sanity: some resamples happened
    for rr in resamples:
        assert len(rr) % _B == 0
        for j in range(0, len(rr), _B):
            block = [int(v) for v in rr[j : j + _B]]
            in_seg0 = all(0 <= i < 5 for i in block)
            in_seg1 = all(5 <= i < 10 for i in block)
            assert in_seg0 or in_seg1, f"block spans the gap: {block}"
    # ...and each segment's bars are actually drawn from THAT segment: a block
    # anchored to seg1 must sample [5,10), not collapse onto [0,5).
    marks = {int(v) for rr in resamples for v in rr}
    assert marks & set(range(0, 5)), "segment [0,5) never sampled"
    assert marks & set(range(5, 10)), "segment [5,10) never sampled"


def test_bootstrap_no_circular_wrap_across_series_end(monkeypatch):
    """The last segment wraps within itself, never from series-end (index 9)
    back to series-start (index 0) -- the maximal-discontinuity wrap the global
    circular bootstrap would produce."""
    fc = [1.0] * 10
    rt = list(range(10))
    rbs = {"SYNTH": _recs(fc, rt, hole_after=4)}

    resamples = _capture_blocks(monkeypatch, rbs, {"SYNTH": _STEP})
    for rr in resamples:
        for j in range(0, len(rr), _B):
            block = {int(v) for v in rr[j : j + _B]}
            assert not (9 in block and 0 in block), f"series-end wrap: {block}"


# ---------------------------------------------------------------------------
# The timestamp-less run_protocol fallback path stays on None (no KeyError)
# ---------------------------------------------------------------------------


def test_pooled_ic_bootstrap_fallback_timestampless_records():
    """run_protocol._pooled_ic_with_bootstrap_fallback builds records with NO
    'timestamp' key and calls the bootstrap with one arg. That must still run
    (expected_step defaults None -> contiguous_segments never reads a
    timestamp) and return a well-formed result."""
    records = [{"forecast": float(i % 3 - 1), "next_return_bps": float(i - 5)} for i in range(12)]
    result = stationary_block_bootstrap_ic_significance(
        {"kraken_ZECUSD": records}, block_size=_B, n_resamples=_R, seed=_SEED
    )
    assert result["method"] == "block_bootstrap_all_bars_v1"
    assert set(result) >= {"pooled_ic", "p_value", "significant", "n_bootstrap_valid"}


# ---------------------------------------------------------------------------
# End-to-end wiring: run_protocol must pass the step map into the bootstrap
# ---------------------------------------------------------------------------


def test_bootstrap_wiring_passes_expected_step():
    """PR #65 isolation lesson: guard the production call site. A silent revert
    to the one-arg call would turn gap-awareness off in production while the
    unit tests above (which pass expected_step directly) stay green."""
    import run_protocol as rp

    src = inspect.getsource(rp._pooled_ic_with_bootstrap_fallback)
    assert "stationary_block_bootstrap_ic_significance(" in src
    assert "expected_step_by_symbol=expected_step_by_symbol" in src


def test_bootstrap_end_to_end_via_run_protocol_fallback(tmp_path):
    """PR #65 isolation lesson, the real thing: drive the bootstrap through its
    production run_protocol caller (_pooled_ic_with_bootstrap_fallback) end to
    end on the degenerate (all-windows-None correlation) path. The records it
    builds carry NO timestamp and it calls with one arg -> None default -> the
    bootstrap must run and return the block_bootstrap method (no KeyError from
    contiguous_segments)."""
    import csv

    import run_protocol as rp

    run_dir = tmp_path / "r1"
    run_dir.mkdir()
    with open(run_dir / "bars.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["forecast", "close"])
        for i in range(30):
            w.writerow([10.0 if i % 2 else 0.0, 100.0 + i])  # degenerate active forecast
    rows = [
        {"window": "w1", "run_id": "r1", "symbol": "SYM", "core": {"forecast_return_corr": None}}
    ]  # forces the bootstrap fallback

    _pooled_ic, method = rp._pooled_ic_with_bootstrap_fallback(rows, str(tmp_path))
    assert method == "block_bootstrap_all_bars_v1"


def test_bootstrap_none_byte_identical_short_series():
    """Bit-identity guard for n < block_size: the pre-#63 global wrap emitted
    block_size items even when the series was shorter (wrapping), so the block
    length cap must NOT apply on the None path. n = block_size - 1."""
    fc = [1.0, 2.0]  # n = 2 = _B - 1 (< block_size)
    rt = [10.0, -5.0]
    rbs = {"SYNTH": _recs(fc, rt)}  # gap-free
    got = stationary_block_bootstrap_ic_significance(rbs, block_size=_B, n_resamples=_R, seed=_SEED)
    assert got == _ref_positional_bootstrap(rbs, _B, _R, _SEED)


def test_bootstrap_block_mass_not_inflated(monkeypatch):
    """A segment shorter than block_size must contribute a whole-segment block,
    not a block_size-length block padded by repetition. On 10 segments of 3 with
    block_size 24, the gap-aware total sampled markers must stay within the
    None-path count (+ block_size slack); without the cap it is ~5x."""
    recs, h = [], 0
    for _s in range(10):
        for _ in range(3):
            recs.append({"forecast": 10.0, "next_return_bps": 1.0, "timestamp": _BASE + pd.Timedelta(h, unit="h")})
            h += 1
        h += 5  # hole between segments
    rbs = {"SYM": recs}
    none_n = sum(len(rr) for rr in _capture_blocks(monkeypatch, rbs, None, block_size=24, n_resamples=20))
    gap_n = sum(len(rr) for rr in _capture_blocks(monkeypatch, rbs, {"SYM": _STEP}, block_size=24, n_resamples=20))
    assert gap_n <= none_n + 24, f"resampled-mass inflation: gap {gap_n} vs None {none_n}"
