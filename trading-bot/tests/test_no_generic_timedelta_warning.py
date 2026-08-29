"""
No numpy generic-unit Timedelta DeprecationWarning from the data path
(backlog 3c, 2026-08-08).

`pd.Timedelta(seconds=|milliseconds=|days=...)` construction emits "The
'generic' unit for NumPy timedelta is deprecated ... implicit conversion of
bare integers" on this numpy/pandas pin -- it fires at CONSTRUCTION, not
arithmetic, and floods every backtest (~5762 warnings over a full `simulate`
run before this fix). It is scheduled to become a hard error on a future
numpy major.

Fix: `data/data_manager.py`, `data/fetchers/base_fetcher.py`, and
`data/fetchers/ccxt_fetcher.py` now build every timedelta with stdlib
`datetime.timedelta(...)` instead of `pd.Timedelta(...)`. NOT
`pd.to_timedelta`: `pd.Timedelta(seconds=nan)` raises `ValueError` today,
`pd.to_timedelta(nan)` returns `NaT` and would silently pass the aux-feed
causality guard (fail-open); `datetime.timedelta(seconds=nan)` raises the
same `ValueError`, preserving the fail-loud behaviour byte-for-byte.

These tests call the real production functions directly (no reimplemented
guard logic) and assert both the absence of the warning and the exact
values the guard/fetcher produce, so a fix that merely silences the warning
while shifting a boundary by even one second still fails.
"""

import ast
import sys
import warnings
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import AuxFeedCausalityError, _merge_asof_with_causality_guard  # noqa: E402
from data.fetchers.base_fetcher import BaseFetcher, FetchGapError  # noqa: E402

DATA_ROOT = PROJECT_ROOT / "data"


def _generic_unit_count(records) -> int:
    return sum(1 for r in records if "generic' unit" in str(r.message))


def _bars(start, periods: int, freq: str = "1h") -> pd.DataFrame:
    """OHLCV-shaped frame; only `timestamp` matters to the guards under test."""
    ts = pd.date_range(start=start, periods=periods, freq=freq)
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": 1.0,
            "high": 1.0,
            "low": 1.0,
            "close": 1.0,
            "volume": 1.0,
        }
    )


class _StubFetcher(BaseFetcher):
    """Minimal concrete BaseFetcher for exercising `_gap_intervals` /
    `_assert_no_new_gap` directly. `_fetch_remote` is never called."""

    def __init__(self, tmp_dir, interval_seconds=3600):
        super().__init__(
            start_date="2024-01-01",
            end_date="2024-01-02",
            symbols=["BTCUSD"],
            interval_seconds=interval_seconds,
            localStorage=True,
            data_dir=str(tmp_dir),
        )

    def _fetch_remote(self, symbol, start, end):  # pragma: no cover
        raise AssertionError("no live fetch in these tests")

    def cache_key(self, symbol):
        return f"stub_{symbol}_1h"


# ---------------------------------------------------------------------------
# data_manager.py:208/209/217 -- _merge_asof_with_causality_guard
# ---------------------------------------------------------------------------


def test_merge_guard_emits_no_generic_unit_warning_and_identical_values():
    bars = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=3, freq="1h"),
            "close": [100.0, 101.0, 102.0],
        }
    )
    feed = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=3, freq="1h"),
            "aux": [1.5, 2.5, 3.5],
        }
    )
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        merged = _merge_asof_with_causality_guard(
            bars,
            feed,
            "aux",
            window_seconds=0,
            interval_seconds=3600,
            feed_label="test_feed",
        )
    assert _generic_unit_count(w) == 0
    assert merged.sort_values("timestamp")["aux"].tolist() == [1.5, 2.5, 3.5]


def test_merge_guard_boundary_equality_passes_violation_raises():
    """window_end == bar_end (window_seconds == interval_seconds) must pass --
    the docstring's explicit allowance. window_seconds one second larger must
    raise. This is the VALUE lock: a +-1s mutation at data_manager.py:208/209
    flips which side of the boundary either case lands on."""
    bars = pd.DataFrame({"timestamp": pd.to_datetime(["2024-01-01 00:00"]), "close": [1.0]})
    feed = pd.DataFrame({"timestamp": pd.to_datetime(["2024-01-01 00:00"]), "aux": [10.0]})
    interval_seconds = 3600

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        merged = _merge_asof_with_causality_guard(
            bars,
            feed,
            "aux",
            window_seconds=interval_seconds,
            interval_seconds=interval_seconds,
            feed_label="test_feed",
        )
    assert _generic_unit_count(w) == 0
    assert merged["aux"].iloc[0] == 10.0

    with warnings.catch_warnings(record=True) as w2:
        warnings.simplefilter("always")
        with pytest.raises(AuxFeedCausalityError, match="ends after bar"):
            _merge_asof_with_causality_guard(
                bars,
                feed,
                "aux",
                window_seconds=interval_seconds + 1,
                interval_seconds=interval_seconds,
                feed_label="test_feed",
            )
    assert _generic_unit_count(w2) == 0


# ---------------------------------------------------------------------------
# base_fetcher.py:262 -- BaseFetcher._inclusive_end
# ---------------------------------------------------------------------------


def test_inclusive_end_date_only_no_warning_exact_value():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = BaseFetcher._inclusive_end("2024-01-05")
    assert _generic_unit_count(w) == 0
    assert result == pd.Timestamp("2024-01-05 23:59:59.999000")


# ---------------------------------------------------------------------------
# base_fetcher.py:349/386 -- _gap_intervals / _assert_no_new_gap
# ---------------------------------------------------------------------------


def test_gap_intervals_no_warning_exact_spans(tmp_path):
    f = _StubFetcher(tmp_path, interval_seconds=3600)
    existing = _bars("2024-01-01 00:00", 3)  # -> 02:00
    combined = pd.concat(
        [existing, _bars("2024-01-01 10:00", 2)],
        ignore_index=True,
    )  # gap 03:00 -> 09:00

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        gaps = f._gap_intervals(combined["timestamp"])
    assert _generic_unit_count(w) == 0
    assert len(gaps) == 1
    start, end = gaps[0]
    assert start == pd.Timestamp("2024-01-01 03:00")
    assert end == pd.Timestamp("2024-01-01 09:00")

    with warnings.catch_warnings(record=True) as w2:
        warnings.simplefilter("always")
        with pytest.raises(FetchGapError) as exc:
            f._assert_no_new_gap("BTCUSD", existing, combined)
    assert _generic_unit_count(w2) == 0
    assert "7 bars" in str(exc.value)  # (09:00 - 03:00) / 1h + 1 = 7


# ---------------------------------------------------------------------------
# Static lock: ccxt_fetcher.py:192 (network-only) and base_fetcher.py:386
# (only reachable through a real gap) can't both be exercised by the runtime
# tests above -- an AST scan bans the construction outright, mirroring the
# house pattern in test_no_sealed_date_literals.py. Two shapes are banned:
# `pd.Timedelta(...)` (Attribute form) and a bare `Timedelta(...)` reachable
# via `from pandas import Timedelta` (Name form) -- the fix idiom swaps to
# `datetime.timedelta(...)`, so neither shape has any legitimate use here.
# ---------------------------------------------------------------------------


def _pd_timedelta_calls(source: str):
    """Yield lineno for every banned Timedelta(...) construction in `source`:
    `pd.Timedelta(...)` or a bare `Timedelta(...)`. Takes a source string
    (not a path) so the detection itself is unit-testable on a synthetic
    snippet, independent of the tree scan below."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (isinstance(func, ast.Attribute) and func.attr == "Timedelta") or (
            isinstance(func, ast.Name) and func.id == "Timedelta"
        ):
            yield node.lineno


@pytest.mark.parametrize(
    ("source", "expected_linenos"),
    [
        ("import pandas as pd\nx = pd.Timedelta(seconds=1)\n", [2]),
        ("from pandas import Timedelta\nx = Timedelta(seconds=1)\n", [2]),
        ("x = 1\n", []),
    ],
)
def test_pd_timedelta_calls_detects_both_construction_forms(source, expected_linenos):
    """Direct proof of the bare-name branch (and a regression guard on the
    pre-existing attribute branch): a synthetic `from pandas import
    Timedelta` snippet must be flagged the same as `pd.Timedelta(...)`."""
    assert list(_pd_timedelta_calls(source)) == expected_linenos


def test_data_tree_bans_pd_timedelta_construction():
    violations = []
    files_scanned = 0
    for path in sorted(DATA_ROOT.rglob("*.py")):
        files_scanned += 1
        source = path.read_text(encoding="utf-8")
        for lineno in _pd_timedelta_calls(source):
            violations.append(f"{path.relative_to(PROJECT_ROOT)}:{lineno}")

    assert files_scanned >= 4, (
        f"scan reached only {files_scanned} files under data/ -- exclusion "
        f"or checkout layout emptied it, so a green result would be vacuous"
    )
    assert not violations, (
        "Timedelta(...) construction found in data/ (banned -- numpy "
        "generic-unit deprecation, backlog 3c; use datetime.timedelta(...) "
        "instead):\n  " + "\n  ".join(violations)
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
