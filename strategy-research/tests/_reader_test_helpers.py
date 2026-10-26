"""The shared helpers the reader-stage tests build on (D-197).

Until D-197 about fifty test files imported their run seeding, flag sets, stub model calls and
reading builders from six TEST files (test_e046a_slice5b_ii_b_readers_stage,
test_c5_7b1_model_id_stamp, test_e068_5_readers_v3, test_e058_s2a_regroup_record,
test_e072_explore_confirm, test_e046a_slice5b_i_reader_skills) and from tests/conftest.py.
Those six files test the readers, which are being retired; their helpers are not reader
tests. They live here, in one module, so deleting a reader test file never breaks another
test file.

Not a test module: the name does not match pytest's `test_*.py`, so it is never collected.
It is imported the way the tests used to import each other (tests/ is on sys.path), e.g.
`from _reader_test_helpers import RUN_ID, _seed_run, _set_orchestrator`.

Names that were defined differently in two of the old files carry distinct names here:
  RUN_ID / ALL_ON                         the readers-stage run id (run_990) / flag set
  REGROUP_RUN_ID / REGROUP_ALL_ON         test_e058_s2a's run id (run_980) / flag set
                                          (READERS_ON plus regroup_record)
  _seed_run / _seed                       the readers-stage seed / the regroup_record seed
  _patch                                  the reader-patch builder of test_e068_5 (the decide-next
                                          `_patch` of test_e059_s2a keeps its own module)
The fixtures `_stub_tbot_python` (autouse in the modules that import it) and `reader_docs`
(opt-in, was in conftest.py) are fixtures: a module that wants one imports it by name.
"""
from __future__ import annotations

import asyncio
import csv
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import reader_proposals as rp  # noqa: E402
import build_reports as br  # noqa: E402
import claim_card as cc  # noqa: E402
import claim_measure as cmeas  # noqa: E402
import explore_confirm as ec  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import protocol_resolution as pres  # noqa: E402
from reader_categories import READER_CATEGORIES  # noqa: E402
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e059_s2a_decide_next import _patch as _decide_next_patch  # noqa: E402


# ---------------------------------------------------------------------------
# fixtures (was tests/conftest.py: reader_docs; and each module's own autouse stub)
# ---------------------------------------------------------------------------

# D-063: every specialist reader is required to receive the two design docs step
# 2 also gets, resolved run-relative as ROOT/docs/. A test that drives the full
# loop THROUGH the reader stage opts in (pytestmark usefixtures) to get verbatim
# copies of the real files in its sandbox -- opt-in, not autouse, so the other
# ~4,400 tests do not each copy ~65 KB into tmp (temp dirs once filled the disk).
_READER_DOCS = ("COMPONENT_CATALOG.md", "STRATEGY_DESIGN_GUIDE.md")


@pytest.fixture
def reader_docs(_sandbox_by_default):
    assert _sandbox_by_default is not None, (
        "reader_docs needs the default sandbox; a real_repo_readonly test reads the real "
        "docs/ already and must not use this fixture")
    docs = Path(_sandbox_by_default) / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    for name in _READER_DOCS:
        shutil.copyfile(Path(__file__).parent.parent / "docs" / name, docs / name)
    return docs


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# from test_e046a_slice5b_ii_b_readers_stage: the readers-stage run
# ---------------------------------------------------------------------------

RUN_ID = "run_990"
ALL_ON = {"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True},
          "specialist_readers": {"enabled": True}}


def _set_orchestrator(orchestrator: dict | None) -> None:
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    path = config_dir / "campaign_config.yaml"
    if orchestrator is None:
        if path.exists():
            path.unlink()
        return
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": orchestrator}, f)


def _protocol_result(errors_count=None, variant_dir: Path | None = None) -> dict:
    entry = {"symbol": "BTCUSDT", "window": "w1", "core": {"sharpe": 0.1}}
    if errors_count is not None:
        entry["component_errors"] = {"count": errors_count, "samples": []}
    return {"verdict": "kill", "results": [entry]}


def _seed_run(run_id=RUN_ID, idea_status="refuted", errors_count=None, pending="specialist_readers",
              with_reports=True) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = pending
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "protocol_result.yaml", _protocol_result(errors_count))
    rpr.save_yaml(arts / "grid_evaluation.yaml", {"result": "X", "marker": "GRID_MARKER"})
    # E-061 C2 S2e: the stage writes this before the first reader; tests that call
    # _run_specialist_readers directly need the stand-in the handoff now requires.
    rpr.save_yaml(arts / "registry_summary.yaml", {"marker": "REGISTRY_SUMMARY_MARKER"})
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-TEST-1"})
    # Reader inputs: this run's base config and the two design docs step 2 also
    # gets (resolved run-relative as ../../docs/, i.e. under the sandbox ROOT).
    (arts / "candidate_strategy_config.json").write_text('{"marker": "CONFIG_MARKER"}\n',
                                                         encoding="utf-8")
    for doc in ("COMPONENT_CATALOG.md", "STRATEGY_DESIGN_GUIDE.md"):
        path = rpr.ROOT / "docs" / doc
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(f"{doc} stub\n", encoding="utf-8")
    _write_menu_pre_registration(run_dir)
    if idea_status is not None:
        rpr.save_yaml(arts / "idea_status.yaml",
                      rpr._build_idea_status_artifact({"idea_status": idea_status, "reason": "r"}, run_id))
    if with_reports:
        for c in READER_CATEGORIES:
            rpr.save_yaml(arts / "reports" / f"{c}.yaml", {"category": c, "marker": f"REPORT_{c.upper()}"})
    return run_dir


MENU_PASS_RULE = {"criteria": [{"id": "c1", "source": "core.sharpe", "reducer": "median"}]}


def _write_menu_pre_registration(run_dir: Path) -> None:
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {"pass_rule": MENU_PASS_RULE})


def _proposal(cat: str, run_id: str = RUN_ID, n: int = 1, score: int = 2) -> dict:
    return {
        "proposal_id": f"{cat}-{run_id}-{n}", "kind": "patch",
        "patch": [{"component_id": "c1", "field": "params.x", "before": 1, "after": 2}],
        "evidence": [f"slices.overall.x=1 ({cat})"],
        "scores": {"confidence_real": score, "distance_to_profitable": score,
                   "mechanism_plausibility": score},
        "model_id": "m", "rubric_version": f"{cat}-reader-v1",
    }


def _fake_llm(outputs: dict | None = None, calls: list | None = None):
    """An async stand-in for _invoke_reader_llm. `outputs` maps category ->
    raw model text; default is an honest empty list for every reader."""
    async def _fake(prompt: str):
        cat = next(c for c in READER_CATEGORIES if f"reader_category: {c}\n" in prompt)
        if calls is not None:
            calls.append((cat, prompt))
        text = (outputs or {}).get(cat, f"```yaml\n# {cat}.yaml\n[]\n```")
        return text, {"usage": {"input_tokens": 10, "output_tokens": 5}, "cost_usd": 0.0,
                      "num_turns": 1}
    return _fake


# ---------------------------------------------------------------------------
# from test_c5_7b1_model_id_stamp: score provenance, stubbed streams, step 1a
# ---------------------------------------------------------------------------

REQUESTED = rpr._CLAUDE_WORKER_MODEL
DATED = f"{REQUESTED}-20251001"
ON = {**ALL_ON, "score_provenance": {"enabled": True}}
BASELINE_ENTRY_KEYS = {"timestamp", "engine", "execution_time_seconds", "cost_usd",
                       "num_turns", "tokens"}


def _reader_text(proposals: list) -> str:
    return "```yaml\n# proposals/profitability.yaml\n" + yaml.safe_dump(proposals) + "```"


def _one_proposal(model_id="self-reported-model", pid="profitability-run_990-1") -> dict:
    p = _decide_next_patch(pid)
    p["model_id"] = model_id
    p["rubric_version"] = "profitability-reader-v2"  # C5.7b-2: the flag-on closed set
    return p


def _bytes(path: Path) -> bytes:
    """File bytes with the platform's text-mode newline translation undone (the
    workers write with open(..., "w"), unchanged by this slice)."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def _loaded(dest: Path) -> list:
    return yaml.safe_load(dest.read_text(encoding="utf-8"))


def _stream(*messages):
    async def _q(*, prompt, options=None):
        for m in messages:
            yield m
    return _q


def _assistant(text: str, model: str):
    return AssistantMessage(content=[TextBlock(text=text)], model=model)


def _result(model_usage=None):
    return ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False,
                         num_turns=1, session_id="s", total_cost_usd=0.0,
                         usage={"input_tokens": 1, "output_tokens": 1}, model_usage=model_usage)


def _run_1a(monkeypatch, tmp_path, text, models, orchestrator=ON):
    _set_orchestrator(orchestrator)
    monkeypatch.chdir(SR_ROOT)  # _build_stage_prompt opens the skill relative to cwd
    run_dir = tmp_path / "runs" / "run_c57"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    # `models` empty: an AssistantMessage whose model is "" -- no observation
    first = models[0] if models else ""
    monkeypatch.setattr(rpr, "query", _stream(
        _assistant(text, first), *[_assistant("", m) for m in models[1:]],
        _result({first: {}} if first else None)))
    handoff = {"required_inputs": [], "optional_inputs": [], "injected_context": {"stage_attempt": "0"}}
    asyncio.run(rpr.run_claude_worker("validation", handoff, run_dir))
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    return run_dir, audit["validation_attempt_0"]


# ---------------------------------------------------------------------------
# from test_e058_s2a_regroup_record: the regroup_record seed
# ---------------------------------------------------------------------------

REGROUP_RUN_ID = "run_980"
READERS_ON = {"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True},
              "specialist_readers": {"enabled": True}}
REGROUP_ALL_ON = {**READERS_ON, "regroup_record": {"enabled": True}}
CRITERIA = ["ic_median", "trade_floor"]


def _memory_path() -> Path:
    return rpr.ROOT / "campaign_record" / "campaign_memory.yaml"


def _grid(variants: list, idea_status: str) -> dict:
    cell = {"result": "PASS", "value": 0.031, "threshold": 0.02, "n_windows": 2, "n_trades": 40}
    grid = {c: {v: dict(cell) for v in variants} for c in CRITERIA}
    if idea_status == "refuted":
        grid["ic_median"][variants[-1]] = {"result": "FAIL", "value": 0.001, "threshold": 0.02,
                                           "n_windows": 2, "n_trades": 40}
        reason = "at least one criterion FAILed with sufficient data on at least one variant"
    elif idea_status == "inconclusive":
        grid["trade_floor"][variants[0]] = {"result": "INCONCLUSIVE", "n_windows": 2, "n_trades": 3,
                                            "reason": "n_trades=3 < floor 20"}
        reason = "no criterion FAILed, but at least one cell lacked sufficient data to judge"
    else:
        reason = "every criterion PASSed on every variant"
    return {"result": "GRID_EVALUATED", "criteria": list(CRITERIA), "variants": list(variants),
            "grid": grid, "idea_status": idea_status, "reason": reason,
            "evaluated_at": "2026-09-23T00:00:00+00:00"}


def _pr(errors_count=None, symbols=("BTCUSDT",)) -> dict:
    results = []
    for sym in symbols:
        for w in ("w1", "w2"):
            entry = {"symbol": sym, "window": w, "core": {"sharpe": 0.1, "trade_count": 20}}
            if errors_count is not None:
                entry["component_errors"] = {"count": errors_count, "samples": []}
            results.append(entry)
    return {"verdict": "kill", "protocol_file": str(rpr.ROOT / "protocols" / "p.json"),
            "results": results}


def _seed(run_id=REGROUP_RUN_ID, idea_status="refuted", errors_count=None, variant_loop=False,
          pending="regroup_record", proposals=1, score=2) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = pending
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-MEM-1", "timeframe": "1h"})
    _write_menu_pre_registration(run_dir)
    rpr.save_yaml(arts / "protocol_result.yaml", _pr(errors_count))
    (arts / "candidate_strategy_config.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    if variant_loop:
        variants = ["base", "design"]
        index = {}
        # E-061 C2 S2b (CUL-342 item 2): a validated idea has every variant graded
        # -- the memory's belt check refuses one with a failed / untested variant
        # -- so a validated seed's index holds only the graded columns.
        whole = idea_status == "validated"
        for v in variants + ([] if whole else ["broken"]):
            cfg = arts / "variants" / v / "strategy_config.json"
            cfg.parent.mkdir(parents=True, exist_ok=True)
            cfg.write_text(json.dumps({"v": v}), encoding="utf-8")
            index[v] = {"status": "validated", "config_path": f"artifacts/variants/{v}/strategy_config.json"}
        if not whole:
            index["asset"] = {"status": "not_tested", "reason": "patch application failed: /x"}
        rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
        for v in variants:
            rpr.save_yaml(arts / "variants" / v / "protocol_result.yaml",
                          _pr(errors_count, symbols=("BTCUSDT", "ETHUSDT") if v == "design" else ("BTCUSDT",)))
    else:
        variants = [run_id]
    grid = _grid(variants, idea_status)
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, run_id))
    for c in READER_CATEGORIES:
        rpr.save_yaml(arts / "reports" / f"{c}.yaml", {"category": c})
        rpr.save_yaml(arts / "proposals" / f"{c}.yaml",
                      [_proposal(c, run_id, n, score) for n in range(1, proposals + 1)])
    _seed_trials(run_id, variant_loop)
    return run_dir


def _seed_trials(run_id: str, variant_loop: bool) -> None:
    # forecast_hash values are deliberately NOT the hash of any file on disk: the
    # memory must copy them from the ledger, never recompute them.
    rows = [{"trial_id": run_id, "source": "prescreen", "sharpe": 0.1, "forecast_hash": "fh-prescreen"}]
    if variant_loop:
        rows += [{"trial_id": f"{run_id}:base", "source": "backtest", "sharpe": 0.3,
                  "forecast_hash": "fh-base"},
                 {"trial_id": f"{run_id}:design", "source": "backtest", "sharpe": 0.3,
                  "forecast_hash": "fh-design"},
                 {"trial_id": f"{run_id}:broken", "source": "backtest_failed", "sharpe": None,
                  "forecast_hash": "fh-broken"}]
    else:
        rows += [{"trial_id": run_id, "source": "backtest", "sharpe": 0.2, "forecast_hash": "fh-run"}]
    rows += [{"trial_id": "run_001", "source": "backtest", "sharpe": 0.9, "forecast_hash": "x"},
             {"trial_id": f"{run_id}0", "source": "backtest", "sharpe": 0.9,
              "forecast_hash": "x"}]  # prefix trap
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": rows})


def _memory() -> dict:
    return yaml.safe_load(_memory_path().read_text(encoding="utf-8"))


def _loop_from_specialist_readers(monkeypatch, orchestrator, idea_status, errors_count=None,
                                  run_id=REGROUP_RUN_ID, spy=None):
    _set_orchestrator(orchestrator)
    run_dir = _seed(run_id=run_id, idea_status=idea_status, errors_count=errors_count,
                    pending="specialist_readers")
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    # A validated route continues into holdout_evaluation; stop there without running it.
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "holdout_evaluation",
                        {**rpr.STAGE_CONFIGS["holdout_evaluation"], "handoff": "missing.yaml"})
    if spy is not None:
        monkeypatch.setattr(rpr, "determine_post_specialist_readers_route", spy)
    if idea_status == "validated" and not errors_count:
        with pytest.raises(FileNotFoundError):
            rpr.run_loop(run_id)
    else:
        rpr.run_loop(run_id)
    assert calls == []  # proposals pre-seeded: no reader re-run, no LLM
    return run_dir, rpr.load_yaml(run_dir / "pipeline_state.yaml")


# ---------------------------------------------------------------------------
# from test_e068_5_readers_v3: readers v3 readings, claims, decide-next inputs
# ---------------------------------------------------------------------------

FIX4 = SR_ROOT / "tests" / "fixtures" / "e068_4" / "run_070"
FIX5 = SR_ROOT / "tests" / "fixtures" / "e068_5"
CLAIMS_ON = {**REGROUP_ALL_ON, "config_direct_authoring": {"enabled": True},
             "claim_tests": {"enabled": True}}
V3_ON = {**CLAIMS_ON, "reader_findings": {"enabled": True}}


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
                "evidence": ["variants.base.slices.overall.y=2"], "scores": _scores()}]}
    if patch is not None:   # a LEGACY v3 file (before continuation 2 removed the patch)
        doc["patch"] = patch
    doc.update(over)
    return doc


def _side_with_change(cat="trade_efficiency", run_id=RUN_ID, n=1, **patch_kw) -> dict:
    """Continuation 2: a side finding carrying the config change to test it with."""
    return {"proposal_id": f"{cat}-{run_id}-{n}", "claim": _claim(),
            "evidence": ["variants.base.slices.overall.y=2"], "scores": _scores(),
            "config_change": _patch(cat, run_id, **patch_kw)["patch"]}


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


def _fix(name):
    path = FIX5 / name
    return json.loads(path.read_text(encoding="utf-8")) if name.endswith(".json") else \
        yaml.safe_load(path.read_text(encoding="utf-8"))


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


# ---------------------------------------------------------------------------
# from test_e072_explore_confirm: the synthetic explore/confirm run
# ---------------------------------------------------------------------------

EC_ON = {**V3_ON, "variant_loop": {"enabled": True}, "explore_confirm": {"enabled": True}}
WINDOWS = [("2022-01", "2022-01-01", "2022-04-30"), ("2022-05", "2022-05-01", "2022-08-31"),
           ("2022-09", "2022-09-01", "2022-12-31"), ("2023-01", "2023-01-01", "2023-04-30"),
           ("2023-05", "2023-05-01", "2023-08-31"), ("2023-09", "2023-09-01", "2023-12-31")]
SYMBOLS = ["BTCUSD", "ETHUSD"]
VARIANTS = ["base", "design"]
SENT_CONF = 919191.0     # every confirmation-window number
SENT_POOL = 828282.0     # every all-window aggregate
N_BARS = 110


def _pure_claim() -> dict:
    return {"statement": "After an up day the next day is higher.", "kind": "event_behaviour",
            "tests": [{"name": "up_day_followthrough",
                       "selector": {"kind": "event", "field": "past_return", "bars": 1,
                                    "op": ">", "value": 0.0},
                       "outcome": {"kind": "fwd_return", "horizons": [1]},
                       "baseline": {"kind": "complement"}, "statistic": "mean_diff",
                       "direction": "greater", "floor": {"min_events": 10}}],
            "pass_if": "effect above zero", "fail_if": "effect at or below zero",
            "rationale": "seen on the exploration windows"}


def _block_claim() -> dict:
    return {"statement": "The forecast ranks next-day returns.", "kind": "direction_forecast",
            "tests": [{"name": "forecast_rank", "selector": {"kind": "all"},
                       "outcome": {"kind": "fwd_return", "horizons": [1]},
                       "statistic": "rank_ic", "direction": "greater",
                       "floor": {"min_events": 10}}],
            "pass_if": "rank IC above zero", "fail_if": "rank IC at or below zero",
            "rationale": "the forecast read on the exploration windows"}


def _bars_rows(start: str, sign: float, seed: int, conf: bool) -> list:
    """Daily bars: r[t+1] = 0.004 * sign * sign(r[t]) + noise (momentum when
    sign is +1, reversal when -1). A confirmation window's component value
    carries the sentinel."""
    import pandas as pd
    rng = np.random.default_rng(seed)
    ts = pd.date_range(start, periods=N_BARS, freq="1D", tz="UTC")
    r = np.zeros(N_BARS)
    r[0] = 0.01
    for t in range(N_BARS - 1):
        r[t + 1] = 0.004 * sign * np.sign(r[t]) + rng.normal(0.0, 0.01)
    close = 100.0 * np.cumprod(1.0 + r)
    rows = []
    for t in range(N_BARS):
        rows.append({"timestamp": ts[t].strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "high": f"{close[t] * 1.01:.6f}", "low": f"{close[t] * 0.99:.6f}",
                     "close": f"{close[t]:.6f}", "forecast": f"{r[t] * 100:.6f}",
                     "regime": "unknown" if t < N_BARS - 1 else "",
                     "debug_info.components.c1.value":
                         f"{SENT_CONF:.1f}" if conf else f"{0.5 + t / 1000:.4f}"})
    return rows


def _write_csv(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _save(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


PRE_REG = {"pass_rule": {"criteria": [
    {"id": "c_win", "metric": "sharpe", "source": "window", "reducer": "median",
     "comparator": ">", "threshold": 0.0, "floor": {"min_windows": 1}},
    {"id": "c_pool", "metric": "realized_edge_to_cost_ratio", "source": "pooled",
     "comparator": ">", "threshold": 2.2}]}}


def _eras_holdout():
    return pres.load_policy_eras(rpr._DATA_POLICY_PATH), rpr._load_holdout_range()[0]


def _make_run(run_dir: Path, conf_sign: float = -1.0, windows=WINDOWS, card_claim=None) -> None:
    """The synthetic run's backtest output (no backtest is run)."""
    arts = run_dir / "artifacts"
    arts.mkdir(parents=True, exist_ok=True)
    conf_labels = {w[0] for w in windows[len(windows) // 2:]}
    (run_dir / "protocol.json").write_text(json.dumps({
        "symbols": SYMBOLS, "timeframe": "1d",
        "windows": [{"label": l, "test": {"start": s, "end": e}} for l, s, e in windows]}),
        encoding="utf-8")
    for vi, vid in enumerate(VARIANTS):
        results, trades = [], []
        for si, sym in enumerate(SYMBOLS):
            for wi, (label, start, _end) in enumerate(windows):
                conf = label in conf_labels
                rid = f"{vid}_{sym}_{label}"
                v = SENT_CONF if conf else round(0.1 * (wi + 1) + 0.01 * si, 4)
                results.append({"symbol": sym, "window": label, "run_id": rid,
                                "core": {"sharpe": v, "net_return_pct": v, "trade_count": 20,
                                         "forecast_return_corr": v,
                                         "forecast_return_corr_pvalue": 0.5},
                                "per_regime": {"unknown": {"return_pct": v}},
                                "regime_validity": {"unknown": {"n_bars": N_BARS, "x": v}}})
                _write_csv(run_dir / "variants" / vid / "results" / rid / "bars.csv",
                           _bars_rows(start, conf_sign if conf else 1.0,
                                      seed=1000 * vi + 100 * si + wi, conf=conf))
                for k in range(3):
                    trades.append({"symbol": sym, "window": label, "regime_at_entry": "unknown",
                                   "trade_id": f"{rid}-{k}", "pnl_pct": v, "bars_held": 2})
        pr = {"results": results,
              "hypothesis_verdict": {"verdict": "x", "diagnostics": {
                  "median_forecast_return_corr": SENT_POOL, "median_sharpe": SENT_POOL}},
              "trade_diagnostics_summary": {"realized_edge_to_cost_ratio": SENT_POOL,
                                            "n_trades": 828282},
              "per_symbol_summary": {s: {"sharpe": SENT_POOL} for s in SYMBOLS}}
        _save(arts / "variants" / vid / "protocol_result.yaml", pr)
        (run_dir / "variants" / vid).mkdir(parents=True, exist_ok=True)
        (run_dir / "variants" / vid / "trade_diagnostics.json").write_text(
            json.dumps({"trades": trades}), encoding="utf-8")
    _save(arts / "pre_registration.yaml", PRE_REG)
    _save(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-TEST-1",
                                          "claim": card_claim or _pure_claim()})
    eras, holdout = _eras_holdout()
    card = yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
    tests = card["claim"]["tests"]
    variants = {}
    for vid in VARIANTS:
        doc = cmeas.measure_variant(run_dir, vid, tests, eras, holdout)
        _save(arts / "variants" / vid / cmeas.VARIANT_FILE, doc)
        variants[vid] = doc
    status = cc.status_of(cc.check_claim(card["claim"]), None, [])
    _save(arts / cmeas.RUN_FILE, cmeas.run_doc(run_dir.name, status, variants))
    prs = _prs(run_dir)
    grid = vce.evaluate_grid(prs, PRE_REG, None, {})
    _save(arts / "grid_evaluation.yaml", grid)
    br.build_reports(run_dir, write=True, variants=_meta())


def _prs(run_dir: Path) -> dict:
    return {vid: yaml.safe_load((run_dir / "artifacts" / "variants" / vid
                                 / "protocol_result.yaml").read_text(encoding="utf-8"))
            for vid in VARIANTS}


def _meta() -> dict:
    return {vid: {"kind": None, "symbol": None, "status": "graded"} for vid in VARIANTS}


def _ec_run(monkeypatch, flags=EC_ON, conf_sign=-1.0, run_id=RUN_ID, windows=WINDOWS,
            card_claim=None) -> Path:
    _set_orchestrator(flags)
    monkeypatch.chdir(SR_ROOT)
    _seed_v3_docs()
    dst = rpr.ROOT / "workflow_artifacts" / "skills" / "readers_v3" / "EXPLORATION.md"
    shutil.copyfile(SR_ROOT / "workflow_artifacts" / "skills" / "readers_v3" / "EXPLORATION.md",
                    dst)
    run_dir = _seed_run(run_id)
    _make_run(run_dir, conf_sign, windows=windows, card_claim=card_claim)
    monkeypatch.setattr(rpr, "_resolve_protocol_path",
                        lambda rd, rid: Path(rd) / "protocol.json")
    return run_dir


def _protocol_execution_part(run_dir: Path, run_id: str = RUN_ID) -> None:
    """What protocol_execution does under the flag: the split at entry, the
    readers' copies after the reports."""
    rpr._prepare_explore_confirm(run_dir, run_id)
    rpr._write_exploration_views(run_dir, run_id, _prs(run_dir), _meta(),
                                 pre_registration=PRE_REG)


def _readings_llm(prompts: list, sides: dict | None = None):
    sides = sides or {}

    async def _llm(prompt):
        prompts.append(prompt)
        cat = next(c for c in READER_CATEGORIES if f"reader_category: {c}\n" in prompt)
        return (_fenced(_reading(cat, sides=sides.get(cat, []))),
                {"usage": {}, "cost_usd": 0.0, "num_turns": 1})
    return _llm


def _sides():
    return {"trade_efficiency": [{"proposal_id": f"trade_efficiency-{RUN_ID}-1",
                                  "claim": _pure_claim(), "evidence": ["exploration only"],
                                  "scores": _scores()}],
            "forecast_power": [{"proposal_id": f"forecast_power-{RUN_ID}-1",
                                "claim": _block_claim(), "evidence": ["exploration only"],
                                "scores": _scores()}]}


def _confirmation(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "artifacts" / ec.CONFIRMATION_ARTIFACT).read_text(
        encoding="utf-8"))


def _child_run(monkeypatch, run_id: str, windows=WINDOWS) -> Path:
    """The run built from forecast_power-run_990-1: its brief names the finding,
    its card carries the block claim."""
    run_dir = _ec_run(monkeypatch, run_id=run_id, windows=windows, card_claim=_block_claim())
    _save(run_dir / "artifacts" / "research_brief.yaml", {"candidate": {"source": {
        "proposal_ref": f"runs/{RUN_ID}/artifacts/proposals/forecast_power.yaml"
                        f"#forecast_power-{RUN_ID}-1"}}})
    return run_dir


# ---------------------------------------------------------------------------
# from test_e046a_slice5b_i_reader_skills: one valid proposal per category
# ---------------------------------------------------------------------------

_VALID_EXAMPLES = {
    "profitability": {
        "proposal_id": "profitability-run_059-1",
        "kind": "patch",
        "patch": [
            {
                "component_id": "keltner",
                "field": "transforms[2].params.min_abs",
                "before": 15.0,
                "after": 20.0,
            }
        ],
        "evidence": [
            "slices.overall.diagnostics.median_cost_drag_pct=142.82, "
            "median_gross_pnl=+21.94 -- gross PnL positive but fees consume it (Rule 1 shape).",
            "slices.per_symbol.BTCUSDT[*].core.cost_drag_pct > 100% in 4/5 windows.",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 2},
        "model_id": "claude-sonnet-5",
        "rubric_version": "profitability-reader-v1",
    },
    "trade_efficiency": {
        "proposal_id": "trade_efficiency-run_059-1",
        "kind": "patch",
        "patch": [
            {"component_id": "keltner", "field": "stop_loss_pct", "before": 0.0, "after": 1.5}
        ],
        "evidence": [
            "slices.overall.pnl_concentration.pct_pnl_from_worst_decile_trades=123%, "
            "slices.overall.exit_reason_breakdown.signal_flip_pct=95% -- holding_sizing "
            "pattern, no stop mechanism (STEP 03 decision table).",
        ],
        "scores": {"confidence_real": 3, "distance_to_profitable": 2, "mechanism_plausibility": 3},
        "model_id": "claude-sonnet-5",
        "rubric_version": "trade_efficiency-reader-v1",
    },
    "forecast_power": {
        "proposal_id": "forecast_power-run_059-1",
        "kind": "new_block",
        "block": {
            "kind": "forecast",
            "config_paths": ["strategies.regimes.unknown.components"],
            "scaffolding": ["new signal component replacing rsi (Rule 2: no directional edge)"],
            "rationale": (
                "slices.overall.median_forecast_return_corr=0.012, below the 0.03 no-edge "
                "floor across 4/5 windows -- propose a structurally different signal."
            ),
        },
        "evidence": [
            "slices.overall.median_forecast_return_corr=0.012 (Rule 2 floor is 0.03); "
            "slices.per_window shows corr < 0.03 in 4/5 windows.",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 1},
        "model_id": "claude-sonnet-5",
        "rubric_version": "forecast_power-reader-v1",
    },
    "regime_power": {
        "proposal_id": "regime_power-run_059-1",
        "kind": "new_block",
        "block": {
            "kind": "regime",
            "config_paths": ["regime_detector"],
            "scaffolding": ["score_product mode instead of threshold_rules (Rule 4, n_bars >= 20)"],
            "rationale": (
                "trending regime's forward_return_mean is near zero with n_bars=340 "
                "(median across windows) -- reliable sample, regime label itself uninformative."
            ),
        },
        "evidence": [
            "slices.per_regime.trending[*].regime_validity.n_bars median=340 (>=20 floor); "
            "forward_return_mean near zero across those entries (Rule 4).",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 2},
        "model_id": "claude-sonnet-5",
        "rubric_version": "regime_power-reader-v1",
    },
    "component_attribution": {
        "proposal_id": "component_attribution-run_059-1",
        "kind": "patch",
        "patch": [
            {"component_id": "keltner", "field": "weight", "before": 1.0, "after": 0.3}
        ],
        "evidence": [
            "slices.overall.components_discovered=['rsi','keltner']; "
            "slices.per_regime.mean_reversion records for component='keltner' are constant "
            "0.0 across every bar listed, while slices.per_regime.trending records for the "
            "same component vary -- keltner appears inert outside trending (Rule CA-2).",
        ],
        "scores": {"confidence_real": 2, "distance_to_profitable": 1, "mechanism_plausibility": 2},
        "model_id": "claude-sonnet-5",
        "rubric_version": "component_attribution-reader-v1",
    },
}
