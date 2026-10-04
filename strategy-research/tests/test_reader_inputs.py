"""
Readers get the claim, the block, the real settings and the design docs.

run_065 and run_066: both trade_efficiency readers proposed a `patch` on a
component and a setting that do not exist (`donchian_breakout.stop_loss_pct`,
`keltner_breakout_entry.params.entry_lookahead_bars`; the real ids were
`donchian_20` and `keltner_momentum`). The readers had never been given the
config, the component catalogue, or the idea they were reading about -- only
their report, the grid and the registry summary. Their SKILLs told them not to
invent names "absent from COMPONENT_CATALOG.md", a file they never received.

Now each reader handoff carries hypothesis_card.yaml, this run's base config,
COMPONENT_CATALOG.md and STRATEGY_DESIGN_GUIDE.md (required -- the same two
docs step 2 gets, O-4/D-053) and block_manifest.yaml (optional: a composition
run has none). Only the flag-on specialist_readers stage changes.

No LLM: _invoke_reader_llm is replaced wherever it is reached.
"""
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    ALL_ON, RUN_ID, _seed_run, _set_orchestrator)

CAT = "trade_efficiency"
CATEGORIES = ["profitability", "forecast_power", "regime_power", "component_attribution",
              "trade_efficiency"]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _paths(handoff: dict, key: str) -> list:
    return [r["path"] for r in handoff.get(key) or []]


def _write_index(run_dir: Path, variants: dict, create_configs: bool = True) -> None:
    """index.yaml plus (by default) each variant's config file, as 5a writes them."""
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": variants})
    if create_configs:
        for vid, info in variants.items():
            rel = (info or {}).get("config_path") or f"artifacts/variants/{vid}/strategy_config.json"
            path = run_dir / str(rel).replace("\\", "/")
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text('{"marker": "%s"}\n' % vid, encoding="utf-8")


def _prompt(run_dir: Path, category: str = CAT) -> str:
    handoff = rpr._reader_handoff(category, RUN_ID, 0, run_dir)
    return rpr._build_stage_prompt("specialist_readers", handoff, run_dir,
                                   skill_file_name=rpr._reader_skill_dir(category))


# ---------------------------------------------------------------------------
# 1. What the handoff lists
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cat", CATEGORIES)
def test_every_reader_gets_the_card_config_and_design_docs(cat):
    handoff = rpr._reader_handoff(cat, RUN_ID, 0)
    req = _paths(handoff, "required_inputs")
    for path in ("artifacts/hypothesis_card.yaml", "artifacts/candidate_strategy_config.json",
                 "../../docs/COMPONENT_CATALOG.md", "../../docs/STRATEGY_DESIGN_GUIDE.md"):
        assert path in req, path
    assert _paths(handoff, "optional_inputs") == ["artifacts/block_manifest.yaml"]
    assert req[-1] == "artifacts/registry_summary.yaml"


def test_the_config_is_the_base_variants_when_the_variant_loop_ran(tmp_path):
    run_dir = tmp_path / "runs" / RUN_ID
    _write_index(run_dir, {
        "base": {"config_path": "artifacts\\variants\\base\\strategy_config.json"},
        "design_1": {"config_path": "artifacts\\variants\\design_1\\strategy_config.json"}})
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/variants/base/strategy_config.json"


def test_without_a_base_id_the_sorted_first_variant_is_the_base(tmp_path):
    """json_pointer.base_variant_id's rule -- the base decide_next resolves against."""
    run_dir = tmp_path / "runs" / RUN_ID
    _write_index(run_dir, {"zeta": {"config_path": "artifacts/variants/zeta/strategy_config.json"},
                           "alpha": {}})
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/variants/alpha/strategy_config.json"


@pytest.mark.parametrize("ids", [["base", "design_1", "asset_1"], ["zeta", "alpha"]])
def test_the_readers_base_is_the_base_decide_next_resolves_patches_against(tmp_path, ids):
    """decide_next.resolve_patch reads the config_ref of decide_next._base_variant;
    the reader must be shown that same config."""
    import decide_next
    run_dir = tmp_path / "runs" / RUN_ID
    rels = {v: f"artifacts\\variants\\{v}\\strategy_config.json" for v in ids}  # as written on Windows
    _write_index(run_dir, {v: {"config_path": rel} for v, rel in rels.items()})
    entry = {"run_id": RUN_ID,
             "variants": {v: {"config_ref": f"runs/{RUN_ID}/" + rel.replace("\\", "/")}
                          for v, rel in rels.items()}}
    _vid, base = decide_next._base_variant(entry)
    assert base["config_ref"] == f"runs/{RUN_ID}/" + rpr._reader_base_config_rel(run_dir)


def test_without_the_variant_loop_the_config_is_the_candidate_config(tmp_path):
    run_dir = tmp_path / "runs" / RUN_ID
    (run_dir / "artifacts").mkdir(parents=True)
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/candidate_strategy_config.json"
    assert rpr._reader_base_config_rel(None) == "artifacts/candidate_strategy_config.json"


# ---------------------------------------------------------------------------
# 2. What the prompt actually contains
# ---------------------------------------------------------------------------

def test_the_prompt_carries_each_new_input_verbatim(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-1", "thesis": "CLAIM_MARKER"})
    rpr.save_yaml(arts / "block_manifest.yaml", {"rationale": "MANIFEST_MARKER"})
    _write_index(run_dir, {"base": {"config_path": "artifacts/variants/base/strategy_config.json"}})
    cfg = arts / "variants" / "base" / "strategy_config.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text('{"id": "BASE_CONFIG_MARKER"}\n', encoding="utf-8")
    (rpr.ROOT / "docs" / "COMPONENT_CATALOG.md").write_text("CATALOG_MARKER\n", encoding="utf-8")
    (rpr.ROOT / "docs" / "STRATEGY_DESIGN_GUIDE.md").write_text("GUIDE_MARKER\n", encoding="utf-8")
    prompt = _prompt(run_dir)
    for marker in ("CLAIM_MARKER", "MANIFEST_MARKER", "BASE_CONFIG_MARKER", "CATALOG_MARKER",
                   "GUIDE_MARKER"):
        assert marker in prompt, marker
    assert '"marker": "CONFIG_MARKER"' not in prompt  # the base variant's, not the candidate's


def test_a_run_without_a_block_manifest_still_builds_the_prompt(monkeypatch):
    """A composition run writes no block_manifest.yaml (E-060 S3b)."""
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    assert not (run_dir / "artifacts" / "block_manifest.yaml").exists()
    assert "CONFIG_MARKER" in _prompt(run_dir)


@pytest.mark.parametrize("missing", ["artifacts/hypothesis_card.yaml",
                                     "artifacts/candidate_strategy_config.json",
                                     "../../docs/COMPONENT_CATALOG.md",
                                     "../../docs/STRATEGY_DESIGN_GUIDE.md"])
def test_a_missing_required_input_stops_before_any_model_call(monkeypatch, missing):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    (run_dir / missing).resolve().unlink()
    calls = []

    async def _spy(prompt):
        calls.append(prompt)
        return "```yaml\n[]\n```", {}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _spy)
    with pytest.raises(FileNotFoundError, match=Path(missing).name):
        rpr.run_reader_worker(CAT, RUN_ID, run_dir, stage_attempt=0)
    assert calls == []


# ---------------------------------------------------------------------------
# 3. Citations into the new files are measured, not reported unresolved
# ---------------------------------------------------------------------------

def test_a_citation_into_the_config_or_the_card_resolves(tmp_path):
    arts = tmp_path / "artifacts"
    rpr.save_yaml(arts / f"reports/{CAT}.yaml", {"marker": {"x": 1}})
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"signal_concept": {"horizon": "1-5 bars"}})
    (arts / "candidate_strategy_config.json").write_text(
        '{"strategies": {"regimes": {"unknown": {"weight": 1}}}}', encoding="utf-8")
    body = yaml.safe_dump([{"proposal_id": f"{CAT}-{RUN_ID}-1",
                            "evidence": ["strategies.regimes.unknown.weight=1",
                                         "signal_concept.horizon is 1-5 bars"]}])
    cit = rpr._citation_provenance(CAT, tmp_path, body)
    assert "candidate_strategy_config.json" in cit["files_read"]
    assert "hypothesis_card.yaml" in cit["files_read"]
    (rec,) = cit["proposals"].values()
    assert rec["unresolved"] == []
    assert sorted(rec["resolved"]) == ["signal_concept.horizon", "strategies.regimes.unknown.weight"]


# ---------------------------------------------------------------------------
# 4. The SKILLs say so
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cat", CATEGORIES)
def test_every_reader_skill_lists_the_new_inputs(cat):
    text = (SR_ROOT / "workflow_artifacts" / "skills" / rpr._reader_skill_dir(cat) /
            "SKILL.md").read_text(encoding="utf-8")
    required = text[text.index("## Required inputs"):text.index("**Scope boundary.**")]
    for name in ("hypothesis_card.yaml", "block_manifest.yaml", "strategy_config.json",
                 "COMPONENT_CATALOG.md", "STRATEGY_DESIGN_GUIDE.md", "registry_summary.yaml"):
        assert name in required, (cat, name)
    assert "(nothing else)" not in text
    # review 2026-10-03: the closing Context rule must not tell the reader to read
    # only report + grid + registry summary (it contradicted the new inputs).
    rule = text.split("## Context rule")[1].split("\n## ")[0]
    for name in ("hypothesis_card.yaml", "block_manifest.yaml", "strategy_config.json",
                 "COMPONENT_CATALOG.md", "STRATEGY_DESIGN_GUIDE.md", "registry_summary.yaml"):
        assert name in rule, (cat, name)
    assert "the one extra input" not in rule


def test_a_base_refused_before_its_config_was_written_falls_back_to_the_candidate(tmp_path):
    """review 2026-10-03: base not_tested with no config file on disk -> the readers
    get candidate_strategy_config.json instead of stopping on a missing input."""
    run_dir = tmp_path / "runs" / RUN_ID
    _write_index(run_dir, {"base": {"status": "not_tested"},
                           "design_1": {"config_path": "artifacts/variants/design_1/strategy_config.json"}},
                 create_configs=False)
    assert not (run_dir / "artifacts/variants/base/strategy_config.json").exists()
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/candidate_strategy_config.json"
