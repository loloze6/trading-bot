"""read_cache_csv must FAIL CLOSED on a non-naive / exotic `end` (CUL-203 F1).

The red-team showed the loader failed OPEN: `_assert_request_window_unsealed`
swallowed parse/compare errors and returned, and the content backstop was gated
on `end is None` -- so a tz-aware Timestamp, an epoch int, or an exotic object as
`end` returned the synthetic cache's sealed rows with no check. These tests pin
every shape from that list, the tz-aware normalisation, the always-on content
backstop, and the fail-loud-without-a-timestamp-column contract. Seal-relative
dates are DERIVED from the policy (the tests/ tree is excluded from the scan).
"""
import datetime
import os
import sys

import pandas as pd
import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.join(os.path.dirname(_HERE), "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

from seal_safe_cache import (  # noqa: E402
    SealedDataError,
    _assert_returned_frame_unsealed,
    _holdout_bounds,
    read_cache_csv,
)

_LO, _HI = _holdout_bounds()
_INSEAL_DAY = (_LO + datetime.timedelta(days=59)).strftime("%Y-%m-%d")
_INSEAL_TS = _INSEAL_DAY + " 00:00:00"
_PRESEAL_TS = (_LO - datetime.timedelta(days=2000)).strftime("%Y-%m-%d %H:%M:%S")
_PRESEAL_DAY = (_LO - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

_TZ_SEALED = pd.Timestamp(_INSEAL_DAY).tz_localize("UTC")           # tz-aware, inside seal
_MS_EPOCH = int(pd.Timestamp(_INSEAL_DAY).value // 10**6)           # ms epoch (int -> ambiguous)
_SEC_EPOCH = int(_MS_EPOCH // 1000)                                 # sec epoch (int -> ambiguous)
_EXOTIC = [
    ("tz_aware_sealed", _TZ_SEALED),
    ("ms_epoch_int", _MS_EPOCH),
    ("sec_epoch_int", _SEC_EPOCH),
    ("object", object()),
    ("nan", float("nan")),
    ("empty_list", []),
    ("bool", True),
]


def _write_funding(path, *stamps):
    path.write_text(
        "timestamp,funding_rate\n" + "".join(f"{s},0.0001\n" for s in stamps),
        encoding="utf-8",
    )


@pytest.mark.parametrize("bad_end", [e[1] for e in _EXOTIC], ids=[e[0] for e in _EXOTIC])
def test_read_cache_csv_fails_closed_on_exotic_end(tmp_path, bad_end):
    """A synthetic cache holding a genuine sealed row: an exotic `end` must RAISE,
    never fail open and hand back the sealed row."""
    p = tmp_path / "x_funding_8h.csv"
    _write_funding(p, _PRESEAL_TS, _INSEAL_TS)
    with pytest.raises(SealedDataError):
        read_cache_csv(p, end=bad_end, usecols=["timestamp", "funding_rate"])


def test_read_cache_csv_tz_aware_pre_seal_end_passes(tmp_path):
    """A tz-aware PRE-seal end is normalised and passes (handled, not denied)."""
    p = tmp_path / "x_funding_8h.csv"
    _write_funding(p, _PRESEAL_TS)
    read_cache_csv(p, end=pd.Timestamp(_PRESEAL_DAY).tz_localize("UTC"),
                   usecols=["timestamp", "funding_rate"])   # no raise


def test_content_backstop_fires_with_end_given():
    """The content check refuses a sealed row in the kept (<= end) portion even
    when `end` is provided -- not gated on `end is None`. Mutation: restore the
    `end is None` gate and this dies."""
    df = pd.DataFrame({"timestamp": [_PRESEAL_TS, _INSEAL_TS], "v": [1, 2]})
    with pytest.raises(SealedDataError):
        _assert_returned_frame_unsealed(
            df, end=pd.Timestamp(_INSEAL_TS), timestamp_col="timestamp", name="x")


def test_read_cache_csv_fails_loud_without_timestamp_column(tmp_path):
    """A cache lacking the timestamp column must RAISE, not silently no-op."""
    p = tmp_path / "headerless.csv"
    p.write_text("epoch,price\n1000000,100\n", encoding="utf-8")
    with pytest.raises(SealedDataError, match="cannot verify"):
        read_cache_csv(p)


def test_read_cache_csv_accepts_explicit_timestamp_col(tmp_path):
    """The caller may name a different timestamp column; a sealed row under it is
    still refused, a pre-seal one passes."""
    clean = tmp_path / "named_clean.csv"
    clean.write_text(f"ts,price\n{_PRESEAL_TS},100\n", encoding="utf-8")
    assert len(read_cache_csv(clean, timestamp_col="ts")) == 1
    sealed = tmp_path / "named_sealed.csv"
    sealed.write_text(f"ts,price\n{_INSEAL_TS},100\n", encoding="utf-8")
    with pytest.raises(SealedDataError):
        read_cache_csv(sealed, timestamp_col="ts")
