"""Seal guard on prescreen's cache reads (CUL-203).

prescreen_signal's three cache loaders (_load_funding_rate, _load_fear_greed,
_load_ohlcv) read holdout-carrying local_data caches and window them. Each now
asserts the windowed frame carries no holdout row (data_manager._assert_no_sealed
_rows, the one shared seal definition, re-exported via seal_safe_cache). The
biting tests point _LOCAL_DATA at a temp cache holding one sealed row and read a
window that reaches it; the bit-identity tests prove the guard is a non-mutating
no-op on a train window (guarded == the same call with the guard stubbed out).
Sealed-era dates are DERIVED from the policy.
"""
import hashlib
import os
import sys

import pandas as pd
import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.join(os.path.dirname(_HERE), "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import prescreen_signal as ps  # noqa: E402
from seal_safe_cache import SealedDataError, _holdout_bounds  # noqa: E402

_LO, _HI = _holdout_bounds()
_PRE = (_LO - pd.Timedelta(90, unit="D")).strftime("%Y-%m-%d")
_POST = (_LO + pd.Timedelta(90, unit="D")).strftime("%Y-%m-%d")     # exclusive end, past the seal
_INSEAL_DAY = (_LO + pd.Timedelta(30, unit="D")).strftime("%Y-%m-%d")
_INSEAL_TS = _INSEAL_DAY + " 00:00:00"
_FG_RAW = (_LO - pd.Timedelta(1, unit="D")).strftime("%Y-%m-%d")    # +1d shift -> first sealed day
_TR_START, _TR_END = "2020-01-01", "2021-01-01"                     # pre-seal train window

_NOOP = staticmethod(lambda *a, **k: None)


def _hash(df):
    return hashlib.sha256(df.to_csv(index=True).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# biting: a window reaching the seal is refused (per loader)
# --------------------------------------------------------------------------- #
def test_load_funding_rate_refuses_a_sealed_window(tmp_path, monkeypatch):
    (tmp_path / "BTCUSDT_funding_8h.csv").write_text(
        f"timestamp,funding_rate\n{_INSEAL_TS},0.0001\n", encoding="utf-8")
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    with pytest.raises(SealedDataError):
        ps._load_funding_rate("BTCUSDT", _PRE, _POST)


def test_load_fear_greed_refuses_a_sealed_window(tmp_path, monkeypatch):
    # raw row on the day BEFORE the seal; the loader's +1d shift lands it on the
    # first sealed decision bar.
    (tmp_path / "fear_greed_daily.csv").write_text(
        f"timestamp,fear_greed\n{_FG_RAW} 00:00:00,50\n", encoding="utf-8")
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    with pytest.raises(SealedDataError):
        ps._load_fear_greed(_PRE, _POST)


def test_load_ohlcv_refuses_a_sealed_window(tmp_path, monkeypatch):
    (tmp_path / "SEALED_1h.csv").write_text(
        f"timestamp,open,high,low,close,volume\n{_INSEAL_TS},1,1,1,1,1\n", encoding="utf-8")
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    with pytest.raises(SealedDataError):
        ps._load_ohlcv("SEALED", _PRE, _POST, "1h")


# --------------------------------------------------------------------------- #
# bit-identity: guard is a non-mutating no-op on a train window
# --------------------------------------------------------------------------- #
def _has(name):
    return os.path.exists(os.path.join(ps._LOCAL_DATA, name))


@pytest.mark.skipif(not _has("BTCUSDT_funding_8h.csv"), reason="funding cache absent")
def test_funding_guard_is_noop_on_train_window(monkeypatch):
    guarded = ps._load_funding_rate("BTCUSDT", _TR_START, _TR_END)
    monkeypatch.setattr(ps, "_assert_no_sealed_rows", lambda *a, **k: None)
    unguarded = ps._load_funding_rate("BTCUSDT", _TR_START, _TR_END)
    assert _hash(guarded) == _hash(unguarded)


@pytest.mark.skipif(not _has("fear_greed_daily.csv"), reason="fear_greed cache absent")
def test_fear_greed_guard_is_noop_on_train_window(monkeypatch):
    guarded = ps._load_fear_greed(_TR_START, _TR_END)
    monkeypatch.setattr(ps, "_assert_no_sealed_rows", lambda *a, **k: None)
    unguarded = ps._load_fear_greed(_TR_START, _TR_END)
    assert _hash(guarded) == _hash(unguarded)


@pytest.mark.skipif(not _has("BTCUSDT_1h.csv"), reason="BTCUSDT_1h cache absent")
def test_ohlcv_guard_is_noop_on_train_window(monkeypatch):
    guarded = ps._load_ohlcv("BTCUSDT", _TR_START, _TR_END, "1h")
    monkeypatch.setattr(ps, "_assert_no_sealed_rows", lambda *a, **k: None)
    unguarded = ps._load_ohlcv("BTCUSDT", _TR_START, _TR_END, "1h")
    assert _hash(guarded) == _hash(unguarded)
