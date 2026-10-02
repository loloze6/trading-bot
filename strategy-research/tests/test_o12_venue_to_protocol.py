"""
O-12: the brief's (venue, product) reaches the backtest.

Until now venue/product fed only the tradability check; the protocol named no
exchange, so every backtest read Binance data with the default costs.
tools/venue_resolver.py turns a brief's (venue, product) into protocol keys
(exchange, market_type, venue labels, the price source's symbol names);
protocol creation writes them, run_protocol passes market_type to the engine
and takes the fee from trading-bot/config/cost_model.json (E-010's single
source) for both the engine and the trade diagnostics; per-coin asset
variants are priced on the run's venue.

Kraken futures (operator O-12 option A): Kraken SPOT prices as a declared
proxy (venue_data_capability.yaml kraken.futures.price_proxy), Kraken FUTURES
costs, funding not modelled. Binance (or no venue): nothing written,
byte-identical. Any other venue that does not resolve fails loud at protocol
creation -- run start, before any LLM call (operator: replaces CUL-183's
separate registration gate).
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_protocol as rp  # noqa: E402
import variant_coin as vc  # noqa: E402
import venue_resolver as vr  # noqa: E402

from test_e061_c1_4_5_pauses_preflight import RUN, _NON_GENERIC, _scaffold  # noqa: E402


# ---------------------------------------------------------------------------
# 1. The resolver
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("venue", [None, "", "binance", "Binance"])
def test_the_default_venue_writes_nothing(venue):
    assert vr.resolve(venue, "perp") is None
    assert vr.protocol_keys({"venue": venue, "product": "perp"}, ["BTCUSDT"]) == {}


@pytest.mark.parametrize("product", ["perp", "futures"])
def test_kraken_futures_is_spot_prices_with_futures_costs(product):
    r = vr.resolve("kraken", product)
    assert r["exchange"] == "kraken" and r["market_type"] == "futures"
    v = r["venue"]
    assert v["price_source"] == "kraken.spot" and v["price_proxy"] is True
    assert v["funding_modelled"] is False and "proxy" in v["label"]
    assert "fee_bps" not in v  # cost_model.json stays the single source (E-010)


@pytest.mark.parametrize("product", ["spot", "margin"])
def test_a_kraken_market_with_no_cost_entry_fails_loud(product):
    with pytest.raises(vr.VenueResolutionError, match="cost_model.json"):
        vr.resolve("kraken", product)


def test_an_unknown_venue_fails_loud():
    with pytest.raises(vr.VenueResolutionError):
        vr.resolve("bybit", "perp")


def test_a_market_without_spot_prices_or_proxy_fails_loud(monkeypatch):
    monkeypatch.setattr(vr, "_fee_bps", lambda exchange, market: 5.0)
    layer1 = {"venues": {"kraken": {"spot": {}, "futures": {"timeframes": {}}}}}
    with pytest.raises(vr.VenueResolutionError, match="reads only 'spot'"):
        vr.resolve("kraken", "perp", layer1=layer1)


def test_a_declared_proxy_needs_its_source_market_in_the_audit(monkeypatch):
    monkeypatch.setattr(vr, "_fee_bps", lambda exchange, market: 5.0)
    layer1 = {"venues": {"kraken": {"futures": {"price_proxy": {"source": "spot"}}}}}
    with pytest.raises(vr.VenueResolutionError, match="kraken.spot is not"):
        vr.resolve("kraken", "perp", layer1=layer1)


@pytest.mark.parametrize("coin,name", [("BTCUSDT", "BTCUSD"), ("ETHUSDT", "ETHUSD"),
                                       ("XBTUSD", "BTCUSD"), ("SOLUSDT", "SOLUSD")])
def test_coins_take_the_price_source_naming(coin, name):
    assert vr.venue_symbol(coin, vr.resolve("kraken", "perp")) == name


def test_a_coin_the_venue_does_not_list_fails_loud():
    with pytest.raises(vr.VenueResolutionError, match="not backtestable"):
        vr.venue_symbol("FOOUSDT", vr.resolve("kraken", "perp"))


def test_the_alias_lives_in_one_place_and_matches_the_vocabularies():
    """perp (venue_tradability.yaml) == futures (cost_model.json, capability)."""
    assert vr.PRODUCT_ALIASES == {"perp": "futures"}
    trad = yaml.safe_load((_SR / "config" / "venue_tradability.yaml").read_text(encoding="utf-8"))
    assert "perp" in json.dumps(trad)
    cost = json.loads((_SR.parent / "trading-bot" / "config" / "cost_model.json").read_text())
    assert "futures" in cost["kraken"]


# ---------------------------------------------------------------------------
# 2. Protocol creation
# ---------------------------------------------------------------------------

def _constraints():
    return {"protocol": {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                         "start": "2022-01-01", "end": "2022-03-01", "promotion": _NON_GENERIC}}


def _generate(brief: dict):
    run_dir = _scaffold(constraints=_constraints())
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    return json.loads(path.read_text(encoding="utf-8"))


def test_a_binance_brief_generates_the_same_protocol_as_before():
    written = _generate({"venue": "binance", "product": "perp"})
    assert list(written) == ["symbols", "timeframe", "windows", "holdout", "promotion"]
    assert written["symbols"] == ["BTCUSDT", "ETHUSDT"] and "exchange" not in written


def test_a_kraken_perp_brief_writes_the_venue_into_the_protocol():
    written = _generate({"venue": "kraken", "product": "perp"})
    assert written["symbols"] == ["BTCUSD", "ETHUSD"]
    assert written["exchange"] == "kraken" and written["market_type"] == "futures"
    assert written["venue"]["price_proxy"] is True
    assert written["venue"]["funding_modelled"] is False


def test_a_kraken_spot_brief_fails_at_protocol_creation():
    """No (kraken, spot) cost entry: refused at run start, before any LLM call."""
    with pytest.raises(vr.VenueResolutionError, match="cost_model.json"):
        _generate({"venue": "kraken", "product": "spot"})


# ---------------------------------------------------------------------------
# 3. Per-coin variants on the run's venue
# ---------------------------------------------------------------------------

def test_coin_entry_finds_a_coin_by_its_base_asset():
    universe = yaml.safe_load((_SR / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    cat_venue, coin = vc.coin_entry(universe, "BTCUSD")
    cat_plain, _ = vc.coin_entry(universe, "BTCUSDT")
    assert coin["symbol"] == "BTCUSDT" and cat_venue == cat_plain


def _venue_source():
    keys = vr.protocol_keys({"venue": "kraken", "product": "perp"}, ["BTCUSDT"])
    windows = [{"label": f"2022-0{m}", "test": {"start": f"2022-0{m}-01",
                                               "end": f"2022-0{m + 1}-01"}} for m in (1, 2)]
    return {**keys, "timeframe": "1h", "windows": windows}


def test_an_asset_variant_is_priced_on_the_runs_venue():
    import data_availability_gate as dag
    universe = yaml.safe_load((_SR / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    layer1 = dag.load_layer1()
    res = vc.resolve_variant({"variant_id": "a", "kind": "asset", "symbol": "SOLUSDT", "patch": []},
                             source=_venue_source(), universe=universe, layer1=layer1,
                             precheck=dag.layer1_price_precheck, era_of=lambda ts: "era")
    assert res["ok"], res
    proto = res["protocol"]
    assert proto["symbols"] == ["SOLUSD"] and proto["exchange"] == "kraken"
    assert proto["market_type"] == "futures" and proto["venue"]["price_proxy"] is True


def test_a_coin_whose_default_venue_differs_is_not_silently_priced_there():
    """DOTUSDT defaults to Binance in coin_universe.yaml and Kraken spot does not
    list it: under a Kraken run it is a D-042 coverage skip, never a Binance
    backtest mixed into a Kraken idea."""
    import data_availability_gate as dag
    universe = yaml.safe_load((_SR / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    res = vc.resolve_variant({"variant_id": "a", "kind": "asset", "symbol": "DOTUSDT", "patch": []},
                             source=_venue_source(), universe=universe, layer1=dag.load_layer1(),
                             precheck=dag.layer1_price_precheck, era_of=lambda ts: "era")
    assert res["ok"] is False
    assert res["reason"].startswith(vc.COVERAGE_REASON_PREFIX) and "not backtestable" in res["reason"]


def test_base_and_design_variants_inherit_the_venue():
    source = _venue_source()
    out = vc.variant_protocol(source, symbol=source["symbols"][0])
    assert out["exchange"] == "kraken" and out["market_type"] == "futures"
    assert out["venue"] == source["venue"]


# ---------------------------------------------------------------------------
# 4. run_protocol: market_type and the single fee source
# ---------------------------------------------------------------------------

class _Recorder:
    def __init__(self, sandbox):
        self.calls, self._sandbox = [], Path(sandbox)

    def __call__(self, config_path, symbol, start, end, results_root, **kw):
        self.calls.append({"symbol": symbol, **kw})
        run_dir = self._sandbox / f"stub_{len(self.calls)}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(json.dumps({"core": {
            "trade_count": 1, "net_pnl": 0.0, "sharpe": 0.0, "win_rate": 0.5,
            "max_drawdown_pct": 0.0, "forecast_return_corr": None}}))
        return run_dir


def _run_protocol(monkeypatch, tmp_path, **extra):
    stub = _Recorder(tmp_path / "sandbox")
    monkeypatch.setattr(rp, "run_backtest", stub)
    monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
    policy = tmp_path / "policy.yaml"
    policy.write_text('holdout_range: ["2022-02-01", "2022-02-02"]\nholdout_consumed_by: []\n',
                      encoding="utf-8")
    monkeypatch.setattr(rp, "_DATA_POLICY_PATH", policy)
    protocol = {"symbols": ["BTCUSDT"], "promotion": {
        "median_sharpe_gt": -999, "max_abs_drawdown_pct_lt": 999, "min_trade_count_gte": 0,
        "kill_median_sharpe_lt": -999999},
        "windows": [{"label": "w1", "test": {"start": "2022-01-01", "end": "2022-01-02"}}],
        **extra}
    (tmp_path / "protocol.json").write_text(json.dumps(protocol))
    (tmp_path / "config.json").write_text(json.dumps({"dummy": True}))
    monkeypatch.setattr(sys, "argv", ["run_protocol.py", str(tmp_path / "config.json"),
                                      str(tmp_path / "protocol.json"),
                                      "--out-dir", str(tmp_path / "out")])
    rp.main()
    result = json.loads((tmp_path / "out" / "protocol_summary.json").read_text(encoding="utf-8"))
    return stub.calls, result


def test_a_protocol_without_a_venue_calls_the_engine_exactly_as_before(monkeypatch, tmp_path):
    calls, result = _run_protocol(monkeypatch, tmp_path)
    assert calls and all("market_type" not in c for c in calls)
    assert calls[0]["commission_rate"] == pytest.approx(7.5 / 10000)  # cost_model.yaml spot
    assert "venue" not in result


def test_a_venue_protocol_uses_the_market_and_the_cost_model_json_fee(monkeypatch, tmp_path):
    keys = vr.protocol_keys({"venue": "kraken", "product": "perp"}, ["BTCUSDT"])
    calls, result = _run_protocol(monkeypatch, tmp_path, **{**keys, "symbols": keys["symbols"]})
    assert calls[0]["market_type"] == "futures" and calls[0]["exchange"] == "kraken"
    assert calls[0]["symbol"] == "BTCUSD"
    assert calls[0]["commission_rate"] == pytest.approx(5.0 / 10000)  # cost_model.json kraken/futures
    assert result["venue"]["fee_bps"] == 5.0 and result["venue"]["price_proxy"] is True
    assert result["venue"]["exchange"] == "kraken"


# ---------------------------------------------------------------------------
# 5. Review fixes (Opus review of d782cfe2)
# ---------------------------------------------------------------------------

import run_campaign as camp  # noqa: E402


def _generate_in(brief: dict):
    run_dir = _scaffold(constraints=_constraints())
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    return run_dir, path, json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("brief", [{"venue": "kraken", "product": "perp"},
                                   {"venue": "binance", "product": "perp"}])
def test_b1_the_preflight_rebuild_matches_generation(brief):
    """B1: the pre-flight rebuilds the protocol through the same venue helper,
    so a re-entered Kraken run is neither refused nor regenerated without its
    venue."""
    run_dir, path, written = _generate_in(brief)
    expected = camp._expected_generated_protocol(_constraints()["protocol"], RUN,
                                                 promotion_retired=False, run_dir=run_dir)
    assert expected == written
    assert camp._generated_protocol_plan(run_dir, RUN, _constraints()["protocol"], {},
                                         promotion_retired=False) == (None, None)


def test_b1_a_protocol_that_lost_its_venue_is_refused_not_regenerated():
    run_dir, path, written = _generate_in({"venue": "kraken", "product": "perp"})
    stripped = {k: v for k, v in written.items()
                if k not in ("exchange", "market_type", "venue", "drop_feeds")}
    path.write_text(json.dumps(stripped), encoding="utf-8")
    refusal, regen = camp._generated_protocol_plan(run_dir, RUN, _constraints()["protocol"], {},
                                                   promotion_retired=False)
    assert regen is None and "exchange" in refusal and "venue" in refusal


def test_m1_a_venue_protocol_drops_the_funding_feed(monkeypatch, tmp_path):
    keys = vr.protocol_keys({"venue": "kraken", "product": "perp"}, ["BTCUSDT"])
    assert keys["drop_feeds"] == ["funding_rate"]
    calls, _ = _run_protocol(monkeypatch, tmp_path, **keys)
    assert calls and all(c["drop_feeds"] == ["funding_rate"] for c in calls)


def test_m1_a_protocol_without_a_venue_drops_nothing(monkeypatch, tmp_path):
    calls, _ = _run_protocol(monkeypatch, tmp_path)
    assert all(c["drop_feeds"] is None for c in calls)


def test_m4_trade_diagnostics_get_the_venue_fee(monkeypatch, tmp_path):
    seen = []
    real = rp._compute_trade_records_for_window
    monkeypatch.setattr(rp, "_compute_trade_records_for_window",
                        lambda *a, **kw: seen.append(kw["commission_bps"]) or real(*a, **kw))
    keys = vr.protocol_keys({"venue": "kraken", "product": "perp"}, ["BTCUSDT"])
    _run_protocol(monkeypatch, tmp_path, **keys)
    assert seen and all(bps == 5.0 for bps in seen)


_KRAKEN_PR_VENUE = {"exchange": "kraken", "market_type": "futures", "fee_bps": 5.0}


def test_m2_profit_bars_v2_use_the_recorded_venue_fee():
    fees = rpr._v2_charged_fees(["BTCUSD"], [{"symbol": "BTCUSD", "cost_paid": 10.0}],
                                _KRAKEN_PR_VENUE)
    assert fees == {"BTCUSD": 5.0}


def test_m2_a_record_charged_another_fee_is_still_refused():
    with pytest.raises(rpr._pd.PortfolioNotEvaluable, match="kraken futures, cost_model.json"):
        rpr._v2_charged_fees(["BTCUSD"], [{"symbol": "BTCUSD", "cost_paid": 15.0}],
                             _KRAKEN_PR_VENUE)


def _outcome(fn):
    try:
        return ("ok", fn())
    except Exception as exc:  # noqa: BLE001 -- the comparison is the point
        return (type(exc).__name__, str(exc))


@pytest.mark.parametrize("coin", ["BTCUSDT", "ETHUSDT"])
def test_m2_no_venue_keeps_the_yaml_spot_path(coin):
    """No venue block: the same outcome (fee or refusal) as the pre-O-12 call."""
    assert (_outcome(lambda: rpr._v2_charged_fees([coin], [], None))
            == _outcome(lambda: rpr._v2_charged_fees([coin], [])))


def _protocol_file(tmp_path, doc):
    p = tmp_path / "p.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def test_m3_a_kraken_brief_on_a_binance_protocol_is_refused(tmp_path):
    run_dir = _scaffold(constraints=_constraints())
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"venue": "kraken", "product": "perp"})
    with pytest.raises(RuntimeError, match=r"\[O-12\]"):
        rpr._assert_protocol_matches_brief_venue(
            run_dir, _protocol_file(tmp_path, {"symbols": ["BTCUSDT"]}))


def test_m3_matching_or_default_venue_passes(tmp_path):
    run_dir = _scaffold(constraints=_constraints())
    keys = vr.protocol_keys({"venue": "kraken", "product": "perp"}, ["BTCUSDT"])
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"venue": "kraken", "product": "perp"})
    rpr._assert_protocol_matches_brief_venue(run_dir, _protocol_file(tmp_path, keys))
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"venue": "binance", "product": "perp"})
    rpr._assert_protocol_matches_brief_venue(run_dir, _protocol_file(tmp_path, {"symbols": ["X"]}))


@pytest.mark.parametrize("kind,patch", [("base", []), ("design", [{"op": "replace"}])])
def test_m4_base_and_design_accept_the_coin_in_binance_naming(kind, patch):
    import data_availability_gate as dag
    universe = yaml.safe_load((_SR / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    vid = "base" if kind == "base" else "d1"
    res = vc.resolve_variant({"variant_id": vid, "kind": kind, "symbol": "BTCUSDT", "patch": patch},
                             source=_venue_source(), universe=universe, layer1=dag.load_layer1(),
                             precheck=dag.layer1_price_precheck, era_of=lambda ts: "era")
    assert res["ok"], res
    assert res["symbol"] == "BTCUSD" and res["protocol"]["symbols"] == ["BTCUSD"]


def test_m4_without_a_venue_the_symbol_must_still_match_exactly():
    import data_availability_gate as dag
    universe = yaml.safe_load((_SR / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    source = {k: v for k, v in _venue_source().items()
              if k not in ("exchange", "market_type", "venue", "drop_feeds")}
    res = vc.resolve_variant({"variant_id": "base", "kind": "base", "symbol": "BTCUSDT", "patch": []},
                             source=source, universe=universe, layer1=dag.load_layer1(),
                             precheck=dag.layer1_price_precheck, era_of=lambda ts: "era")
    assert res["ok"] is False


@pytest.mark.parametrize("sym,base", [("BUSD", "BUSD"), ("LUSD", "LUSD"), ("BUSDUSDT", "BUSD"),
                                      ("XBTUSD", "BTC"), ("OPUSDT", "OP")])
def test_nit_base_asset_keeps_at_least_two_characters(sym, base):
    assert vr.base_asset(sym) == base


def test_nit_an_ambiguous_base_asset_match_raises():
    universe = {"categories": {"a": {"coins": [{"symbol": "BTCUSDT"}, {"symbol": "BTCUSDC"}]}}}
    with pytest.raises(vc.VariantCoinError, match="ambiguous"):
        vc.coin_entry(universe, "BTCUSD")


def test_m3_the_check_runs_where_the_protocol_is_first_resolved(monkeypatch, tmp_path):
    """_resolve_protocol_path (5a, the data gate, protocol_execution) refuses a
    Kraken brief whatever branch picked the protocol (here: a pin)."""
    import protocol_resolution
    run_dir = _scaffold(constraints=_constraints())
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"venue": "kraken", "product": "perp"})
    pinned = _protocol_file(tmp_path, {"symbols": ["BTCUSDT"]})
    monkeypatch.setattr(protocol_resolution, "resolve_protocol_path", lambda **kw: pinned)
    monkeypatch.setattr(rpr, "load_campaign_state", lambda: {})
    with pytest.raises(RuntimeError, match=r"\[O-12\]"):
        rpr._resolve_protocol_path(run_dir, RUN)
