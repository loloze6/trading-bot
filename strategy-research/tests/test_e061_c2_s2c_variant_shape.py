"""
E-061 C2 S2c -- variant shape (C2_S1_FINDINGS.md G12 / C2.5, card D; review A5).

Covers:
  1. tools/variant_coin.check_variant_shape: 3-4 variants, exactly one base, >= 1
     design, 1-2 asset, G4's multi-coin refusal, ids, and S2b's per-entry
     checks reused (a COIN_REASON_PREFIX refusal is a shape problem; an asset
     refused only for coverage is NOT -- D-042 makes it untested, never blocking).
  2. The retry/pause flow: one retry of Step 2 shared by the shape and the
     config check, then the variant_shape_invalid / variant_config_error pause;
     the counter lives in pipeline_state.yaml (it survives a restart) and is
     reset once 5a's route accepts the variants; the error reaches Step 2's
     handoff.
  3. 5a's config errors: a patch that does not apply, unresolved manifest paths,
     another V-code -> retry; a V12 missing class, a repeat skip, a coverage skip
     -> not a config error.
  4. The data-gate floor at 5a when the data gate is off (per-coin only).
  5. Flag-off byte identity: variant loop off, config-direct off, a legacy
     variant_patches.yaml and a composition run never reach the new checks, and
     the routes / pipeline_state.yaml bytes are what they were.
  6. run_campaign: both flags classify as themselves, are in the flag table, and
     have a RUNBOOK row.

Sandbox: tests/conftest.py's autouse fixture (rpr.ROOT etc. in tmp). No LLM, no
network, no market data, no backtest. Every window date here is before 2023.
"""
import copy
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import variant_coin as vc  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e061_c2_s2b_one_coin_per_variant import (  # noqa: E402
    DESIGN_PATCH, PER_COIN_PATCHES, _copy_coin_configs, _ctx, _months, _ok_subprocess,
    _run_5a, _run_protocol_file, _set_flags, _source, _strip_coin, _synthetic)

KEY = rpr.VARIANT_STEP2_RETRY_STATE_KEY
SHAPE, CONFIG = rpr.VARIANT_SHAPE_INVALID_FLAG, rpr.VARIANT_CONFIG_ERROR_FLAG
SOURCE = _source(_months("2022-01", 6))


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _shape(variants, ctx=None):
    return vc.check_variant_shape(variants, **(ctx or _ctx(SOURCE)))


def _v(vid, kind, symbol=None, patch=None):
    e = {"variant_id": vid, "kind": kind, "patch": patch or [], "rationale": "r"}
    if symbol is not None:
        e["symbol"] = symbol
    return e


BASE = _v("base", "base", "BTCUSDT")
DESIGN = _v("design", "design", "BTCUSDT", DESIGN_PATCH)
ASSET = _v("asset", "asset", "XRPUSDT")


# ---------------------------------------------------------------------------
# 1. check_variant_shape
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variants", [
    [BASE, DESIGN, ASSET],
    [BASE, DESIGN, _v("d2", "design", None, DESIGN_PATCH), ASSET],
    [BASE, DESIGN, ASSET, _v("asset2", "asset", "SOLUSDT")],
    [_v("base", "base"), _v("design", "design", None, DESIGN_PATCH), ASSET],  # coin left to code
], ids=["3", "4_two_designs", "4_two_assets", "base_design_symbol_omitted"])
def test_valid_shapes(variants):
    assert _shape(variants) == []


@pytest.mark.parametrize("variants,needles", [
    ([BASE, DESIGN], ["2 variants", "0 kind-asset"]),
    ([BASE, DESIGN, ASSET, _v("d2", "design", None, DESIGN_PATCH),
      _v("d3", "design", None, DESIGN_PATCH)], ["5 variants"]),
    ([_v("d0", "design", None, DESIGN_PATCH), DESIGN, ASSET], ["0 kind-base"]),
    ([BASE, _v("base2", "base"), DESIGN, ASSET],
     ["2 kind-base", "the kind-base variant must be variant_id 'base'"]),
    ([_v("b", "base"), DESIGN, ASSET], ["the kind-base variant must be variant_id 'base'"]),
    ([BASE, ASSET, _v("asset2", "asset", "SOLUSDT")], ["no kind-design"]),
    ([BASE, _v("design", "design"), ASSET], ["its patch must not be empty"]),
    ([BASE, _v("design", "design", "ETHUSDT", DESIGN_PATCH), ASSET], ["runs on the base coin"]),
    ([BASE, DESIGN, _v("asset", "asset", "ETHUSDT")], ["base coin's own category"]),
    ([BASE, DESIGN, _v("asset", "asset", "XRPUSDT", DESIGN_PATCH)], ["patch must be empty"]),
    ([BASE, DESIGN, _v("asset", "asset", "NOPEUSDT")], ["not in config/coin_universe.yaml"]),
    ([BASE, DESIGN, _v("asset", "asset")], ["must name its coin"]),
    ([BASE, DESIGN, _v("x", "wrong")], ["kind 'wrong' is not one of", "0 kind-asset"]),
    ([BASE, _v("asset", "asset", "XRPUSDT"), _v("a2", "asset", "SOLUSDT"),
      _v("a3", "asset", "DOGEUSDT")], ["no kind-design", "3 kind-asset"]),
    ([BASE, DESIGN, {**ASSET, "symbols": ["XRPUSDT", "SOLUSDT"]}], ["multi-coin", "G4"]),
    ([BASE, DESIGN, {**ASSET, "symbol": ["XRPUSDT", "SOLUSDT"]}], ["multi-coin", "G4"]),
    ([BASE, DESIGN, ASSET, {**ASSET}], ["duplicate variant_id 'asset'"]),
    ([BASE, DESIGN, {**ASSET, "variant_id": "../x"}], ["not a safe bare identifier"]),
    ([BASE, DESIGN, "asset"], ["variants[2] is not a mapping"]),
])
def test_each_violation_is_named(variants, needles):
    problems = _shape(copy.deepcopy(variants))
    text = "; ".join(problems)
    assert problems, variants
    for needle in needles:
        assert needle in text, (needle, problems)


@pytest.mark.parametrize("variants", [None, [], {"base": {}}])
def test_variants_must_be_a_non_empty_list(variants):
    assert _shape(variants) and "non-empty list" in _shape(variants)[0]


def test_a_coverage_only_asset_is_not_a_shape_problem():
    """D-042 (binding): an asset coin below the coverage share is untested --
    the idea at best inconclusive -- never blocking; 5a already does that. The
    shape check therefore reads it as the one asset Step 2 wrote."""
    universe, layer1 = _synthetic("2020-02-15T00:00:00Z")
    source = _source(_months("2019-06", 13))
    ctx = _ctx(source, universe, layer1)
    res = vc.resolve_variant(ASSET, **ctx)
    assert not res["ok"] and res["reason"].startswith(vc.COVERAGE_REASON_PREFIX)
    assert _shape([BASE, DESIGN, ASSET], ctx) == []


# ---------------------------------------------------------------------------
# 2. The retry / pause flow (pipeline_state.yaml)
# ---------------------------------------------------------------------------

def _state(run_dir):
    return rpr.load_yaml(run_dir / "pipeline_state.yaml")


def _per_coin_run(run_id, patches, monkeypatch, *, flags=None):
    _set_flags(**(flags or {"config_direct_authoring": True, "variant_loop": True}))
    _copy_coin_configs()
    _run_protocol_file(monkeypatch, _months("2022-01", 6))
    _ok_subprocess(monkeypatch)
    return _run_5a(run_id, patches)


def test_shape_retry_once_then_pause_and_the_counter_is_on_disk(monkeypatch):
    run_dir = _per_coin_run("run_950", PER_COIN_PATCHES[:2], monkeypatch)  # no asset
    assert rpr._variant_shape_check_applies(run_dir)
    assert rpr._route_variant_shape_check(run_dir, "run_950") == "innovation_expansion"
    rec = _state(run_dir)[KEY]  # read back from disk: a restart sees the same count
    assert rec["attempts"] == 1 and rec["last_check"] == SHAPE and "0 kind-asset" in rec["last_error"]
    assert len(rec["history"]) == 1 and not (_state(run_dir).get("flags") or {}).get(SHAPE)
    assert _state(run_dir)["status"] == "active"
    # the retry carries the error into Step 2's handoff
    handoff = {}
    rpr._apply_variant_shape_retry_context("innovation_expansion", handoff, run_dir)
    ctx = handoff["injected_context"]["variant_shape_error"]
    assert ctx.startswith("Retry 1/1.") and "0 kind-asset" in ctx
    other = {}
    rpr._apply_variant_shape_retry_context("backtest_specification", other, run_dir)
    assert other == {}
    # a second invalid output: the pause, never a raise
    assert rpr._route_variant_shape_check(run_dir, "run_950") == "human_pause"
    st = _state(run_dir)
    assert st["status"] == "paused_for_human" and st["flags"][SHAPE] is True
    assert st[KEY]["attempts"] == 1 and len(st[KEY]["history"]) == 2
    assert camp._classify_human_pause(run_dir, st) == SHAPE


def test_valid_shape_routes_to_5a_and_writes_nothing(monkeypatch):
    run_dir = _per_coin_run("run_951", PER_COIN_PATCHES, monkeypatch)
    before = (run_dir / "pipeline_state.yaml").read_bytes()
    assert rpr._route_variant_shape_check(run_dir, "run_951") == "backtest_specification"
    assert (run_dir / "pipeline_state.yaml").read_bytes() == before


def test_one_budget_for_both_checks_and_reset_on_acceptance(monkeypatch):
    """A shape retry spends the one retry: a config error on the next output
    pauses variant_config_error at once. An accepted output resets the counter
    (history kept)."""
    bad_design = copy.deepcopy(PER_COIN_PATCHES)
    bad_design[1]["patch"] = [{"path": "/no/such/parent/key", "value": 1}]
    run_dir = _per_coin_run("run_952", bad_design, monkeypatch)
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    assert index["design"]["reason"].startswith("patch application failed")
    rpr.update_state(path=run_dir, **{KEY: {"attempts": 1, "last_check": SHAPE,
                                            "last_error": "x", "history": [{"check": SHAPE}]}})
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"
    st = _state(run_dir)
    assert st["flags"][CONFIG] is True and SHAPE not in st["flags"]
    assert "variant 'design' not tested -- patch application failed" in st[KEY]["last_error"]
    assert camp._classify_human_pause(run_dir, st) == CONFIG

    ok_dir = _per_coin_run("run_953", PER_COIN_PATCHES, monkeypatch)
    rpr.update_state(path=ok_dir, **{KEY: {"attempts": 1, "last_check": SHAPE,
                                           "last_error": "x", "history": [{"check": SHAPE}]}})
    assert rpr._route_post_config_direct_backtest_specification(ok_dir) == "data_availability_gate"
    rec = _state(ok_dir)[KEY]
    assert rec["attempts"] == 0 and rec["last_error"] is None and rec["history"] == [{"check": SHAPE}]
    handoff = {}
    rpr._apply_variant_shape_retry_context("innovation_expansion", handoff, ok_dir)
    assert handoff == {}


def test_retry_that_drops_kind_and_symbol_is_a_shape_failure(monkeypatch):
    """Review fix M1: once the run produced a per-coin output, a Step 2 retry
    that strips kind/symbol is NOT read as a legacy file -- the check still
    applies and the second invalid output pauses variant_shape_invalid."""
    run_dir = _per_coin_run("run_957", PER_COIN_PATCHES[:2], monkeypatch)  # no asset
    assert rpr._route_variant_shape_check(run_dir, "run_957") == "innovation_expansion"
    rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml",
                  {"variants": _strip_coin(PER_COIN_PATCHES)})
    assert rpr._variant_shape_check_applies(run_dir) is True
    assert rpr._route_variant_shape_check(run_dir, "run_957") == "human_pause"
    st = _state(run_dir)
    assert st["status"] == "paused_for_human" and st["flags"][SHAPE] is True
    assert "per-coin fields (kind/symbol) missing" in st[KEY]["last_error"]
    assert _shape(_strip_coin(PER_COIN_PATCHES))[0].startswith("per-coin fields (kind/symbol) missing")


def test_error_reaches_step2_after_an_operator_reset_of_attempts(monkeypatch):
    """Review fix T2: the RUNBOOK reset variant_shape_retry={'attempts': 0} gives
    the retry back, and Step 2 still sees the last error."""
    run_dir = _per_coin_run("run_958", PER_COIN_PATCHES, monkeypatch)
    rpr.update_state(path=run_dir, **{KEY: {"attempts": 1, "last_check": SHAPE,
                                            "last_error": "0 kind-asset variant(s)"}})
    rpr.update_state(path=run_dir, **{KEY: {"attempts": 0}})  # the operator reset
    handoff = {}
    rpr._apply_variant_shape_retry_context("innovation_expansion", handoff, run_dir)
    ctx = handoff["injected_context"]["variant_shape_error"]
    assert ctx.startswith("Your previous variant_patches.yaml was rejected") and "0 kind-asset" in ctx


def test_coin_info_line_prints_once_per_pass(monkeypatch, capsys):
    """Review fix T4: the S2b 'one coin per variant' line prints at most once per
    pass (same variant_patches.yaml), again for a new Step 2 output."""
    run_dir = _per_coin_run("run_959", PER_COIN_PATCHES, monkeypatch)
    monkeypatch.setattr(rpr, "_COIN_INFO_PRINTED", set())
    capsys.readouterr()  # drop 5a's own output
    multi = {**SOURCE, "symbols": ["BTCUSDT", "ETHUSDT"]}
    monkeypatch.setattr(vc, "load_protocol_file", lambda p: copy.deepcopy(multi))
    for _ in range(3):
        rpr._variant_coin_context(run_dir, "run_959")
    assert capsys.readouterr().out.count("one coin per variant") == 1
    rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml",
                  {"variants": PER_COIN_PATCHES[:2]})
    rpr._variant_coin_context(run_dir, "run_959")
    assert capsys.readouterr().out.count("one coin per variant") == 1


# ---------------------------------------------------------------------------
# 3. 5a's config errors
# ---------------------------------------------------------------------------

def _entry(reason, report=None):
    e = {"status": "not_tested", "reason": reason}
    if report is not None:
        e["report"] = report
    return e


def test_config_error_classification(monkeypatch):
    missing = "VIOLATION V12 x: cannot load 'strategies.strategy_components.Nope'"
    monkeypatch.setattr(rpr, "_v12_missing_classes",
                        lambda report: ["strategies.strategy_components.Nope"]
                        if report == missing else [])
    variants = {
        "ok": {"status": "validated"},
        "patch": _entry("patch application failed: no parent"),
        "manifest": _entry("manifest paths unresolved: ['/x']"),
        "v3": _entry("validate_config.py violations", "VIOLATION V3 op: 'z' " + "y" * 3000),
        "coin": _entry("variant_coin: an asset variant must name its coin (`symbol`)"),
        "missing_class": _entry("validate_config.py violations", missing),
        "repeat": _entry("repeat: run_001:design"),
        "coverage": _entry(vc.COVERAGE_REASON_PREFIX + " the coin covers 2/6"),
        "layer2": _entry(vc.LAYER2_COVERAGE_REASON_PREFIX + " decline"),
    }
    errors = dict(rpr._variant_config_errors(variants))
    assert sorted(errors) == ["coin", "manifest", "patch", "v3"]
    assert errors["v3"].startswith("validate_config.py violations: VIOLATION V3")
    assert errors["v3"].endswith("...[truncated]") and len(errors["v3"]) < 1600


def test_config_error_retries_then_pauses_and_never_reaches_the_data_gate(monkeypatch):
    bad = copy.deepcopy(PER_COIN_PATCHES)
    bad[1]["patch"] = [{"path": "/no/such/parent/key", "value": 1}]
    run_dir = _per_coin_run("run_954", bad, monkeypatch)
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "innovation_expansion"
    assert _state(run_dir)[KEY]["last_check"] == CONFIG
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"
    st = _state(run_dir)
    assert st["flags"] == {CONFIG: True}
    assert "variant_gate_insufficient" not in st["flags"]


def test_base_config_error_pauses_at_once_without_a_step2_retry(monkeypatch):
    """Review fix M2: `base` (empty patch) not_tested for a config reason is 1b's
    fault -- no Step 2 retry, the variant_config_error pause at once, the retry
    budget untouched, the error naming the base config (1b)."""
    run_dir = _per_coin_run("run_968", PER_COIN_PATCHES, monkeypatch)
    idx_path = run_dir / "artifacts" / "variants" / "index.yaml"
    idx = rpr.load_yaml(idx_path)
    idx["variants"]["base"].update({"status": "not_tested",
                                    "reason": "validate_config.py violations",
                                    "report": "VIOLATION V3 op: 'z'"})
    rpr.save_yaml(idx_path, idx)
    monkeypatch.setattr(rpr, "_v12_missing_classes", lambda report: [])
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"
    st = _state(run_dir)
    assert st["status"] == "paused_for_human" and st["flags"] == {CONFIG: True}
    assert st[KEY]["attempts"] == 0 and st[KEY]["last_check"] == CONFIG
    err = st[KEY]["last_error"]
    assert "base config" in err and "1b" in err and "VIOLATION V3" in err
    assert camp._classify_human_pause(run_dir, st) == CONFIG
    runbook = (SR_ROOT / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert "If the base config is at fault" in runbook and "fix/re-author 1b" in runbook


def test_missing_class_stays_the_component_park(monkeypatch):
    """A V12 missing class is not a config error: under verdict_routing_retired a
    run whose every variant lacks a class still parks as component."""
    run_dir = _per_coin_run("run_955", PER_COIN_PATCHES, monkeypatch)
    idx_path = run_dir / "artifacts" / "variants" / "index.yaml"
    idx = rpr.load_yaml(idx_path)
    for v in idx["variants"].values():
        v.update({"status": "not_tested", "reason": "validate_config.py violations",
                  "report": "V12 missing"})
    rpr.save_yaml(idx_path, idx)
    monkeypatch.setattr(rpr, "_v12_missing_classes", lambda report: ["x.Missing"])
    parks = []
    monkeypatch.setattr(rpr, "_park_run", lambda run_dir, **k: parks.append(k) or "human_pause")
    assert rpr._route_post_config_direct_backtest_specification(
        run_dir, routing_retired=True) == "human_pause"
    assert parks and parks[0]["kind"] == "component"
    assert KEY not in _state(run_dir) and not (_state(run_dir).get("flags") or {})


# ---------------------------------------------------------------------------
# 4. The floor at 5a with the data gate off
# ---------------------------------------------------------------------------

def test_floor_at_5a_when_the_data_gate_is_off(monkeypatch):
    flags = {"config_direct_authoring": True, "variant_loop": True,
             "data_availability_gate": False}
    run_dir = _per_coin_run("run_956", PER_COIN_PATCHES, monkeypatch, flags=flags)
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "protocol_execution"
    idx_path = run_dir / "artifacts" / "variants" / "index.yaml"
    idx = rpr.load_yaml(idx_path)
    idx["variants"]["design"].update({"status": "not_tested",
                                      "reason": "validate_config.py violations",
                                      "report": "V12 missing"})
    rpr.save_yaml(idx_path, idx)
    monkeypatch.setattr(rpr, "_v12_missing_classes", lambda report: ["x.Missing"])
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"
    assert _state(run_dir)["flags"] == {"variant_gate_insufficient": True}
    # a D-042 coverage skip lowers the floor exactly as at the gate
    assert rpr._variant_floor({"a": {"status": "validated"}, "b": {"status": "validated"},
                               "c": _entry(vc.COVERAGE_REASON_PREFIX + " x")}) == (["a", "b"], 2)
    assert rpr._variant_floor({"a": {"status": "validated"}}) == (["a"], 3)


# ---------------------------------------------------------------------------
# 5. Flag-off / legacy byte identity
# ---------------------------------------------------------------------------

def _forbid_new_checks(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("E-061 C2 S2c check reached with the flag off / a legacy file")
    for name in ("_variant_shape_problems", "_variant_config_errors",
                 "_variant_step2_retry_or_pause", "_variant_coin_context"):
        monkeypatch.setattr(rpr, name, _boom)


@pytest.mark.parametrize("run_id,loop,per_coin", [
    ("run_960", False, True), ("run_961", True, False), ("run_962", False, False)],
    ids=["loop_off_per_coin", "loop_on_legacy", "loop_off_legacy"])
def test_flag_off_and_legacy_never_reach_the_checks(monkeypatch, run_id, loop, per_coin):
    """variant_loop off (5a ignores kind/symbol) and a legacy variant_patches.yaml
    under the loop: 5a's route returns what it returned before, the new checks
    are never called, and pipeline_state.yaml is byte-identical before/after;
    a shape violation (2 variants) changes nothing either."""
    flags = {"config_direct_authoring": True, **({"variant_loop": True} if loop else {})}
    patches = PER_COIN_PATCHES if per_coin else _strip_coin(PER_COIN_PATCHES)
    run_dir = _per_coin_run(run_id, patches[:2], monkeypatch, flags=flags)
    _forbid_new_checks(monkeypatch)
    assert rpr._variant_shape_check_applies(run_dir) is False
    before = (run_dir / "pipeline_state.yaml").read_bytes()
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "data_availability_gate"
    assert (run_dir / "pipeline_state.yaml").read_bytes() == before
    handoff = {"x": 1}
    rpr._apply_variant_shape_retry_context("innovation_expansion", handoff, run_dir)
    assert handoff == {"x": 1}


def test_config_direct_off_never_applies(monkeypatch):
    _set_flags()
    run_dir = _minimal_run(rpr.ROOT, "run_970")
    rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml", {"variants": PER_COIN_PATCHES})
    _forbid_new_checks(monkeypatch)
    assert rpr._variant_shape_check_applies(run_dir) is False
    handoff = {}
    rpr.update_state(path=run_dir, **{KEY: {"attempts": 1, "last_error": "stale"}})
    rpr._apply_variant_shape_retry_context("innovation_expansion", handoff, run_dir)
    assert handoff == {}


def test_composition_run_is_exempt(monkeypatch):
    _set_flags(config_direct_authoring=True, variant_loop=True)
    run_dir = _minimal_run(rpr.ROOT, "run_971")
    rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml", {"variants": PER_COIN_PATCHES[:1]})
    monkeypatch.setattr(rpr, "_composition_mode", lambda d: True)
    _forbid_new_checks(monkeypatch)
    assert rpr._variant_shape_check_applies(run_dir) is False


def test_data_gate_floor_refactor_is_unchanged():
    """_variant_floor is the data gate's former inline computation, moved."""
    cases = [
        ({"a": {"status": "validated"}, "b": {"status": "validated"}, "c": {"status": "validated"}},
         (["a", "b", "c"], 3)),
        ({"a": {"status": "validated"}, "b": _entry("repeat: x")}, (["a"], 1)),
        ({"a": {"status": "validated"}, "b": _entry("data_availability_gate outcome=decline: x"),
          "c": _entry("repeat: y"), "d": {"status": "validated"}}, (["a", "d"], 3)),
    ]
    for idx, want in cases:
        assert rpr._variant_floor(idx) == want


# ---------------------------------------------------------------------------
# 6. run_campaign + RUNBOOK
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("flag", [SHAPE, CONFIG])
def test_pause_flags_classify_and_are_documented(tmp_path, flag):
    (tmp_path / "artifacts").mkdir()
    assert camp._classify_human_pause(tmp_path, {"flags": {flag: True}}) == flag
    assert (flag, flag) in camp._PAUSE_FLAG_TO_REASON
    # an older sticky flag still wins, a later-pipeline one does not
    assert camp._classify_human_pause(
        tmp_path, {"flags": {flag: True, "conformance_violation": True}}) == "conformance_gate_failure"
    assert camp._classify_human_pause(
        tmp_path, {"flags": {flag: True, "variant_gate_insufficient": True}}) == flag
    runbook = (SR_ROOT / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert f"| `{flag}` |" in runbook
    assert f"'{flag}': False" in runbook
