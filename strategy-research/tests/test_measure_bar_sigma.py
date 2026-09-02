"""
Per-bar sigma measurement: the return definition, the holdout assertion, and
the structural guarantee that this tool cannot see a whale feature.

The sigma definition is checked against a hand-constructed price series with a
known standard deviation rather than against `prescreen_signal._sigma_from_records`
— the two must agree, but asserting that directly would let a shared misreading of
"per-bar return in bps" pass both.
"""

from __future__ import annotations

import ast
import math
import statistics
import sys
import warnings
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.measure_bar_sigma import (  # noqa: E402
    DEFAULT_BASES,
    DEFAULT_END,
    DEFAULT_START,
    HOLDOUT_RANGE,
    HoldoutViolation,
    _assert_window,
    bar_returns_bps,
    cache_path,
    measure,
    sigma_bar_bps,
)


def _write_cache(tmp_path: Path, base: str, closes, start="2025-01-01 00:00:00"):
    ts = pd.date_range(start, periods=len(closes), freq="h")
    pd.DataFrame({"timestamp": ts, "close": closes}).to_csv(
        tmp_path / f"kraken_{base}USD_1h.csv", index=False
    )
    return tmp_path


# ---------------------------------------------------------------------------
# the return definition
# ---------------------------------------------------------------------------

def test_returns_are_close_to_close_in_bps(tmp_path):
    # +1%, -1% -> +100 bps, -100 bps
    _write_cache(tmp_path, "TEST", [100.0, 101.0, 99.99])
    rets = bar_returns_bps("TEST", None, None, tmp_path)
    assert rets == pytest.approx([100.0, -100.0], rel=1e-9)


def test_n_returns_is_n_bars_minus_one(tmp_path):
    _write_cache(tmp_path, "TEST", [100.0] * 10)
    assert len(bar_returns_bps("TEST", None, None, tmp_path)) == 9


def test_sigma_matches_hand_computed_stdev(tmp_path):
    closes = [100.0, 101.0, 100.0, 102.0, 101.0, 103.0]
    _write_cache(tmp_path, "TEST", closes)
    rets = bar_returns_bps("TEST", None, None, tmp_path)
    expected = [
        (closes[i + 1] - closes[i]) / closes[i] * 10_000.0
        for i in range(len(closes) - 1)
    ]
    assert sigma_bar_bps(rets) == pytest.approx(statistics.stdev(expected))


def test_sigma_is_none_below_five_returns(tmp_path):
    """
    The counterpart of prescreen's <5-record fallback — but this tool returns
    None rather than a placeholder constant. Substituting a number nobody
    measured is exactly the failure this module was written to correct, so it
    refuses instead.
    """
    assert sigma_bar_bps([1.0, 2.0, 3.0, 4.0]) is None
    assert sigma_bar_bps([1.0, 2.0, 3.0, 4.0, 5.0]) is not None


def test_constant_price_gives_zero_sigma(tmp_path):
    _write_cache(tmp_path, "TEST", [100.0] * 10)
    assert sigma_bar_bps(bar_returns_bps("TEST", None, None, tmp_path)) == 0.0


def test_nonpositive_close_is_skipped_not_divided_by(tmp_path):
    _write_cache(tmp_path, "TEST", [100.0, 0.0, 100.0, 101.0])
    rets = bar_returns_bps("TEST", None, None, tmp_path)
    assert all(math.isfinite(r) for r in rets)


def test_window_filters(tmp_path):
    _write_cache(tmp_path, "TEST", [100.0] * 48, start="2025-01-01 00:00:00")
    all_r = bar_returns_bps("TEST", None, None, tmp_path)
    win_r = bar_returns_bps("TEST", "2025-01-02", "2025-01-02", tmp_path)
    assert len(win_r) < len(all_r)


# ---------------------------------------------------------------------------
# holdout protection
# ---------------------------------------------------------------------------

def test_holdout_window_is_refused():
    with pytest.raises(HoldoutViolation):
        _assert_window("2026-01-01", "2026-03-31")


def test_window_straddling_holdout_start_is_refused():
    with pytest.raises(HoldoutViolation):
        _assert_window("2025-06-01", "2026-02-01")


def test_window_enclosing_the_holdout_is_refused():
    with pytest.raises(HoldoutViolation):
        _assert_window("2020-01-01", "2027-01-01")


def test_registered_default_window_is_clean():
    _assert_window(DEFAULT_START, DEFAULT_END)  # must not raise


def test_default_window_ends_before_holdout_opens():
    assert pd.Timestamp(DEFAULT_END) < pd.Timestamp(HOLDOUT_RANGE[0])


def test_measure_refuses_a_holdout_window(tmp_path):
    _write_cache(tmp_path, "TEST", [100.0, 101.0, 102.0, 103.0, 104.0, 105.0])
    with pytest.raises(HoldoutViolation):
        measure(["TEST"], "2026-02-01", "2026-03-01", tmp_path)


# ---------------------------------------------------------------------------
# pooling
# ---------------------------------------------------------------------------

def test_pooled_is_over_concatenated_returns_not_a_mean_of_sigmas(tmp_path):
    _write_cache(tmp_path, "CALM", [100.0, 100.1, 100.0, 100.1, 100.0, 100.1])
    _write_cache(tmp_path, "WILD", [100.0, 110.0, 100.0, 110.0, 100.0, 110.0])
    m = measure(["CALM", "WILD"], "2024-12-01", "2025-12-31", tmp_path)
    assert m["min"] == m["per_pair"]["CALM"]
    assert m["max"] == m["per_pair"]["WILD"]
    # concatenating a calm and a wild series gives a spread wider than the mean
    # of the two individual spreads
    assert m["pooled"] > m["mean"]


def test_per_pair_and_counts_cover_every_requested_base(tmp_path):
    for b in ("A", "B", "C"):
        _write_cache(tmp_path, b, [100.0, 101.0, 100.0, 101.0, 100.0, 101.0])
    m = measure(["A", "B", "C"], "2024-12-01", "2025-12-31", tmp_path)
    assert set(m["per_pair"]) == {"A", "B", "C"}
    assert set(m["n_bars"]) == {"A", "B", "C"}


def test_missing_cache_raises_rather_than_silently_dropping(tmp_path):
    with pytest.raises(FileNotFoundError):
        bar_returns_bps("NOPE", None, None, tmp_path)


# ---------------------------------------------------------------------------
# registration invariants
# ---------------------------------------------------------------------------

def test_default_bases_are_the_nineteen_recorded_pairs():
    assert len(DEFAULT_BASES) == 19
    assert set(DEFAULT_BASES) == {
        "BTC", "ETH", "XRP", "SOL", "ADA", "SUI", "ZEC", "DOGE", "XMR", "LTC",
        "ONDO", "NEAR", "LINK", "TAO", "AVAX", "TRX", "AAVE", "INJ", "UNI",
    }


def test_cache_path_uses_the_kraken_exchange_qualified_convention():
    assert cache_path("BTC", Path("/x")).name == "kraken_BTCUSD_1h.csv"


# ---------------------------------------------------------------------------
# the module cannot see a whale feature — structural no-peek guarantee
# ---------------------------------------------------------------------------

def test_module_cannot_reach_the_recorded_capture():
    """
    Twin of test_whale_persistence.py's import guard. Together they are what
    `w11_correction.why_this_amendment_cannot_be_a_peek` in
    prereg_whale_footprint_v2.yaml actually rests on: the two measured inputs
    come from two programs that share no data, so neither can encode the
    feature-vs-return relationship under test.
    """
    import tools.measure_bar_sigma as mbs

    tree = ast.parse(open(mbs.__file__, encoding="utf-8").read())
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])

    assert "recorder" not in imported, (
        "measure_bar_sigma.py imports recorder.* — it must not be able to read "
        "the forward capture or any whale feature"
    )
    assert imported <= {
        "__future__", "argparse", "math", "os", "statistics", "pathlib",
        "typing", "pandas",
    }, f"unexpected imports in measure_bar_sigma.py: {imported}"

    src = open(mbs.__file__, encoding="utf-8").read()
    for path_fragment in ("recorded_reserved", "holdout_sealed", "kraken_ws_v2"):
        assert f'"{path_fragment}"' not in src and f"'{path_fragment}'" not in src, (
            f"measure_bar_sigma.py references {path_fragment!r} as a path — it "
            "must read only local_data/kraken_<BASE>USD_1h.csv"
        )


# ---------------------------------------------------------------------------
# the seal boundary (2026-08-19): the loader must not out-read its own assertion
# ---------------------------------------------------------------------------

def test_end_date_does_not_admit_the_first_sealed_bar(tmp_path):
    """end="2025-12-31" must not pull in the 2026-01-01 00:00 bar.

    This is the one case where the off-by-one mattered. _assert_window
    correctly PASSES end="2025-12-31" -- it is outside holdout_range -- and the
    loader then filtered on `<= end + 1 day`, which is exactly 2026-01-01
    00:00: the first sealed timestamp. So the tool read one bar past the
    boundary its own assertion exists to defend, silently, and only on the
    boundary itself.

    The fixture straddles the seal so a regression has something to leak.
    """
    # Straddles the boundary on purpose: 12-31 22:00, 12-31 23:00 | 01-01 00:00,
    # 01-01 01:00. Only the first two are legal to read.
    closes = [100.0, 101.0, 102.0, 103.0]
    _write_cache(tmp_path, "BTC", closes, start="2025-12-31 22:00:00")

    got = bar_returns_bps("BTC", "2025-12-31", "2025-12-31", tmp_path)

    # 2 legal bars -> 1 return. Before the fix the filter admitted the
    # 2026-01-01 00:00 bar as well, giving 3 bars and 2 returns.
    assert len(got) == 1, (
        f"expected only pre-seal bars, got {len(got)} returns; >1 means the "
        f"2026-01-01 00:00 bar was admitted")


def test_end_date_still_includes_the_whole_end_day(tmp_path):
    """Control: the fix must not truncate the end day itself.

    `<` on the following midnight keeps every bar of `end`; a naive fix to
    `<= end` would silently drop 23 hours of the last day, which would be a
    quieter bug than the one being fixed.
    """
    closes = [100.0] * 25                           # 2025-06-01 00:00 .. 2025-06-02 00:00
    _write_cache(tmp_path, "BTC", closes, start="2025-06-01 00:00:00")

    got = bar_returns_bps("BTC", "2025-06-01", "2025-06-01", tmp_path)

    # 24 bars of the 1st (00:00..23:00) -> 23 returns. The 2nd's 00:00 is excluded.
    assert len(got) == 23


def test_end_window_filter_raises_no_deprecation_warning(tmp_path):
    """CUL-204 follow-up: the end-window filter built its +1-day bound via
    pd.Timedelta(days=1) -- fixed to pd.Timedelta(1, unit="D") (not
    datetime.timedelta: this module's import allowlist, enforced by
    test_module_cannot_reach_the_recorded_capture, does not include it)."""
    closes = [100.0] * 25
    _write_cache(tmp_path, "BTC", closes, start="2025-06-01 00:00:00")
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        got = bar_returns_bps("BTC", "2025-06-01", "2025-06-01", tmp_path)
    assert len(got) == 23


def test_a_time_bearing_end_does_not_widen_past_its_own_day(tmp_path):
    """end="2025-12-31 23:00" must not admit a whole day of sealed bars.

    Caught in review of the `<=` -> `<` fix: `<` alone was correct only for a
    date-only `end`. With a time component the bound became 2026-01-01 23:00,
    so the tool read 24 sealed bars instead of the single one the original bug
    leaked -- a worse version of the defect being fixed. `.normalize()` pins the
    bound to the end DAY regardless of any time supplied.
    """
    closes = [100.0] * 30                       # 2025-12-31 22:00 .. 2026-01-02 03:00
    _write_cache(tmp_path, "BTC", closes, start="2025-12-31 22:00:00")

    got = bar_returns_bps("BTC", "2025-12-31", "2025-12-31 23:00", tmp_path)

    # Only 12-31 22:00 and 23:00 are legal -> 1 return.
    assert len(got) == 1, (
        f"expected only the two pre-seal bars, got {len(got)} returns -- a "
        f"time-bearing end widened the window into the holdout")
