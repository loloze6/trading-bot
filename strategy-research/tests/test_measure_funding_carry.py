"""Seal-safe read routing for measure_funding_carry (CUL-203).

The standalone carry-measurement CLI read {SYMBOL}_funding_8h.csv directly with
pd.read_csv, bypassing the seal guard. It now routes through
seal_safe_cache.read_cache_csv with end=WINDOW_END (request-window mode): the CSV
physically extends past the seal, so a window whose end reaches the holdout is
refused before the read. WINDOW_END is 2023-12-31 (pre-seal), so the committed
measurement is byte-identical. Sealed-era dates below are DERIVED from the policy
(the tests/ tree is excluded from the literal scan anyway).
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

import measure_funding_carry as mfc  # noqa: E402
from seal_safe_cache import SealedDataError, _holdout_bounds, read_cache_csv  # noqa: E402

_LO, _HI = _holdout_bounds()
_INSEAL = _LO + pd.Timedelta(59, unit="D")     # a day inside the seal


def _write_funding(path, *stamps):
    path.write_text(
        "timestamp,funding_rate\n" + "".join(f"{s},0.0001\n" for s in stamps),
        encoding="utf-8",
    )


def _hash(df):
    return hashlib.sha256(df.to_csv(index=True).encode("utf-8")).hexdigest()


def test_load_bounded_refuses_a_window_end_reaching_the_seal(tmp_path, monkeypatch):
    """Mutation: revert load_bounded to raw pd.read_csv -> the clean in-window row
    bounds normally and no SealedDataError is raised -> this test dies."""
    _write_funding(tmp_path / "BTCUSDT_funding_8h.csv", "2020-06-01 00:00:00")
    monkeypatch.setattr(mfc, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(mfc, "WINDOW_END", _INSEAL)
    with pytest.raises(SealedDataError):
        mfc.load_bounded("BTCUSDT")


@pytest.mark.skipif(
    not os.path.exists(os.path.join(mfc.DATA_DIR, "BTCUSDT_funding_8h.csv")),
    reason="BTCUSDT_funding_8h cache absent",
)
def test_load_bounded_read_is_bit_identical_on_the_committed_window():
    path = os.path.join(mfc.DATA_DIR, "BTCUSDT_funding_8h.csv")
    guarded = read_cache_csv(path, end=mfc.WINDOW_END, usecols=["timestamp", "funding_rate"])
    raw = pd.read_csv(path, usecols=["timestamp", "funding_rate"])
    assert _hash(guarded) == _hash(raw) and guarded.equals(raw)
    # and the full load_bounded still returns rows clamped to the pre-seal window
    _raw, bounded, _n, _lo, _hi = mfc.load_bounded("BTCUSDT")
    assert not bounded.empty
    assert bounded["timestamp"].dt.normalize().max() <= mfc.WINDOW_END
