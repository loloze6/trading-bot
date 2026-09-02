"""Range-check seal guard on the READ path (CUL-203).

`_assert_no_sealed_rows` (already shipped) inspects the rows a fetch RETURNS. It
is blind to the case the .gitignore seal-exclusion comment flags as still open:
a request whose WINDOW reaches into the holdout but whose cache happens to carry
no rows there (a gap, a short cache) comes back clean, and the caller is handed a
silently-short series it believes covered the sealed window. `.gitignore`'s own
note: "no range check exists anywhere today that would catch it."

`_assert_request_window_unsealed` closes that: it refuses on the requested RANGE,
before any candle (or aux feed) is read, keyed on BOTH ends of the seal so
post-seal windows still pass. The seal start/end are DERIVED from
campaign_data_policy.yaml via `_holdout_bounds()` — never a literal here, per
`tests/test_no_sealed_date_literals.py`. Sealed-era literals below are test
fixtures (the `tests/` tree is excluded from that scan) that prove the guard
fires; they are read to derive the boundary, not hardcoded into it.
"""
import datetime
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import data.data_manager as dm  # noqa: E402
from data.data_manager import (  # noqa: E402
    SealedDataError,
    _assert_request_window_unsealed,
    _holdout_bounds,
)

# Boundary instants derived from the policy, not restated.
_LO, _HI = _holdout_bounds()                       # [first sealed, first-after-seal)
_LAST_SEALED = _HI - datetime.timedelta(days=1)     # inclusive upper end of the seal


def _frame(*stamps):
    return pd.DataFrame({"timestamp": [pd.Timestamp(s) for s in stamps],
                         "close": [1.0] * len(stamps)})


# --------------------------------------------------------------------------- #
# Pure-function behaviour
# --------------------------------------------------------------------------- #
def test_window_overlapping_the_seal_is_refused():
    """A window straddling the seal start raises — the core refusal."""
    with pytest.raises(SealedDataError, match="overlaps the"):
        _assert_request_window_unsealed(_LO - datetime.timedelta(days=180),
                                        _LO + datetime.timedelta(days=60), "BTCUSDT")


def test_window_entirely_inside_the_seal_is_refused():
    with pytest.raises(SealedDataError):
        _assert_request_window_unsealed(_LO, _LAST_SEALED, "BTCUSDT")


def test_pre_seal_window_passes():
    """The reference-simulate shape: a window ending before the seal is a no-op.
    This is the byte-identity anchor — the default read path is unchanged."""
    _assert_request_window_unsealed(_LO - datetime.timedelta(days=600),
                                    _LO - datetime.timedelta(days=1), "BTCUSDT")


def test_post_seal_window_passes():
    """A window that begins AFTER the seal ends must pass — data is usable again.
    Guards against a naive `end < seal_start` check that would refuse the whole
    future; the guard is keyed on both ends of the closed seal."""
    _assert_request_window_unsealed(_HI, _HI + datetime.timedelta(days=60), "BTCUSDT")


# --------------------------------------------------------------------------- #
# Boundary — a one-day shift either way must break a test
# --------------------------------------------------------------------------- #
def test_end_on_last_pre_seal_instant_passes():
    """End at 23:00 the day before the seal (still pre-seal) must NOT raise.
    If `lo` shifted one day earlier, this bar would fall inside and this fails."""
    end = _LO - datetime.timedelta(hours=1)
    _assert_request_window_unsealed(_LO - datetime.timedelta(days=90), end, "BTCUSDT")


def test_end_exactly_at_seal_start_is_refused():
    """End exactly on the first sealed instant must raise. If `lo` shifted one
    day later, or `>=` weakened to `>`, this stops firing and this fails."""
    with pytest.raises(SealedDataError):
        _assert_request_window_unsealed(_LO - datetime.timedelta(days=90), _LO, "BTCUSDT")


def test_start_exactly_at_first_post_seal_instant_passes():
    """Start exactly at `hi` (first instant after the seal) must NOT raise. If
    `hi` shifted one day later, or `<` weakened to `<=`, this window would be
    judged to overlap and this fails."""
    _assert_request_window_unsealed(_HI, _HI + datetime.timedelta(days=30), "BTCUSDT")


# --------------------------------------------------------------------------- #
# Escape + best-effort delegation
# --------------------------------------------------------------------------- #
def test_absent_none_bound_is_permissive():
    """A genuinely ABSENT (None) bound is left to the content backstop — the
    engine call path always supplies both bounds, so this only spares a caller
    that omits one."""
    _assert_request_window_unsealed(None, _LO + datetime.timedelta(days=10), "BTCUSDT")
    _assert_request_window_unsealed(_LO - datetime.timedelta(days=10), None, "BTCUSDT")


def test_present_but_non_date_bound_is_denied():
    """A PRESENT bound that is not an unambiguous naive date RAISES (deny), never
    silently returns — the CUL-203 fail-open on tz-aware / epoch / exotic `end`
    (red-team F1). Epoch ints are ambiguous (pandas reads them as nanoseconds ->
    a 1970 date that silently passes the seal), so they are refused too."""
    good_start = _LO - datetime.timedelta(days=10)
    for bad in ("not-a-date", 1767225600000, 1767225600, object(), float("nan"), [], True):
        with pytest.raises(SealedDataError):
            _assert_request_window_unsealed(good_start, bad, "BTCUSDT")


def test_tz_aware_end_is_normalised_and_compared():
    """A tz-aware `end` must be normalised to UTC-naive and compared correctly:
    a tz-aware SEALED end refuses; a tz-aware PRE-seal end passes."""
    with pytest.raises(SealedDataError):
        _assert_request_window_unsealed(
            _LO - datetime.timedelta(days=10),
            pd.Timestamp(_LO + datetime.timedelta(days=30)).tz_localize("UTC"), "BTCUSDT")
    _assert_request_window_unsealed(
        _LO - datetime.timedelta(days=400),
        pd.Timestamp(_LO - datetime.timedelta(days=1)).tz_localize("UTC"), "BTCUSDT")  # no raise


def test_fetch_historical_data_honours_allow_sealed(monkeypatch):
    """allow_sealed=True bypasses BOTH the request guard and the content guard —
    the single-use holdout evaluation must stay possible, visibly at the call site."""
    class _StubFetcher:
        def __init__(self, *a, **k):
            pass

        def get_data(self):
            return {"BTCUSDT": _frame(_LO)}   # a sealed row

        def validate_data_continuity(self, _symbol):
            return True, []

    monkeypatch.setattr(dm, "HistoricalDataFetcher", _StubFetcher)
    mgr = dm.DataManager.__new__(dm.DataManager)
    mgr.interval_seconds = 3600

    got = dm.DataManager.fetch_historical_data(
        mgr, "BTCUSDT", str(_LO.date()), str(_LAST_SEALED.date()), allow_sealed=True)
    assert len(got) == 1


# --------------------------------------------------------------------------- #
# Integration through fetch_historical_data
# --------------------------------------------------------------------------- #
def test_sealed_request_refused_before_the_fetch_runs(monkeypatch):
    """The value the content guard cannot provide: a sealed-intent request whose
    cache carries NO sealed rows is still refused, and get_data() never runs."""
    calls = {"get_data": 0}

    class _StubFetcher:
        def __init__(self, *a, **k):
            pass

        def get_data(self):
            calls["get_data"] += 1
            return {"BTCUSDT": _frame("2020-01-01")}   # clean frame, no sealed rows

        def validate_data_continuity(self, _symbol):
            return True, []

    monkeypatch.setattr(dm, "HistoricalDataFetcher", _StubFetcher)
    mgr = dm.DataManager.__new__(dm.DataManager)
    mgr.interval_seconds = 3600

    with pytest.raises(SealedDataError):
        dm.DataManager.fetch_historical_data(
            mgr, "BTCUSDT", str((_LO - datetime.timedelta(days=90)).date()),
            str((_LO + datetime.timedelta(days=30)).date()))
    assert calls["get_data"] == 0, "request guard must refuse before the fetch"


def test_content_guard_still_backstops_a_nonoverlapping_request(monkeypatch):
    """The request guard preempts overlapping windows, so this pins that the
    RETURNED-rows guard still fires and propagates when a fetch overshoots on a
    window the request guard judged clean — keeping that path covered."""
    class _StubFetcher:
        def __init__(self, *a, **k):
            pass

        def get_data(self):
            return {"BTCUSDT": _frame(_LO + datetime.timedelta(days=5))}  # overshoot into seal

        def validate_data_continuity(self, _symbol):
            return True, []

    monkeypatch.setattr(dm, "HistoricalDataFetcher", _StubFetcher)
    mgr = dm.DataManager.__new__(dm.DataManager)
    mgr.interval_seconds = 3600

    # A pre-seal request window: the request guard passes, the content guard bites.
    with pytest.raises(SealedDataError):
        dm.DataManager.fetch_historical_data(
            mgr, "BTCUSDT", str((_LO - datetime.timedelta(days=90)).date()),
            str((_LO - datetime.timedelta(days=1)).date()))
