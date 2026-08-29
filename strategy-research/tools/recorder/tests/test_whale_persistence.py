"""
Sign-persistence measurement: the turnover definition, and the censoring guard.

The turnover cases are checked against hand-counted expectations rather than
against `_compute_turnover_proxy` itself — importing the original and asserting
the two agree would pass on a shared misreading, and the point of this module is
that it is a faithful transcription.

The censoring tests carry the most weight. `avg_holding_bars` computed over short
segments looks like a perfectly good measurement — plenty of episodes, tight
standard error — while being bounded above by the segment length. That is how the
W11 capture produced H ~ 1.05 with 71 episodes when the true H was simply not
observable, so the guard that catches it is tested directly rather than trusted.
"""

from __future__ import annotations

import math

import pandas as pd
import pytest

from recorder.whale_persistence import (
    ACTIVE_THRESHOLD,
    MAX_CENSORED_FRACTION,
    MIN_OPENS_FOR_STABLE_H,
    SIGNAL_COLUMNS,
    PersistenceResult,
    _attested_segments,
    _signs,
    measure_symbol,
    pool,
    stability_verdict,
    turnover_from_sign_segments,
)


# ---------------------------------------------------------------------------
# sign mapping
# ---------------------------------------------------------------------------


def test_signs_tristate_and_threshold():
    vals = [1.0, -1.0, 0.0, ACTIVE_THRESHOLD, -ACTIVE_THRESHOLD, 1e-3]
    # exactly AT the threshold is inactive: the comparison is strict `>`
    assert _signs(vals) == [1, -1, 0, 0, 0, 1]


def test_nan_is_flat_by_default_and_droppable():
    vals = [1.0, float("nan"), 1.0]
    assert _signs(vals, nan_is_flat=True) == [1, 0, 1]
    assert _signs(vals, nan_is_flat=False) == [1, 1]


# ---------------------------------------------------------------------------
# the turnover definition, transcribed from prescreen_signal.py:505-545
# ---------------------------------------------------------------------------


def test_flat_gap_closes_an_episode():
    """The 2026-07-07 redefinition: a flat bar ends a trade, so +,0,+ is TWO."""
    r = turnover_from_sign_segments([[1, 0, 1]])
    assert r["active_bars_total"] == 2
    assert r["opens"] == 2
    assert r["avg_holding_bars"] == 1.0


def test_direct_sign_flip_counts_as_one_open():
    r = turnover_from_sign_segments([[1, -1]])
    assert r["active_bars_total"] == 2
    assert r["opens"] == 2  # one close + one open, exactly one NEW episode per bar


def test_persistent_run_is_one_episode():
    r = turnover_from_sign_segments([[1, 1, 1, 1, 1, 1]])
    assert r["opens"] == 1
    assert r["avg_holding_bars"] == 6.0


def test_segments_do_not_bridge():
    """Two segments of +++ are two episodes, never one six-bar episode."""
    joined = turnover_from_sign_segments([[1, 1, 1, 1, 1, 1]])
    split = turnover_from_sign_segments([[1, 1, 1], [1, 1, 1]])
    assert joined["avg_holding_bars"] == 6.0
    assert split["avg_holding_bars"] == 3.0
    assert split["opens"] == 2


def test_all_flat_yields_no_estimate():
    r = turnover_from_sign_segments([[0, 0, 0]])
    assert r["opens"] == 0
    assert r["avg_holding_bars"] is None  # not 0.0 — nothing was measured


# ---------------------------------------------------------------------------
# censoring
# ---------------------------------------------------------------------------


def test_episode_ending_at_segment_edge_is_censored():
    r = turnover_from_sign_segments([[1, 1, 1]])
    assert r["censored_episodes"] == 1


def test_episode_ending_on_a_flat_bar_is_not_censored():
    r = turnover_from_sign_segments([[1, 1, 0]])
    assert r["censored_episodes"] == 0


def test_sign_flip_before_the_edge_leaves_only_the_last_censored():
    r = turnover_from_sign_segments([[1, 1, -1, -1]])
    assert r["opens"] == 2
    assert r["censored_episodes"] == 1


def test_short_segments_cap_measurable_h_regardless_of_episode_count():
    """
    THE FAILURE MODE THIS MODULE EXISTS TO CATCH.

    A signal that truly persists for 50 bars, observed through 2-bar windows,
    reports H = 2.0 with excellent precision. Precision passes; the number is
    wrong by 25x. Only the censoring flag distinguishes this from a real H of 2.
    """
    truly_persistent = [[1, 1]] * 200  # 200 windows, signal never flips
    r = turnover_from_sign_segments(truly_persistent)
    assert r["avg_holding_bars"] == 2.0
    assert r["opens"] == 200  # plenty of episodes
    assert r["censored_episodes"] == 200  # every one truncated

    res = PersistenceResult(
        symbol=None,
        feature="f",
        active_bars=int(r["active_bars_total"]),
        opens=int(r["opens"]),
        censored_episodes=int(r["censored_episodes"]),
        episode_lengths=list(r["episode_lengths"]),
        segment_lengths=[2] * 200,
        avg_holding_bars=r["avg_holding_bars"],
    )
    assert res.precise is True  # 200 >= 30
    assert res.uncensored is False  # 1.0 > 0.20
    assert res.stable is False  # the conjunction is what gates
    assert res.max_observable_h == 2.0


def test_long_segments_are_not_flagged():
    """Same signal, observed through windows long enough to see it end."""
    segs = [[1] * 5 + [0] * 3 for _ in range(40)]
    r = turnover_from_sign_segments(segs)
    res = PersistenceResult(
        symbol=None,
        feature="f",
        active_bars=int(r["active_bars_total"]),
        opens=int(r["opens"]),
        censored_episodes=int(r["censored_episodes"]),
        episode_lengths=list(r["episode_lengths"]),
        segment_lengths=[8] * 40,
        avg_holding_bars=r["avg_holding_bars"],
    )
    assert res.avg_holding_bars == 5.0
    assert res.censored_fraction == 0.0
    assert res.stable is True


# ---------------------------------------------------------------------------
# attested segmentation off the bar frame
# ---------------------------------------------------------------------------


def test_attested_segments_split_on_unattested_bars():
    df = pd.DataFrame(
        {
            "whale_attested": [1.0, 1.0, 0.0, 1.0, 1.0, 1.0],
            "f": [0.5, 0.6, 9.9, 0.7, 0.8, 0.9],
        }
    )
    segs = _attested_segments(df, "f")
    assert [len(s) for s in segs] == [2, 3]
    # the unattested bar's value never enters any segment
    assert 9.9 not in [v for s in segs for v in s]


# ---------------------------------------------------------------------------
# pooling
# ---------------------------------------------------------------------------


def test_pool_sums_numerators_not_ratios():
    """
    A pair with 1 episode of 10 bars and one with 10 episodes of 1 bar pool to
    20/11, not to the mean of 10.0 and 1.0.
    """
    a = PersistenceResult(symbol="A", feature="f", active_bars=10, opens=1, avg_holding_bars=10.0)
    b = PersistenceResult(symbol="B", feature="f", active_bars=10, opens=10, avg_holding_bars=1.0)
    p = pool([a, b], "f")
    assert p.active_bars == 20 and p.opens == 11
    assert p.avg_holding_bars == pytest.approx(20 / 11)
    assert p.avg_holding_bars != pytest.approx(5.5)  # not the mean of ratios


def test_pool_ignores_other_features():
    a = PersistenceResult(symbol="A", feature="f", active_bars=10, opens=2)
    b = PersistenceResult(symbol="A", feature="g", active_bars=99, opens=99)
    assert pool([a, b], "f").active_bars == 10


# ---------------------------------------------------------------------------
# verdict
# ---------------------------------------------------------------------------


def _res(opens, active, censored, seg_len, n_segs, feature="f"):
    return PersistenceResult(
        symbol=None,
        feature=feature,
        bars_attested=n_segs * seg_len,
        active_bars=active,
        opens=opens,
        censored_episodes=censored,
        episode_lengths=[1] * opens,
        segment_lengths=[seg_len] * n_segs,
        avg_holding_bars=active / max(opens, 1),
    )


def test_verdict_fails_on_censoring_even_when_precise():
    v = stability_verdict([_res(opens=200, active=400, censored=200, seg_len=2, n_segs=200)])
    assert v["precise"] is True
    assert v["uncensored"] is False
    assert v["stable"] is False
    assert v["required_segment_bars"] == math.ceil(5.74 / MAX_CENSORED_FRACTION)


def test_verdict_fails_on_precision_even_when_uncensored():
    v = stability_verdict([_res(opens=5, active=25, censored=0, seg_len=50, n_segs=5)])
    assert v["precise"] is False
    assert v["uncensored"] is True
    assert v["stable"] is False


def test_verdict_passes_when_both_hold():
    v = stability_verdict([_res(opens=MIN_OPENS_FOR_STABLE_H, active=200, censored=1, seg_len=40, n_segs=10)])
    assert v["stable"] is True


def test_required_segment_scales_with_target_h():
    """Resolving a longer holding period needs proportionally longer runs."""
    a = stability_verdict([_res(20, 40, 20, 2, 20)], target_h=5.74)
    b = stability_verdict([_res(20, 40, 20, 2, 20)], target_h=50.0)
    assert b["required_segment_bars"] > a["required_segment_bars"]
    assert b["required_interruptions_per_bar"] < a["required_interruptions_per_bar"]


# ---------------------------------------------------------------------------
# the module cannot see a return — the structural no-peek guarantee
# ---------------------------------------------------------------------------


def test_module_imports_no_price_or_return_machinery():
    """
    `w11_correction.why_this_amendment_cannot_be_a_peek` in
    prereg_whale_footprint_v2.yaml rests on this module being unable to relate a
    feature to a return. That is a property of its imports, so it is asserted
    here rather than left as a comment that can rot.
    """
    import ast

    import recorder.whale_persistence as wp

    tree = ast.parse(open(wp.__file__, encoding="utf-8").read())

    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
            imported.add(node.module)

    # Prose is not evidence — the docstring legitimately discusses returns in
    # order to say it cannot see them. What matters is what the code can reach.
    forbidden_modules = {
        "prescreen_signal",
        "tools",
        "data_manager",
        "backtester",
        "performance",
        "strategies",
        "scipy",
        "sklearn",
        "statsmodels",
    }
    assert not (imported & forbidden_modules), (
        f"whale_persistence.py imports {imported & forbidden_modules} — this "
        "module must not be able to reach price, return or correlation machinery"
    )
    assert imported <= {
        "__future__",
        "argparse",
        "math",
        "statistics",
        "dataclasses",
        "pathlib",
        "typing",
        "numpy",
        "pandas",
        "sys",
        "recorder",
        "recorder.shard_reader",
        "recorder.whale_features",
        "shard_reader",
        "whale_features",  # the relative-import spellings
    }, f"unexpected imports in whale_persistence.py: {imported}"

    # No call anywhere in the module loads a file the recorder does not own.
    calls = {
        node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    for reader in ("read_csv", "read_parquet", "read_json", "corr", "corrwith"):
        assert reader not in calls, (
            f"whale_persistence.py calls .{reader}() — it must load no price series and compute no correlation"
        )


def test_measure_symbol_covers_every_registered_feature():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-07-27", periods=4, freq="h"),
            "whale_attested": [1.0, 1.0, 1.0, 1.0],
            "whale_lt_imbalance": [0.5, 0.5, -0.5, float("nan")],
            "whale_cvd_delta": [10.0, -10.0, -10.0, 10.0],
            "whale_size_shift": [0.1, 0.1, 0.1, 0.1],
        }
    )
    out = measure_symbol(df, "BTCUSD")
    assert set(out) == set(SIGNAL_COLUMNS)
    assert out["whale_size_shift"].avg_holding_bars == 4.0
    assert out["whale_size_shift"].censored_episodes == 1
    # +,+,-,NaN  ->  episodes [2 bars +], [1 bar -]; NaN is flat so the second closes
    assert out["whale_lt_imbalance"].opens == 2
    assert out["whale_lt_imbalance"].censored_episodes == 0
