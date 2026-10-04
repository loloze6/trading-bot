"""
E-056 Slice 3b (config-direct authoring) -- unit + flag-off-identity tests.

Covers:
  1. orchestrator.config_direct_authoring.enabled flag helper (on/off/absent).
  2. STAGE_CONFIGS / _SKILL_MAP registration (unconditional, per data_availability_gate's
     own precedent) and flag-off stage-graph identity (test_e054_stage_wiring.py's pattern).
  3. async_invoke_agent's conditional tool_stages membership for backtest_specification.
  4. _apply_config_direct_authoring_context's file-presence injection (flag off: no-op).
  5. JSON-pointer patch application (_apply_json_pointer_patch): clean patch, patch
     targeting a nonexistent parent (raises), malformed pointer (raises), list index,
     '-' append.
  6. Manifest-path checking (_check_manifest_paths): absent manifest, empty manifest,
     resolving/unresolving paths.
  7. determine_post_strategy_config_authoring_route / _route_post_config_direct_
     backtest_specification routing.
  8. run_tool_worker("backtest_specification", ...) end to end (subprocess.run mocked):
     a clean base variant, a variant whose patch fails to apply, a variant that fails
     validate_config.py -- confirms artifacts/variants/index.yaml,
     artifacts/candidate_strategy_config.json (base only), and
     campaign_record/component_requests.yaml are all written correctly.
  9. validate_config.py's real VIOLATION V12 check, invoked directly (not through
     subprocess/TBOT_PYTHON resolution, which needs a real venv this environment may
     not have) on a variant with an invented class name -- proves the check this new
     tool-stage branch relies on actually fires, independent of the orchestrator glue.
  10. Permanent regression guard: strategy-config-authoring/SKILL.md's "Ungated
      hypotheses" and "Forbidden" sections must stay byte-identical to
      backtest-engineering/SKILL.md's own -- the pre-registered success signal for
      this slice's build step 1 (E-056 Slice 3b dispatch). A future edit to either
      file that silently drops a rule fails this test, not just a one-time manual
      diff at build time.

Sandboxing: relies on tests/conftest.py's autouse _sandbox_by_default fixture (rpr.ROOT
already redirected to a per-test tmp_path sandbox), same precedent as
test_e054_stage_wiring.py / test_k3_protocol_pinning.py.
"""
import asyncio
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
TRADING_BOT_TOOLS_PATH = Path(__file__).parent.parent.parent / "trading-bot" / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    """This worktree/environment may not have a resolvable trading-bot venv
    (_resolve_tbot_python() raises RuntimeError otherwise) -- every
    run_tool_worker test in this file mocks subprocess.run, so the actual
    interpreter path is never really invoked; stub it out so tests aren't
    coupled to whether a real venv happens to exist here."""
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _set_cda_flag(root: Path, enabled) -> None:
    """Same shape as test_e054_stage_wiring.py's _set_dag_flag: enabled=None means
    'write an empty orchestrator section' (key absent, section present)."""
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text("orchestrator: {}\n", encoding="utf-8")
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {"config_direct_authoring": {"enabled": bool(enabled)}}}, f)


# ---------------------------------------------------------------------------
# 1. Flag helper
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_config_direct_authoring_enabled_reads_flag(enabled, expected):
    _set_cda_flag(rpr.ROOT, enabled)
    assert rpr._config_direct_authoring_enabled() is expected


def test_config_direct_authoring_enabled_false_when_config_file_absent():
    # No config/campaign_config.yaml written -- must default False (unlike
    # _data_availability_gate_enabled()'s deliberate True-default exception).
    assert rpr._config_direct_authoring_enabled() is False


# ---------------------------------------------------------------------------
# 2. STAGE_CONFIGS / _SKILL_MAP registration + flag-off stage-graph identity
# ---------------------------------------------------------------------------

def test_strategy_config_authoring_registered_in_stage_configs():
    """Registered UNCONDITIONALLY -- same convention as data_availability_gate's own
    addition (strategy-research/CLAUDE.md documents this precedent)."""
    assert "strategy_config_authoring" in rpr.STAGE_CONFIGS
    assert rpr.STAGE_CONFIGS["strategy_config_authoring"]["handoff"] == \
        "hypothesis_to_strategy_config_authoring.yaml"
    assert rpr.STAGE_CONFIGS["strategy_config_authoring"]["default_next"] == "innovation_expansion"
    assert rpr.STAGE_CONFIGS["strategy_config_authoring"]["skill"] == "strategy-config-authoring"


def test_validation_stage_still_registered_regardless_of_flag():
    """The validation stage becomes unreached under the flag, never deleted --
    its STAGE_CONFIGS entry must survive exactly as before this slice."""
    assert "validation" in rpr.STAGE_CONFIGS
    assert rpr.STAGE_CONFIGS["validation"]["skill"] == "quant-validation"


def test_skill_map_has_strategy_config_authoring_entry():
    assert rpr._SKILL_MAP.get("strategy_config_authoring") == "strategy-config-authoring"


def test_hypothesis_generation_default_next_unchanged_by_this_slice():
    """STAGE_CONFIGS itself must NOT be mutated to point hypothesis_generation at the
    new stage -- the override lives in run_loop's routing logic, gated by the flag, so
    flag-off runs stay byte-identical without needing a second code path here."""
    assert rpr.STAGE_CONFIGS["hypothesis_generation"]["default_next"] == "innovation_expansion"


# ---------------------------------------------------------------------------
# 3. async_invoke_agent tool_stages conditional membership
# ---------------------------------------------------------------------------

def test_backtest_specification_is_tool_stage_only_when_flag_on():
    _set_cda_flag(rpr.ROOT, True)

    async def _assert_tool_dispatch():
        called = {}

        async def _fake_run_tool_worker(stage_name, run_id):
            called["stage_name"] = stage_name

        orig = rpr.run_tool_worker
        rpr.run_tool_worker = _fake_run_tool_worker
        try:
            await rpr.async_invoke_agent("backtest_specification", "run_999")
        finally:
            rpr.run_tool_worker = orig
        return called

    called = asyncio.run(_assert_tool_dispatch())
    assert called.get("stage_name") == "backtest_specification"


def test_backtest_specification_is_not_tool_stage_when_flag_off():
    _set_cda_flag(rpr.ROOT, False)

    async def _assert_not_tool_dispatch():
        called = {}

        async def _fake_run_tool_worker(stage_name, run_id):
            called["stage_name"] = stage_name

        orig = rpr.run_tool_worker
        rpr.run_tool_worker = _fake_run_tool_worker
        try:
            # No handoff file exists for this run -- async_invoke_agent will raise
            # trying to load it, which is fine: we only care whether run_tool_worker
            # was invoked BEFORE that failure.
            with pytest.raises(Exception):
                await rpr.async_invoke_agent("backtest_specification", "run_998")
        finally:
            rpr.run_tool_worker = orig
        return called

    called = asyncio.run(_assert_not_tool_dispatch())
    assert called == {}, "backtest_specification must not dispatch through run_tool_worker when the flag is off"


def test_protocol_execution_and_data_availability_gate_stay_tool_stages_regardless_of_flag():
    """Sanity check that this slice's conditional union doesn't accidentally shrink
    the pre-existing unconditional tool_stages set."""
    for enabled in (True, False):
        _set_cda_flag(rpr.ROOT, enabled)

        async def _assert_tool_dispatch(stage):
            called = {}

            async def _fake_run_tool_worker(stage_name, run_id):
                called["stage_name"] = stage_name

            orig = rpr.run_tool_worker
            rpr.run_tool_worker = _fake_run_tool_worker
            try:
                await rpr.async_invoke_agent(stage, "run_997")
            finally:
                rpr.run_tool_worker = orig
            return called

        for stage in ("protocol_execution", "data_availability_gate"):
            called = asyncio.run(_assert_tool_dispatch(stage))
            assert called.get("stage_name") == stage


# ---------------------------------------------------------------------------
# 4. _apply_config_direct_authoring_context
# ---------------------------------------------------------------------------

def test_apply_config_direct_authoring_context_noop_when_flag_off():
    _set_cda_flag(rpr.ROOT, False)
    handoff = {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "x"}]}
    before = yaml.safe_dump(handoff)
    run_dir = _minimal_run(rpr.ROOT, "run_800")
    rpr._apply_config_direct_authoring_context("hypothesis_generation", handoff, run_dir)
    assert yaml.safe_dump(handoff) == before, "flag off must never mutate the handoff dict"


def test_apply_config_direct_authoring_context_adds_criterion_menu_and_cost_model_for_hypothesis_generation():
    _set_cda_flag(rpr.ROOT, True)
    handoff = {"required_inputs": []}
    run_dir = _minimal_run(rpr.ROOT, "run_801")
    rpr._apply_config_direct_authoring_context("hypothesis_generation", handoff, run_dir)
    paths = {r["path"] for r in handoff["required_inputs"]}
    assert "../../config/criterion_menu.yaml" in paths
    assert "../../config/cost_model.yaml" in paths


def test_apply_config_direct_authoring_context_adds_backtest_spec_for_innovation_expansion():
    _set_cda_flag(rpr.ROOT, True)
    handoff = {"required_inputs": []}
    run_dir = _minimal_run(rpr.ROOT, "run_802")
    rpr._apply_config_direct_authoring_context("innovation_expansion", handoff, run_dir)
    paths = {r["path"] for r in handoff["required_inputs"]}
    assert "artifacts/backtest_spec.yaml" in paths


def test_apply_config_direct_authoring_context_ignores_unrelated_stages():
    _set_cda_flag(rpr.ROOT, True)
    handoff = {"required_inputs": []}
    run_dir = _minimal_run(rpr.ROOT, "run_803")
    rpr._apply_config_direct_authoring_context("verdict_interpreter", handoff, run_dir)
    assert handoff["required_inputs"] == []


def test_apply_config_direct_authoring_context_is_idempotent():
    _set_cda_flag(rpr.ROOT, True)
    handoff = {"required_inputs": []}
    run_dir = _minimal_run(rpr.ROOT, "run_804")
    rpr._apply_config_direct_authoring_context("hypothesis_generation", handoff, run_dir)
    rpr._apply_config_direct_authoring_context("hypothesis_generation", handoff, run_dir)
    paths = [r["path"] for r in handoff["required_inputs"]]
    assert paths.count("../../config/criterion_menu.yaml") == 1
    assert paths.count("../../config/cost_model.yaml") == 1


# ---------------------------------------------------------------------------
# 5. JSON-pointer patch application
# ---------------------------------------------------------------------------

_BASE_CONFIG = {
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
    "strategies": {
        "warmup": 51,
        "regimes": {
            "unknown": {"components": [
                {"id": "rsi", "class": "strategies.strategy_components.RSIPullbackComponent",
                 "params": {"period": 14}, "weight": 1.0, "transforms": [{"op": "identity"}]},
            ]},
            "trending": None, "mean_reversion": None, "chop": None,
        },
    },
}


def test_patch_application_clean_patch_sets_leaf_value():
    patch = [{"path": "/strategies/regimes/unknown/components/0/params/period", "value": 21}]
    result = rpr._apply_json_pointer_patch(_BASE_CONFIG, patch)
    assert result["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"] == 21
    # base config itself must never be mutated
    assert _BASE_CONFIG["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"] == 14


def test_patch_application_adds_new_leaf_key_under_existing_parent():
    patch = [{"path": "/strategies/regimes/unknown/components/0/params/scaling_factor", "value": 2.0}]
    result = rpr._apply_json_pointer_patch(_BASE_CONFIG, patch)
    assert result["strategies"]["regimes"]["unknown"]["components"][0]["params"]["scaling_factor"] == 2.0


def test_patch_application_nonexistent_parent_raises_not_silent():
    """A patch targeting a path whose PARENT doesn't exist must raise loudly -- it must
    never silently create a new nested chain and must never silently no-op."""
    patch = [{"path": "/strategies/regimes/unknown/components/5/params/period", "value": 21}]
    with pytest.raises(rpr.PatchApplicationError, match="out of range"):
        rpr._apply_json_pointer_patch(_BASE_CONFIG, patch)

    patch2 = [{"path": "/totally/invented/nested/path", "value": 1}]
    with pytest.raises(rpr.PatchApplicationError, match="does not exist"):
        rpr._apply_json_pointer_patch(_BASE_CONFIG, patch2)


def test_patch_application_malformed_pointer_raises():
    for bad_path in ["no-leading-slash", "", None]:
        with pytest.raises(rpr.PatchApplicationError):
            rpr._apply_json_pointer_patch(_BASE_CONFIG, [{"path": bad_path, "value": 1}])


def test_patch_application_missing_value_key_raises():
    with pytest.raises(rpr.PatchApplicationError, match="value"):
        rpr._apply_json_pointer_patch(_BASE_CONFIG, [{"path": "/strategies/warmup"}])


def test_patch_application_list_append_token():
    base = {"aux_feeds": ["fear_greed"]}
    patch = [{"path": "/aux_feeds/-", "value": "funding_rate"}]
    result = rpr._apply_json_pointer_patch(base, patch)
    assert result["aux_feeds"] == ["fear_greed", "funding_rate"]
    assert base["aux_feeds"] == ["fear_greed"]


def test_patch_application_empty_patch_returns_unmodified_copy():
    result = rpr._apply_json_pointer_patch(_BASE_CONFIG, [])
    assert result == _BASE_CONFIG
    assert result is not _BASE_CONFIG


# ---------------------------------------------------------------------------
# 6. Manifest-path checking
# ---------------------------------------------------------------------------

def test_check_manifest_paths_absent_manifest_returns_empty():
    assert rpr._check_manifest_paths(_BASE_CONFIG, None) == []


def test_check_manifest_paths_empty_block_returns_empty():
    assert rpr._check_manifest_paths(_BASE_CONFIG, {"block": {}}) == []


def test_check_manifest_paths_resolving_and_unresolving():
    manifest = {"block": {"kind": "forecast", "config_paths": [
        "/strategies/warmup",
        "/strategies/regimes/unknown/components/0/params/period",
        "/does/not/exist",
    ]}}
    missing = rpr._check_manifest_paths(_BASE_CONFIG, manifest)
    assert missing == ["/does/not/exist"]


# ---------------------------------------------------------------------------
# 7. Routing functions
# ---------------------------------------------------------------------------

def test_determine_post_strategy_config_authoring_route_spec_ready():
    run_dir = _minimal_run(rpr.ROOT, "run_810")
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", {"status": "spec_ready"})
    # E-056 1b block manifest: spec_ready now also needs a valid manifest.
    _write_backtest_spec_and_patches(run_dir, [])
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"


def test_determine_post_strategy_config_authoring_route_component_gap():
    run_dir = _minimal_run(rpr.ROOT, "run_811")
    # O-21: a complete gap (with a `tried` list naming a transform) pauses as before;
    # a bare one gets 1b's one retry first (tests/test_o21_component_gap_tried.py).
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", {
        "status": "component_gap",
        "tried": [{"config": "PriceEvolutionComponent(period=1) + [zscore]", "fails_on": "x"}]})
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"


def test_determine_post_strategy_config_authoring_route_unexpected_status():
    run_dir = _minimal_run(rpr.ROOT, "run_812")
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", {"status": "something_else"})
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"


def test_route_post_config_direct_backtest_specification_base_validated_routes_to_gate_when_enabled():
    _set_cda_flag(rpr.ROOT, True)
    # data_availability_gate defaults True (own inverted-default flag) when unset here.
    run_dir = _minimal_run(rpr.ROOT, "run_813")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml",
                   {"variants": {"base": {"status": "validated"}}})
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "data_availability_gate"


def test_route_post_config_direct_backtest_specification_base_missing_pauses():
    run_dir = _minimal_run(rpr.ROOT, "run_814")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {}})
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"


def test_route_post_config_direct_backtest_specification_base_not_tested_pauses():
    run_dir = _minimal_run(rpr.ROOT, "run_815")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml",
                   {"variants": {"base": {"status": "not_tested", "reason": "boom"}}})
    assert rpr._route_post_config_direct_backtest_specification(run_dir) == "human_pause"


# ---------------------------------------------------------------------------
# 8. run_tool_worker("backtest_specification", ...) end to end (subprocess mocked)
# ---------------------------------------------------------------------------

# E-056 1b block manifest: stage 1b now writes artifacts/block_manifest.yaml and
# the tool stage fails loud without it, so every tool-stage fixture carries one.
_MANIFEST = {
    "block": {"kind": "forecast", "config_paths": ["/strategies/regimes/unknown/components/0"]},
    "scaffolding": ["/strategies/warmup", "/regime_detector"],
    "rationale": "the RSI pullback component is the idea",
}


def _write_backtest_spec_and_patches(run_dir: Path, patches: list, manifest=_MANIFEST) -> None:
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml", {
        "status": "spec_ready", "config": _BASE_CONFIG, "config_rationale": ["x"],
        "component_gap": None,
    })
    rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml", {
        "base_config_ref": "artifacts/backtest_spec.yaml", "variants": patches,
    })
    if manifest is not None:
        rpr.save_yaml(run_dir / "artifacts" / "block_manifest.yaml", manifest)


def test_run_tool_worker_backtest_specification_all_variants_pass(monkeypatch):
    run_dir = _minimal_run(rpr.ROOT, "run_820")
    _write_backtest_spec_and_patches(run_dir, [
        {"variant_id": "base", "patch": [], "rationale": "base"},
        {"variant_id": "design_v2", "patch": [
            {"path": "/strategies/regimes/unknown/components/0/params/period", "value": 21}
        ], "rationale": "longer period"},
    ])

    def _fake_subprocess_run(cmd, *args, **kwargs):
        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("backtest_specification", "run_820"))

    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")
    assert index["variants"]["base"]["status"] == "validated"
    assert index["variants"]["design_v2"]["status"] == "validated"
    assert (run_dir / "artifacts" / "candidate_strategy_config.json").exists()
    assert (run_dir / "artifacts" / "variants" / "design_v2" / "strategy_config.json").exists()
    # base variant must NOT get its own subdirectory conflated with the top-level candidate --
    # both should exist independently.
    assert (run_dir / "artifacts" / "variants" / "base" / "strategy_config.json").exists()


def test_run_tool_worker_backtest_specification_patch_failure_records_component_request(monkeypatch):
    run_dir = _minimal_run(rpr.ROOT, "run_821")
    _write_backtest_spec_and_patches(run_dir, [
        {"variant_id": "base", "patch": [], "rationale": "base"},
        {"variant_id": "bad_patch", "patch": [
            {"path": "/does/not/exist", "value": 1}
        ], "rationale": "invalid target"},
    ])

    def _fake_subprocess_run(cmd, *args, **kwargs):
        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("backtest_specification", "run_821"))

    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")
    assert index["variants"]["base"]["status"] == "validated"
    assert index["variants"]["bad_patch"]["status"] == "not_tested"
    assert "patch application failed" in index["variants"]["bad_patch"]["reason"]

    requests = rpr.load_yaml(rpr.ROOT / "campaign_record" / "component_requests.yaml")
    reqs = requests["requests"]
    assert any(r["variant_id"] == "bad_patch" and r["run_id"] == "run_821" for r in reqs)


def test_run_tool_worker_backtest_specification_validate_config_failure_marks_not_tested_and_names_which_variant(monkeypatch):
    run_dir = _minimal_run(rpr.ROOT, "run_822")
    _write_backtest_spec_and_patches(run_dir, [
        {"variant_id": "base", "patch": [], "rationale": "base"},
        {"variant_id": "broken_config", "patch": [], "rationale": "duplicate of base, but validator fails it"},
    ])

    def _fake_subprocess_run(cmd, *args, **kwargs):
        config_path = cmd[-1]

        class _Fail:
            returncode = 1
            stdout = f"VIOLATION V9 {config_path}: fake failure\n"
            stderr = ""

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""

        return _Fail() if "broken_config" in config_path else _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("backtest_specification", "run_822"))

    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")
    assert index["variants"]["base"]["status"] == "validated"
    assert index["variants"]["broken_config"]["status"] == "not_tested"
    assert index["variants"]["broken_config"]["reason"] == "validate_config.py violations"
    report_path = run_dir / "artifacts" / "variants" / "broken_config" / "spec_validation_report.txt"
    assert report_path.exists()
    assert "VIOLATION V9" in report_path.read_text(encoding="utf-8")

    requests = rpr.load_yaml(rpr.ROOT / "campaign_record" / "component_requests.yaml")
    reqs = requests["requests"]
    match = [r for r in reqs if r["variant_id"] == "broken_config"]
    assert len(match) == 1
    assert match[0]["run_id"] == "run_822"
    assert "VIOLATION V9" in match[0]["report"]


def _no_subprocess(*a, **kw):
    raise AssertionError("validate_config.py must not be reached")


def test_run_tool_worker_backtest_specification_manifest_absent_fails_loud(monkeypatch):
    """E-056 1b block manifest (was: 'gracefully absent'). 1b now writes
    block_manifest.yaml; without it the tool stage stops before building any
    variant."""
    run_dir = _minimal_run(rpr.ROOT, "run_823")
    _write_backtest_spec_and_patches(run_dir, [{"variant_id": "base", "patch": [], "rationale": "base"}],
                                     manifest=None)
    assert not (run_dir / "artifacts" / "block_manifest.yaml").exists()
    monkeypatch.setattr(rpr.subprocess, "run", _no_subprocess)
    with pytest.raises(RuntimeError, match="block_manifest.yaml is missing"):
        asyncio.run(rpr.run_tool_worker("backtest_specification", "run_823"))
    assert not (run_dir / "artifacts" / "variants" / "index.yaml").exists()


def test_run_tool_worker_backtest_specification_manifest_missing_path_marks_not_tested(monkeypatch):
    """The base config resolves every manifest path (checked up front); a variant
    whose patch removes a block path is not tested."""
    run_dir = _minimal_run(rpr.ROOT, "run_824")
    _write_backtest_spec_and_patches(run_dir, [
        {"variant_id": "base", "patch": [], "rationale": "base"},
        {"variant_id": "drops_block", "patch": [{"path": "/strategies/regimes/unknown", "value": None}],
         "rationale": "removes the block"},
    ])
    tested = []

    def _fake_subprocess_run(cmd, *args, **kwargs):
        tested.append(cmd[-1])

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    asyncio.run(rpr.run_tool_worker("backtest_specification", "run_824"))
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")
    assert index["variants"]["base"]["status"] == "validated"
    assert index["variants"]["drops_block"]["status"] == "not_tested"
    assert "manifest paths unresolved" in index["variants"]["drops_block"]["reason"]
    assert not any("drops_block" in t for t in tested)


def test_run_tool_worker_backtest_specification_raises_on_duplicate_variant_id(monkeypatch):
    """Self-adversarial-review finding: a duplicate variant_id must raise loudly, not
    silently overwrite the first entry's recorded result in index.yaml."""
    run_dir = _minimal_run(rpr.ROOT, "run_827")
    _write_backtest_spec_and_patches(run_dir, [
        {"variant_id": "base", "patch": [], "rationale": "first"},
        {"variant_id": "base", "patch": [], "rationale": "duplicate id, different rationale"},
    ])

    def _fake_subprocess_run(cmd, *args, **kwargs):
        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    with pytest.raises(RuntimeError, match="duplicate variant_id"):
        asyncio.run(rpr.run_tool_worker("backtest_specification", "run_827"))


def test_run_tool_worker_backtest_specification_raises_if_base_spec_not_spec_ready():
    run_dir = _minimal_run(rpr.ROOT, "run_825")
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml", {"status": "component_gap", "config": None})
    with pytest.raises(RuntimeError, match="spec_ready"):
        asyncio.run(rpr.run_tool_worker("backtest_specification", "run_825"))


def test_run_tool_worker_backtest_specification_raises_if_variant_patches_missing():
    run_dir = _minimal_run(rpr.ROOT, "run_826")
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml", {"status": "spec_ready", "config": _BASE_CONFIG})
    with pytest.raises(RuntimeError, match="variant_patches"):
        asyncio.run(rpr.run_tool_worker("backtest_specification", "run_826"))


# ---------------------------------------------------------------------------
# 9. validate_config.py's real VIOLATION V12 check on an invented class name
# ---------------------------------------------------------------------------

def test_validate_config_v12_fires_on_invented_class_name():
    """Direct import, not subprocess/TBOT_PYTHON -- proves the check this new tool-stage
    branch relies on (validate_config.py's V12) actually fires, independent of whether
    this environment has a resolvable trading-bot venv for the subprocess path."""
    if str(TRADING_BOT_TOOLS_PATH) not in sys.path:
        sys.path.insert(0, str(TRADING_BOT_TOOLS_PATH))
    import validate_config as _vc

    bad_config = {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                             "default_regime": "unknown"},
        "strategies": {"warmup": 51, "regimes": {
            "unknown": {"components": [
                {"id": "x", "class": "strategies.strategy_components.TotallyInventedComponent",
                 "params": {}, "weight": 1.0, "transforms": [{"op": "identity"}]},
            ]},
            "trending": None, "mean_reversion": None, "chop": None,
        }},
    }
    violations = _vc.validate(bad_config)
    assert any("VIOLATION V12" in v and "TotallyInventedComponent" in v for v in violations), (
        f"expected a V12 violation naming the invented class; got: {violations}"
    )


def test_validate_config_v12_passes_on_real_class_name():
    if str(TRADING_BOT_TOOLS_PATH) not in sys.path:
        sys.path.insert(0, str(TRADING_BOT_TOOLS_PATH))
    import validate_config as _vc

    violations = _vc.validate(_BASE_CONFIG)
    assert not any("VIOLATION V12" in v for v in violations), (
        f"a real component class must never trip V12; got: {violations}"
    )


# ---------------------------------------------------------------------------
# 10. Permanent regression guard: no rule silently dropped in the skill rewrite
#     (build step 1's own pre-registered success signal, E-056 Slice 3b)
# ---------------------------------------------------------------------------

_SKILLS_DIR = Path(__file__).parent.parent / "workflow_artifacts" / "skills"


def _extract_section(text: str, header: str, next_header: str) -> str:
    start = text.index(header)
    end = text.index(next_header, start)
    return text[start:end]


def test_ungated_hypotheses_and_forbidden_sections_carried_over_byte_identical():
    """The retired skill (backtest-engineering) and the new one
    (strategy-config-authoring) must carry these two sections byte-identically --
    this is the literal pre-registered success signal named in this slice's own
    build-step-1 instructions. Fails loudly (with the actual diff) the moment either
    file drifts, instead of relying on a one-time manual read at build time."""
    old = (_SKILLS_DIR / "backtest-engineering" / "SKILL.md").read_text(encoding="utf-8")
    new = (_SKILLS_DIR / "strategy-config-authoring" / "SKILL.md").read_text(encoding="utf-8")

    old_ungated = _extract_section(old, "## Ungated hypotheses", "## Replication guard")
    new_ungated = _extract_section(new, "## Ungated hypotheses", "## Replication guard")
    old_forbidden = _extract_section(old, "## Forbidden", "## Context rule")
    new_forbidden = _extract_section(new, "## Forbidden", "## Context rule")

    if old_ungated != new_ungated or old_forbidden != new_forbidden:
        import difflib
        diff = "\n".join(difflib.unified_diff(
            (old_ungated + old_forbidden).splitlines(),
            (new_ungated + new_forbidden).splitlines(),
            fromfile="backtest-engineering/SKILL.md", tofile="strategy-config-authoring/SKILL.md",
            lineterm="",
        ))
        pytest.fail(
            "A rule was silently dropped or changed in the 'Ungated hypotheses' or "
            f"'Forbidden' section between the retired and new skill:\n{diff}"
        )


# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSIONS (2026-09-21)
# ---------------------------------------------------------------------------

def test_config_direct_authoring_enabled_raises_on_non_bool_value():
    """A quoted "false" string reads truthy under bool() -- the same trap
    _data_availability_gate_enabled() was already patched to fail loudly on
    in this same file. This flag is off_incomplete/unproven against a real
    LLM pass; a misconfiguration that reads as truthy would silently
    activate the whole reshaped pipeline."""
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {"config_direct_authoring": {"enabled": "false"}}}, f)

    with pytest.raises(ValueError, match="not a real"):
        rpr._config_direct_authoring_enabled()


def test_config_direct_authoring_enabled_raises_on_null_value():
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        f.write("orchestrator:\n  config_direct_authoring:\n    enabled:\n")

    with pytest.raises(ValueError, match="not a real"):
        rpr._config_direct_authoring_enabled()


def test_patch_application_non_dict_entry_raises_patch_error_not_typeerror():
    """A malformed patch entry that isn't a mapping at all (e.g. `patch: [21]`
    instead of `patch: [{path: ..., value: 21}]`) used to reach
    `"value" not in (op or {})`, which for a truthy non-dict like an int
    raises a bare TypeError instead of PatchApplicationError -- uncaught by
    run_tool_worker's per-variant handler, crashing the whole tool stage for
    every variant instead of marking just this one not_tested."""
    with pytest.raises(rpr.PatchApplicationError, match="expected a mapping"):
        rpr._apply_json_pointer_patch(_BASE_CONFIG, [21])
    with pytest.raises(rpr.PatchApplicationError, match="expected a mapping"):
        rpr._apply_json_pointer_patch(_BASE_CONFIG, ["not-a-dict"])
    with pytest.raises(rpr.PatchApplicationError, match="expected a mapping"):
        rpr._apply_json_pointer_patch(_BASE_CONFIG, [None])


def test_run_tool_worker_backtest_specification_unsafe_variant_id_raises(monkeypatch):
    """variant_id is LLM-authored and gets used as a bare filesystem path
    segment (variants_dir / variant_id). A path-separator or '..' in it
    (an authoring slip, or worse) must be refused before it's ever used to
    construct a write path, not silently followed outside artifacts/variants/."""
    run_dir = _minimal_run(rpr.ROOT, "run_823")
    _write_backtest_spec_and_patches(run_dir, [
        {"variant_id": "../../escape", "patch": [], "rationale": "malicious or malformed"},
    ])

    def _fake_subprocess_run(cmd, *args, **kwargs):
        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    with pytest.raises(RuntimeError, match="not a safe bare identifier"):
        asyncio.run(rpr.run_tool_worker("backtest_specification", "run_823"))


def test_b7_mandatory_input_stages_includes_strategy_config_authoring():
    """Under config-direct-authoring, strategy_config_authoring -- not
    backtest_specification -- is the LLM stage that compiles the hypothesis
    into a binding config. B7 exists specifically to prevent a compiling
    stage from deciding without pre_registration.yaml; omitting the new
    stage here would silently reopen that exact gap."""
    assert "strategy_config_authoring" in rpr._B7_MANDATORY_INPUT_STAGES
    # backtest_specification must remain too -- flag-off it is still the
    # LLM-authoring stage exactly as before.
    assert "backtest_specification" in rpr._B7_MANDATORY_INPUT_STAGES
