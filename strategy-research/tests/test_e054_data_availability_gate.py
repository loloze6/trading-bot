"""
E-054 Layer 2 (data_availability_gate.py) unit + integration tests.

Sandboxing note: `check_price_window`/`check_aux_feed_window` ultimately call
into `data.data_manager.DataManager` / `data.feed_registry.FEED_REGISTRY`,
whose local-cache path is computed internally from `data_manager.py`'s own
file location (`trading-bot/local_data/`) -- it is not an injectable
parameter. The integration tests below write a small synthetic CSV directly
under that real directory using a symbol name (`ZZZ_E054_TEST*`) that cannot
collide with any real market symbol, and remove it in a fixture teardown --
mirroring exactly how the real fetch path is used in production rather than
monkeypatching internals. Every other test here is a pure-function test with
no filesystem/network dependency at all.
"""
import datetime
import json
import os
import sys
from pathlib import Path

import pandas as pd
import pytest

_TOOLS = str(Path(__file__).resolve().parent.parent / "tools")
_TBOT = str(Path(__file__).resolve().parent.parent.parent / "trading-bot")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import data_availability_gate as dag  # noqa: E402


# ---------------------------------------------------------------------------
# resolve_exchange -- Option Y precedence (tools/run_protocol.py parity)
# ---------------------------------------------------------------------------

def test_resolve_exchange_cli_override_wins():
    assert dag.resolve_exchange({"exchange": "kraken"}, cli_override="binance") == "binance"


def test_resolve_exchange_protocol_field_used_when_no_override():
    assert dag.resolve_exchange({"exchange": "kraken"}, cli_override=None) == "kraken"


def test_resolve_exchange_defaults_to_binance():
    assert dag.resolve_exchange({}, cli_override=None) == "binance"


def test_resolve_exchange_explicit_empty_override_preserved_not_swallowed():
    """Option Y is resolved with `is not None`, not truthiness -- an
    explicitly empty override must not silently fall through to the
    protocol field or 'binance' (mirrors run_protocol.py's own reasoning)."""
    assert dag.resolve_exchange({"exchange": "kraken"}, cli_override="") == ""


# ---------------------------------------------------------------------------
# _missing_fraction / classify_missing_fraction
# ---------------------------------------------------------------------------

def _bars(start: str, end: str, interval_seconds: int, skip_indices=frozenset()) -> pd.DataFrame:
    """Build a fully-populated timestamp series on the grid, optionally
    dropping specific bar indices to create controlled gaps."""
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    n = int((end_ts - start_ts).total_seconds() // interval_seconds)
    rows = [start_ts + pd.Timedelta(seconds=i * interval_seconds) for i in range(n) if i not in skip_indices]
    return pd.DataFrame({"timestamp": rows})


def test_missing_fraction_fully_populated_is_zero():
    df = _bars("2024-01-01", "2024-01-02", 3600)  # 24 hourly bars
    start = pd.Timestamp("2024-01-01").to_pydatetime()
    end = pd.Timestamp("2024-01-02").to_pydatetime()
    assert dag._missing_fraction(df, start, end, 3600) == 0.0


def test_missing_fraction_empty_frame_is_one():
    df = pd.DataFrame({"timestamp": []})
    start = pd.Timestamp("2024-01-01").to_pydatetime()
    end = pd.Timestamp("2024-01-02").to_pydatetime()
    assert dag._missing_fraction(df, start, end, 3600) == 1.0


def test_missing_fraction_single_internal_gap_matches_expected_ratio():
    df = _bars("2024-01-01", "2024-01-02", 3600, skip_indices={5})  # drop 1 of 24 bars
    start = pd.Timestamp("2024-01-01").to_pydatetime()
    end = pd.Timestamp("2024-01-02").to_pydatetime()
    frac = dag._missing_fraction(df, start, end, 3600)
    assert frac == pytest.approx(1 / 24, rel=1e-6)


def test_missing_fraction_trailing_shortfall_counted():
    # Drop the last 3 of 24 bars -- a trailing boundary shortfall, not an
    # internal gap.
    df = _bars("2024-01-01", "2024-01-02", 3600, skip_indices={21, 22, 23})
    start = pd.Timestamp("2024-01-01").to_pydatetime()
    end = pd.Timestamp("2024-01-02").to_pydatetime()
    frac = dag._missing_fraction(df, start, end, 3600)
    assert frac == pytest.approx(3 / 24, rel=1e-6)


def test_missing_fraction_millisecond_serialization_noise_never_manufactures_a_gap():
    """Regression: BTCUSDT_funding_8h.csv / ETHUSDT_funding_8h.csv (real
    caches inspected 2026-09-11) carry a literal '.001000'ms tail on some
    timestamps -- a writer artifact, not a missing observation. Before the
    epsilon guard, EVERY window of a fully-available series classified as
    'refine' (missing_fraction ~1e-8), never 'validate'."""
    start = pd.Timestamp("2024-01-01")
    end = pd.Timestamp("2024-02-01")
    n = int((end - start).total_seconds() // 28800)
    rows = [start + pd.Timedelta(seconds=i * 28800) for i in range(n)]
    # Perturb every timestamp by exactly 1ms, matching the observed artifact.
    rows = [r + pd.Timedelta(milliseconds=1) for r in rows]
    df = pd.DataFrame({"timestamp": rows})
    frac = dag._missing_fraction(df, start.to_pydatetime(), end.to_pydatetime(), 28800)
    assert frac == 0.0
    assert dag.classify_missing_fraction(frac) == "validate"


@pytest.mark.parametrize("fraction,expected", [
    (0.0, "validate"),
    (0.01, "refine"),
    (0.05, "refine"),
    (0.050001, "decline"),
    (1.0, "decline"),
])
def test_classify_missing_fraction_thresholds(fraction, expected):
    assert dag.classify_missing_fraction(fraction, gap_tolerance=0.05) == expected


# ---------------------------------------------------------------------------
# Layer 1 precheck (pure function, inline fixture -- not the real 500-line file)
# ---------------------------------------------------------------------------

_LAYER1_FIXTURE = {
    "venues": {
        "binance": {
            "spot": {
                "timeframes": {"available": ["1h", "4h"]},
                "symbols": {"earliest_ohlcv_utc": {"BTCUSDT": "2017-08-17T00:00:00Z"}},
            },
        },
        "kraken": {
            "spot": {
                "timeframes": {
                    "live_rest_api": {
                        "intervals_minutes": [60, 240],
                        "history_depth_candles": 720,
                    },
                },
            },
        },
    },
}


def test_layer1_price_precheck_unknown_venue_declines():
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE, "coinbase", "BTCUSDT", "1h",
        datetime.datetime(2024, 1, 1), datetime.datetime(2024, 2, 1),
    )
    assert ok is False
    assert "coinbase" in reason


def test_layer1_price_precheck_unknown_timeframe_declines():
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE, "binance", "BTCUSDT", "15m",
        datetime.datetime(2024, 1, 1), datetime.datetime(2024, 2, 1),
    )
    assert ok is False
    assert "15m" in reason


def test_layer1_price_precheck_unconfirmed_symbol_declines_by_default():
    """Silence must never resolve to a green light (venue_data_capability.yaml's
    own closing policy) -- a symbol with no earliest_ohlcv_utc entry declines,
    it is not assumed available."""
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE, "binance", "SOMECOINUSDT", "1h",
        datetime.datetime(2024, 1, 1), datetime.datetime(2024, 2, 1),
    )
    assert ok is False
    assert "unconfirmed" in reason


def test_layer1_price_precheck_window_before_earliest_declines():
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE, "binance", "BTCUSDT", "1h",
        datetime.datetime(2015, 1, 1), datetime.datetime(2015, 2, 1),
    )
    assert ok is False
    assert "earliest" in reason


def test_layer1_price_precheck_valid_binance_window_passes():
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE, "binance", "BTCUSDT", "1h",
        datetime.datetime(2024, 1, 1), datetime.datetime(2024, 2, 1),
    )
    assert ok is True


def test_layer1_price_precheck_kraken_720_cap_declines_old_window():
    """The load-bearing Kraken finding: a window older than 720 candles back
    from 'now' at the requested resolution is structurally unreachable via
    this codebase's live fetch path, independent of local cache state."""
    now = datetime.datetime(2026, 9, 11)
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE, "kraken", "XBTUSD", "1h",
        datetime.datetime(2020, 1, 1), datetime.datetime(2020, 2, 1),
        now=now,
    )
    assert ok is False
    assert "720" in reason


def test_layer1_price_precheck_kraken_recent_window_within_720_cap_passes():
    now = datetime.datetime(2026, 9, 11)
    recent_start = now - datetime.timedelta(hours=100)
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE, "kraken", "XBTUSD", "1h",
        recent_start, now,
        now=now,
    )
    assert ok is True


_LAYER1_FIXTURE_WITH_ARCHIVE = {
    "venues": {
        "kraken": {
            "spot": {
                "timeframes": {
                    "live_rest_api": {
                        "intervals_minutes": [60, 240],
                        "history_depth_candles": 720,
                    },
                    "downloadable_archive": {
                        "intervals_minutes": [60],
                    },
                },
            },
        },
    },
}


def test_layer1_price_precheck_kraken_old_window_rescued_by_declared_archive_mechanism():
    """Jeremy's 2026-09-11 catch: local_data/kraken_BTCUSD_1h.csv reaches back
    to 2013 via a one-time bulk-archive ingestion (tools/ingest_kraken_archive.py)
    -- a SECOND declared mechanism (downloadable_archive) with no 720-candle
    recency cap. A window older than the live-REST cutoff must NOT decline at
    Layer 1 when the archive mechanism also lists this interval; Layer 2's
    real fetch/cache check is what confirms whether it's actually there."""
    now = datetime.datetime(2026, 9, 11)
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE_WITH_ARCHIVE, "kraken", "BTCUSD", "1h",
        datetime.datetime(2020, 1, 1), datetime.datetime(2020, 2, 1),
        now=now,
    )
    assert ok is True, reason


def test_layer1_price_precheck_kraken_old_window_still_declines_when_interval_only_in_live_rest():
    """The 240-minute (4h) interval is declared ONLY under live_rest_api in
    this fixture (not in downloadable_archive's [60]) -- the 720-candle cap
    must still bite for that interval specifically, confirming the rescue
    above is interval-scoped, not a blanket pass for the whole venue."""
    now = datetime.datetime(2026, 9, 11)
    ok, reason = dag.layer1_price_precheck(
        _LAYER1_FIXTURE_WITH_ARCHIVE, "kraken", "BTCUSD", "4h",
        datetime.datetime(2020, 1, 1), datetime.datetime(2020, 2, 1),
        now=now,
    )
    assert ok is False
    assert "720" in reason


def test_layer1_price_precheck_kraken_unreachable_timeframe_rescued_by_aggregation():
    """5-minute isn't listed under any mechanism in this fixture, but
    1-minute is declared and divides it evenly -- reachable via
    CandleBuilder aggregation, Layer 2 confirms the rest."""
    layer1 = {
        "venues": {"kraken": {"spot": {"timeframes": {
            "live_rest_api": {"intervals_minutes": [1], "history_depth_candles": 720},
        }}}},
    }
    now = datetime.datetime(2026, 9, 11)
    ok, reason = dag.layer1_price_precheck(
        layer1, "kraken", "BTCUSD", "5m",
        now - datetime.timedelta(hours=1), now,
        now=now,
    )
    assert ok is True, reason
    assert "aggregation" in reason


def test_layer1_price_precheck_binance_unreachable_timeframe_rescued_by_aggregation():
    """Same aggregation fallback for the flat timeframes.available branch:
    only 1m is listed, 5m divides it evenly -- must not decline outright."""
    layer1 = {
        "venues": {"binance": {"spot": {
            "timeframes": {"available": ["1m"]},
            "symbols": {"earliest_ohlcv_utc": {"BTCUSDT": "2017-08-17T00:00:00Z"}},
        }}},
    }
    ok, reason = dag.layer1_price_precheck(
        layer1, "binance", "BTCUSDT", "5m",
        datetime.datetime(2024, 1, 1), datetime.datetime(2024, 2, 1),
    )
    assert ok is True, reason


def test_timeframe_to_seconds_parses_non_standard_but_valid_intervals():
    """Regression, Jeremy's catch (2026-09-11, 'Binance BTC 7m'): a timeframe
    string absent from the fixed _TIMEFRAME_SECONDS enum must still resolve
    to a real second count if it matches '<N><m|h|d|w>' -- CandleBuilder's
    real aggregation mechanism has no requirement that an interval be a
    'named' venue-native token, only that it's a real number of seconds."""
    assert dag._timeframe_to_seconds("7m") == 420
    assert dag._timeframe_to_seconds("9d") == 9 * 86400
    assert dag._timeframe_to_seconds("2w") == 2 * 604800
    assert dag._timeframe_to_seconds("1h") == 3600  # still hits the fixed dict first
    assert dag._timeframe_to_seconds("1M") == 2592000  # month: fixed dict only, never regex
    assert dag._timeframe_to_seconds("not_a_timeframe") is None


def test_layer1_price_precheck_nonstandard_timeframe_rescued_by_aggregation():
    """The exact bug: '7m' (420s) isn't a venue-native token anywhere, but
    Binance's declared '1m' (60s) divides it evenly -- before the
    _timeframe_to_seconds fix, this fell through as an unparseable interval
    (silently treated as 'not real' rather than 'not named') and declined
    despite being genuinely reachable via aggregation."""
    layer1 = {
        "venues": {"binance": {"spot": {
            "timeframes": {"available": ["1m"]},
            "symbols": {"earliest_ohlcv_utc": {"BTCUSDT": "2017-08-17T00:00:00Z"}},
        }}},
    }
    ok, reason = dag.layer1_price_precheck(
        layer1, "binance", "BTCUSDT", "7m",
        datetime.datetime(2024, 1, 1), datetime.datetime(2024, 2, 1),
    )
    assert ok is True, reason


def test_layer1_price_precheck_kraken_unconfirmed_symbol_declines_regardless_of_date():
    """Jeremy's catch: an unaudited Kraken symbol (SHIBUSD, outside the
    19-pair confirmed_universe) must decline unconditionally -- not just for
    an impossible date, for ANY date -- same policy binance.spot already
    applies via earliest_ohlcv_utc."""
    layer1 = {
        "venues": {"kraken": {"spot": {
            "symbols": {"confirmed_universe": ["BTCUSD"]},
            "timeframes": {"live_rest_api": {"intervals_minutes": [5], "history_depth_candles": 720}},
        }}},
    }
    ok, reason = dag.layer1_price_precheck(
        layer1, "kraken", "SHIBUSD", "5m",
        datetime.datetime(2024, 1, 15), datetime.datetime(2024, 1, 16),
    )
    assert ok is False
    assert "confirmed_universe" in reason


def test_layer1_price_precheck_kraken_window_before_venue_existed_declines():
    """Jeremy's catch: the archive-mechanism rescue has no lower bound of its
    own -- a confirmed symbol requesting a window before Kraken's own public
    launch must still decline, even though the interval is otherwise listed
    under BOTH mechanisms (so the archive rescue alone would have let it
    through)."""
    layer1 = {
        "venues": {"kraken": {"spot": {
            "symbols": {"confirmed_universe": ["BTCUSD"], "earliest_possible_utc": "2013-09-01T00:00:00Z"},
            "timeframes": {
                "live_rest_api": {"intervals_minutes": [5], "history_depth_candles": 720},
                "downloadable_archive": {"intervals_minutes": [5]},
            },
        }}},
    }
    ok, reason = dag.layer1_price_precheck(
        layer1, "kraken", "BTCUSD", "5m",
        datetime.datetime(2010, 1, 15), datetime.datetime(2010, 1, 16),
    )
    assert ok is False
    assert "public launch" in reason


def test_layer1_price_precheck_kraken_confirmed_symbol_after_launch_still_passes():
    """Regression: the two new gates above must not over-trigger -- a
    confirmed symbol on a real, post-launch date still passes."""
    layer1 = {
        "venues": {"kraken": {"spot": {
            "symbols": {"confirmed_universe": ["BTCUSD"], "earliest_possible_utc": "2013-09-01T00:00:00Z"},
            "timeframes": {"live_rest_api": {"intervals_minutes": [5], "history_depth_candles": 720}},
        }}},
    }
    now = datetime.datetime(2026, 9, 11)
    ok, reason = dag.layer1_price_precheck(
        layer1, "kraken", "BTCUSD", "5m",
        now - datetime.timedelta(hours=1), now,
        now=now,
    )
    assert ok is True, reason


def test_layer1_price_precheck_unreachable_timeframe_with_no_finer_available_still_declines():
    """Regression: the genuinely-impossible case (no direct match, no finer
    interval to aggregate from) must still decline -- this is the existing
    behavior test_layer1_price_precheck_unknown_timeframe_declines already
    covers for binance('15m' vs ['1h','4h'], both coarser); this variant
    pins the same guarantee explicitly for kraken."""
    layer1 = {
        "venues": {"kraken": {"spot": {"timeframes": {
            "live_rest_api": {"intervals_minutes": [1440], "history_depth_candles": 720},
        }}}},
    }
    ok, reason = dag.layer1_price_precheck(
        layer1, "kraken", "BTCUSD", "1h",
        datetime.datetime(2024, 1, 1), datetime.datetime(2024, 2, 1),
    )
    assert ok is False
    assert "no finer" in reason


# ---------------------------------------------------------------------------
# Aggregation (_aggregate) -- the validate/refine/decline outcome model
# ---------------------------------------------------------------------------

def _window(symbol, label, outcome, reason="x"):
    return {"symbol": symbol, "label": label, "outcome": outcome, "reason": reason,
             "missing_fraction": {"validate": 0.0, "refine": 0.02, "decline": 1.0}[outcome]}


def test_aggregate_all_validate_is_validate():
    windows = [_window("BTCUSDT", "2024-01", "validate")]
    result = dag._aggregate(windows, [], 1)
    assert result["overall"] == "validate"


def test_aggregate_some_windows_bad_is_refine_not_decline():
    """E-039's own example: 'a handful of specific months are missing
    entirely out of a 76-window protocol (drop those windows, keep the
    rest)' is explicitly REFINE, not decline."""
    windows = [_window("BTCUSDT", "2024-01", "validate"),
               _window("BTCUSDT", "2024-02", "decline")]
    result = dag._aggregate(windows, [], 2)
    assert result["overall"] == "refine"


def test_aggregate_every_window_declines_is_decline():
    windows = [_window("BTCUSDT", "2024-01", "decline"),
               _window("ETHUSDT", "2024-01", "decline")]
    result = dag._aggregate(windows, [], 2)
    assert result["overall"] == "decline"


def test_aggregate_aux_feed_declined_on_every_window_is_decline():
    """A structurally-missing aux feed (declines for every window checked)
    has no workaround by narrowing -- decline, even if price is fine."""
    windows = [_window("BTCUSDT", "2024-01", "validate")]
    aux = [
        {"feed": "funding_rate", "label": "2024-01", "outcome": "decline", "reason": "x"},
        {"feed": "funding_rate", "label": "2024-02", "outcome": "decline", "reason": "x"},
    ]
    result = dag._aggregate(windows, aux, 1)
    assert result["overall"] == "decline"


def test_aggregate_aux_feed_declined_on_some_windows_only_is_refine():
    windows = [_window("BTCUSDT", "2024-01", "validate")]
    aux = [
        {"feed": "funding_rate", "label": "2019-09", "outcome": "decline", "reason": "x"},
        {"feed": "funding_rate", "label": "2019-10", "outcome": "refine", "reason": "x"},
    ]
    result = dag._aggregate(windows, aux, 1)
    assert result["overall"] == "refine"


def test_aggregate_empty_protocol_declines():
    result = dag._aggregate([], [], 0)
    assert result["overall"] == "decline"


# ---------------------------------------------------------------------------
# Aux-feed branching -- the two confirmed rules, each with a concrete example
# ---------------------------------------------------------------------------

def test_check_aux_feed_reserved_feed_declines_without_touching_data(monkeypatch):
    """Rule: reserved (whale_*) feeds decline unconditionally -- a policy
    gate, never attempted here. Proven by asserting FEED_REGISTRY is never
    consulted (a KeyError would fire if the reserved branch fell through)."""
    reserved_name = next(iter(dag._RESERVED_FEED_NAMES))
    result = dag.check_aux_feed_window(reserved_name, "binance", ["BTCUSDT"],
                                        "2024-01-01", "2024-02-01")
    assert result["outcome"] == "decline"
    assert "RESERVED" in result["reason"]


def test_check_aux_feed_unknown_feed_name_declines():
    result = dag.check_aux_feed_window("not_a_real_feed", "binance", ["BTCUSDT"],
                                        "2024-01-01", "2024-02-01")
    assert result["outcome"] == "decline"
    assert "not a known feed" in result["reason"]


def test_check_aux_feed_fear_greed_is_venue_less_and_measured_in_own_cadence(tmp_path, monkeypatch):
    """Rule 1 (venue-less) + Rule 2 (own native cadence, 86400s for
    fear_greed, never the hourly candle interval): construct a synthetic
    FearGreedFetcher-shaped local cache covering the window fully, confirm
    the check reports 0% missing measured in DAYS, not hours (which would
    show ~95%+ missing by construction if measured in candle units)."""
    import data.fetchers.fear_greed_fetcher as fgf

    local_data_dir = tmp_path / "local_data"
    local_data_dir.mkdir()
    csv_path = local_data_dir / "fear_greed_daily.csv"
    days = pd.date_range("2024-01-01", "2024-01-31", freq="D")
    pd.DataFrame({
        "timestamp": days, "value": [50] * len(days), "classification": ["Neutral"] * len(days),
    }).to_csv(csv_path, index=False)

    # check_aux_feed_window computes data_dir = os.path.join(_TBOT, "local_data")
    # -- point the module's _TBOT at tmp_path so it reads our synthetic cache
    # (fear_greed_fetcher's cache_key is fixed to "fear_greed_daily", not
    # parametrizable, so tmp_path/local_data/fear_greed_daily.csv is the only
    # way to feed it a controlled fixture).
    monkeypatch.setattr(dag, "_TBOT", str(tmp_path))
    result = dag.check_aux_feed_window("fear_greed", "binance", ["BTCUSDT"],
                                        "2024-01-01", "2024-01-31")
    assert result["outcome"] in ("validate", "refine")
    assert result["cadence_seconds"] == fgf._FEAR_GREED_INTERVAL_SECONDS
    assert result["cadence_seconds"] == 86400


# ---------------------------------------------------------------------------
# check_price_window -- integration against a REAL (synthetic) local_data cache
# ---------------------------------------------------------------------------

_FAKE_SYMBOL = "ZZZE054TESTUSDT"


@pytest.fixture
def fake_price_cache():
    """Writes a small, fully-populated synthetic 1h OHLCV cache for a symbol
    name that cannot collide with any real market symbol, at the REAL
    trading-bot/local_data path DataManager/CcxtFetcher actually read from
    (that path is not injectable -- see module docstring). Removes it after."""
    csv_path = Path(_TBOT) / "local_data" / f"{_FAKE_SYMBOL}_1h.csv"
    hours = pd.date_range("2024-01-01", "2024-01-03", freq="h", inclusive="left")
    df = pd.DataFrame({
        "timestamp": hours,
        "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 10.0,
    })
    df.to_csv(csv_path, index=False)
    try:
        yield csv_path
    finally:
        if csv_path.exists():
            csv_path.unlink()


def test_check_price_window_fully_available_synthetic_cache_validates(fake_price_cache):
    result = dag.check_price_window(_FAKE_SYMBOL, "binance", "1h",
                                     "2024-01-01", "2024-01-02",
                                     fetch_interval_seconds=None)
    assert result["outcome"] == "validate", result
    assert result["missing_fraction"] == 0.0


def test_check_price_window_symbol_never_cached_declines():
    """No cache, no network reachable (this test asserts the OUTCOME, not
    the network state) -- fetch_historical_data degrades any failure to an
    empty frame (data_manager.py's own documented contract), which this gate
    must classify as decline, never crash."""
    result = dag.check_price_window("ZZZE054_DOES_NOT_EXIST", "binance", "1h",
                                     "2024-01-01", "2024-01-02",
                                     fetch_interval_seconds=None)
    assert result["outcome"] == "decline"
    assert result["missing_fraction"] == 1.0


def test_check_price_window_uses_default_localstorage_true(monkeypatch):
    """`localStorage=False` was tried and reverted (2026-09-11): it gates the
    CACHE READ in base_fetcher.py's `_load_all`, not only the write, so
    passing it would make this gate ignore an already-complete local cache
    and always attempt a live fetch -- a strictly worse availability check.
    This asserts the gate calls fetch_historical_data with the SAME defaults
    a real backtest uses (core/backtester.py's own load_data()), i.e. never
    overrides localStorage."""
    captured = {}

    def _fake_fetch_historical_data(self, symbol, start, end, exchange="binance", **kwargs):
        captured.update(kwargs)
        return pd.DataFrame({"timestamp": []})

    monkeypatch.setattr(dag.DataManager, "fetch_historical_data", _fake_fetch_historical_data)
    dag.check_price_window("BTCUSDT", "binance", "1h", "2024-01-01", "2024-01-02",
                            fetch_interval_seconds=None)
    assert "localStorage" not in captured


# ---------------------------------------------------------------------------
# evaluate_variant -- top-level wiring, aggregation end-to-end
# ---------------------------------------------------------------------------

def test_evaluate_variant_validates_when_fully_cached(fake_price_cache):
    protocol = {
        "symbols": [_FAKE_SYMBOL], "timeframe": "1h", "exchange": "binance",
        "windows": [{"label": "2024-01", "test": {"start": "2024-01-01", "end": "2024-01-02"}}],
    }
    config = {"aux_feeds": []}
    layer1 = {"venues": {"binance": {"spot": {
        "timeframes": {"available": ["1h"]},
        "symbols": {"earliest_ohlcv_utc": {_FAKE_SYMBOL: "2020-01-01T00:00:00Z"}},
    }}}}
    result = dag.evaluate_variant(config, protocol, layer1=layer1)
    assert result["outcome"] == "validate"
    assert result["exchange"] == "binance"


def test_evaluate_variant_layer1_structural_decline_never_touches_layer2():
    """A symbol/timeframe Layer 1 cannot confirm declines WITHOUT a data
    touch -- proven by using a nonexistent symbol that would otherwise hang
    trying to reach the network in this sandboxed test."""
    protocol = {
        "symbols": ["TOTALLY_UNKNOWN_SYMBOL"], "timeframe": "1h", "exchange": "binance",
        "windows": [{"label": "2024-01", "test": {"start": "2024-01-01", "end": "2024-01-02"}}],
    }
    config = {}
    layer1 = {"venues": {"binance": {"spot": {"timeframes": {"available": ["1h"]}, "symbols": {}}}}}
    result = dag.evaluate_variant(config, protocol, layer1=layer1)
    assert result["outcome"] == "decline"
    assert result["windows"][0]["layer"] == 1
