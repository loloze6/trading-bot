"""
E-060 S2 -- residual-IC criterion, composite cache, registry timeframe
(delivery_plan_v26.md slice 7 item 7.1; engineering/roadmap/E-060/
S1_FINDINGS.md guesses 4-8 + the operator decisions), all under
orchestrator.composition_runs.enabled (off by default).

No LLM, no real backtest: the composite's protocol run is a fake
subprocess.run writing synthetic bars.csv files. tests/conftest.py sandboxes
rpr.ROOT (with a verbatim copy of the real campaign_data_policy.yaml).
"""
import asyncio
import hashlib
import json
import random
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import block_registry as br  # noqa: E402
import composite_cache as cc  # noqa: E402
import residual_ic as ric  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
from performance.signal_statistics import spearman_correlation  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_e058_s2b_registry_kb_scoreboard import BASE_CONFIG, MANIFEST  # noqa: E402
from test_e059_6c_s2a_route_retirement import RETIRED_ON  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

REAL_MENU = yaml.safe_load((SR_ROOT / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
COMP_ON = {**RETIRED_ON, "variant_loop": {"enabled": True}, "composition_runs": {"enabled": True}}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _recs(forecasts, rets, start=0):
    return [{"timestamp": start + i, "forecast": f, "next_return_bps": r}
            for i, (f, r) in enumerate(zip(forecasts, rets))]


def _gauss(n, seed):
    rng = random.Random(seed)
    return [rng.gauss(0.0, 1.0) for _ in range(n)]


N = 2000
Z_COMP, Z_CAND, NOISE = _gauss(N, 1), _gauss(N, 2), _gauss(N, 3)
RETS = [a + b + 0.5 * c for a, b, c in zip(Z_COMP, Z_CAND, NOISE)]


def _ric(cand, comp, rets=RETS, **kw):
    return ric.compute_residual_ic({"BTCUSDT": _recs(cand, rets)},
                                   None if comp is None else {"BTCUSDT": _recs(comp, rets)},
                                   block_size=kw.pop("block_size", 1),
                                   expected_step_by_symbol={"BTCUSDT": 1},
                                   composite_label=kw.pop("label", "block" if comp is not None
                                                          else "none"))


# ---------------------------------------------------------------------------
# 1. The residual IC on synthetic series
# ---------------------------------------------------------------------------

def test_independent_signal_keeps_a_high_residual_ic():
    d = _ric(Z_CAND, Z_COMP)
    assert d["value"] > 0.4 and d["fully_explained"] is False
    assert abs(d["correlation_to_composite"]) < 0.1
    assert d["n_eff"] == N and d["n_bars"] == N and d["p_value"] < 1e-6


def test_exact_duplicate_is_fully_explained_with_no_fake_zero():
    d = _ric(Z_COMP, Z_COMP)
    assert d["fully_explained"] is True and d["value"] is None
    assert d["correlation_to_composite"] == 1.0


def test_scaled_and_shifted_duplicate_is_fully_explained():
    d = _ric([3.0 * x + 2.0 for x in Z_COMP], Z_COMP)
    assert d["fully_explained"] is True and d["value"] is None


def test_duplicate_plus_small_noise_is_near_zero():
    cand = [x + 0.01 * e for x, e in zip(Z_COMP, _gauss(N, 9))]
    d = _ric(cand, Z_COMP)
    assert d["fully_explained"] is False
    assert abs(d["value"]) < 0.1
    # ... while the composite itself is strongly predictive
    assert spearman_correlation(Z_COMP, RETS) > 0.4


def test_scale_free_in_candidate_and_composite():
    base = _ric(Z_CAND, Z_COMP)["value"]
    assert _ric([5.0 * x for x in Z_CAND], Z_COMP)["value"] == base
    # float residue of the refit may swap a near-tie rank: equal to 1e-5
    assert _ric(Z_CAND, [1e-3 * x for x in Z_COMP])["value"] == pytest.approx(base, abs=1e-5)


def test_constant_candidate_is_inconclusive_not_zero():
    d = _ric([4.0] * N, Z_COMP)
    assert d["value"] is None and d["fully_explained"] is False
    assert d["reason"].startswith("candidate_constant")


def test_no_composite_is_the_candidates_own_rank_ic():
    d = _ric(Z_CAND, None)
    assert d["composite"] == "none" and d["correlation_to_composite"] is None
    assert d["value"] == round(spearman_correlation(Z_CAND, RETS), 6)


def test_no_composite_needs_label_none():
    with pytest.raises(ValueError, match="composite_label"):
        _ric(Z_CAND, None, label="block")


def test_join_drops_and_counts_missing_bars_and_n_eff_is_gap_aware():
    cand = _recs(Z_CAND[:100], RETS[:100])
    comp = _recs(Z_COMP[:100], RETS[:100])
    del cand[10]          # candidate lacks bar 10
    del comp[50:58]       # composite lacks bars 50..57 (-> a gap in the joined series)
    d = ric.compute_residual_ic({"BTCUSDT": cand}, {"BTCUSDT": comp}, block_size=24,
                                expected_step_by_symbol={"BTCUSDT": 1}, composite_label="block")
    assert d["n_dropped_composite_only"] == 1 and d["n_dropped_candidate_only"] == 8
    assert d["n_bars"] == 91 and d["coverage_by_symbol"] == {"BTCUSDT": round(91 / 99, 6)}
    # joined bars: 0..9 | 11..49 | 58..99 -> runs of 10, 39, 42 bars -> 0+1+1 blocks of 24
    assert d["n_eff"] == 2


def test_two_symbols_pooled_and_n_eff_summed():
    half = N // 2
    cand = {"BTCUSDT": _recs(Z_CAND[:half], RETS[:half]), "ETHUSDT": _recs(Z_CAND[half:], RETS[half:])}
    comp = {"BTCUSDT": _recs(Z_COMP[:half], RETS[:half]), "ETHUSDT": _recs(Z_COMP[half:], RETS[half:])}
    d = ric.compute_residual_ic(cand, comp, block_size=10,
                                expected_step_by_symbol={"BTCUSDT": 1, "ETHUSDT": 1},
                                composite_label="block")
    assert d["n_bars"] == N and d["n_eff"] == 2 * (half // 10) and d["value"] > 0.4


# ---------------------------------------------------------------------------
# 2. No lookahead: a future bar never changes a past value
# ---------------------------------------------------------------------------

def test_residual_at_a_bar_never_depends_on_later_bars():
    full = ric.expanding_ols_residuals(Z_CAND, Z_COMP)
    k = 700
    changed_cand = Z_CAND[:k] + [100.0 * x for x in Z_CAND[k:]]
    changed_comp = Z_COMP[:k] + [-50.0 + x for x in Z_COMP[k:]]
    assert ric.expanding_ols_residuals(changed_cand, changed_comp)[:k] == full[:k]
    assert ric.expanding_ols_residuals(Z_CAND[:k], Z_COMP[:k]) == full[:k]


def test_expanding_fit_converges_to_the_whole_sample_fit_at_the_last_bar():
    """At the last bar the expanding fit IS the whole-sample OLS fit."""
    import statistics as st
    mx, my = st.fmean(Z_COMP), st.fmean(Z_CAND)
    b = sum((x - mx) * (y - my) for x, y in zip(Z_COMP, Z_CAND)) / sum((x - mx) ** 2 for x in Z_COMP)
    a = my - b * mx
    assert ric.expanding_ols_residuals(Z_CAND, Z_COMP)[-1] == pytest.approx(
        Z_CAND[-1] - (a + b * Z_COMP[-1]), abs=1e-9)


# ---------------------------------------------------------------------------
# 3. The grid cell: n_eff floor, fully_explained, STALE (evaluator)
# ---------------------------------------------------------------------------

def _menu_residual_crit():
    entry = next(e for e in REAL_MENU["code_added_criteria"] if e["id"] == "residual_ic")
    return {k: v for k, v in entry.items() if k not in rpr._CODE_CRITERION_META_KEYS}


def _cell(diag, crit=None):
    pr = {"results": [{"symbol": "BTCUSDT", "window": "2020-01", "core": {"trade_count": 3}}],
          "hypothesis_verdict": {"diagnostics": {"residual_ic": diag}}}
    pre_reg = {"pass_rule": {"criteria": [crit or _menu_residual_crit()]}}
    return vce.evaluate_grid({"base": pr}, pre_reg, {}, REAL_MENU,
                             composition_runs=True)["grid"]["residual_ic"]["base"]


def _diag(**kw):
    d = {"value": 0.05, "n_eff": 30, "p_value_one_sided": 0.01, "fully_explained": False,
         "composite": "block"}
    d.update(kw)
    return d


def test_menu_entry_is_the_operator_placeholder():
    # E-062 S2b-1: the D-039 values (0.02, one-sided p 0.05, n_eff 30); still
    # `ratified: false` until the operator signs.
    crit = _menu_residual_crit()
    assert (crit["comparator"], crit["threshold"], crit["floor"]) == (">", 0.02, {"min_n_eff": 30})
    raw = next(e for e in REAL_MENU["code_added_criteria"] if e["id"] == "residual_ic")
    assert raw["ratified"] is False
    assert crit["max_p_value"] == 0.05
    assert crit["source"] == "pooled" and crit["statistic"] == "value" and crit["scale_free"]
    assert "residual_ic" not in {c["id"] for c in REAL_MENU["criteria"]}  # never picked by 1a


@pytest.mark.parametrize("diag,result", [
    (_diag(), "PASS"),
    (_diag(value=0.01), "FAIL"),                        # strictly greater than
    (_diag(n_eff=29), "INCONCLUSIVE"),                  # n_eff floor
    (_diag(n_eff=None), "INCONCLUSIVE"),                # no n_eff with the metric
    (_diag(value=None, fully_explained=True), "FAIL"),  # exact duplicate (guess 7)
    (_diag(value=None, n_eff=None, composite="STALE"), "INCONCLUSIVE"),  # guess 4
    (_diag(value=None, reason="candidate_constant"), "INCONCLUSIVE"),
    (_diag(p_value_one_sided=0.05), "FAIL"),            # significance gate (review fix 4)
    (_diag(p_value_one_sided=None), "INCONCLUSIVE"),
])
def test_residual_ic_cell(diag, result):
    cell = _cell(diag)
    assert cell["result"] == result
    assert cell["n_eff"] == diag["n_eff"]


def test_missing_diagnostic_is_inconclusive():
    pr = {"results": [{"symbol": "BTCUSDT", "window": "2020-01", "core": {"trade_count": 3}}]}
    pre_reg = {"pass_rule": {"criteria": [_menu_residual_crit()]}}
    grid = vce.evaluate_grid({"base": pr}, pre_reg, {}, REAL_MENU, composition_runs=True)
    assert grid["grid"]["residual_ic"]["base"]["result"] == "INCONCLUSIVE"


def test_flag_off_min_n_eff_still_raises_for_every_criterion():
    """Review fix 3: the residual_ic cell path runs ONLY for residual_ic AND
    only with composition_runs=True; everything else keeps raising."""
    diag = _diag()
    pr = {"results": [{"symbol": "BTCUSDT", "window": "2020-01", "core": {"trade_count": 3}}],
          "hypothesis_verdict": {"diagnostics": {"residual_ic": diag, "other_ic": diag}}}
    residual = {"pass_rule": {"criteria": [_menu_residual_crit()]}}
    with pytest.raises(NotImplementedError, match="min_n_eff"):
        vce.evaluate_grid({"b": pr}, residual, {}, REAL_MENU)  # flag off
    other = {"pass_rule": {"criteria": [{**_menu_residual_crit(), "id": "other_ic",
                                         "metric": "other_ic"}]}}
    with pytest.raises(NotImplementedError, match="min_n_eff"):
        vce.evaluate_grid({"b": pr}, other, {}, REAL_MENU, composition_runs=True)


def test_pure_noise_block_at_the_n_eff_floor_rarely_passes():
    """Review fix 4: 720 hourly bars -> n_eff 30. Without the p gate about
    half of pure-noise blocks clear IC > 0.01."""
    passes = 0
    trials = 200
    for seed in range(trials):
        rng = random.Random(1000 + seed)
        f = [rng.gauss(0, 1) for _ in range(720)]
        r = [rng.gauss(0, 1) for _ in range(720)]
        d = ric.compute_residual_ic({"BTCUSDT": _recs(f, r)}, None, block_size=24,
                                    expected_step_by_symbol={"BTCUSDT": 1})
        assert d["n_eff"] == 30
        passes += _cell(d)["result"] == "PASS"
    assert passes / trials < 0.10


def test_min_n_eff_on_a_window_source_criterion_still_raises():
    crit = {"id": "c1", "metric": "net_return_pct", "source": "window", "reducer": "median",
            "comparator": ">", "threshold": 0.0, "floor": {"min_n_eff": 30}}
    pr = {"results": [{"symbol": "BTCUSDT", "window": "2020-01", "core": {"net_return_pct": 1.0}}]}
    with pytest.raises(NotImplementedError, match="min_n_eff"):
        vce.evaluate_grid({"v": pr}, {"pass_rule": {"criteria": [crit]}}, {}, {})


def test_existing_pooled_cell_shape_unchanged():
    """A pooled criterion without min_n_eff keeps the pre-S2 cell keys."""
    crit = next(c for c in REAL_MENU["criteria"] if c["id"] == "realized_edge_to_cost_ratio")
    pr = {"results": [{"symbol": "BTCUSDT", "window": f"2020-{m:02d}",
                       "core": {"trade_count": 20}} for m in range(1, 7)],
          "trade_diagnostics_summary": {"realized_edge_to_cost_ratio": 2.5}}
    cell = vce.evaluate_grid({"v": pr}, {"pass_rule": {"criteria": [{"id": crit["id"], "source": "pooled"}]}}, {},
                             REAL_MENU)["grid"][crit["id"]]["v"]
    # E-062 S2b-1: the menu's D-039 values (> 2.2, floor 100 trades).
    assert cell == {"result": "PASS", "value": 2.5, "threshold": 2.2, "comparator": ">",
                    "n_windows": 6, "n_trades": 120}


def test_a_card_cannot_pick_residual_ic():
    with pytest.raises(ValueError, match="not a live entry"):
        rpr._pass_rule_from_card({"criteria": [{"id": "residual_ic"}]}, REAL_MENU, "card.yaml")


# ---------------------------------------------------------------------------
# 4. Timeframe categories (operator decision 3)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tf,cat", [
    ("1m", "high"), ("15m", "high"), ("16m", "medium"), ("59m", "medium"), ("1h", "low"),
    ("60m", "low"), ("4h", "low"), ("23h", "low"), ("1d", "daily"), ("24h", "daily"),
    ("1w", "daily")])
def test_timeframe_category_boundaries(tf, cat):
    assert cc.timeframe_category(tf) == cat


def test_timeframe_category_refuses_garbage():
    with pytest.raises(ValueError):
        cc.timeframe_category("hourly")


# ---------------------------------------------------------------------------
# 5. The composite: resolver (0 / 1 / 2+ blocks, STALE) and cache
# ---------------------------------------------------------------------------

def _block(bid, tf="1h", kind="forecast", ref=None, sha=None):
    return {"block_id": bid, "kind": kind, "timeframe": tf,
            "source_config_ref": ref or f"runs/{bid}/cfg.json",
            "source_config_sha256": sha or hashlib.sha256(bid.encode()).hexdigest()}


def test_resolver_no_block_is_none():
    r = cc.resolve_current_composite({"blocks": [_block("H9:r9", tf="1d")]}, [], "1h")
    assert r["kind"] == "none" and r["registry_hash"] is None and r["block_ids"] == []


def test_resolver_regime_blocks_never_enter_the_composite():
    r = cc.resolve_current_composite({"blocks": [_block("H9:r9", kind="regime")]}, [], "1h")
    assert r["kind"] == "none"


def test_resolver_one_block_is_that_blocks_config():
    b = _block("H1:r1")
    r = cc.resolve_current_composite({"blocks": [b, _block("H2:r2", tf="4h")]}, [], "60m")
    assert r["kind"] == "block" and r["config_ref"] == b["source_config_ref"]
    assert r["expected_config_sha256"] == b["source_config_sha256"]
    assert r["registry_hash"] == cc.composite_registry_hash([b])


def test_resolver_two_blocks_without_a_composition_run_is_stale():
    blocks = [_block("H1:r1"), _block("H2:r2")]
    r = cc.resolve_current_composite({"blocks": blocks}, [
        {"registry_hash": "someothersetxxxx", "base_config_ref": "x.json"}], "1h")
    assert r["kind"] == "stale" and "stale" in r["reason"] and r["config_ref"] is None


def test_resolver_two_blocks_with_their_composition_run():
    blocks = [_block("H1:r1"), _block("H2:r2")]
    h = cc.composite_registry_hash(blocks)
    r = cc.resolve_current_composite({"blocks": blocks}, [
        {"registry_hash": h, "base_config_ref": "runs/run_c/variants/base.json",
         "base_config_sha256": "a" * 64}], "1h")
    assert r["kind"] == "composition" and r["config_ref"] == "runs/run_c/variants/base.json"
    assert r["expected_config_sha256"] == "a" * 64
    # a block on another timeframe does not change this timeframe's composite
    assert cc.composite_registry_hash(blocks) == cc.composite_registry_hash(list(reversed(blocks)))


def test_resolver_composition_without_its_config_sha_raises():
    """Review fix 7: same rule as the single-block path."""
    blocks = [_block("H1:r1"), _block("H2:r2")]
    h = cc.composite_registry_hash(blocks)
    with pytest.raises(cc.CompositeError, match="base_config_sha256"):
        cc.resolve_current_composite({"blocks": blocks}, [
            {"registry_hash": h, "base_config_ref": "runs/run_c/variants/base.json"}], "1h")


def test_resolver_excludes_a_block_without_timeframe_loudly(capsys):
    """Review fix 5: never breaks composition, on this or any timeframe."""
    b = _block("H1:r1")
    del b["timeframe"]
    ok = _block("H2:r2")
    r = cc.resolve_current_composite({"blocks": [b, ok]}, [], "1h")
    assert r["kind"] == "block" and r["block_ids"] == ["H2:r2"]
    assert r["excluded_blocks"][0]["block_id"] == "H1:r1"
    assert "H1:r1" in capsys.readouterr().out
    assert cc.resolve_current_composite({"blocks": [b]}, [], "1d")["kind"] == "none"


GIT = "g" * 40


def _write_bars(results_dir: Path, wrid: str, forecasts, t0="2020-01-01", tz=None,
                data_sha="d" * 64, git_sha=GIT):
    """bars.csv with timestamp/close/forecast (+ the window's manifest.json);
    closes are a fixed random walk so next-bar returns are identical for every
    config run on the same bars."""
    import pandas as pd
    rng = random.Random(42)
    closes, c = [], 100.0
    for _ in forecasts:
        closes.append(c)
        c *= 1.0 + rng.gauss(0.0, 0.01)
    ts = pd.date_range(t0, periods=len(forecasts), freq="h", tz=tz)
    d = results_dir / wrid
    d.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"timestamp": ts, "close": closes, "forecast": forecasts}).to_csv(
        d / "bars.csv", index=False)
    (d / "manifest.json").write_text(json.dumps({"git_sha": git_sha,
                                                 "data": {"data_sha256": data_sha}}),
                                     encoding="utf-8")


def _summary(wrid):
    return {"results": [{"symbol": "BTCUSDT", "window": "2020-01", "run_id": wrid,
                         "core": {"trade_count": 10}}],
            "per_symbol_summary": {}, "verdict": "kill",
            "hypothesis_verdict": {"verdict": "refine", "diagnostics": {}}}


def _seal() -> tuple:
    """The sealed range, read at run time from campaign_data_policy.yaml (the
    sandbox holds a verbatim copy) -- never written literally here."""
    return rpr._load_holdout_range()


def _protocol() -> dict:
    start, end = _seal()
    return {"symbols": ["BTCUSDT"], "timeframe": "1h",
            "windows": [{"label": "2020-01", "test": {"start": "2020-01-01", "end": "2020-02-10"}}],
            "holdout": {"start": start, "end": end}}


def _composite_runner(forecasts, calls, **bars_kw):
    def run(config_path, protocol_path, out_dir):
        calls.append(Path(config_path))
        _write_bars(Path(out_dir) / "results", "wr_comp", forecasts, **bars_kw)
        (Path(out_dir) / "protocol_summary.json").write_text(json.dumps(_summary("wr_comp")),
                                                             encoding="utf-8")
    return run


FP = {"git_sha": GIT, "data": {"BTCUSDT|2020-01": "d" * 64}}


def _series(resolved, proto, runner, fp=FP):
    return cc.composite_series(resolved, root=rpr.ROOT, protocol_path=proto,
                               holdout_range=_seal(), candidate_fingerprint=fp, runner=runner)


def _config_on_disk(rel="runs/run_700/artifacts/variants/base/strategy_config.json"):
    p = rpr.ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(BASE_CONFIG), encoding="utf-8")
    return rel, hashlib.sha256(json.dumps(BASE_CONFIG, sort_keys=True).encode()).hexdigest()


def _resolved(rel, sha, registry_hash="0123456789abcdef"):
    return {"kind": "block", "timeframe": "1h", "registry_hash": registry_hash,
            "block_ids": ["H1:run_700"], "config_ref": rel, "expected_config_sha256": sha,
            "reason": None}


def test_composite_series_is_computed_once_then_cached():
    rel, sha = _config_on_disk()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    calls = []
    runner = _composite_runner(Z_COMP[:900], calls)
    recs, steps, cache_dir = _series(_resolved(rel, sha), proto, runner)
    assert len(calls) == 1 and len(recs["BTCUSDT"]) == 899  # last bar has no next return
    assert cache_dir.parent == rpr.ROOT / "campaign_record" / "composite" / "0123456789abcdef"
    meta = yaml.safe_load((cache_dir / "composite.yaml").read_text(encoding="utf-8"))
    assert meta["config_sha256"] == sha and meta["kind"] == "block"
    assert meta["engine_git_sha"] == GIT
    again, _, dir2 = _series(_resolved(rel, sha), proto, runner)
    assert len(calls) == 1 and dir2 == cache_dir and again == recs
    # not a trial: nothing touched the trial ledger
    assert not rpr.CAMPAIGN_STATE_PATH.exists()


def test_cache_hit_with_missing_bars_is_recomputed():
    """Review fix 1."""
    rel, sha = _config_on_disk()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    calls = []
    runner = _composite_runner(Z_COMP[:900], calls)
    _, _, cache_dir = _series(_resolved(rel, sha), proto, runner)
    (cache_dir / "results" / "wr_comp" / "bars.csv").unlink()
    recs, _, _ = _series(_resolved(rel, sha), proto, runner)
    assert len(calls) == 2 and len(recs["BTCUSDT"]) == 899


def test_cache_key_covers_engine_and_market_data():
    """Review fix 2: another engine version or other data -> another entry;
    a composite that read different data from the candidate is refused."""
    rel, sha = _config_on_disk()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    calls = []
    _, _, d1 = _series(_resolved(rel, sha), proto, _composite_runner(Z_COMP[:900], calls))
    fp2 = {"git_sha": "h" * 40, "data": FP["data"]}
    _, _, d2 = _series(_resolved(rel, sha), proto,
                       _composite_runner(Z_COMP[:900], calls, git_sha="h" * 40), fp=fp2)
    assert len(calls) == 2 and d1 != d2
    fp3 = {"git_sha": GIT, "data": {"BTCUSDT|2020-01": "e" * 64}}
    with pytest.raises(cc.CompositeError, match="different market data"):
        _series(_resolved(rel, sha), proto, _composite_runner(Z_COMP[:900], calls), fp=fp3)


def test_cache_writes_are_locked(monkeypatch):
    """Review fix 2: a held lock (a concurrent miss) is waited on, never raced."""
    import campaign_lock
    rel, sha = _config_on_disk()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    parent = rpr.ROOT / "campaign_record" / "composite" / "0123456789abcdef"
    parent.mkdir(parents=True)
    campaign_lock.acquire(parent / cc.COMPOSITE_LOCK_FILENAME)
    monkeypatch.setattr(cc, "COMPOSITE_LOCK_WAIT_SECONDS", 0.2)
    calls = []
    try:
        with pytest.raises(cc.CompositeError, match="still held"):
            _series(_resolved(rel, sha), proto, _composite_runner(Z_COMP[:900], calls))
    finally:
        campaign_lock.release(parent / cc.COMPOSITE_LOCK_FILENAME)
    assert calls == []


def test_composite_never_reaches_the_holdout():
    rel, sha = _config_on_disk()
    bad = _protocol()
    seal_start, _ = _seal()  # a window on the seal's first day
    bad["windows"].append({"label": seal_start[:7], "test": {"start": seal_start, "end": seal_start}})
    proto = _write_protocol(rpr.ROOT, "bad.json", bad)
    calls = []
    with pytest.raises(cc.CompositeError, match="holdout"):
        _series(_resolved(rel, sha), proto, _composite_runner([1.0], calls))
    assert calls == []


@pytest.mark.parametrize("test_dates", [None, {"start": "2020-01-01"}, {"start": "2020-01-01",
                                        "end": "someday"}, {"start": 20200101, "end": "2020-02-01"}])
def test_holdout_guard_fails_closed_on_missing_or_non_iso_dates(test_dates):
    """Review fix 9: reuses _load_holdout_range + HoldoutBoundaryBreach."""
    proto = _protocol()
    w = {"label": "2020-03"}
    if test_dates is not None:
        w["test"] = test_dates
    proto["windows"].append(w)
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        cc.check_protocol_outside_holdout(proto, rpr._load_holdout_range(),
                                          breach_cls=rpr.HoldoutBoundaryBreach)
    cc.check_protocol_outside_holdout(_protocol(), rpr._load_holdout_range(),
                                      breach_cls=rpr.HoldoutBoundaryBreach)  # clean one passes


def test_composite_refuses_the_sealed_store_and_a_changed_config():
    rel, sha = _config_on_disk()
    sealed = rpr.ROOT / "local_data" / "holdout_sealed" / "p.json"
    sealed.parent.mkdir(parents=True)
    sealed.write_text(json.dumps(_protocol()), encoding="utf-8")
    with pytest.raises(cc.CompositeError, match="holdout_sealed"):
        _series(_resolved(rel, sha), sealed, lambda *a: None)
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    with pytest.raises(cc.CompositeError, match="changed"):
        _series(_resolved(rel, "f" * 64), proto, lambda *a: None)


def _registry_file(blocks):
    path = rpr._block_registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    full = []
    for b in blocks:
        full.append({**{f: None for f in br.BLOCK_FIELDS}, "hypothesis_id": "H",
                     "criteria_passed": ["c"], "variants_passed": ["base"], "numbers": {},
                     "symbols_tested": [], "regime_assignment": {"regimes": [], "detector_paths": []},
                     "config_fragment": {}, "validated_by_run": "run_x", "registered_at": "t",
                     "timeframe_category": cc.timeframe_category(b["timeframe"]), **b})
    path.write_text(yaml.safe_dump({"schema_version": 1, "revision": len(full),
                                    "updated_at": None, "blocks": full}), encoding="utf-8")
    return path


def _variant_results(run_dir, forecasts_by_vid):
    out = {}
    for vid, f in forecasts_by_vid.items():
        res = run_dir / "variants" / vid / "results"
        _write_bars(res, f"wr_{vid}", f)
        out[vid] = res
    return out


@pytest.mark.parametrize("n_blocks", [0, 1, 2])
def test_residual_ic_by_variant_for_0_1_2_blocks(n_blocks):
    rel, sha = _config_on_disk()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    blocks = [_block("H1:run_700", ref=rel, sha=sha), _block("H2:run_701")][:n_blocks]
    reg = _registry_file(blocks)
    run_dir = rpr.ROOT / "runs" / "run_800"
    n = 900
    results = _variant_results(run_dir, {"base": Z_COMP[:n], "other": Z_CAND[:n]})
    summaries = {v: _summary(f"wr_{v}") for v in results}
    calls = []
    doc = cc.residual_ic_by_variant(
        summaries, results, root=rpr.ROOT, protocol_path=proto, registry_path=reg,
        compositions_path=rpr.ROOT / "campaign_record" / "compositions.yaml",
        holdout_range=_seal(), runner=_composite_runner(Z_COMP[:n], calls))
    assert doc["timeframe"] == "1h" and doc["timeframe_category"] == "low"
    base, other = doc["variants"]["base"], doc["variants"]["other"]
    if n_blocks == 0:
        assert doc["composite"]["kind"] == "none" and calls == []
        assert base["composite"] == "none" and base["value"] is not None
    elif n_blocks == 1:
        assert doc["composite"]["kind"] == "block" and len(calls) == 1
        # the base variant IS the composite -> fully explained; the other is not
        assert base["fully_explained"] is True and base["value"] is None
        assert other["fully_explained"] is False and other["value"] is not None
        assert base["n_eff"] == (n - 1) // 24
        assert base["composite_registry_hash"] == doc["composite"]["registry_hash"]
    else:
        assert doc["composite"]["kind"] == "stale" and calls == []
        assert base["composite"] == "STALE" and base["value"] is None
        pre_reg = {"pass_rule": {"criteria": [_menu_residual_crit()]}}
        pr = {**summaries["base"], "hypothesis_verdict": {"diagnostics": {"residual_ic": base}}}
        grid = vce.evaluate_grid({"base": pr}, pre_reg, {}, REAL_MENU, composition_runs=True)
        assert grid["grid"]["residual_ic"]["base"]["result"] == "INCONCLUSIVE"
    assert not rpr.CAMPAIGN_STATE_PATH.exists()  # no trial row, ever


def test_exempt_run_computes_nothing_and_runs_no_subprocess():
    """Review fix 5: an exempt idea skips the residual IC and its composite run."""
    rel, sha = _config_on_disk()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    reg = _registry_file([_block("H1:run_700", ref=rel, sha=sha)])
    calls = []
    doc = cc.residual_ic_by_variant(
        {"base": _summary("wr_base")}, {"base": rpr.ROOT / "nowhere"}, root=rpr.ROOT,
        protocol_path=proto, registry_path=reg,
        compositions_path=rpr.ROOT / "campaign_record" / "compositions.yaml",
        holdout_range=_seal(), exempt_reason="regime block",
        runner=_composite_runner(Z_COMP[:10], calls))
    assert doc["skipped"] == "regime block" and doc["variants"] == {} and calls == []
    assert doc["timeframe"] == "1h" and doc["timeframe_category"] == "low"


# ---------------------------------------------------------------------------
# 5b. Review fixes 1, 8, 10: coverage, tz, finiteness, ordering
# ---------------------------------------------------------------------------

def test_low_composite_coverage_is_inconclusive():
    cand = _recs(Z_CAND[:200], RETS[:200])
    comp = _recs(Z_COMP[:200], RETS[:200])[:170]  # 85% of the candidate's bars
    d = ric.compute_residual_ic({"BTCUSDT": cand}, {"BTCUSDT": comp}, block_size=1,
                                composite_label="block")
    assert d["value"] is None and d["reason"].startswith("composite_coverage")
    assert d["coverage_by_symbol"] == {"BTCUSDT": 0.85}
    assert ric.MIN_COMPOSITE_COVERAGE == 0.9
    ok = ric.compute_residual_ic({"BTCUSDT": cand}, {"BTCUSDT": _recs(Z_COMP[:200], RETS[:200])[:180]},
                                 block_size=1, composite_label="block")
    assert ok["value"] is not None  # exactly 90% is enough


def test_composite_missing_a_symbol_is_inconclusive():
    cand = {"BTCUSDT": _recs(Z_CAND[:100], RETS[:100]), "ETHUSDT": _recs(Z_CAND[:100], RETS[:100])}
    comp = {"BTCUSDT": _recs(Z_COMP[:100], RETS[:100])}
    d = ric.compute_residual_ic(cand, comp, block_size=1, composite_label="block")
    assert d["value"] is None and "ETHUSDT" in d["reason"]


def test_timestamps_are_utc_normalised_before_the_join():
    import pandas as pd
    base = pd.Timestamp("2020-01-01 00:00")
    naive = [{"timestamp": base + pd.Timedelta(hours=i), "forecast": f, "next_return_bps": r}
             for i, (f, r) in enumerate(zip(Z_CAND[:300], RETS[:300]))]
    aware = [{"timestamp": (base + pd.Timedelta(hours=i)).tz_localize("UTC").tz_convert("Europe/Paris"),
              "forecast": f, "next_return_bps": r}
             for i, (f, r) in enumerate(zip(Z_COMP[:300], RETS[:300]))]
    d = ric.compute_residual_ic({"BTCUSDT": naive}, {"BTCUSDT": aware}, block_size=24,
                                expected_step_by_symbol={"BTCUSDT": pd.Timedelta(hours=1)},
                                composite_label="block")
    assert d["n_bars"] == 300 and d["n_dropped_candidate_only"] == 0 and d["value"] is not None
    assert d["n_eff"] == 300 // 24


@pytest.mark.parametrize("where", ["forecast", "return", "composite"])
def test_non_finite_inputs_are_rejected_never_ranked(where):
    cand = _recs(Z_CAND[:100], RETS[:100])
    comp = _recs(Z_COMP[:100], RETS[:100])
    if where == "forecast":
        cand[5]["forecast"] = float("nan")
    elif where == "return":
        cand[7]["next_return_bps"] = float("inf")
    else:
        comp[9]["forecast"] = float("nan")
    d = ric.compute_residual_ic({"BTCUSDT": cand}, {"BTCUSDT": comp}, block_size=1,
                                composite_label="block")
    assert d["value"] is None and d["reason"].startswith("non_finite")


def test_out_of_order_records_are_refused():
    cand = _recs(Z_CAND[:50], RETS[:50])
    cand[10], cand[11] = cand[11], cand[10]
    with pytest.raises(ric.RecordOrderError):
        ric.compute_residual_ic({"BTCUSDT": cand}, None, block_size=1)


def test_reader_sorts_by_timestamp_not_window_label(tmp_path):
    """Two windows whose labels sort opposite to their times."""
    res = tmp_path / "results"
    _write_bars(res, "wr_late", [1.0, 2.0, 3.0], t0="2020-03-01")
    _write_bars(res, "wr_early", [4.0, 5.0, 6.0], t0="2020-01-01")
    summary = {"results": [
        {"symbol": "BTCUSDT", "window": "a_late", "run_id": "wr_late"},
        {"symbol": "BTCUSDT", "window": "b_early", "run_id": "wr_early"}]}
    recs, _ = ric.symbol_records_from_protocol_result(summary, res)
    ts = [r["timestamp"] for r in recs["BTCUSDT"]]
    assert ts == sorted(ts) and [r["forecast"] for r in recs["BTCUSDT"]] == [4.0, 5.0, 1.0, 2.0]
    ric.compute_residual_ic(recs, None, block_size=1)  # accepted: strictly increasing


# ---------------------------------------------------------------------------
# 6. Registry fields + schema
# ---------------------------------------------------------------------------

def _registry_run(run_id="run_750", diag=None, timeframe="1h"):
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(MANIFEST), encoding="utf-8")
    cfg = arts / "candidate_strategy_config.json"
    cfg.write_text(json.dumps(BASE_CONFIG), encoding="utf-8")
    sha = hashlib.sha256(json.dumps(BASE_CONFIG, sort_keys=True).encode("utf-8")).hexdigest()
    entry = {"run_id": run_id, "hypothesis_id": "H-1", "legacy": False, "idea_status": "validated",
             "engineering_fault": None,
             "variants": {"base": {"status": "tested", "config_ref": cfg.relative_to(rpr.ROOT).as_posix(),
                                   "forecast_hash": sha, "symbols": ["BTCUSDT"]}},
             "grid": {"criteria": ["residual_ic"], "variants": ["base"],
                      "cells": {"residual_ic": {"base": {"result": "PASS", "value": 0.05,
                                                         "threshold": 0.01}}}}}
    if diag is not None:
        rpr.save_yaml(arts / "residual_ic.yaml", {
            "timeframe": timeframe, "timeframe_category": cc.timeframe_category(timeframe),
            "composite": {"kind": "block"}, "variants": {"base": diag}})
    return run_dir, entry


DIAG = {"value": 0.05, "n_eff": 41, "p_value": 0.2, "p_value_one_sided": 0.1,
        "fully_explained": False,
        "correlation_to_composite": 0.31, "composite": "block",
        "composite_registry_hash": "0123456789abcdef", "n_bars": 999}


def _schema_validate(doc):
    import jsonschema
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" /
                         "block_registry.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(doc, schema)


def test_registry_flag_off_block_is_the_e058_shape():
    run_dir, entry = _registry_run(diag=DIAG)
    block = br.build_block(run_dir, entry, br.load_manifest(run_dir), root=rpr.ROOT)
    assert tuple(block) == br.BLOCK_FIELDS
    assert block["residual_ic"] is None and block["correlation_to_composite"] is None
    _schema_validate({"schema_version": 1, "revision": 1, "updated_at": None, "blocks": [block]})


def test_registry_flag_on_records_timeframe_and_residual_ic():
    run_dir, entry = _registry_run(diag=DIAG, timeframe="4h")
    block = br.build_block(run_dir, entry, br.load_manifest(run_dir), root=rpr.ROOT,
                           composition_runs=True)
    assert block["timeframe"] == "4h" and block["timeframe_category"] == "low"
    assert block["residual_ic"] == {"value": 0.05, "n_eff": 41, "p_value": 0.2,
                                    "p_value_one_sided": 0.1,
                                    "fully_explained": False, "composite": "block",
                                    "composite_registry_hash": "0123456789abcdef"}
    assert block["correlation_to_composite"] == {"value": 0.31, "composite": "block",
                                                 "composite_registry_hash": "0123456789abcdef"}
    doc = {"schema_version": 1, "revision": 1, "updated_at": None, "blocks": [block]}
    _schema_validate(doc)
    path = rpr._block_registry_path()
    br.record_run(path, run_dir, entry, root=rpr.ROOT, composition_runs=True)
    loaded = br.load_registry(path)
    assert loaded["blocks"][0]["timeframe"] == "4h"


def test_registry_flag_on_without_the_artifact_is_absent_by_design(capsys):
    """Review fix 5: protocol_execution ran with the flag off -> no raise,
    the E-058 shape, a loud line."""
    run_dir, entry = _registry_run(diag=None)
    block = br.build_block(run_dir, entry, br.load_manifest(run_dir), root=rpr.ROOT,
                           composition_runs=True)
    assert tuple(block) == br.BLOCK_FIELDS and block["residual_ic"] is None
    assert "residual_ic.yaml" in capsys.readouterr().out


def test_registry_skipped_artifact_records_timeframe_only():
    run_dir, entry = _registry_run(diag=None)
    rpr.save_yaml(run_dir / "artifacts" / "residual_ic.yaml",
                  {"timeframe": "1d", "timeframe_category": "daily", "skipped": "regime block",
                   "composite": None, "variants": {}})
    block = br.build_block(run_dir, entry, br.load_manifest(run_dir), root=rpr.ROOT,
                           composition_runs=True)
    assert block["timeframe"] == "1d" and block["residual_ic"] is None


def test_registry_present_artifact_without_the_base_variant_raises():
    run_dir, entry = _registry_run(diag=None)
    rpr.save_yaml(run_dir / "artifacts" / "residual_ic.yaml",
                  {"timeframe": "1h", "timeframe_category": "low", "skipped": None,
                   "variants": {"other": DIAG}})
    with pytest.raises(br.BlockRegistryError, match="base variant"):
        br.build_block(run_dir, entry, br.load_manifest(run_dir), root=rpr.ROOT,
                       composition_runs=True)


def test_registry_schema_and_loader_reject_half_a_timeframe():
    import jsonschema
    run_dir, entry = _registry_run(diag=DIAG)
    block = br.build_block(run_dir, entry, br.load_manifest(run_dir), root=rpr.ROOT,
                           composition_runs=True)
    del block["timeframe_category"]
    doc = {"schema_version": 1, "revision": 1, "updated_at": None, "blocks": [block]}
    with pytest.raises(jsonschema.ValidationError):
        _schema_validate(doc)
    path = rpr._block_registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc), encoding="utf-8")
    with pytest.raises(br.BlockRegistryError, match="written together"):
        br.load_registry(path)
    bad = dict(block, timeframe_category="weekly")
    with pytest.raises(jsonschema.ValidationError):
        _schema_validate({**doc, "blocks": [bad]})


# ---------------------------------------------------------------------------
# 7. The flag: reader, 1a append, protocol_execution wiring, flag-off identity
# ---------------------------------------------------------------------------

def test_flag_absent_is_off():
    assert rpr._composition_runs_enabled() is False


@pytest.mark.parametrize("missing", ["decide_next", "variant_loop", "profit_bars_every_backtest",
                                     "verdict_routing_retired"])
def test_flag_raises_without_each_dependency(missing):
    _set_orchestrator({**COMP_ON, missing: {"enabled": False}})
    with pytest.raises(ValueError, match="requires"):
        rpr._composition_runs_enabled()


def test_flag_on_with_every_dependency():
    _set_orchestrator(COMP_ON)
    assert rpr._composition_runs_enabled() is True


def test_flag_non_bool_raises():
    _set_orchestrator({"composition_runs": {"enabled": "true"}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._composition_runs_enabled()


def test_code_appends_residual_ic_replacing_any_1a_version():
    rule = {"criteria": [{"id": "sign_consistent_by_era", "source": "window"},
                         {"id": "residual_ic", "threshold": 0.5}]}
    out = rpr._with_residual_ic_criterion(rule, REAL_MENU)
    assert [c["id"] for c in out["criteria"]] == ["sign_consistent_by_era", "residual_ic"]
    assert out["criteria"][-1] == _menu_residual_crit()
    assert rule["criteria"][1]["threshold"] == 0.5  # input not mutated


def _brief(run_dir, brief):
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)


def test_exemptions_regime_and_composition():
    run_dir = _minimal_run(rpr.ROOT, "run_760")
    assert rpr._residual_ic_exempt_reason(run_dir) is None
    _brief(run_dir, {"candidate": {"source": {"proposal": {"kind": "new_block",
                                                          "block": {"kind": "regime"}}}}})
    assert rpr._residual_ic_exempt_reason(run_dir) == "regime block"
    _brief(run_dir, {"candidate": {"manifest": {"block": {"kind": "regime"}}, "source": {}}})
    assert rpr._residual_ic_exempt_reason(run_dir) == "regime block"
    _brief(run_dir, {"candidate": {"source": {"origin": "composition"}}})
    assert rpr._residual_ic_exempt_reason(run_dir) == "composition run"
    _brief(run_dir, {"candidate": {"manifest": {"block": {"kind": "forecast"}}, "source": {}}})
    assert rpr._residual_ic_exempt_reason(run_dir) is None


def test_regime_idea_from_an_ordinary_brief_is_exempt_via_manifest_or_card():
    """Review fix 6: no candidate block -- 1b's manifest (or a card kind) decides."""
    run_dir = _minimal_run(rpr.ROOT, "run_762")
    _brief(run_dir, {"research_goal": "a detector idea"})
    assert rpr._residual_ic_exempt_reason(run_dir) is None
    rpr.save_yaml(run_dir / "artifacts" / "block_manifest.yaml",
                  {"block": {"kind": "regime", "config_paths": ["/regime_detector"]}})
    assert rpr._residual_ic_exempt_reason(run_dir) == "regime block"
    (run_dir / "artifacts" / "block_manifest.yaml").unlink()
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml",
                  {"hypothesis_id": "H", "block": {"kind": "regime"}})
    assert rpr._residual_ic_exempt_reason(run_dir) == "regime block"


def _menu_into_sandbox():
    (rpr.ROOT / "config" / "criterion_menu.yaml").write_text(
        (SR_ROOT / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"), encoding="utf-8")


def test_ensure_residual_ic_on_a_1a_written_pass_rule():
    _menu_into_sandbox()
    run_dir = _minimal_run(rpr.ROOT, "run_761")
    pre = {"machine_constraints": {"pass_rule": {"criteria": [
        {"id": "sign_consistent_by_era", "source": "window"}]}}}
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", pre)
    assert rpr._ensure_residual_ic_in_pre_registration(run_dir) is True
    doc = rpr.load_yaml(run_dir / "artifacts" / "pre_registration.yaml")
    assert [c["id"] for c in doc["machine_constraints"]["pass_rule"]["criteria"]] == \
        ["sign_consistent_by_era", "residual_ic"]
    assert rpr._ensure_residual_ic_in_pre_registration(run_dir) is False  # idempotent
    # a legacy prose pass_rule is left alone
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {"pass_rule": "IC > 0.02"})
    assert rpr._ensure_residual_ic_in_pre_registration(run_dir) is False


def _variant_loop_run(monkeypatch, run_id, flag_on, manifest_kind=None):
    """A 2-variant protocol_execution with a fake subprocess writing bars.csv;
    grid on; pre_registration carries a menu criterion (+ residual_ic when on)."""
    if manifest_kind:
        arts0 = rpr.ROOT / "runs" / run_id / "artifacts"
        arts0.mkdir(parents=True, exist_ok=True)
        rpr.save_yaml(arts0 / "block_manifest.yaml",
                      {"block": {"kind": manifest_kind, "config_paths": ["/x"]}})
    _set_orchestrator({"config_direct_authoring": {"enabled": True},
                       "variant_loop": {"enabled": True}, "grid_evaluation": {"enabled": True}})
    monkeypatch.setattr(rpr, "_composition_runs_enabled", lambda: flag_on)
    _menu_into_sandbox()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    (arts / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": "protocols/p1h.json"})
    vdir = arts / "variants"
    for vid in ("base", "other"):
        (vdir / vid).mkdir(parents=True, exist_ok=True)
        (vdir / vid / "strategy_config.json").write_text(json.dumps({"variant": vid}), encoding="utf-8")
    rpr.save_yaml(vdir / "index.yaml", {"variants": {
        v: {"status": "validated", "config_path": f"artifacts/variants/{v}/strategy_config.json"}
        for v in ("base", "other")}})
    crits = [{"id": "realized_edge_to_cost_ratio", "source": "pooled"}]
    if flag_on:
        crits = rpr._with_residual_ic_criterion({"criteria": crits}, REAL_MENU)["criteria"]
    rpr.save_yaml(arts / "pre_registration.yaml", {"pass_rule": {"criteria": crits}})
    forecasts = {"base": Z_CAND[:900], "other": Z_COMP[:900]}

    def fake_run(cmd, *a, **k):
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        vid = Path(cmd[2]).parent.name
        _write_bars(out_dir / "results", f"wr_{vid}", forecasts[vid])
        s = _summary(f"wr_{vid}")
        s["trade_diagnostics_summary"] = {"realized_edge_to_cost_ratio": 0.5}
        (out_dir / "protocol_summary.json").write_text(json.dumps(s), encoding="utf-8")

        class _Ok:
            returncode, stdout, stderr = 0, "", ""
        return _Ok()
    monkeypatch.setattr(rpr.subprocess, "run", fake_run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))
    return run_dir, proto


def test_protocol_execution_flag_off_writes_nothing_new(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("flag off must never compute a residual IC")
    monkeypatch.setattr(rpr, "_residual_ic_grid_inputs", boom)
    run_dir, _ = _variant_loop_run(monkeypatch, "run_770", flag_on=False)
    arts = run_dir / "artifacts"
    assert not (arts / "residual_ic.yaml").exists()
    assert not (rpr.ROOT / "campaign_record").exists()
    grid = rpr.load_yaml(arts / "grid_evaluation.yaml")
    assert grid["criteria"] == ["realized_edge_to_cost_ratio"]
    # the grid is exactly evaluate_grid on the saved per-variant results
    saved = {v: rpr.load_yaml(arts / "variants" / v / "protocol_result.yaml") for v in ("base", "other")}
    expect = vce.evaluate_grid(saved, rpr.load_yaml(arts / "pre_registration.yaml"),
                               {}, REAL_MENU)
    grid.pop("evaluated_at")
    assert grid == expect


def test_protocol_execution_flag_on_grades_residual_ic_without_touching_saved_results(monkeypatch):
    run_dir, _ = _variant_loop_run(monkeypatch, "run_771", flag_on=True)
    arts = run_dir / "artifacts"
    doc = rpr.load_yaml(arts / "residual_ic.yaml")
    assert doc["composite"]["kind"] == "none" and set(doc["variants"]) == {"base", "other"}
    grid = rpr.load_yaml(arts / "grid_evaluation.yaml")
    assert grid["criteria"] == ["realized_edge_to_cost_ratio", "residual_ic"]
    cell = grid["grid"]["residual_ic"]["base"]
    assert cell["n_eff"] == doc["variants"]["base"]["n_eff"] == 899 // 24
    assert cell["result"] in ("PASS", "FAIL")
    # the saved protocol results and the trial rows are untouched by the injection
    saved = rpr.load_yaml(arts / "variants" / "base" / "protocol_result.yaml")
    assert "residual_ic" not in saved["hypothesis_verdict"]["diagnostics"]
    rows = rpr.load_campaign_state()["trial_sharpes"]
    assert sorted(r["trial_id"] for r in rows) == ["run_771:base", "run_771:other"]


def test_protocol_execution_regime_idea_is_exempt_at_grid_time(monkeypatch):
    """Review fix 6: 1a appended residual_ic before the manifest existed; at
    grid time the regime manifest exempts it -- nothing computed, not graded."""
    calls = []
    real_series = cc.composite_series
    monkeypatch.setattr(cc, "composite_series",
                        lambda *a, **k: calls.append(1) or real_series(*a, **k))
    run_dir, _ = _variant_loop_run(monkeypatch, "run_772", flag_on=True, manifest_kind="regime")
    arts = run_dir / "artifacts"
    doc = rpr.load_yaml(arts / "residual_ic.yaml")
    assert doc["skipped"] == "regime block" and doc["variants"] == {} and calls == []
    grid = rpr.load_yaml(arts / "grid_evaluation.yaml")
    assert grid["criteria"] == ["realized_edge_to_cost_ratio"]
