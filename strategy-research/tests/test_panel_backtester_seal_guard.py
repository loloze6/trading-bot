"""panel_backtester.load_ohlcv routes through the shared seal-safe loader (CUL-203).

load_ohlcv now reads via seal_safe_cache.read_cache_csv, so a cache carrying a
holdout row is refused (content mode) and a window whose end reaches the seal is
refused (request-window mode). Minimal, self-contained: imports only
panel_backtester and the seal exception; the sealed date is DERIVED from the
policy, never a literal.
"""
import os
import sys

import pandas as pd
import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.join(os.path.dirname(_HERE), "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import panel_backtester as pb  # noqa: E402
from seal_safe_cache import SealedDataError, _holdout_bounds  # noqa: E402

_LO, _HI = _holdout_bounds()
_INSEAL = (_LO + pd.Timedelta(30, unit="D")).strftime("%Y-%m-%d %H:%M:%S")
_INSEAL_DAY = (_LO + pd.Timedelta(30, unit="D")).strftime("%Y-%m-%d")
_PRESEAL = (_LO - pd.Timedelta(2000, unit="D")).strftime("%Y-%m-%d %H:%M:%S")


def _write(path, *stamps):
    path.write_text(
        "timestamp,open,high,low,close,volume\n"
        + "".join(f"{s},1,1,1,1,1\n" for s in stamps),
        encoding="utf-8",
    )


def test_load_ohlcv_refuses_a_cache_carrying_a_sealed_row(tmp_path):
    p = tmp_path / "SEALED_1h.csv"
    _write(p, _PRESEAL, _INSEAL)
    with pytest.raises(SealedDataError):
        pb.load_ohlcv(str(p))


def test_load_ohlcv_refuses_a_sealed_end_window(tmp_path):
    p = tmp_path / "SPOT_1h.csv"
    _write(p, _PRESEAL)                       # clean content; refusal is on the END
    with pytest.raises(SealedDataError):
        pb.load_ohlcv(str(p), end=_INSEAL_DAY)


def test_load_ohlcv_pre_seal_cache_passes(tmp_path):
    p = tmp_path / "CLEAN_1h.csv"
    _write(p, _PRESEAL)
    assert not pb.load_ohlcv(str(p)).empty   # no raise, returns rows
