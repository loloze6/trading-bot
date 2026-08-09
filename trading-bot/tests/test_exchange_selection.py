"""
Exchange selection: config.json's optional `trading.exchange` key must reach
DataManager.fetch_historical_data() through the backtest engine.

data/data_manager.py's fetch_historical_data() has carried an `exchange`
parameter since the Kraken ingest work (the data layer itself is covered by
tests/test_kraken_cache_reachability.py), but BacktestEngine.load_data() never
passed one -- so every kraken_*_1h.csv in local_data/ was unreachable from a
normal backtest: the engine always asked for the unqualified Binance cache,
missed, and fell through to a live remote fetch that returns nothing for a
Kraken store symbol.

The key is OPTIONAL and its ABSENCE means "binance". No tracked config file
declares it, so the reference baseline is unaffected by construction rather
than by matching values.

Fail-loud: a bogus id used to flow all the way down to CcxtFetcher, which logs
"failed to initialise" and sets self.exchange = None, after which the run
reports an empty DataFrame and "No data" -- a typo must not be indistinguishable
from missing history, so the launcher rejects it at the point the key is read.

Offline by construction: the reachability test reads a gap-free 5-day slice
(2022-01-01..01-05, 120 bars) of the BTC 2022 window that
test_kraken_cache_reachability.py audits as gap-free, so the fetcher finds no
missing period and performs no remote fetch or cache re-save. That is enforced
here rather than assumed -- see the sha256 assertion in the test. Every other
test in this file uses a recording stub and never reaches the data layer,
except the run_backtest end-to-end tests further down (T-12/T-13), which
follow the identical gap-free-window + sha256 pattern.

Ticket 13 (fix/exchange-plumbing-campaign-aux, 2026-08-09): run_backtest() --
the module-level function the campaign runner (run_protocol.py) calls -- built
its own TradingParams and BacktestEngine with no `exchange` among their
arguments, so the engine's own default ("binance") always won regardless of
what a campaign wanted: a kraken campaign silently scored binance caches, and
a bogus exchange id ran to completion instead of exiting loudly like
simulate() does. run_backtest() now takes an optional `exchange` parameter
(None resolves to config.json's trading.exchange, exactly like
_read_trading_params) validated through the same _validated_exchange() choke
point (extracted from _read_trading_params, which now calls it too). See
that function's docstring and the tests in the "run_backtest() -> engine"
sections below.
"""

import hashlib
import json
import logging
import socket
import sys
from pathlib import Path
from typing import ClassVar

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import ConfigManager         # noqa: E402
from core import launcher as launcher_mod         # noqa: E402
from core.backtester import BacktestEngine        # noqa: E402
from data.data_manager import DataManager         # noqa: E402

KRAKEN_BTC_CACHE = PROJECT_ROOT / "local_data" / "kraken_BTCUSD_1h.csv"
BINANCE_BTC_CACHE = PROJECT_ROOT / "local_data" / "BTCUSDT_1h.csv"
KRAKEN_BTC_FUNDING_CACHE = PROJECT_ROOT / "local_data" / "kraken_BTCUSD_funding_8h.csv"
_RUN_BACKTEST_CONFIG = PROJECT_ROOT / "tests" / "fixtures" / "warmup_prefetch_check_config.json"

WINDOW_START = "2022-01-01"
WINDOW_END = "2022-01-05"
EXPECTED_WINDOW_ROWS = 120
WINDOW_FIRST = pd.Timestamp("2022-01-01 00:00:00")
WINDOW_LAST = pd.Timestamp("2022-01-05 23:00:00")

# Distinguishes "the caller passed no exchange at all" from "the caller passed
# 'binance'". The two are equivalent in effect but not in evidence: only the
# second proves the value travelled the whole way down.
ABSENT = "<no exchange argument>"

TEST_LOGGER = logging.getLogger("test_exchange_selection")


class _RecordingDataManager:
    """Captures the exchange the engine asks for; serves one bar."""

    def __init__(self):
        self.exchange_arg = ABSENT
        self.historical_data = {}
        self._aux_feeds = {}

    def fetch_historical_data(self, symbol, start_date, end_date, exchange=ABSENT):
        self.exchange_arg = exchange
        return pd.DataFrame({"timestamp": [WINDOW_FIRST], "close": [1.0]})

    def initialize(self):
        pass


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _engine(data_manager, **kwargs):
    return BacktestEngine(
        data_manager=data_manager,
        logger=TEST_LOGGER,
        symbols=["BTCUSD"],
        **kwargs,
    )


def _launcher(trading_section, tmp_path):
    """A Launcher reading a tmp config.json -- the tracked one is never touched."""
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"trading": trading_section}))
    lau = launcher_mod.Launcher.__new__(launcher_mod.Launcher)
    lau.config = ConfigManager(str(cfg_path))
    lau.logger = TEST_LOGGER
    return lau


# ---------------------------------------------------------------------------
# Engine -> data layer
# ---------------------------------------------------------------------------

def test_engine_forwards_the_configured_exchange_to_the_data_layer():
    dm = _RecordingDataManager()
    _engine(dm, exchange="kraken").load_data(start_date=WINDOW_START, end_date=WINDOW_END)
    assert dm.exchange_arg == "kraken"


def test_engine_without_an_exchange_asks_for_binance():
    """The default must be forwarded explicitly, not left to the callee's own."""
    dm = _RecordingDataManager()
    _engine(dm).load_data(start_date=WINDOW_START, end_date=WINDOW_END)
    assert dm.exchange_arg == "binance"


@pytest.mark.skipif(
    not KRAKEN_BTC_CACHE.exists(),
    reason=f"Kraken BTC cache not present: {KRAKEN_BTC_CACHE}",
)
def test_kraken_cache_is_reachable_through_the_backtest_engine():
    """
    The whole point of the parameter: a real BacktestEngine over a real
    DataManager loads kraken_BTCUSD_1h.csv from the REAL local_data/ cache.

    The sha256 assertion is the load-bearing one. BaseFetcher._load_all treats
    an internal gap as a missing period, calls _fetch_remote, and then
    _merge_and_store(save=True) rewrites the CSV even when the remote call
    returned nothing -- so a window spanning a gap turns this read into a
    network attempt and an 11 MB cache rewrite. The Kraken caches are gapped
    (kraken_BTCUSD_1h: 3,262 gaps), so the gap-free window above is what keeps
    this read pure. Asserting the file is byte-identical afterwards makes that
    an enforced invariant instead of a property of the window someone happened
    to pick, and fails loudly if a future edit widens it.
    """
    dm = DataManager(symbols=["BTCUSD"], interval_seconds=3600, mode="backtest")
    engine = _engine(dm, exchange="kraken")
    cache_sha_before = _sha256(KRAKEN_BTC_CACHE)

    engine.load_data(start_date=WINDOW_START, end_date=WINDOW_END)

    assert _sha256(KRAKEN_BTC_CACHE) == cache_sha_before, (
        f"{KRAKEN_BTC_CACHE.name} was rewritten by a read. The window "
        f"{WINDOW_START}..{WINDOW_END} must span no gap in the cache; if it "
        f"now does, this test attempted a remote top-up and re-saved the file."
    )

    df = engine.historical_data["BTCUSD"]
    assert len(df) == EXPECTED_WINDOW_ROWS, len(df)
    assert df["timestamp"].dt.tz is None
    assert df["timestamp"].iloc[0] == WINDOW_FIRST
    assert df["timestamp"].iloc[-1] == WINDOW_LAST


# ---------------------------------------------------------------------------
# config.json -> TradingParams
# ---------------------------------------------------------------------------

def test_absent_exchange_key_resolves_to_binance(tmp_path):
    params = _launcher({"symbols": ["BTCUSDT"]}, tmp_path)._read_trading_params()
    assert params.exchange == "binance"


def test_exchange_key_is_read_from_the_trading_section(tmp_path):
    params = _launcher(
        {"symbols": ["BTCUSD"], "exchange": "kraken"}, tmp_path
    )._read_trading_params()
    assert params.exchange == "kraken"


def test_a_bogus_exchange_exits_loudly_instead_of_fetching_nothing(tmp_path, caplog):
    lau = _launcher({"symbols": ["BTCUSD"], "exchange": "krakn"}, tmp_path)

    with (
        caplog.at_level(logging.ERROR, logger=TEST_LOGGER.name),
        pytest.raises(SystemExit) as exit_info,
    ):
        lau._read_trading_params()

    assert exit_info.value.code == 1
    assert "krakn" in caplog.text


# ---------------------------------------------------------------------------
# Launcher -> engine
# ---------------------------------------------------------------------------

class _RecordingEngine:
    """Stands in for BacktestEngine; records its construction kwargs."""

    kwargs: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        type(self).kwargs = kwargs

    def load_data(self, **kwargs):
        pass

    def simulate_on_loaded_data(self):
        pass


@pytest.fixture
def simulate_with(monkeypatch, tmp_path):
    def _run(trading_section):
        _RecordingEngine.kwargs = {}
        monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingEngine)
        _launcher(trading_section, tmp_path).simulate()
        return _RecordingEngine.kwargs.get("exchange", ABSENT)
    return _run


def test_simulate_hands_the_configured_exchange_to_the_engine(simulate_with):
    assert simulate_with({"symbols": ["BTCUSD"], "exchange": "kraken"}) == "kraken"


def test_simulate_defaults_the_engine_to_binance(simulate_with):
    assert simulate_with({"symbols": ["BTCUSDT"]}) == "binance"


def test_every_launcher_mode_forwards_the_configured_exchange():
    """
    The defect this parameter closes is an engine reading a venue nobody asked
    for, and it returns the moment a mode builds a BacktestEngine without
    forwarding params.exchange -- a config saying "kraken" would quietly load
    Binance caches again. Only `simulate` is driven end-to-end above (the other
    two modes plot and grid-search), so the remaining sites are held statically.

    Scoped to the Launcher class: run_backtest() is module-level, not a
    Launcher method, so it falls outside ast.walk(launcher_class)'s scope --
    covered separately by test_run_backtest_forwards_the_resolved_exchange
    further down, using the identical AST-matching approach and the same
    evasion caveats.

    What this guard is and is not. It matches TEXT, not semantics: it collects
    ast.Call nodes whose func is an ast.Name "BacktestEngine" and compares
    ast.unparse(kw.value) to "params.exchange". Three consequences, all measured
    adversarially on this branch (evidence-leg3/rt_E_defeat_ast.out), none of
    which describes code that exists in the tree today:

      * The len(sites) == 3 anchor is FAIL-CLOSED BY DESIGN. A legitimate fourth
        mode that forwards correctly still fails this test until the count is
        raised deliberately. That is the intent -- adding an engine site should
        be a decision someone records here, not a silent event.
      * Three shapes evade it: an attribute-form call
        (backtester.BacktestEngine(...)), a call through a module-level alias
        (_Engine = BacktestEngine), and keeping the exact text while rebinding
        `params` so .exchange no longer comes from _read_trading_params. A whole
        -tree scan confirms none of these exists today; the three live sites are
        all plain Name calls forwarding params.exchange.
      * One false positive: a correct forward written as a splat,
        **{"exchange": params.exchange}, carries no keyword arg named exchange
        and would fail. Write the keyword literally.

    Comments and string literals do NOT fool it: ast.parse drops comments, and a
    literal is a Constant, not a Call.
    """
    import ast

    source = (PROJECT_ROOT / "core" / "launcher.py").read_text(encoding="utf-8")
    launcher_class = next(
        node for node in ast.parse(source).body
        if isinstance(node, ast.ClassDef) and node.name == "Launcher"
    )

    sites = [
        node for node in ast.walk(launcher_class)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "BacktestEngine"
    ]
    assert len(sites) == 3, f"expected 3 BacktestEngine call sites, found {len(sites)}"

    for site in sites:
        forwarded = [
            kw for kw in site.keywords
            if kw.arg == "exchange" and ast.unparse(kw.value) == "params.exchange"
        ]
        assert forwarded, (
            f"BacktestEngine at core/launcher.py:{site.lineno} does not pass "
            f"exchange=params.exchange"
        )


# ---------------------------------------------------------------------------
# TradingParams dataclass contract (T-04)
# ---------------------------------------------------------------------------

def test_trading_params_exchange_defaults_to_binance():
    """Dataclass contract pin (M2): TradingParams.exchange's own default must
    stay 'binance'. run_backtest always resolves and passes exchange=
    explicitly (E2), so without this pin a default-flip here (launcher.py:41)
    is a dead mutation nothing else would catch."""
    params = launcher_mod.TradingParams(
        symbols=["BTCUSDT"], interval=3600, check_interval=3600, test_mode=True,
    )
    assert params.exchange == "binance"


# ---------------------------------------------------------------------------
# run_backtest() -> engine (T-01, T-02, T-03, T-05)
# ---------------------------------------------------------------------------
# Unlike the Launcher-based tests above, these call the REAL run_backtest()
# against the REAL tracked config.json -- no tracked config declares
# trading.exchange (P0/R-CRUX: cwd tricks cannot redirect a bare Launcher()
# construction, and the locked parameter design means these tests don't need
# to try -- `exchange` is passed as an argument, bypassing config entirely).
# BacktestEngine is monkeypatched to a recording stub so no real fetch or
# strategy run happens.

class _RecordingRunBacktestEngine:
    """Stands in for BacktestEngine inside run_backtest(): records
    construction kwargs, touches no data, runs no strategy."""

    kwargs: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        type(self).kwargs = kwargs
        self._last_run_dir = None

    def load_data(self, **kwargs):
        pass

    def simulate_on_loaded_data(self):
        pass


@pytest.fixture
def run_backtest_with(monkeypatch, tmp_path):
    def _run(**kwargs):
        _RecordingRunBacktestEngine.kwargs = {}
        monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingRunBacktestEngine)
        from core.launcher import run_backtest
        run_backtest(
            config_path=str(_RUN_BACKTEST_CONFIG),
            symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            **kwargs,
        )
        return _RecordingRunBacktestEngine.kwargs.get("exchange", ABSENT)
    return _run


def test_run_backtest_forwards_an_explicit_exchange(run_backtest_with):
    assert run_backtest_with(exchange="kraken") == "kraken"


def test_run_backtest_without_an_exchange_defaults_to_binance(run_backtest_with):
    """The real tracked config.json declares no trading.exchange key, so the
    None -> config-read -> absent -> 'binance' chain must resolve exactly
    like _read_trading_params does."""
    assert run_backtest_with() == "binance"


def test_run_backtest_bogus_exchange_exits_loudly(monkeypatch, tmp_path, caplog):
    monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingRunBacktestEngine)
    from core.launcher import run_backtest

    with (
        caplog.at_level(logging.ERROR, logger="trading_bot"),
        pytest.raises(SystemExit) as exit_info,
    ):
        run_backtest(
            config_path=str(_RUN_BACKTEST_CONFIG),
            symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            exchange="krakn",
        )

    assert exit_info.value.code == 1
    assert "krakn" in caplog.text


def test_run_backtest_forwards_the_resolved_exchange_to_the_engine():
    """
    Companion to test_every_launcher_mode_forwards_the_configured_exchange
    above, scoped to run_backtest() -- module-level, not a Launcher method, so
    outside that test's ast.walk(launcher_class) scope. Same AST-matching
    approach and the same evasion caveats apply (see that test's docstring);
    not re-derived here.
    """
    import ast

    source = (PROJECT_ROOT / "core" / "launcher.py").read_text(encoding="utf-8")
    run_backtest_fn = next(
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == "run_backtest"
    )

    sites = [
        node for node in ast.walk(run_backtest_fn)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "BacktestEngine"
    ]
    assert len(sites) == 1, f"expected 1 BacktestEngine call site in run_backtest, found {len(sites)}"

    forwarded = [
        kw for kw in sites[0].keywords
        if kw.arg == "exchange" and ast.unparse(kw.value) == "params.exchange"
    ]
    assert forwarded, (
        f"BacktestEngine at core/launcher.py:{sites[0].lineno} inside run_backtest "
        f"does not pass exchange=params.exchange"
    )


# ---------------------------------------------------------------------------
# run_backtest() end-to-end (T-12, T-13) -- real engine, real caches,
# gap-free window so a pure read never triggers a remote top-up / re-save.
# ---------------------------------------------------------------------------

class _NoNetworkSocket:
    """Raises at construction -- no real connection attempt is ever made, not
    even a DNS lookup (see FundingRateFetcher._fetch_remote's own try/except,
    which is exactly the boundary this proves reaches its catch clause -- P9)."""

    def __init__(self, *a, **kw):
        raise OSError("network access blocked in test (T-13 socket-block fixture)")


@pytest.fixture
def block_network(monkeypatch):
    monkeypatch.setattr(socket, "socket", _NoNetworkSocket)


@pytest.mark.slow
@pytest.mark.skipif(
    not KRAKEN_BTC_CACHE.exists(),
    reason=f"Kraken BTC cache not present: {KRAKEN_BTC_CACHE}",
)
def test_run_backtest_kraken_price_path_is_pure_and_completes(monkeypatch, tmp_path):
    """T-12: run_backtest(exchange='kraken') over the gap-free 2022-01-01..05
    window reaches kraken_BTCUSD_1h.csv end to end. FEED_REGISTRY is blanked
    to isolate the PRICE path from Ticket 12's aux-feed fail-loud (covered
    separately by T-13 below) -- completes, produces all 120 bars, and
    rewrites neither price cache (G1 purity, re-deriving the same invariant
    test_kraken_cache_is_reachable_through_the_backtest_engine proves for the
    engine alone, this time through the full run_backtest() campaign path)."""
    import data.feed_registry as feed_registry_mod
    from core.launcher import run_backtest

    monkeypatch.setattr(feed_registry_mod, "FEED_REGISTRY", {})

    kraken_sha_before = _sha256(KRAKEN_BTC_CACHE)
    binance_sha_before = _sha256(BINANCE_BTC_CACHE) if BINANCE_BTC_CACHE.exists() else None

    run_dir = run_backtest(
        config_path=str(_RUN_BACKTEST_CONFIG),
        symbol="BTCUSD", start=WINDOW_START, end=WINDOW_END,
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
        exchange="kraken",
    )

    assert _sha256(KRAKEN_BTC_CACHE) == kraken_sha_before, (
        f"{KRAKEN_BTC_CACHE.name} was rewritten by a read."
    )
    if binance_sha_before is not None:
        assert _sha256(BINANCE_BTC_CACHE) == binance_sha_before

    assert run_dir is not None
    bars = pd.read_csv(run_dir / "bars.csv")
    assert len(bars) == EXPECTED_WINDOW_ROWS, len(bars)


@pytest.mark.slow
@pytest.mark.skipif(
    not KRAKEN_BTC_CACHE.exists(),
    reason=f"Kraken BTC cache not present: {KRAKEN_BTC_CACHE}",
)
def test_run_backtest_kraken_aux_feed_fails_loud(block_network, tmp_path):
    """
    T-13 [C-D3]: the REAL FEED_REGISTRY (not blanked this time), so the
    funding feed is actually constructed with exchange_id='kraken'. No
    kraken_BTCUSD_funding_8h.csv cache exists, and the socket block proves the
    empty result comes from a genuinely-attempted, genuinely-failed fetch (P9),
    not a construction-time short-circuit. run_backtest has no try/except
    around its BacktestEngine.load_data() call, so the typed AuxFeedVenueError
    crosses run_backtest's boundary uncaught -- the deliberate fail-fast this
    ticket exists to produce (D-iii). The price cache is still read purely
    (the raise fires strictly after the price fetch, per R-G1).
    """
    from core.launcher import run_backtest
    from data.data_manager import AuxFeedVenueError

    assert not KRAKEN_BTC_FUNDING_CACHE.exists()
    kraken_sha_before = _sha256(KRAKEN_BTC_CACHE)

    with pytest.raises(AuxFeedVenueError):
        run_backtest(
            config_path=str(_RUN_BACKTEST_CONFIG),
            symbol="BTCUSD", start=WINDOW_START, end=WINDOW_END,
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            exchange="kraken",
        )

    assert _sha256(KRAKEN_BTC_CACHE) == kraken_sha_before
    assert not KRAKEN_BTC_FUNDING_CACHE.exists(), "no funding stub CSV should be written"


# ---------------------------------------------------------------------------
# run_backtest() config-fallback arm (T-16)
# ---------------------------------------------------------------------------

def test_run_backtest_exchange_none_falls_back_to_config(monkeypatch, tmp_path):
    """T-16: exchange=None (the default) must fall through to config.json's
    trading.exchange exactly like _read_trading_params, not silently stay
    'binance' regardless of what the config says (M14). Injects via a
    pre-built Launcher instance (Launcher.__new__ + the _launcher() helper
    above, same mechanism as every config-injection test in this file) --
    the only test in this section that needs injection at all (R8): T-01/02/
    03/12/13 pass exchange= directly and never touch config."""
    prebuilt = _launcher({"symbols": ["BTCUSD"], "exchange": "kraken"}, tmp_path)
    monkeypatch.setattr(launcher_mod, "Launcher", lambda: prebuilt)
    monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingRunBacktestEngine)
    from core.launcher import run_backtest

    _RecordingRunBacktestEngine.kwargs = {}
    run_backtest(
        config_path=str(_RUN_BACKTEST_CONFIG),
        symbol="BTCUSD", start="2024-01-01", end="2024-01-02",
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
    )

    assert _RecordingRunBacktestEngine.kwargs.get("exchange") == "kraken"
