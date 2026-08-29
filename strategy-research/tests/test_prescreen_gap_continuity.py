"""
Issue #50 -- prescreen forward-return continuity.

Pins the policy in docs/analysis-reports/PRESCREEN_GAP_POLICY.md against the
six acceptance criteria pre-registered in its section 9, BEFORE the code was
written:

  C1  bit-identity on a gap-free series (if this moves, part A is wrong)
  C2  gap_skipped_pairs is exact
  C3  gap-aware n_eff, validated on a KNOWN active-bar pattern -- not against
      the census column, which counts total rows (Dorian, #50 R1)
  C4  one known hole: the spanning pair is skipped, its neighbours untouched
  C5  a malformed timestamp raises, naming file and count (section 8)
  C6  covered by the suites, not here

Plus the ordering the policy promises: gap-awareness is applied to the block
term BEFORE the max(..., len(ic_values)) floor, so a floor above the placeable
count can never silently restore the inflated n_eff.
"""
import csv
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

TOOLS = Path(__file__).parent.parent / "tools"
TBOT = Path(__file__).parent.parent.parent / "trading-bot"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TBOT))

import prescreen_signal as ps  # noqa: E402

HOUR = pd.Timedelta(hours=1)


def _recs(spec):
    """spec: list of (hours_since_epoch_start, active). Builds record dicts of
    the shape _gap_aware_block_count consumes."""
    base = pd.Timestamp("2024-01-01 00:00:00")
    return [{"timestamp": base + pd.Timedelta(hours=h), "active": a} for h, a in spec]


# --------------------------------------------------------------------------
# C3 + the ordering guarantee
# --------------------------------------------------------------------------

def test_c3_gap_aware_block_count_on_known_active_pattern():
    """C3: blocks are counted WITHIN contiguous runs. 12 consecutive active
    bars at block_size 4 give 3 blocks; the same 12 split 6+6 by a hole give
    1+1=2, because the two half-blocks either side of the hole cannot be
    joined across it -- that join is exactly the defect."""
    contiguous = _recs([(h, True) for h in range(12)])
    assert ps._gap_aware_block_count(contiguous, 4, HOUR) == 3

    # identical bar count, one 5-hour hole after the 6th bar
    split = _recs([(h, True) for h in range(6)] + [(h, True) for h in range(11, 17)])
    assert ps._gap_aware_block_count(split, 4, HOUR) == 2
    # the pre-#50 arithmetic would have counted 12 // 4 == 3
    assert sum(1 for r in split if r["active"]) // 4 == 3


def test_c3_counts_active_bars_not_total_rows():
    """C3, the R1 point: the statistic is over ACTIVE bars. 12 contiguous rows
    of which only 4 are active give 1 block at block_size 4, not 3."""
    mixed = _recs([(h, h % 3 == 0) for h in range(12)])
    assert sum(1 for r in mixed if r["active"]) == 4
    assert ps._gap_aware_block_count(mixed, 4, HOUR) == 1


def test_c3_none_step_reproduces_pre_50_value():
    """expected_step=None must return the ungapped count exactly, which is what
    keeps episode_significance.py's caller byte-identical."""
    split = _recs([(h, True) for h in range(6)] + [(h, True) for h in range(11, 17)])
    assert ps._gap_aware_block_count(split, 4, None) == 12 // 4


def test_floor_is_applied_after_gap_awareness_not_instead():
    """The ordering the policy promises. With a placeable count of 2 and a
    THREE-element ic_values, n_eff must be the floor (3) only because 3 > 2 --
    and with a single-element ic_values (both real call sites) it must be the
    gap-aware 2, never the inflated nominal."""
    single = ps._block_adjusted_significance([0.05], 480, 24, placeable_blocks=2)
    assert single["n_eff"] == 2, "gap-aware term must survive the floor"

    # nominal would have been 480 // 24 == 20; prove we are not getting that
    nominal = ps._block_adjusted_significance([0.05], 480, 24)
    assert nominal["n_eff"] == 20

    floored = ps._block_adjusted_significance([0.05, 0.06, 0.07], 480, 24, placeable_blocks=2)
    assert floored["n_eff"] == 3


def test_gap_aware_neff_lowers_significance_never_raises_it():
    """The correction must err toward LESS significance, since z = IC *
    sqrt(n_eff - 3). A gap-aware count below nominal must not produce a larger
    |z| or a smaller p."""
    nominal = ps._block_adjusted_significance([0.08], 4800, 24)
    gapped = ps._block_adjusted_significance([0.08], 4800, 24, placeable_blocks=73)
    assert abs(gapped["z_stat"]) < abs(nominal["z_stat"])
    assert gapped["p_value"] > nominal["p_value"]


def test_block_size_zero_raises():
    """Fail loud, not flattering: a degenerate block size must raise rather
    than divide by a silently-clamped 1."""
    with pytest.raises(ValueError):
        ps._gap_aware_block_count(_recs([(0, True)]), 0, HOUR)


# --------------------------------------------------------------------------
# C1 / C2 / C4 -- _extract_forecasts
# --------------------------------------------------------------------------

def _frame(hours):
    base = pd.Timestamp("2024-01-01 00:00:00")
    return pd.DataFrame({
        "timestamp": [base + pd.Timedelta(hours=h) for h in hours],
        "open":  [100.0 + h for h in hours],
        "high":  [100.0 + h for h in hours],
        "low":   [100.0 + h for h in hours],
        "close": [100.0 + h for h in hours],
        "volume": [1.0] * len(hours),
    })


@pytest.fixture
def config(tmp_path):
    """Minimal always-ready strategy config, so is_ready() does not gate the
    tiny fixtures below. Reuses whatever the repo's own prescreen tests use as
    a valid shape; skips if no such config is reachable."""
    candidates = list((Path(__file__).parent).glob("**/*prescreen*config*.json"))
    if not candidates:
        pytest.skip("no prescreen config fixture available in this checkout")
    return str(candidates[0])


def test_c1_c2_c4_gap_free_is_identical_and_hole_is_skipped(monkeypatch):
    """C1/C2/C4 in one, driven through the real _extract_forecasts by stubbing
    only the strategy (the gap logic is in the loop, not the strategy).

    C1: on a GAP-FREE frame, passing expected_step must change nothing --
        identical records, zero skips.
    C4: one hole -> exactly the spanning pair is suppressed and its
        neighbours keep their original returns.
    C2: the skip count is exact.
    """
    class _AlwaysReady:
        component_error_count = 0
        component_error_samples = []
        def __init__(self, *a, **k): pass
        def update(self, row): pass
        def is_ready(self): return True
        def generate_forecast(self): return (1.0,)

    monkeypatch.setattr(ps, "AdvancedStrategy", _AlwaysReady)

    # ---- C1: gap-free, bounded vs unbounded must agree exactly
    clean = _frame(range(6))
    unbounded, _, _, skipped_u = ps._extract_forecasts("ignored", clean)
    bounded, _, _, skipped_b = ps._extract_forecasts("ignored", clean, expected_step=HOUR)
    assert skipped_u == 0 and skipped_b == 0
    assert [r["next_return_bps"] for r in unbounded] == [r["next_return_bps"] for r in bounded]
    assert [r["timestamp"] for r in unbounded] == [r["timestamp"] for r in bounded]

    # ---- C4/C2: one 5-hour hole between index 2 and 3
    holed = _frame([0, 1, 2, 8, 9, 10])
    recs, _, _, skipped = ps._extract_forecasts("ignored", holed, expected_step=HOUR)
    assert skipped == 1                                    # C2: exact
    base = pd.Timestamp("2024-01-01 00:00:00")
    kept = [r["timestamp"] for r in recs]
    assert base + pd.Timedelta(hours=2) not in kept        # the spanning pair is gone
    # neighbours keep their ORIGINAL one-bar returns
    by_ts = {r["timestamp"]: r["next_return_bps"] for r in recs}
    assert by_ts[base] == pytest.approx((101.0 - 100.0) / 100.0 * 10_000.0)
    assert by_ts[base + pd.Timedelta(hours=8)] == pytest.approx(
        (109.0 - 108.0) / 108.0 * 10_000.0)

    # and without the step, the corrupt pair is still present -- proving the
    # fixture actually exercises the defect
    unguarded, _, _, _ = ps._extract_forecasts("ignored", holed)
    assert base + pd.Timedelta(hours=2) in [r["timestamp"] for r in unguarded]


# --------------------------------------------------------------------------
# C5 -- section 8, malformed timestamps and non-finite values
# --------------------------------------------------------------------------

def _write(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        w.writerows(rows)


def test_c5_malformed_timestamp_raises_not_silently_dropped(monkeypatch, tmp_path):
    """C5: the lexical window filter used to drop these before the parse guard
    could see them. Each of these sorts PAST the window end and vanished."""
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    for bad in ("garbage", "NaN", "not-a-date"):
        rows = [[f"2020-01-01 {i:02d}:00:00", 100 + i, 100 + i, 100 + i, 100 + i, 1]
                for i in range(4)]
        rows.insert(2, [bad, 1, 1, 1, 1, 1])
        _write(tmp_path / "BADTS_1h.csv", rows)
        with pytest.raises(ValueError) as exc:
            ps._load_ohlcv("BADTS", "2020-01-01", "2020-02-01")
        assert "BADTS_1h.csv" in str(exc.value)


def test_c5_non_finite_close_raises(monkeypatch, tmp_path):
    """C5, second half: float('NaN') and float('inf') PARSE, so #45's guard
    passes them through. They must not reach the positional pairing."""
    for poison in ("NaN", "inf", "-inf"):
        monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
        rows = [[f"2020-01-01 {i:02d}:00:00", 100 + i, 100 + i, 100 + i, 100 + i, 1]
                for i in range(4)]
        rows[2][4] = poison
        _write(tmp_path / "POISON_1h.csv", rows)
        with pytest.raises(ValueError):
            ps._load_ohlcv("POISON", "2020-01-01", "2020-02-01")


def test_c5_clean_file_still_loads(monkeypatch, tmp_path):
    """Negative control: the guards must not reject a clean file."""
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    _write(tmp_path / "CLEAN_1h.csv",
           [[f"2020-01-01 {i:02d}:00:00", 100 + i, 100 + i, 100 + i, 100 + i, 1]
            for i in range(5)])
    df = ps._load_ohlcv("CLEAN", "2020-01-01", "2020-02-01")
    assert len(df) == 5


# --------------------------------------------------------------------------
# Call-site wiring (added after a red-team pass, 2026-08-29)
#
# The tests above exercise _gap_aware_block_count and
# _block_adjusted_significance in ISOLATION. A red-team pass showed that was
# not enough: three separate mutations of run_prescreen's wiring left the whole
# 1148-test suite green, including one that made part (B) entirely inert --
#   expected_step_by_symbol.get(sym)  ->  .get(sym + "_MUTANT")
# which returns None for every symbol, and None means "ungapped count".
# These tests pin the wiring itself.
# --------------------------------------------------------------------------

def _write_cache(dirpath, name, hours, step_hours=1):
    base = pd.Timestamp("2020-01-01 00:00:00")
    rows = []
    for k, h in enumerate(hours):
        px = 100.0 + k
        ts = base + pd.Timedelta(hours=h * step_hours)
        rows.append([ts.strftime("%Y-%m-%d %H:%M:%S"), px, px, px, px, 1])
    _write(Path(dirpath) / f"{name}_1h.csv", rows)


def test_wiring_gap_aware_neff_actually_reaches_the_artifact(monkeypatch, tmp_path):
    """Kills the `.get(sym + "_MUTANT")` and dropped-`placeable_blocks` mutants:
    on a gappy cache the artifact's placeable count must be BELOW the nominal
    one. If the wiring is broken they are equal."""
    class _AlwaysReady:
        component_error_count = 0
        component_error_samples = []
        def __init__(self, *a, **k): pass
        def update(self, row): pass
        def is_ready(self): return True
        def generate_forecast(self): return (1.0,)

    monkeypatch.setattr(ps, "AdvancedStrategy", _AlwaysReady)
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))

    # 40 runs of 6 contiguous bars, each separated by a hole -> every run is
    # shorter than block_size, so gap-aware must collapse to 0 while the
    # pooled nominal count stays high.
    hours = []
    for run in range(40):
        hours.extend([run * 100 + k for k in range(6)])
    _write_cache(tmp_path, "GAPPY", hours)

    df = ps._load_ohlcv("GAPPY", "2020-01-01", "2021-01-01")
    recs, _, _, skipped = ps._extract_forecasts(
        "cfg", df, expected_step=pd.Timedelta(hours=1))
    nominal = sum(1 for r in recs if r["active"]) // 24
    placeable = ps._gap_aware_block_count(recs, 24, pd.Timedelta(hours=1))

    assert skipped == 39, f"expected 39 gap-spanning pairs, got {skipped}"
    assert nominal > 0, "fixture must have a non-trivial nominal count"
    assert placeable == 0, (
        "every contiguous run is shorter than block_size, so no block can be "
        f"placed; got {placeable}. A None step (the D1 mutant) would give {nominal}."
    )


def test_wiring_none_step_is_the_inflated_value_the_mutant_would_restore():
    """States the D1 hazard explicitly: passing None where the step belongs
    silently returns the ungapped count. This is why the call site uses
    [sym] rather than .get(sym)."""
    split = _recs([(h, True) for h in range(6)] + [(h, True) for h in range(200, 206)])
    assert ps._gap_aware_block_count(split, 4, HOUR) == 2
    assert ps._gap_aware_block_count(split, 4, None) == 3   # the inflated value


def test_wiring_gap_skipped_counter_is_not_stuck_at_zero(monkeypatch):
    """Kills the `total_gap_skipped += 0` mutant at the accumulator."""
    class _AlwaysReady:
        component_error_count = 0
        component_error_samples = []
        def __init__(self, *a, **k): pass
        def update(self, row): pass
        def is_ready(self): return True
        def generate_forecast(self): return (1.0,)

    monkeypatch.setattr(ps, "AdvancedStrategy", _AlwaysReady)
    holed = _frame([0, 1, 2, 20, 21, 22, 40, 41])
    _, _, _, skipped = ps._extract_forecasts(
        "cfg", holed, expected_step=pd.Timedelta(hours=1))
    assert skipped == 2, f"two holes -> two suppressed pairs, got {skipped}"


def test_multi_symbol_neff_is_per_symbol_not_pooled():
    """D2, pinned rather than papered over. The per-symbol sum is intentionally
    NOT equal to the pooled floor on gap-free data: a block spanning a symbol
    boundary is as meaningless as one spanning a gap. sum(floor(a_i/b)) can be
    below floor(sum(a_i)/b) by up to n_symbols-1."""
    a = _recs([(h, True) for h in range(10)])
    b = _recs([(h, True) for h in range(10)])
    per_symbol = (ps._gap_aware_block_count(a, 4, HOUR)
                  + ps._gap_aware_block_count(b, 4, HOUR))
    pooled = (len(a) + len(b)) // 4
    assert per_symbol == 4 and pooled == 5, (
        "the documented multi-symbol divergence must hold: "
        f"per_symbol={per_symbol}, pooled={pooled}"
    )


# --------------------------------------------------------------------------
# END-TO-END through run_prescreen.
#
# The "wiring" tests above STILL did not kill the red-team's three mutants,
# because they call _extract_forecasts and _gap_aware_block_count directly --
# the mutated lines live inside run_prescreen and were never executed. Only a
# test that drives the real entry point pins the wiring. Recorded because it is
# the same trap twice: a test that exercises the ingredients is not a test of
# the recipe.
# --------------------------------------------------------------------------

def _minimal_protocol(tmp_path, symbols, timeframe="1h"):
    path = tmp_path / "protocol.json"
    path.write_text(json.dumps({
        "symbols": symbols,
        "timeframe": timeframe,
        "windows": [{"label": "w1",
                     "train": {"start": "2019-01-01", "end": "2020-01-01"},
                     "test":  {"start": "2020-01-01", "end": "2021-01-01"}}],
    }))
    return str(path)


def _minimal_config(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"aux_feeds": [], "strategy": "stub"}))
    return str(path)


@pytest.fixture
def e2e(monkeypatch, tmp_path):
    """run_prescreen driven over synthetic caches with a stubbed strategy."""
    class _Varying:
        """Forecasts must VARY across bars. A constant forecast has only one
        distinct active value, so ic_active_bars is undefined by construction,
        _is_degenerate_active_forecast fires, and the artifact reports the
        BOOTSTRAP branch -- which is NOT the branch part (B) corrects. A mutant
        survived against a constant-1.0 stub for exactly this reason."""
        component_error_count = 0
        component_error_samples = []
        def __init__(self, *a, **k): self._i = 0
        def update(self, row): self._i += 1
        def is_ready(self): return True
        def generate_forecast(self):
            return (float((self._i * 7919) % 11) - 5.0,)

    monkeypatch.setattr(ps, "AdvancedStrategy", _Varying)
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    monkeypatch.setattr(ps, "_load_cost_model", lambda: {
        "fee_rate_bps": {"default": 7.5},
        "round_trip_cost_bps": {"default": 18.5},
        "safety_factor": 2.0,
    })
    return tmp_path


def test_e2e_gap_aware_neff_reaches_the_artifact(e2e, tmp_path):
    """THE test that kills the D1 mutants. On a gappy cache the artifact's
    placeable count must sit BELOW the nominal one; every one of the three
    surviving mutations makes them equal."""
    hours = []
    for run in range(40):
        hours.extend([run * 100 + k for k in range(6)])   # runs of 6, block is 24
    _write_cache(e2e, "GAPPY", hours)

    out = ps.run_prescreen(_minimal_config(tmp_path),
                           _minimal_protocol(tmp_path, ["GAPPY"]),
                           run_id="e2e_gap", out_dir=tmp_path / "out")

    assert out["gap_skipped_pairs"] == 39, out["gap_skipped_pairs"]
    assert out["n_eff_placeable_blocks"] == 0, (
        "runs of 6 cannot host a 24-bar block; a broken step lookup would "
        f"report the ungapped {out['n_eff_nominal_blocks']}"
    )
    assert out["n_eff_placeable_blocks"] < out["n_eff_nominal_blocks"]
    assert out["gap_stats_by_symbol"]["GAPPY"]["gap_skipped_pairs"] == 39

    # The artifact FIELD is set from the local variable; the number that steers
    # the verdict is the one inside ic_significance. Asserting only the field
    # left "drop placeable_blocks= from the significance call" alive as a
    # mutant -- the field stayed correct while the statistic reverted.
    assert out["ic_significance"]["n_eff"] < out["n_eff_nominal_blocks"], (
        "gap-aware n_eff must reach the SIGNIFICANCE call, not just the "
        f"artifact field: ic_significance.n_eff={out['ic_significance']['n_eff']}, "
        f"nominal={out['n_eff_nominal_blocks']}"
    )


def test_e2e_gap_free_single_symbol_is_unchanged(e2e, tmp_path):
    """C1 where it genuinely holds: one gap-free symbol, nothing moves."""
    _write_cache(e2e, "CLEAN", list(range(600)))
    out = ps.run_prescreen(_minimal_config(tmp_path),
                           _minimal_protocol(tmp_path, ["CLEAN"]),
                           run_id="e2e_clean", out_dir=tmp_path / "out")
    assert out["gap_skipped_pairs"] == 0
    assert out["gap_skipped_pct"] == 0.0
    assert out["n_eff_placeable_blocks"] == out["n_eff_nominal_blocks"]


def test_e2e_fully_gapped_symbol_raises(e2e, tmp_path):
    """Policy section 6 / red-team D3: a symbol whose every pair spans a gap
    must RAISE, not emit a route from zero records with a placeholder sigma
    flagged as a measurement."""
    _write_cache(e2e, "ALLGAP", [k * 2 for k in range(200)])   # 2h steps at 1h tf
    with pytest.raises(RuntimeError, match="ZERO usable forecast records"):
        ps.run_prescreen(_minimal_config(tmp_path),
                         _minimal_protocol(tmp_path, ["ALLGAP"]),
                         run_id="e2e_allgap", out_dir=tmp_path / "out")
