"""
E-060 S3a -- weighting schemes, code-written composition variants and the
compositions.yaml writer (tools/composition.py), behind
orchestrator.composition_runs.enabled. Engine-side standardisation is pinned
in trading-bot/tests/test_e060_block_standardisation.py; here the written
configs are loaded by the real validator and the real AdvancedStrategy.

No LLM, no backtest, no market data: synthetic bars, temp roots.
"""
import copy
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))

import composite_cache as cc  # noqa: E402
import composition as comp  # noqa: E402
import campaign_memory as cm  # noqa: E402

PE = "strategies.strategy_components.PriceEvolutionComponent"


def _canon(cfg) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode("utf-8")).hexdigest()


def _source_config(period, transforms, aux=None, warmup=51):
    cfg = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                               "default_regime": "unknown"},
           "strategies": {"warmup": warmup, "regimes": {
               "unknown": {"components": [
                   {"id": "sig", "class": PE, "params": {"period": period}, "weight": 1.0,
                    "transforms": transforms}]},
               "trending": None, "mean_reversion": None, "chop": None}}}
    if aux:
        cfg["aux_feeds"] = aux
    return cfg


def _registry(root: Path, n=2, tf="1h", ics=(0.03, 0.01), extra=None):
    """A registry doc with n forecast blocks on `tf`, their tested configs on disk."""
    blocks = []
    for k in range(n):
        bid = f"H-{k}:run_90{k}"
        cfg = _source_config(5 + 7 * k, [{"op": "identity"}, {"op": "scale", "params": {"factor": 10 ** k}}],
                             warmup=40 + k)
        ref = f"runs/run_90{k}/artifacts/variants/base/strategy_config.json"
        (root / ref).parent.mkdir(parents=True, exist_ok=True)
        (root / ref).write_text(json.dumps(cfg), encoding="utf-8")
        blocks.append({
            "block_id": bid, "hypothesis_id": f"H-{k}", "kind": "forecast",
            "config_fragment": {"/strategies/regimes/unknown/components/0":
                                cfg["strategies"]["regimes"]["unknown"]["components"][0]},
            "regime_assignment": {"regimes": ["unknown"], "detector_paths": []},
            "criteria_passed": [], "variants_passed": [], "numbers": {}, "symbols_tested": ["BTCUSDT"],
            "correlation_to_composite": {"value": None},
            "residual_ic": {"value": ics[k % len(ics)], "n_eff": 60, "fully_explained": False},
            "source_config_ref": ref, "source_config_sha256": _canon(cfg),
            "validated_by_run": f"run_90{k}", "registered_at": "x",
            "timeframe": tf, "timeframe_category": cc.timeframe_category(tf)})
    blocks += extra or []
    return {"schema_version": 1, "revision": len(blocks), "updated_at": None, "blocks": blocks}


def _returns(sigma, n=60, seed=0):
    rng = np.random.default_rng(seed)
    r = rng.normal(0.0, 1.0, n)
    r = (r - r.mean()) / r.std(ddof=1)
    return list(r * sigma)


def _rets_for(doc, sigmas=(0.01, 0.03)):
    return {b["block_id"]: _returns(sigmas[i % len(sigmas)], seed=i)
            for i, b in enumerate(doc["blocks"])}


# --- 1. weighting schemes ----------------------------------------------------

def test_equal_weights():
    assert comp.equal_weights(["b", "a", "c"]) == {"a": 1 / 3, "b": 1 / 3, "c": 1 / 3}


def test_inverse_vol_weights_proportional_to_one_over_sigma():
    w = comp.inverse_vol_weights({"a": _returns(0.01), "b": _returns(0.03, seed=1)}, ["a", "b"])
    assert w["a"] == pytest.approx(0.75, rel=1e-12) and w["b"] == pytest.approx(0.25, rel=1e-12)
    assert sum(w.values()) == pytest.approx(1.0, abs=1e-15)


def test_ic_weights_proportional_to_residual_ic():
    blocks = [{"block_id": "a", "residual_ic": {"value": 0.03}},
              {"block_id": "b", "residual_ic": {"value": 0.01}}]
    assert comp.ic_weights(blocks) == {"a": pytest.approx(0.75), "b": pytest.approx(0.25)}


@pytest.mark.parametrize("fn", [
    lambda: comp.equal_weights(["a"]),
    lambda: comp.inverse_vol_weights({"a": _returns(0.01)}, ["a"]),
    lambda: comp.ic_weights([{"block_id": "a", "residual_ic": {"value": 0.02}}]),
    lambda: comp.equal_weights(["a", "a"]),
])
def test_single_block_or_duplicate_fails_loud(fn):
    with pytest.raises(comp.CompositionError):
        fn()


@pytest.mark.parametrize("series, needle", [
    (None, "no stand-alone daily return series"),
    ("missing", "no stand-alone daily return series"),
    ([0.01] * 60, "no variance"),
    ([0.01, -0.01] * 5, "at least"),
    ([0.01, float("nan")] * 30, "non-finite"),
    (["x"] * 60, "not numbers"),
])
def test_inverse_vol_degenerate_series_fail_loud(series, needle):
    rets = {"a": _returns(0.01)}
    if series != "missing":
        rets["b"] = series
    with pytest.raises(comp.CompositionError, match=needle):
        comp.inverse_vol_weights(rets, ["a", "b"])


@pytest.mark.parametrize("ric, needle", [
    ({"value": 0.0}, "zero or negative"),
    ({"value": -0.02}, "zero or negative"),
    ({"value": None}, "not a finite number"),
    ({"value": float("inf")}, "not a finite number"),
    ({"value": True}, "not a finite number"),
    ({"value": None, "fully_explained": True}, "fully_explained"),
    (None, "no residual IC"),
])
def test_ic_weights_degenerate_fail_loud(ric, needle):
    blocks = [{"block_id": "a", "residual_ic": {"value": 0.02}},
              {"block_id": "b", "residual_ic": ric}]
    with pytest.raises(comp.CompositionError, match=needle):
        comp.ic_weights(blocks)


# --- 3. the variant writer ---------------------------------------------------

def _write(tmp_path, doc=None, rets=None, tf="1h", enabled=True):
    doc = doc or _registry(tmp_path)
    out = tmp_path / "campaign_record" / "compositions" / "c1"
    m = comp.write_composition_variants(doc, tf, out, root=tmp_path,
                                        daily_returns_by_block=rets or _rets_for(doc),
                                        enabled=enabled)
    return doc, out, m


def test_writer_refuses_with_flag_off(tmp_path):
    with pytest.raises(comp.CompositionError, match="composition_runs is off"):
        _write(tmp_path, enabled=False)
    with pytest.raises(comp.CompositionError, match="composition_runs is off"):
        _write(tmp_path, enabled="true")  # strict: only the boolean True
    assert not (tmp_path / "campaign_record").exists()


def test_writer_produces_three_valid_configs_and_a_manifest(tmp_path):
    doc, out, m = _write(tmp_path)
    assert sorted(p.name for p in out.iterdir()) == [
        "base.json", "composition_manifest.yaml", "ic_weighted.json", "vol_scaled.json"]
    on_disk = yaml.safe_load((out / "composition_manifest.yaml").read_text(encoding="utf-8"))
    assert on_disk == m
    assert m["registry_hash"] == cc.composite_registry_hash(doc["blocks"])
    assert m["timeframe"] == "1h" and m["timeframe_category"] == "low"
    assert [b["block_id"] for b in m["blocks"]] == ["H-0:run_900", "H-1:run_901"]
    assert m["variants"]["base"]["weights"] == {"H-0:run_900": 0.5, "H-1:run_901": 0.5}
    assert m["variants"]["vol_scaled"]["weights"]["H-0:run_900"] == pytest.approx(0.75)
    assert m["variants"]["ic_weighted"]["weights"]["H-0:run_900"] == pytest.approx(0.75)
    cfgs = {vid: json.loads((out / f"{vid}.json").read_text(encoding="utf-8"))
            for vid in ("base", "vol_scaled", "ic_weighted")}
    for vid, cfg in cfgs.items():
        assert m["variants"][vid]["config_sha256"] == _canon(cfg)
        assert m["variants"][vid]["config_ref"] == f"campaign_record/compositions/c1/{vid}.json"
        reg = cfg["strategies"]["regimes"]["unknown"]
        # block weights are the scheme's; nothing else differs between variants
        assert {b["id"]: b["weight"] for b in reg["blocks"]} == {
            mb["config_block_id"]: m["variants"][vid]["weights"][mb["block_id"]] for mb in m["blocks"]}
        assert reg["block_standardisation"] == {"target": 10.0, "window": 500, "min_periods": 30}
    strip = lambda c: [{**b, "weight": None} for b in c["strategies"]["regimes"]["unknown"]["blocks"]]
    assert strip(cfgs["base"]) == strip(cfgs["vol_scaled"]) == strip(cfgs["ic_weighted"])
    for c in cfgs.values():
        c["strategies"]["regimes"]["unknown"]["blocks"] = None
    assert cfgs["base"] == cfgs["vol_scaled"] == cfgs["ic_weighted"]
    # components copied verbatim from the registry fragments, only the id prefixed
    base = json.loads((out / "base.json").read_text(encoding="utf-8"))
    for mb, block in zip(m["blocks"], doc["blocks"]):
        [frag] = block["config_fragment"].values()
        [ptr] = mb["config_paths"]
        idx = int(ptr.rsplit("/", 1)[1])
        got = base["strategies"]["regimes"]["unknown"]["components"][idx]
        assert {**got, "id": frag["id"]} == frag and got["id"] == f"{mb['config_block_id']}__sig"
    assert base["strategies"]["warmup"] == 41  # max of the blocks' own warmups
    assert base["regime_detector"]["default_regime"] == "unknown"


def test_writer_ignores_other_timeframes_and_regime_blocks(tmp_path):
    other = _registry(tmp_path / "o", n=1, tf="4h")["blocks"][0]
    other["block_id"] = "H-9:run_999"
    regime = copy.deepcopy(other)
    regime.update(block_id="H-8:run_998", kind="regime", timeframe="1h", timeframe_category="low")
    doc = _registry(tmp_path, extra=[other, regime])
    _, _, m = _write(tmp_path, doc=doc)
    assert [b["block_id"] for b in m["blocks"]] == ["H-0:run_900", "H-1:run_901"]


def test_writer_single_block_on_timeframe_fails_loud_and_writes_nothing(tmp_path):
    doc = _registry(tmp_path, n=1)
    with pytest.raises(comp.CompositionError, match="at least two blocks"):
        _write(tmp_path, doc=doc)
    assert not (tmp_path / "campaign_record").exists()


def test_writer_missing_return_series_and_bad_ic_write_nothing(tmp_path):
    doc = _registry(tmp_path)
    rets = _rets_for(doc)
    rets.pop("H-1:run_901")
    with pytest.raises(comp.CompositionError, match="no stand-alone daily return series"):
        _write(tmp_path, doc=doc, rets=rets)
    doc["blocks"][1]["residual_ic"]["value"] = -0.01
    with pytest.raises(comp.CompositionError, match="zero or negative"):
        _write(tmp_path, doc=doc)
    assert not (tmp_path / "campaign_record").exists()


def test_writer_refuses_tampered_source_config_and_param_level_fragment(tmp_path):
    doc = _registry(tmp_path)
    p = tmp_path / doc["blocks"][0]["source_config_ref"]
    p.write_text(p.read_text(encoding="utf-8").replace('"period": 5', '"period": 6'), encoding="utf-8")
    with pytest.raises(comp.CompositionError, match="changed after it was tested"):
        _write(tmp_path, doc=doc)
    doc = _registry(tmp_path / "b")
    doc["blocks"][0]["config_fragment"] = {"/strategies/regimes/unknown/components/0/params": {"period": 5}}
    with pytest.raises(comp.CompositionError, match="below a component spec"):
        _write(tmp_path / "b", doc=doc)


def test_writer_is_idempotent_and_never_overwrites(tmp_path):
    doc, out, m1 = _write(tmp_path)
    before = {p.name: p.read_bytes() for p in out.iterdir()}
    _, _, m2 = _write(tmp_path, doc=doc)
    assert m1 == m2 and before == {p.name: p.read_bytes() for p in out.iterdir()}
    with pytest.raises(comp.CompositionError, match="different content"):
        _write(tmp_path, doc=doc, rets=_rets_for(doc, sigmas=(0.02, 0.02)))
    assert before == {p.name: p.read_bytes() for p in out.iterdir()}


def test_aux_feeds_carried_and_disagreeing_min_allocation_change_raises(tmp_path):
    doc = _registry(tmp_path)
    for k, feeds in enumerate((["funding_rate"], ["funding_rate", "fear_greed"])):
        b = doc["blocks"][k]
        p = tmp_path / b["source_config_ref"]
        cfg = json.loads(p.read_text(encoding="utf-8"))
        cfg["aux_feeds"] = feeds
        p.write_text(json.dumps(cfg), encoding="utf-8")
        b["source_config_sha256"] = _canon(cfg)
    _, out, m = _write(tmp_path, doc=doc)
    assert json.loads((out / "base.json").read_text(encoding="utf-8"))["aux_feeds"] == [
        "funding_rate", "fear_greed"]
    assert "/aux_feeds" in m["scaffolding"]
    doc2 = _registry(tmp_path / "m")
    b = doc2["blocks"][0]
    p = tmp_path / "m" / b["source_config_ref"]
    cfg = json.loads(p.read_text(encoding="utf-8"))
    cfg["strategies"]["min_allocation_change"] = 0.1
    p.write_text(json.dumps(cfg), encoding="utf-8")
    b["source_config_sha256"] = _canon(cfg)
    with pytest.raises(comp.CompositionError, match="min_allocation_change"):
        _write(tmp_path / "m", doc=doc2)


def test_written_configs_load_in_the_engine_and_forecast(tmp_path):
    """The real validator passes and the real AdvancedStrategy runs the
    written base config on synthetic bars: NOT_READY first, then a finite,
    non-zero combined forecast in the ungated regime."""
    _, out, _ = _write(tmp_path)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_vc", SR_ROOT.parent / "trading-bot" / "tools" / "validate_config.py")
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)
    from strategies.main_strategy import AdvancedStrategy
    for vid in ("base", "vol_scaled", "ic_weighted"):
        assert vc.validate(json.loads((out / f"{vid}.json").read_text(encoding="utf-8"))) == []
    strat = AdvancedStrategy(config_path=str(out / "base.json"))
    rng = np.random.default_rng(0)
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, 400)))
    df = pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=400, freq="h"),
                       "open": close, "high": close, "low": close, "close": close, "volume": 1.0})
    sigs = []
    for i in range(len(df)):
        strat.update(df.iloc[[i]])
        sigs.append(strat.generate_signals())
    assert strat.component_error_count == 0
    assert sigs[0].regime == "NOT_READY"
    ready = [s for s in sigs if s.regime != "NOT_READY"]
    assert ready and all(s.regime == "unknown" for s in ready)
    assert all(math.isfinite(s.forecast) and -20 <= s.forecast <= 20 for s in ready)
    assert any(s.forecast != 0.0 for s in ready)
    assert set(ready[-1].debug_info["components"]) == {"b0", "b1"}


# --- 4. compositions.yaml ----------------------------------------------------

def _entry(tmp_path):
    _, out, m = _write(tmp_path)
    return comp.composition_entry(m, "campaign_record/compositions/c1/composition_manifest.yaml",
                                  recorded_at="t0"), m


def test_compositions_yaml_is_what_composite_cache_reads(tmp_path):
    entry, m = _entry(tmp_path)
    path = tmp_path / "campaign_record" / "compositions.yaml"
    assert comp.record_composition(path, entry, root=tmp_path, enabled=True) is True
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert doc["schema_version"] == 1 and doc["compositions"] == [entry]
    assert set(entry) == set(comp.COMPOSITION_ENTRY_FIELDS)
    registry = _registry(tmp_path / "again")  # same block ids + configs -> same registry_hash
    for b in registry["blocks"]:
        b["source_config_sha256"] = next(x["source_config_sha256"] for x in m["blocks"]
                                         if x["block_id"] == b["block_id"])
    r = cc.resolve_current_composite(registry, cc.load_compositions(path), "1h")
    assert r["kind"] == "composition"
    assert r["config_ref"] == entry["base_config_ref"] == m["variants"]["base"]["config_ref"]
    assert r["expected_config_sha256"] == entry["base_config_sha256"]
    assert cc._canonical_config_sha256(tmp_path / r["config_ref"]) == r["expected_config_sha256"]


@pytest.mark.parametrize("field", comp.COMPOSITION_ENTRY_FIELDS)
def test_compositions_entry_requires_every_field(tmp_path, field):
    entry, _ = _entry(tmp_path)
    entry.pop(field)
    with pytest.raises(comp.CompositionError, match=field):
        comp.record_composition(tmp_path / "c.yaml", entry, root=tmp_path, enabled=True)
    assert not (tmp_path / "c.yaml").exists()


def test_compositions_entry_rejects_unknown_field_wrong_sha_and_flag_off(tmp_path):
    entry, _ = _entry(tmp_path)
    path = tmp_path / "c.yaml"
    with pytest.raises(comp.CompositionError, match="unknown"):
        comp.record_composition(path, {**entry, "outcome": "x"}, root=tmp_path, enabled=True)
    with pytest.raises(comp.CompositionError, match="differs from base_config_sha256"):
        comp.record_composition(path, {**entry, "base_config_sha256": "0" * 64}, root=tmp_path,
                                enabled=True)
    with pytest.raises(comp.CompositionError, match="composition_runs is off"):
        comp.record_composition(path, entry, root=tmp_path, enabled=False)
    assert not path.exists()


def test_compositions_append_only(tmp_path):
    entry, _ = _entry(tmp_path)
    path = tmp_path / "campaign_record" / "compositions.yaml"
    assert comp.record_composition(path, entry, root=tmp_path, enabled=True)
    # the same entry again (only recorded_at differs): no-op
    assert comp.record_composition(path, {**entry, "recorded_at": "later"}, root=tmp_path,
                                   enabled=True) is False
    before = path.read_bytes()
    with pytest.raises(comp.CompositionError, match="append-only"):
        comp.record_composition(path, {**entry, "registry_revision": 99}, root=tmp_path,
                                enabled=True)
    assert path.read_bytes() == before
    # a second composition (another block set) appends after the first
    second = {**entry, "registry_hash": "f" * 16}
    assert comp.record_composition(path, second, root=tmp_path, enabled=True)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert [c["registry_hash"] for c in doc["compositions"]] == [entry["registry_hash"], "f" * 16]


def test_compositions_writer_holds_the_lock(tmp_path, monkeypatch):
    entry, _ = _entry(tmp_path)
    path = tmp_path / "campaign_record" / "compositions.yaml"
    lock = path.parent / comp.COMPOSITIONS_LOCK_FILENAME
    seen = {}
    real = cm._atomic_write

    def spy(p, doc):
        seen["locked_during_write"] = lock.exists()
        return real(p, doc)

    monkeypatch.setattr(cm, "_atomic_write", spy)
    comp.record_composition(path, entry, root=tmp_path, enabled=True)
    assert seen == {"locked_during_write": True} and not lock.exists()
    # a lock held by another (live) writer: refused after the wait, nothing written
    import campaign_lock
    campaign_lock.acquire(lock)
    try:
        monkeypatch.setattr(cm, "MEMORY_LOCK_WAIT_SECONDS", 0.0)
        before = path.read_bytes()
        with pytest.raises(comp.CompositionError, match="still held"):
            comp.record_composition(path, {**entry, "registry_hash": "e" * 16}, root=tmp_path,
                                    enabled=True)
        assert path.read_bytes() == before
    finally:
        campaign_lock.release(lock)


def test_composite_is_never_registered_as_a_block(tmp_path):
    """The writers never touch the block registry file."""
    entry, _ = _entry(tmp_path)
    comp.record_composition(tmp_path / "campaign_record" / "compositions.yaml", entry,
                            root=tmp_path, enabled=True)
    assert not (tmp_path / "campaign_record" / "block_registry.yaml").exists()
    src = (SR_ROOT / "tools" / "composition.py").read_text(encoding="utf-8")
    assert "block_registry" not in src.replace("block registry", "")
