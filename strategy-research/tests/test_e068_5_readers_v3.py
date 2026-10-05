"""
E-068 slice 5 (D-073, CUL-403): readers v3, behind orchestrator.reader_findings.enabled.

Operator decisions 2026-10-05: five short v3 SKILLs (the v2 SKILLs untouched);
the claim's measured numbers as a code digest; CLAIM_TESTS.md instead of the
design guide (the catalogue stays); two code skip rules; a side finding is a
full claim block, at most 2 per reader; a changed pre-filled claim is a
warning. Additions: (1) no verdict in the format or in any code-written
wording; (2) every skip recorded with its rule, shown in the campaign summary,
never written as `[]`; (3) a side finding whose tests cannot see a block is
allowed (a pure finding); a block-kind claim gets CLAIM_TESTS.md's visibility
rule as a warning.

Sections:
  1. The flag.
  2. Flag off: byte-identical (v2 SKILLs, handoff, retry text, files, memory, summary).
  3. The v3 shape (reader_proposals), and v2 + v3 coexisting.
  4. No verdict: no field, no code-written wording.
  5. Checks where a reading is written (check_claim, the patch on the real config,
     scaffolding), the retry and the salvage.
  6. Skip rules, on run_070's real manifest, config and report.
  7. Inputs: handoff, prompt, digest (run_070's real numbers), earlier findings.
  8. Side findings: warnings, decide-next candidates and the brief.
  9. Step 1a: the pre-filled claim.
 10. The v3 rubric names are pinned to the v3 SKILLs.

No LLM: _invoke_reader_llm is replaced wherever it is reached.
"""
import ast
import copy
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import reader_proposals as rp  # noqa: E402
import reader_findings as rf  # noqa: E402
import decide_next as dn  # noqa: E402
import claim_findings as cf  # noqa: E402
import campaign_memory as cm  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    RUN_ID, _seed_run, _set_orchestrator, _fake_llm, _proposal)
from test_e058_s2a_regroup_record import ALL_ON as REGROUP_ON  # noqa: E402

FIX4 = SR_ROOT / "tests" / "fixtures" / "e068_4" / "run_070"
FIX5 = SR_ROOT / "tests" / "fixtures" / "e068_5"
CLAIMS_ON = {**REGROUP_ON, "config_direct_authoring": {"enabled": True},
             "claim_tests": {"enabled": True}}
V3_ON = {**CLAIMS_ON, "reader_findings": {"enabled": True}}
HIGH, LOW = "high_close_shock_reversion", "low_close_shock_reversion"
HIGH_HASH = "c688b1863f8cb3ff4d3a3bb05e0c15d5b885d27a65d3b805ad1990263fa83a99"
VERDICT_WORDS = re.compile(r"\b(true|false|supported|refuted|supports|refutes)\b", re.IGNORECASE)
# sha256 of origin/master's v2 reader SKILLs (LF), measured 2026-10-05 with
# `git show origin/master:<path> | sha256sum` at 4a6185b7.
V2_SKILL_SHA256 = {
    "profitability": "95dd0d9bcf1a8456f4a737528031eaebcf2e3d36ba9684d36c41dcccd4188b56",
    "forecast_power": "8139b546a575aaf57da9d1763b08b9d9e71aa1ab8c4df71fcc163284f4d9d59a",
    "regime_power": "00e68c366e32d14602d8cdedebb985c1956df4b7d366d450814ce101dad532d3",
    "component_attribution": "96783aec70dc2fc806e71b00af7baec28e32a55d1542624599ddc335852f2dbe",
    "trade_efficiency": "da251b6efa68faf174f22eeae2e187ebfb2228d1b9251e34076c3b8701147785",
}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _seed_v3_docs() -> None:
    """The real flag-on input files, under the sandbox ROOT (run-relative ../../)."""
    for rel in ("workflow_artifacts/skills/hypothesis-design/CLAIM_TESTS.md",
                "workflow_artifacts/skills/readers_v3/READING_CONTRACT.md",
                "workflow_artifacts/skills/hypothesis-design/PREFILLED_CLAIM.md"):
        dst = rpr.ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SR_ROOT / rel, dst)


def _claim(statement="After a large 1h up-move, the next 1-6h returns are higher.",
           kind="event_behaviour", field="past_return", side="top", tests=None) -> dict:
    sel = {"kind": "quantile", "field": field, "side": side, "q": 0.1, "lookback": 100}
    if field == "past_return":
        sel["bars"] = 1
    return {
        "statement": statement, "kind": kind,
        "tests": tests if tests is not None else [{
            "name": "big_move_followthrough", "selector": sel,
            "outcome": {"kind": "fwd_return", "horizons": [1, 2, 4, 6]},
            "baseline": {"kind": "complement"}, "statistic": "decay_curve",
            "direction": "greater", "floor": {"min_events": 50, "min_windows": 4},
            "consistency": {"unit": "window", "min_same_sign": 3}}],
        "pass_if": "effect above zero at 1-6h in most windows",
        "fail_if": "effect at or below zero",
        "rationale": "seen in the trade report's entry drift",
    }


def _scores(n=2) -> dict:
    return {"confidence_real": n, "distance_to_profitable": n, "mechanism_plausibility": n}


def _reading(cat="trade_efficiency", run_id=RUN_ID, sides=None, patch=None, **over) -> dict:
    rid = f"{cat}-{run_id}"
    doc = {"schema_version": 3, "reading_id": rid, "model_id": "m",
           "rubric_version": f"{cat}-reading-v1",
           "explanation": "Entries came one bar late on most trades.",
           "evidence": ["variants.base.slices.overall.x=1"],
           "side_findings": sides if sides is not None else [
               {"proposal_id": f"{rid}-1", "claim": _claim(),
                "evidence": ["variants.base.slices.overall.y=2"], "scores": _scores()}],
           "patch": patch}
    doc.update(over)
    return doc


def _patch(cat="trade_efficiency", run_id=RUN_ID, n=2, component="shock_reversal",
           field="params.period", before=1, after=2) -> dict:
    return {"proposal_id": f"{cat}-{run_id}-{n}",
            "patch": [{"component_id": component, "field": field, "before": before,
                       "after": after}],
            "evidence": ["variants.base.slices.overall.boundary_recross_rate=0.9926"],
            "scores": _scores(3)}


def _fenced(doc) -> str:
    return "```yaml\n" + yaml.safe_dump(doc, sort_keys=False) + "```"


def _write(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _run070_shaped(monkeypatch, flags=V3_ON) -> Path:
    """A seeded run with run_070's real base config and block manifest."""
    _set_orchestrator(flags)
    monkeypatch.chdir(SR_ROOT)
    _seed_v3_docs()
    run_dir = _seed_run()
    arts = run_dir / "artifacts"
    shutil.copyfile(FIX5 / "base_strategy_config.json", arts / "candidate_strategy_config.json")
    shutil.copyfile(FIX4 / "artifacts" / "block_manifest.yaml", arts / "block_manifest.yaml")
    shutil.copyfile(FIX5 / "component_attribution_overall.yaml",
                    arts / "reports" / "component_attribution.yaml")
    if flags.get("reader_findings", {}).get("enabled"):
        rpr._write_reader_v3_inputs(run_dir, RUN_ID)  # the stage writes them before any reader
    return run_dir


def _strings(obj, skip=("statement", "evidence", "explanation")):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield str(k)
            if k not in skip:
                yield from _strings(v, skip)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v, skip)
    elif isinstance(obj, str):
        yield obj


# ---------------------------------------------------------------------------
# 1. The flag
# ---------------------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(CLAIMS_ON)
    assert rpr._reader_findings_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(
        encoding="utf-8"))
    assert shipped["orchestrator"]["reader_findings"]["enabled"] is False


def test_flag_on_with_its_dependencies():
    _set_orchestrator(V3_ON)
    assert rpr._reader_findings_enabled() is True


@pytest.mark.parametrize("missing", ["claim_tests", "specialist_readers"])
def test_flag_on_without_a_dependency_raises(missing):
    flags = copy.deepcopy(V3_ON)
    flags[missing] = {"enabled": False}
    if missing == "specialist_readers":  # regroup_record itself requires it
        flags["regroup_record"] = {"enabled": False}
    _set_orchestrator(flags)
    with pytest.raises(ValueError, match=f"orchestrator.{missing}.enabled=true"):
        rpr._reader_findings_enabled()


@pytest.mark.parametrize("bad", ["true", "false", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**CLAIMS_ON, "reader_findings": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._reader_findings_enabled()


# ---------------------------------------------------------------------------
# 2. Flag off: byte-identical
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_v2_reader_skills_are_master_bytes(cat):
    raw = (SR_ROOT / "workflow_artifacts" / "skills" / "readers" / f"{cat}-reader"
           / "SKILL.md").read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(raw).hexdigest() == V2_SKILL_SHA256[cat]


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_flag_off_handoff_and_skill_are_v2(cat, monkeypatch):
    _set_orchestrator(CLAIMS_ON)  # claim_tests on, reader_findings off
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    h = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert rpr._reader_skill_dir(cat) == f"readers/{cat}-reader"
    assert [r["path"] for r in h["required_inputs"]] == [
        f"artifacts/reports/{cat}.yaml", "artifacts/grid_evaluation.yaml",
        "artifacts/hypothesis_card.yaml", "artifacts/candidate_strategy_config.json",
        "../../docs/COMPONENT_CATALOG.md", "../../docs/STRATEGY_DESIGN_GUIDE.md",
        "artifacts/registry_summary.yaml"]
    assert [r["path"] for r in h["optional_inputs"]] == ["artifacts/block_manifest.yaml"]
    assert h["objective"] == (
        f"Read artifacts/reports/{cat}.yaml (and artifacts/grid_evaluation.yaml) and propose "
        f"zero or more evidence-grounded changes. Output a single YAML list (`[]` for none) -- "
        f"it is written to artifacts/proposals/{cat}.yaml.")
    prompt = rpr._build_stage_prompt("specialist_readers", h, run_dir,
                                     skill_file_name=rpr._reader_skill_dir(cat))
    skill = (SR_ROOT / "workflow_artifacts" / "skills" / "readers" / f"{cat}-reader"
             / "SKILL.md").read_text(encoding="utf-8")
    assert skill in prompt and "READING_CONTRACT" not in prompt


def test_flag_off_retry_text_and_files_are_v2(monkeypatch):
    _set_orchestrator(CLAIMS_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    prompts = []
    answers = iter(["no block", "```yaml\n[]\n```"])

    async def _llm(prompt):
        prompts.append(prompt)
        return next(answers), {"usage": {}, "cost_usd": 0.0, "num_turns": 1}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm)
    rpr.run_reader_worker("profitability", RUN_ID, run_dir)
    assert prompts[1].endswith(
        "\n\n    Fix exactly this and output ONE fenced ```yaml block holding a YAML "
        "list of proposals (`[]` for none).\n")
    assert (run_dir / "artifacts" / "proposals" / "profitability.yaml").read_text(
        encoding="utf-8") == "[]\n"
    for name in (rf.DIGEST_ARTIFACT, rf.READER_SUMMARY_ARTIFACT):
        assert not (run_dir / "artifacts" / name).exists()


def test_flag_off_stage_writes_no_v3_file_and_no_skip_record(monkeypatch):
    run_dir = _run070_shaped(monkeypatch, flags=CLAIMS_ON)
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(None, calls))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert [c for c, _ in calls] == list(REPORT_CATEGORIES)  # nobody skipped
    for c in REPORT_CATEGORIES:
        assert yaml.safe_load((run_dir / "artifacts" / "proposals" / f"{c}.yaml").read_text(
            encoding="utf-8")) == []
    assert not (rpr.ROOT / rf.SKIPS_REL).exists()
    assert not (run_dir / "artifacts" / rf.DIGEST_ARTIFACT).exists()
    assert rf.skip_summary_lines(rpr.ROOT) == []


def test_memory_proposals_block_unchanged_for_v2_files(tmp_path):
    pdir = tmp_path / "artifacts" / "proposals"
    _write(pdir / "profitability.yaml", [_proposal("profitability", "run_1")])
    block = cm._proposals_block(tmp_path, "run_1", ["profitability", "regime_power"])
    assert [sorted(b) for b in block] == [["category", "count", "proposal_ids", "ref"]] * 2


def test_v2_candidate_record_has_no_new_keys():
    """A v2 patch still gets exactly the pre-slice-5 novelty keys and no warnings."""
    p = _proposal("trade_efficiency", "run_070")
    p["patch"] = [{"component_id": "shock_reversal", "field": "params.period",
                   "before": 1, "after": 2}]
    cand = dn._candidate("run_070", _memory_entry(), _src(), "trade_efficiency", p,
                         _inputs(), {})
    assert set(cand["gates"]["novelty"]) == {"exact_match", "matched_runs", "digest_advisory"}
    assert "warnings" not in cand


# ---------------------------------------------------------------------------
# 3. The v3 shape
# ---------------------------------------------------------------------------

def test_a_reading_loads_and_flattens(tmp_path):
    doc = _reading(patch=_patch())
    _write(tmp_path / "trade_efficiency.yaml", doc)
    items = rp.load_proposals(tmp_path, ["trade_efficiency"])["trade_efficiency"]
    assert [(i["proposal_id"], i["kind"]) for i in items] == [
        (f"trade_efficiency-{RUN_ID}-1", "side_finding"), (f"trade_efficiency-{RUN_ID}-2", "patch")]
    assert all(i["model_id"] == "m" and i["rubric_version"] == "trade_efficiency-reading-v1"
               for i in items)
    assert items[1]["patch"] == _patch()["patch"]
    assert rp.load_readings(tmp_path, ["trade_efficiency"])["trade_efficiency"] == doc


def test_an_empty_reading_proposes_nothing(tmp_path):
    _write(tmp_path / "profitability.yaml", _reading("profitability", sides=[]))
    assert rp.load_proposals(tmp_path, ["profitability"]) == {"profitability": []}


_BAD = [
    ("verdict key", lambda d: d.update(supports=True), "undeclared field"),
    ("claim_status key", lambda d: d.update(claim_status="measured"), "undeclared field"),
    ("idea_status key", lambda d: d.update(idea_status="refuted"), "undeclared field"),
    ("no explanation", lambda d: d.pop("explanation"), "missing"),
    ("blank explanation", lambda d: d.update(explanation=" "), "explanation"),
    ("empty evidence", lambda d: d.update(evidence=[]), "evidence"),
    ("no patch key", lambda d: d.pop("patch"), "missing"),
    ("three side findings", lambda d: d.update(side_findings=[
        {"proposal_id": f"{d['reading_id']}-{n}", "claim": _claim(), "evidence": ["e"],
         "scores": _scores()} for n in (1, 2, 3)]), "at most 2"),
    ("bad id", lambda d: d["side_findings"][0].update(proposal_id="trade_efficiency-x-1"),
     "proposal_id"),
    ("claim not a mapping", lambda d: d["side_findings"][0].update(claim="x"), "claim block"),
    ("side verdict key", lambda d: d["side_findings"][0].update(refutes=True), "side finding"),
    ("bad score", lambda d: d["side_findings"][0]["scores"].update(confidence_real=4), "0..3"),
    ("patch item", lambda d: d.update(patch={**_patch(), "patch": [{"component_id": "a",
                                                                     "field": "f"}]}),
     "component_id, field, before, after"),
    ("duplicate id", lambda d: d.update(patch=_patch(n=1)), "duplicate"),
    ("wrong category", lambda d: d.update(reading_id=f"profitability-{RUN_ID}"), "reading_id"),
]


@pytest.mark.parametrize("label,mutate,match", _BAD, ids=[b[0] for b in _BAD])
def test_a_malformed_reading_is_refused(tmp_path, label, mutate, match):
    doc = _reading()
    mutate(doc)
    _write(tmp_path / "trade_efficiency.yaml", doc)
    with pytest.raises(rp.ProposalError, match=re.escape(match) if " " in match else match):
        rp.load_proposals(tmp_path, ["trade_efficiency"])


def test_skipped_is_written_by_code_only():
    doc = rf.skipped_reading("regime_power", RUN_ID, {"rule": rf.SKIP_REGIME_SCAFFOLDING,
                                                      "reason": "r"})
    rp.check_reading(doc, "regime_power", "w")              # code's file: accepted
    with pytest.raises(rp.ProposalError, match="written by code only"):
        rp.check_reading(doc, "regime_power", "w", from_model=True)
    bad = {**doc, "skipped": {"rule": "nothing_to_say", "reason": "r"}}
    with pytest.raises(rp.ProposalError, match="rule in"):
        rp.check_reading(bad, "regime_power", "w")


def test_strict_provenance_wants_the_v3_rubric(tmp_path):
    _write(tmp_path / "trade_efficiency.yaml",
           _reading(rubric_version="trade_efficiency-reader-v2"))
    with pytest.raises(rp.ProposalError, match="v3 rubric"):
        rp.load_proposals(tmp_path, ["trade_efficiency"], strict_provenance=True)
    _write(tmp_path / "trade_efficiency.yaml", _reading())
    rp.load_proposals(tmp_path, ["trade_efficiency"], strict_provenance=True)


def test_v2_and_v3_files_load_side_by_side(tmp_path):
    shutil.copyfile(FIX5 / "trade_efficiency_v2.yaml", tmp_path / "trade_efficiency.yaml")
    shutil.copyfile(FIX5 / "regime_power_v2.yaml", tmp_path / "regime_power.yaml")
    _write(tmp_path / "profitability.yaml", _reading("profitability", run_id="run_070"))
    out = rp.load_proposals(tmp_path, ["trade_efficiency", "regime_power", "profitability"])
    assert out["trade_efficiency"][0]["proposal_id"] == "trade_efficiency-run_070-1"
    assert out["regime_power"][0]["kind"] == "new_block"
    assert out["profitability"][0]["kind"] == "side_finding"


# ---------------------------------------------------------------------------
# 4. No verdict
# ---------------------------------------------------------------------------

def test_the_format_has_no_verdict_field():
    keys = (rp._READING_KEYS | rp._SIDE_FINDING_KEYS | rp._V3_PATCH_KEYS
            | rp._SKIPPED_READING_KEYS | rp._SKIP_RECORD_KEYS)
    assert not keys & {"supports", "refutes", "verdict", "claim_status", "idea_status",
                       "supported", "refuted", "true", "false", "claim_reading"}


def test_no_verdict_words_in_the_new_modules_strings():
    for rel in ("tools/reader_findings.py",):
        tree = ast.parse((SR_ROOT / rel).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert not VERDICT_WORDS.search(node.value), (rel, node.value)


def test_no_verdict_words_in_any_code_written_output(tmp_path, monkeypatch):
    run_dir = tmp_path / "run_070"
    shutil.copytree(FIX4, run_dir)
    outputs = [rf.claim_result_digest(run_dir)]
    memory = {"runs": {"run_070": {"recorded_at": "x", cf.FINDING_KEY: cf.build_finding(
        run_dir, "run_070", yaml.safe_load((run_dir / "memory_entry.yaml").read_text(
            encoding="utf-8")))}}}
    outputs.append(rf.reader_findings_summary(memory, "run_071"))
    for rule in rp.SKIP_RULES:
        outputs.append(rf.skipped_reading("regime_power", "run_071", {"rule": rule,
                                                                      "reason": "r"}))
    outputs.append(rf.skip_rule("regime_power", manifest={"scaffolding": ["/regime_detector"]}))
    outputs.append(rf.skip_rule("regime_power", base_config={"regime_detector": {}}))
    outputs.append(rf.skip_rule("component_attribution", report=yaml.safe_load(
        (FIX5 / "component_attribution_overall.yaml").read_text(encoding="utf-8"))))
    item = {"proposal_id": "x-run_071-1", "claim": _claim(kind="direction_forecast",
                                                          field="close")}
    review = rf.side_finding_review(item, prior={}, own=set(), run_id="run_071")
    outputs.append(review)
    outputs.append(rf.test_request_row("run_071", "H", "x", {"proposal_id": "x-run_071-1",
                                                           "claim": {"tests": "none"}},
                                       {"missing_block": "m"}))
    _write(rpr.ROOT / rf.SKIPS_REL, {"runs": {"run_071": {"regime_power": {
        "rule": rf.SKIP_REGIME_SCAFFOLDING, "reason": "r"}}}})
    outputs.append(rf.skip_summary_lines(rpr.ROOT))
    for out in outputs:
        for s in _strings(out):
            assert not VERDICT_WORDS.search(s), s


# ---------------------------------------------------------------------------
# 5. Checks where a reading is written
# ---------------------------------------------------------------------------

def _validate(run_dir, doc, cat="trade_efficiency"):
    return rpr._validate_reader_output(_fenced(doc), cat, run_dir)


def test_run_070s_real_patch_passes_against_its_real_config(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    real = yaml.safe_load((FIX5 / "trade_efficiency_v2.yaml").read_text(encoding="utf-8"))[0]
    patch = {k: real[k] for k in ("patch", "evidence", "scores")}
    body, err = _validate(run_dir, _reading(sides=[], patch={
        "proposal_id": f"trade_efficiency-{RUN_ID}-1", **patch}))
    assert err is None, err


def test_an_invented_component_is_refused(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    _body, err = _validate(run_dir, _reading(patch=_patch(component="keltner_breakout_entry")))
    assert err and "patch_unresolvable" in err and "keltner_breakout_entry" in err


def test_a_stale_before_is_refused(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    _body, err = _validate(run_dir, _reading(patch=_patch(before=5)))
    assert err and "stale_before" in err


def test_a_patch_under_scaffolding_is_refused(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    cfg = json.loads((FIX5 / "base_strategy_config.json").read_text(encoding="utf-8"))
    cfg["regime_detector"]["components"] = [{"id": "er", "class": "x", "params": {"period": 20}}]
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text(
        json.dumps(cfg), encoding="utf-8")
    _body, err = _validate(run_dir, _reading(patch=_patch(component="er", before=20, after=30)))
    assert err and "/regime_detector/components/0/params/period" in err and "scaffolding" in err


def test_a_side_finding_claim_goes_through_check_claim(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    claim = _claim()
    claim["tests"][0]["selector"]["field"] = "volume_spike"
    _body, err = _validate(run_dir, _reading(sides=[{
        "proposal_id": f"trade_efficiency-{RUN_ID}-1", "claim": claim, "evidence": ["e"],
        "scores": _scores()}]))
    assert err and err.startswith("side_findings[0]: claim.tests[0]")


def test_a_wrong_run_and_a_model_skip_are_refused(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    _b, err = _validate(run_dir, _reading(run_id="run_001", sides=[]))
    assert err and "must be 'trade_efficiency-run_990'" in err
    _b, err = _validate(run_dir, rf.skipped_reading("trade_efficiency", RUN_ID,
                                                    {"rule": rf.SKIP_SINGLE_COMPONENT,
                                                     "reason": "r"}))
    assert err and "written by code only" in err


def test_retry_text_is_v3_and_a_bad_side_finding_is_dropped(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    bad = _claim()
    bad["tests"][0]["statistic"] = "magic"
    doc = _reading(sides=[
        {"proposal_id": f"trade_efficiency-{RUN_ID}-1", "claim": bad, "evidence": ["e"],
         "scores": _scores()},
        {"proposal_id": f"trade_efficiency-{RUN_ID}-2", "claim": _claim(), "evidence": ["e"],
         "scores": _scores()}])
    prompts = []

    async def _llm(prompt):
        prompts.append(prompt)
        return _fenced(doc), {"usage": {}, "cost_usd": 0.0, "num_turns": 1}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm)
    dest = rpr.run_reader_worker("trade_efficiency", RUN_ID, run_dir)
    assert "ONE reading mapping (schema_version: 3" in prompts[1]
    kept = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert [s["proposal_id"] for s in kept["side_findings"]] == [f"trade_efficiency-{RUN_ID}-2"]
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    dropped = audit["specialist_readers_trade_efficiency_attempt_0_retry1"]["dropped_proposals"]
    assert [d["index"] for d in dropped] == [0]


@pytest.mark.parametrize("answer", ["no yaml at all", "```yaml\n- a\n- b\n```",
                                    "```yaml\nschema_version: 3\nexplanation: x\n```"])
def test_an_unusable_answer_becomes_a_recorded_skip_not_an_empty_list(monkeypatch, answer):
    run_dir = _run070_shaped(monkeypatch)

    async def _llm(prompt):
        return answer, {"usage": {}, "cost_usd": 0.0, "num_turns": 1}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm)
    dest = rpr.run_reader_worker("profitability", RUN_ID, run_dir)
    doc = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert doc["skipped"]["rule"] == rf.SKIP_OUTPUT_REFUSED and doc != []
    assert rp.load_proposals(dest.parent, ["profitability"]) == {"profitability": []}
    block = cm._proposals_block(run_dir, RUN_ID, ["profitability"])[0]
    assert block["skipped"]["rule"] == rf.SKIP_OUTPUT_REFUSED and block["count"] == 0


# ---------------------------------------------------------------------------
# 6. Skip rules (run_070's real manifest, config and report)
# ---------------------------------------------------------------------------

def _fix(name):
    path = FIX5 / name
    return json.loads(path.read_text(encoding="utf-8")) if name.endswith(".json") else \
        yaml.safe_load(path.read_text(encoding="utf-8"))


def test_skip_rules_on_run_070():
    manifest = yaml.safe_load((FIX4 / "artifacts" / "block_manifest.yaml").read_text(
        encoding="utf-8"))
    cfg = _fix("base_strategy_config.json")
    assert rf.skip_rule("regime_power", manifest=manifest, base_config=cfg)["rule"] == \
        rf.SKIP_REGIME_SCAFFOLDING
    assert rf.skip_rule("regime_power", manifest=None, base_config=cfg)["rule"] == \
        rf.SKIP_REGIME_CONSTANT
    skip = rf.skip_rule("component_attribution", report=_fix("component_attribution_overall.yaml"))
    assert skip["rule"] == rf.SKIP_SINGLE_COMPONENT and "base: 1" in skip["reason"]
    for cat in ("profitability", "forecast_power", "trade_efficiency"):
        assert rf.skip_rule(cat, manifest=manifest, base_config=cfg,
                            report=_fix("component_attribution_overall.yaml")) is None


def test_no_skip_when_the_detector_is_a_real_gate_or_components_differ():
    gated = {"regime_detector": {"components": [{"id": "er"}], "rules": [{"if": "x"}]}}
    assert rf.skip_rule("regime_power", manifest={"scaffolding": ["/strategies/x"]},
                        base_config=gated) is None
    rules_only = {"regime_detector": {"components": [], "rules": [{"if": "x"}]}}
    assert rf.skip_rule("regime_power", base_config=rules_only) is None
    assert rf.skip_rule("regime_power", manifest={"scaffolding": ["/regime_detector/rules"]},
                        base_config=gated) is None   # part of the detector only
    report = _fix("component_attribution_overall.yaml")
    report["variants"]["uni_defi"]["slices"]["overall"]["components_discovered"].append("b")
    assert rf.skip_rule("component_attribution", report=report) is None
    single = _fix("component_attribution_overall.yaml")
    del single["variants"]["base"]["slices"]["overall"]["components_discovered"]
    assert rf.skip_rule("component_attribution", report=single) is None   # unknown: no skip


def test_the_stage_skips_two_readers_records_them_and_calls_three(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    calls = []
    answers = {c: _fenced(_reading(c, sides=[])) for c in REPORT_CATEGORIES}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(answers, calls))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert [c for c, _ in calls] == [c for c in REPORT_CATEGORIES if c in
                                     ("profitability", "forecast_power", "trade_efficiency")]
    pdir = run_dir / "artifacts" / "proposals"
    rules = {c: yaml.safe_load((pdir / f"{c}.yaml").read_text(encoding="utf-8"))
             .get("skipped", {}).get("rule") for c in REPORT_CATEGORIES}
    assert rules == {"profitability": None, "forecast_power": None,
                     "regime_power": rf.SKIP_REGIME_SCAFFOLDING,
                     "component_attribution": rf.SKIP_SINGLE_COMPONENT,
                     "trade_efficiency": None}
    record = yaml.safe_load((rpr.ROOT / rf.SKIPS_REL).read_text(encoding="utf-8"))
    assert sorted(record["runs"][RUN_ID]) == ["component_attribution", "regime_power"]
    lines = rf.skip_summary_lines(rpr.ROOT)
    assert "- Reader calls skipped: 2 in 1 run(s)" in lines
    assert any(rf.SKIP_SINGLE_COMPONENT in x and f"component_attribution in {RUN_ID}" in x
               for x in lines)
    block = {b["category"]: b for b in cm._proposals_block(run_dir, RUN_ID, REPORT_CATEGORIES)}
    assert block["regime_power"]["skipped"]["rule"] == rf.SKIP_REGIME_SCAFFOLDING
    assert "skipped" not in block["profitability"]


def test_the_campaign_summary_shows_the_skips_only_when_recorded():
    import run_campaign as camp
    queue = {"version": "1.0", "queue": []}
    camp._regenerate_summary(queue)
    assert "Readers skipped" not in camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")
    rf.record_skips(camp.ROOT, "run_071", {"regime_power": {
        "rule": rf.SKIP_REGIME_CONSTANT, "reason": "r"}})
    camp._regenerate_summary(queue)
    text = camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")
    assert "## Readers skipped by a code rule" in text
    assert f"{rf.SKIP_REGIME_CONSTANT}: 1 (regime_power in run_071)" in text


def test_summary_survives_an_unreadable_skip_record(tmp_path):
    (tmp_path / "campaign_record").mkdir()
    (tmp_path / rf.SKIPS_REL).write_text("runs: [unclosed", encoding="utf-8")
    assert "unreadable" in "\n".join(rf.skip_summary_lines(tmp_path))


def test_a_resume_reruns_neither_a_skip_nor_a_reader(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    monkeypatch.setattr(rpr, "_invoke_reader_llm",
                        _fake_llm({c: _fenced(_reading(c, sides=[])) for c in REPORT_CATEGORIES}))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(None, calls))
    rpr._run_specialist_readers(RUN_ID, run_dir)
    assert calls == []


# ---------------------------------------------------------------------------
# 7. Inputs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_v3_handoff_inputs(cat, monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    h = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    req = [r["path"] for r in h["required_inputs"]]
    assert rpr._reader_skill_dir(cat) == f"readers_v3/{cat}-reader"
    assert rpr.READER_V3_CONTRACT in req and rpr.CLAIM_TESTS_GUIDE in req
    assert "../../docs/COMPONENT_CATALOG.md" in req
    assert "../../docs/STRATEGY_DESIGN_GUIDE.md" not in req
    assert f"artifacts/{rf.DIGEST_ARTIFACT}" in req and f"artifacts/{rf.READER_SUMMARY_ARTIFACT}" in req
    assert [r["path"] for r in h["optional_inputs"]] == ["artifacts/block_manifest.yaml",
                                                         "artifacts/claim_status.yaml"]
    assert f"reading_id: {cat}-{RUN_ID}" in h["objective"]


def test_v3_prompt_carries_the_contract_and_the_short_skill(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    rpr._write_reader_v3_inputs(run_dir, RUN_ID)
    h = rpr._reader_handoff("trade_efficiency", RUN_ID, 0, run_dir)
    prompt = rpr._build_stage_prompt("specialist_readers", h, run_dir,
                                     skill_file_name=rpr._reader_skill_dir("trade_efficiency"))
    assert "# Reading contract (readers v3" in prompt
    assert "# Trade Efficiency Reader (v3)" in prompt
    assert "enter_earlier` is HINDSIGHT" in prompt
    assert "carried forward from verdict-interpreter" not in prompt  # no v2 SKILL text


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_v3_skills_are_short(cat):
    path = SR_ROOT / "workflow_artifacts" / "skills" / "readers_v3" / f"{cat}-reader" / "SKILL.md"
    assert len(path.read_bytes()) < 3_000   # v2: 20.6-25.6 KB
    assert len((SR_ROOT / "workflow_artifacts" / "skills" / "readers_v3"
                / "READING_CONTRACT.md").read_bytes()) < 6_000


@pytest.fixture
def run070(tmp_path) -> Path:
    dst = tmp_path / "run_070"
    shutil.copytree(FIX4, dst)
    return dst


def _horizon(digest, vid, test, h):
    return digest["variants"][vid]["tests"][test]["horizons"][h]


def test_digest_reproduces_run_070s_numbers(run070):
    d = rf.claim_result_digest(run070)
    assert d["claim_status"] == "measured" and d["block_visibility"] == "blind"
    assert d["manifest_kind"] == "forecast" and [t["name"] for t in d["tests"]] == [HIGH, LOW]
    assert d["tests"][0]["spec_hash"] == HIGH_HASH
    # VALIDATION_RUN.md: uni_defi top-10% close, 1h: -5.8 bp, 5/6 windows
    row = _horizon(d, "uni_defi", HIGH, "1")
    assert round(row["effect"] * 1e4, 1) == -5.8
    assert (row["windows_claimed_sign"], row["windows_with_value"]) == (5, 6)
    # base and shock_lookback_250 measure the same (the tests read price)
    assert d["variants"]["base"]["tests"] == d["variants"]["shock_lookback_250"]["tests"]
    # the same compact numbers slice 4's finding attaches
    finding = cf.build_finding(run070, "run_070", yaml.safe_load(
        (run070 / "memory_entry.yaml").read_text(encoding="utf-8")))
    for vid, rec in finding["result"]["per_variant"].items():
        assert d["variants"][vid]["tests"] == rec["tests"]
    assert len(yaml.safe_dump(d)) < 12_000   # vs 74 KB for the four raw files


def test_digest_attaches_no_stale_numbers(run070):
    path = run070 / "artifacts" / "variants" / "uni_defi" / "protocol_result.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    for e in doc["results"]:
        e["run_id"] = e["run_id"] + "_later_attempt"
    path.write_text(yaml.safe_dump(doc), encoding="utf-8")
    v = rf.claim_result_digest(run070)["variants"]["uni_defi"]
    assert v["status"] == "not_measured" and v["reason"] == "stale" and "tests" not in v


def test_digest_without_claim_status(run070):
    (run070 / "artifacts" / "claim_status.yaml").unlink()
    d = rf.claim_result_digest(run070)
    assert d["claim_status"] == "absent" and d["variants"] == {}


def test_reader_summary_leaves_this_run_out_and_is_compact(run070):
    entry = yaml.safe_load((run070 / "memory_entry.yaml").read_text(encoding="utf-8"))
    finding = cf.build_finding(run070, "run_070", entry)
    memory = {"runs": {"run_070": {"recorded_at": "2026-10-04", cf.FINDING_KEY: finding},
                       "run_071": {"recorded_at": "2026-10-05",
                                   cf.FINDING_KEY: {**finding, "finding_id": "F-run_071-1"}}}}
    s = rf.reader_findings_summary(memory, "run_071")
    assert [r["run_id"] for r in s["findings"]] == ["run_070"] and s["excludes_run"] == "run_071"
    test = s["findings"][0]["tests"][0]
    assert test["selector"]["field"] == "close" and test["spec_hash"] == HIGH_HASH
    assert test["by_variant"]["uni_defi"]["largest_effect"]["horizon"] == "12"
    assert len(yaml.safe_dump(s["findings"][0])) < 2_500   # slice 4's row: 3.8 KB
    assert rf.reader_findings_summary(memory, "run_071") == s   # deterministic
    many = {"runs": {f"run_{n:03d}": {"recorded_at": f"t{n:03d}", cf.FINDING_KEY: finding}
                     for n in range(30)}}
    assert rf.reader_findings_summary(many, "run_999")["n_listed"] == rf.READER_SUMMARY_MAX_ROWS


def test_v3_inputs_written_before_the_readers(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    for name in (rf.DIGEST_ARTIFACT, rf.READER_SUMMARY_ARTIFACT):
        (run_dir / "artifacts" / name).unlink()   # the stage itself must write them
    seen = []

    async def _llm(prompt):
        seen.append(rf.DIGEST_ARTIFACT in prompt and "CONTENT OF artifacts/"
                    + rf.READER_SUMMARY_ARTIFACT in prompt)
        cat = next(c for c in REPORT_CATEGORIES if f"reader_category: {c}\n" in prompt)
        return _fenced(_reading(cat, sides=[])), {"usage": {}, "cost_usd": 0.0, "num_turns": 1}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _llm)
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert seen and all(seen)
    assert (run_dir / "artifacts" / rf.DIGEST_ARTIFACT).exists()


# ---------------------------------------------------------------------------
# 8. Side findings: warnings, candidates, the brief
# ---------------------------------------------------------------------------

def test_review_of_a_side_finding():
    item = {"claim": _claim()}
    clean = rf.side_finding_review(item, prior={}, own=set(), run_id="r")
    assert clean["errors"] == [] and clean["warnings"] == [] and len(clean["spec_hashes"]) == 1
    h = clean["spec_hashes"][0]
    prior = {h: [{"run_id": "run_060", "status": "measured"}]}
    w = rf.side_finding_review(item, prior=prior, own=set(), run_id="r")["warnings"]
    assert w == [{"kind": rf.WARN_REPEAT, "spec_hash": h, "own_claim": False,
                  "runs": prior[h]}]
    w = rf.side_finding_review(item, prior=prior, own={h}, run_id="r")["warnings"]
    assert w[0]["own_claim"] is True and w[0]["runs"] == [{"run_id": "r", "status": None}]


def test_a_pure_finding_may_be_blind_a_block_claim_gets_a_warning():
    pure = rf.side_finding_review({"claim": _claim(kind="event_behaviour", field="close")},
                                  prior={}, own=set(), run_id="r")
    assert pure["errors"] == [] and pure["warnings"] == []
    block = rf.side_finding_review({"claim": _claim(kind="direction_forecast", field="close")},
                                   prior={}, own=set(), run_id="r")
    assert block["errors"] == [] and [w["kind"] for w in block["warnings"]] == [rf.WARN_BLIND]
    seeing = rf.side_finding_review({"claim": _claim(kind="direction_forecast",
                                                     field="forecast")},
                                    prior={}, own=set(), run_id="r")
    assert seeing["warnings"] == []


def test_tests_none_is_a_test_request():
    claim = {**_claim(), "tests": "none", "missing_block": "order book imbalance field"}
    review = rf.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r")
    assert review["tests_none"] and review["missing_block"] == "order book imbalance field"
    row = rf.test_request_row("run_070", "H-1", "trade_efficiency",
                              {"proposal_id": "trade_efficiency-run_070-1", "claim": claim},
                              review)
    assert row["hypothesis_id"] == "H-1__trade_efficiency-run_070-1"
    assert row["missing_block"] == "order book imbalance field"


def test_the_reading_review_records_warnings_and_test_requests(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    none_claim = {**_claim(), "tests": "none", "missing_block": "funding skew field"}
    doc = _reading(sides=[
        {"proposal_id": f"trade_efficiency-{RUN_ID}-1", "claim": _claim(
            kind="direction_forecast", field="close"), "evidence": ["e"], "scores": _scores()},
        {"proposal_id": f"trade_efficiency-{RUN_ID}-2", "claim": none_claim,
         "evidence": ["e"], "scores": _scores()}])
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm({"trade_efficiency": _fenced(doc)}))
    rpr.run_reader_worker("trade_efficiency", RUN_ID, run_dir)
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    review = audit["specialist_readers_trade_efficiency_attempt_0"]["reading_review"]
    assert [w["kind"] for w in review[f"trade_efficiency-{RUN_ID}-1"]["warnings"]] == [rf.WARN_BLIND]
    assert review[f"trade_efficiency-{RUN_ID}-2"]["tests_none"] is True
    reqs = yaml.safe_load((rpr.ROOT / "campaign_record" / "test_requests.yaml").read_text(
        encoding="utf-8"))
    assert [r["missing_block"] for r in reqs["requests"]] == ["funding skew field"]


# decide-next -------------------------------------------------------------

def _memory_entry() -> dict:
    return {"run_id": "run_070", "hypothesis_id": "H-070", "timeframe": "1h",
            "variants": {"base": {"status": "tested", "symbols": ["BTCUSD"], "n_windows": 6,
                                  "config_ref": "runs/run_070/artifacts/variants/base/"
                                                "strategy_config.json"}}}


def _src(items=None) -> dict:
    card = yaml.safe_load((FIX4 / "artifacts" / "hypothesis_card.yaml").read_text(
        encoding="utf-8"))
    return {"proposals": items or [], "base_variant": "base",
            "base_config": _fix("base_strategy_config.json"),
            "base_config_ref": "runs/run_070/artifacts/variants/base/strategy_config.json",
            "manifest": yaml.safe_load((FIX4 / "artifacts" / "block_manifest.yaml").read_text(
                encoding="utf-8")),
            "pre_registration": {"machine_constraints": {"protocol_ref": "protocols/p.json"}},
            "research_brief": {"strategy_domain": "d", "market_universe": "u",
                               "timeframe": "1h", "venue": "kraken", "product": "perp"},
            "card": card, "card_text": yaml.safe_dump(card)}


def _inputs(memory=None, runs=None) -> dict:
    return {"memory": memory or {"runs": {}}, "queue": {"queue": []},
            "existing_candidate_briefs": [], "known_classes": None, "feed_set": None,
            "digest": None, "protocol_specs": {}, "runs": runs or {}}


def _side(cat="trade_efficiency", n=1, claim=None) -> dict:
    return {"proposal_id": f"{cat}-run_070-{n}", "kind": rp.SIDE_FINDING,
            "claim": claim or _claim(), "evidence": ["variants.base.slices.overall.y=2"],
            "scores": _scores(), "model_id": "m", "rubric_version": f"{cat}-reading-v1"}


def test_a_side_finding_becomes_an_eligible_candidate():
    p = _side()
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(), {})
    assert cand["kind"] == "side_finding" and cand["eligible"] is True
    assert cand["gates"]["feasibility"]["result"] == "UNKNOWN"
    assert cand["gates"]["novelty"]["exact_match"] == "NOT_APPLICABLE"
    assert len(cand["gates"]["novelty"]["spec_hashes"]) == 1
    assert cand["hypothesis_id"] == "H-070__trade_efficiency-run_070-1"
    assert "warnings" not in cand


def test_a_repeated_test_is_a_warning_never_a_refusal():
    p = _side()
    h = rf.side_finding_review(p, prior={}, own=set(), run_id="x")["spec_hashes"][0]
    memory = {"runs": {"run_060": {cf.FINDING_KEY: {"status": "measured",
                                                    "tests": [{"spec_hash": h}]}}}}
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(memory), {})
    assert cand["eligible"] is True
    assert cand["warnings"] == [{"kind": rf.WARN_REPEAT, "spec_hash": h, "own_claim": False,
                                 "runs": [{"run_id": "run_060", "status": "measured"}]}]


def test_repeating_the_source_runs_own_claim_is_a_warning():
    card = yaml.safe_load((FIX4 / "artifacts" / "hypothesis_card.yaml").read_text(
        encoding="utf-8"))
    own_test = copy.deepcopy(card["claim"]["tests"][0])
    p = _side(claim=_claim(tests=[own_test]))
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(), {})
    assert cand["eligible"] is True
    assert cand["warnings"][0]["spec_hash"] == HIGH_HASH and cand["warnings"][0]["own_claim"]


@pytest.mark.parametrize("claim,reason", [
    ({**_claim(), "tests": "none", "missing_block": "m"}, "next_test_none"),
    ({**_claim(), "kind": "not_a_kind"}, "next_test_refused"),
    (_claim(kind="regime_classifier"), "regime_block_needs_composition"),
])
def test_ineligible_side_findings(claim, reason):
    p = _side(claim=claim)
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(), {})
    assert cand["eligible"] is False
    assert any(r.startswith(reason) for r in cand["gates"]["feasibility"]["reasons"])


def test_two_readers_with_the_same_tests_collapse():
    a, b = _side("trade_efficiency"), _side("profitability")
    b["scores"] = _scores(3)
    src = _src([a, b])
    cands = [dn._candidate("run_070", _memory_entry(), src, c, p, _inputs(), {})
             for c, p in (("trade_efficiency", a), ("profitability", b))]
    out = dn._collapse(cands)
    assert len(out) == 1 and out[0]["candidate_id"] == "profitability-run_070-1"


def test_the_brief_carries_the_claim_pre_filled():
    p = _side()
    src = _src([{"category": "trade_efficiency", "proposal": p}])
    inputs = _inputs(runs={"run_070": src})
    cand = dn._candidate("run_070", _memory_entry(), src, "trade_efficiency", p, inputs, {})
    record = {"picked": {"candidate_id": cand["candidate_id"],
                         "brief_path": f"x/{cand['candidate_id']}.md"},
              "candidates": [cand]}
    rel, text = dn.candidate_brief(record, inputs, decision_ref="d")
    front = yaml.safe_load(text.split("---\n")[1])
    assert front["candidate"]["claim"] == p["claim"]
    assert front["candidate"]["source"]["proposal"]["claim"] == p["claim"]
    assert "config" not in front["candidate"] and "manifest" not in front["candidate"]
    assert p["claim"]["statement"] in front["research_goal"]
    assert not VERDICT_WORDS.search(front["research_goal"].replace(p["claim"]["statement"], "")
                                    .replace("; ".join(p["evidence"]), ""))


def test_a_v2_brief_carries_no_claim():
    p = _proposal("trade_efficiency", "run_070")
    p["patch"] = [{"component_id": "shock_reversal", "field": "params.period",
                   "before": 1, "after": 2}]
    src = _src([{"category": "trade_efficiency", "proposal": p}])
    inputs = _inputs(runs={"run_070": src})
    cand = dn._candidate("run_070", _memory_entry(), src, "trade_efficiency", p, inputs, {})
    record = {"picked": {"candidate_id": cand["candidate_id"], "brief_path": "x/y.md"},
              "candidates": [cand]}
    _rel, text = dn.candidate_brief(record, inputs, decision_ref="d")
    front = yaml.safe_load(text.split("---\n")[1])
    assert "claim" not in front["candidate"] and "claim" not in front["candidate"]["source"]["proposal"]


# ---------------------------------------------------------------------------
# 9. Step 1a: the pre-filled claim
# ---------------------------------------------------------------------------

def _brief_with_claim(run_dir: Path, claim) -> None:
    cand = {"criteria_from": "hypothesis_generation", "source": {"hypothesis_id": "H-X"}}
    if claim is not None:
        cand["claim"] = claim
    _write(run_dir / "artifacts" / "research_brief.yaml", {"candidate": cand})


def test_1a_gets_the_note_only_when_the_brief_has_a_claim(monkeypatch):
    _set_orchestrator(CLAIMS_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    for claim, expected in ((None, False), (_claim(), True)):
        _brief_with_claim(run_dir, claim)
        handoff = {"required_inputs": []}
        rpr._apply_claim_tests_context("hypothesis_generation", handoff, run_dir)
        paths = [r["path"] for r in handoff["required_inputs"]]
        assert (rpr.PREFILLED_CLAIM_NOTE in paths) is expected


@pytest.mark.parametrize("change,status,changed", [
    (lambda c: c, "unchanged", []),
    (lambda c: {**c, "statement": "something else"}, "changed", ["statement"]),
    (lambda c: {**c, "tests": [{**c["tests"][0], "direction": "less"}]}, "changed",
     ["tests (spec_hash)"]),
])
def test_a_changed_prefilled_claim_is_a_recorded_warning(monkeypatch, capsys, change, status,
                                                         changed):
    _set_orchestrator(CLAIMS_ON)
    run_dir = _seed_run()
    _brief_with_claim(run_dir, _claim())
    _write(run_dir / "artifacts" / "hypothesis_card.yaml",
           {"hypothesis_id": "H-X", "claim": change(_claim())})
    rpr._check_prefilled_claim(run_dir, RUN_ID)
    rec = yaml.safe_load((run_dir / "artifacts" / rpr._CLAIM_PREFILL_FILE).read_text(
        encoding="utf-8"))
    assert (rec["status"], rec["changed"]) == (status, changed)
    assert ("changed the pre-filled claim" in capsys.readouterr().out) is bool(changed)


def test_no_prefill_record_without_a_prefilled_claim():
    _set_orchestrator(CLAIMS_ON)
    run_dir = _seed_run()
    _brief_with_claim(run_dir, None)
    rpr._check_prefilled_claim(run_dir, RUN_ID)
    assert not (run_dir / "artifacts" / rpr._CLAIM_PREFILL_FILE).exists()


# ---------------------------------------------------------------------------
# 10. Rubric pins
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_v3_rubric_is_the_one_its_skill_writes(cat):
    text = (SR_ROOT / "workflow_artifacts" / "skills" / "readers_v3" / f"{cat}-reader"
            / "SKILL.md").read_text(encoding="utf-8")
    assert f"name: {cat}-reader\n" in text
    assert f"`rubric_version: {rp.READER_RUBRIC_VERSIONS_V3[cat]}`" in text
    assert set(rp.READER_RUBRIC_VERSIONS_V3) == set(REPORT_CATEGORIES)
