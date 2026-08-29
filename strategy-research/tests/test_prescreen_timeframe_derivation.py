"""
Prescreen data loading: DERIVE a coarser timeframe, never demand a file per one.

Guards the run_060 failure of 2026-08-28. The prescreen mapped timeframe
straight to a filename, so a 4h run demanded BTCUSDT_4h.csv, did not find it,
silently skipped BOTH symbols, and still emitted `Route=no_signal_artifact`
with active_n=0 -- while BTCUSDT_1h.csv sat on disk spanning 2018-01-01 to
2026-07-05 and covering the window completely.

Two separate defects, tested separately here:
  A. the loader could not derive 4h from a 1h cache (the engine's CandleBuilder
     has always done exactly that, on both the live and backtest paths);
  B. losing every symbol produced a VERDICT instead of an error.
"""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))

import prescreen_signal as ps  # noqa: E402


def _write_csv(path, start, periods, freq_seconds):
    ts = pd.date_range(start, periods=periods, freq=f"{freq_seconds}s")
    pd.DataFrame(
        {
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "open": [100.0 + i for i in range(periods)],
            "high": [101.0 + i for i in range(periods)],
            "low": [99.0 + i for i in range(periods)],
            "close": [100.5 + i for i in range(periods)],
            "volume": [1.0] * periods,
        }
    ).to_csv(path, index=False)


@pytest.fixture
def local_data(tmp_path, monkeypatch):
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    return tmp_path


# ---------------------------------------------------------------------------
# A. Derivation
# ---------------------------------------------------------------------------


def test_derives_4h_from_a_1h_cache(local_data):
    """The exact run_060 case: no _4h.csv, a _1h.csv that covers the window."""
    _write_csv(local_data / "FOOUSDT_1h.csv", "2020-01-01", 24 * 10, 3600)
    assert not (local_data / "FOOUSDT_4h.csv").exists()

    df = ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-11", "4h")
    assert len(df) == 6 * 10, "10 days at 6 bars/day"
    assert list(df.columns) == ["timestamp", "open", "high", "low", "close", "volume"]


def test_derived_bars_use_the_engines_own_aggregation(local_data):
    """OHLCV must aggregate first/max/min/last/sum with closed+label='left',
    matching core/backtester.py:296 -- a prescreen bar and a backtest bar for
    the same window have to be the same bar."""
    _write_csv(local_data / "FOOUSDT_1h.csv", "2020-01-01", 8, 3600)
    df = ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-02", "4h")

    first = df.iloc[0]
    assert first["open"] == 100.0  # first of bars 0-3
    assert first["high"] == 104.0  # max
    assert first["low"] == 99.0  # min
    assert first["close"] == 103.5  # last of bars 0-3
    assert first["volume"] == 4.0  # sum
    assert str(first["timestamp"]) == "2020-01-01 00:00:00"  # label='left'


def test_an_exact_cache_still_wins_over_derivation(local_data):
    """Bit-identity: when the exact file exists nothing changes, so every
    archived 1h run reproduces."""
    _write_csv(local_data / "FOOUSDT_1h.csv", "2020-01-01", 24, 3600)
    df = ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-02", "1h")
    assert len(df) == 24
    assert df.iloc[0]["open"] == 100.0


@pytest.mark.parametrize(
    "target,expected_bars",
    [
        ("2h", 12 * 5),
        ("4h", 6 * 5),
        ("6h", 4 * 5),
        ("8h", 3 * 5),
        ("12h", 2 * 5),
        ("1d", 5),
    ],
)
def test_derives_any_dividing_timeframe(local_data, target, expected_bars):
    """Not just 4h -- the point of the fix is that the NEXT timeframe works too."""
    _write_csv(local_data / "FOOUSDT_1h.csv", "2020-01-01", 24 * 5, 3600)
    df = ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-06", target)
    assert len(df) == expected_bars


def test_picks_the_coarsest_cache_that_divides(local_data):
    """With 1m and 1h both present, a 4h request must read the 1h file.
    Verified by making the two caches disagree: the 1m file is priced at 1000
    and would be visible in the output if it had been chosen."""
    _write_csv(local_data / "FOOUSDT_1h.csv", "2020-01-01", 24, 3600)
    ts = pd.date_range("2020-01-01", periods=24 * 60, freq="60s")
    pd.DataFrame(
        {
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "open": 1000.0,
            "high": 1000.0,
            "low": 1000.0,
            "close": 1000.0,
            "volume": 1.0,
        }
    ).to_csv(local_data / "FOOUSDT_1m.csv", index=False)

    _, src = ps._resolve_ohlcv_source("FOOUSDT", "4h")
    assert src == "1h"
    df = ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-02", "4h")
    assert df.iloc[0]["open"] == 100.0, "came from the 1h cache, not the 1m one"


def test_non_ohlcv_siblings_are_not_mistaken_for_caches(local_data):
    """FOOUSDT_funding_8h.csv must never be treated as an 8h OHLCV cache.
    Excluded structurally (funding_8h does not parse as a timeframe), not by a
    blocklist that the next feed name would slip past."""
    _write_csv(local_data / "FOOUSDT_1h.csv", "2020-01-01", 24, 3600)
    (local_data / "FOOUSDT_funding_8h.csv").write_text(
        "timestamp,rate\n", encoding="utf-8"
    )
    assert "funding_8h" not in ps._available_cached_timeframes("FOOUSDT")
    _, src = ps._resolve_ohlcv_source("FOOUSDT", "8h")
    assert src == "1h"


def test_refuses_a_source_that_does_not_divide_evenly(local_data):
    """A 4h bar built from 90m rows would be silently misaligned. Refuse."""
    _write_csv(local_data / "FOOUSDT_90m.csv", "2020-01-01", 100, 5400)
    with pytest.raises(FileNotFoundError, match="divides"):
        ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-06", "4h")


def test_refuses_when_only_a_coarser_cache_exists(local_data):
    """1d cannot be disaggregated into 4h. Never invent bars."""
    _write_csv(local_data / "FOOUSDT_1d.csv", "2020-01-01", 30, 86400)
    with pytest.raises(FileNotFoundError):
        ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-06", "4h")


def test_error_names_what_is_actually_on_disk(local_data):
    """The original message named only the missing file, which is why the same
    diagnosis had to be made twice. It must say what IS available."""
    _write_csv(local_data / "FOOUSDT_1d.csv", "2020-01-01", 30, 86400)
    with pytest.raises(FileNotFoundError) as e:
        ps._load_ohlcv("FOOUSDT", "2020-01-01", "2020-01-06", "4h")
    assert "1d" in str(e.value)


# ---------------------------------------------------------------------------
# B. Zero usable data is an ERROR, not a route
# ---------------------------------------------------------------------------


def _minimal_run_inputs(tmp_path, symbols):
    cfg = tmp_path / "candidate_strategy_config.json"
    cfg.write_text(
        json.dumps({"aux_feeds": [], "regime_detector": {}, "strategies": {}}),
        encoding="utf-8",
    )
    proto = tmp_path / "p.json"
    proto.write_text(
        json.dumps(
            {
                "timeframe": "4h",
                "symbols": symbols,
                "windows": [{"test": {"start": "2020-01-01", "end": "2020-01-06"}}],
            }
        ),
        encoding="utf-8",
    )
    return cfg, proto


def test_no_usable_symbol_raises_rather_than_routing(local_data, tmp_path):
    """run_060 emitted Route=no_signal_artifact and recorded a trial after
    loading zero bars. 'the signal never activated on this data' and 'no data
    was loaded' are different claims and must not share an output."""
    cfg, proto = _minimal_run_inputs(tmp_path, ["FOOUSDT"])
    with pytest.raises(RuntimeError, match="NO usable data"):
        ps.run_prescreen(
            str(cfg), str(proto), run_id="test_run", out_dir=tmp_path / "out"
        )


def test_the_message_names_why_each_symbol_was_lost(local_data, tmp_path):
    cfg, proto = _minimal_run_inputs(tmp_path, ["FOOUSDT", "BARUSDT"])
    with pytest.raises(RuntimeError) as e:
        ps.run_prescreen(
            str(cfg), str(proto), run_id="test_run", out_dir=tmp_path / "out"
        )
    assert "FOOUSDT" in str(e.value) and "BARUSDT" in str(e.value)
