"""
CUL-336: stage agents run closed-book.

Before this fix every LLM stage agent was started with
``ClaudeAgentOptions(model=..., allowed_tools=[])``. In claude_agent_sdk 0.2.82
``allowed_tools=[]`` sends no CLI flag at all (it only lists tools that run
without asking); the base tool set is ``tools``, which was never set, so every
stage got Claude Code's default tool set. ``setting_sources`` was unset too, so
the operator's user/project/local settings files (and their permission allow
rules) loaded. A retained run_060 validation transcript holds two self-directed
``Read`` calls (engineering/roadmap/E-035/S1_FINDINGS.md section 1.2).

What this file pins (no API key; the SDK ``query`` is stubbed everywhere):

1. The one options helper: ``tools=[]``, ``setting_sources=[]``,
   ``strict_mcp_config=True``, auto-memory disabled through ``env``, a neutral
   ``cwd`` outside the repository -- and the installed SDK turns them into the
   closed-book CLI invocation.
2. Both call sites (``run_claude_worker``, ``_invoke_reader_llm``) pass exactly
   those options to ``query`` -- these fail on the pre-CUL-336 code.
3. The helper is the only ``ClaudeAgentOptions(...)`` construction in the
   orchestrator, every ``query(...)`` call uses it, and no other Python file in
   the repository imports the SDK.
4. The files the stage skills tell the agent to read reach the prompt through
   the handoff (``_apply_closed_book_inputs``), with their conditions.
5. Drift guard: every repo path a stage skill names, and every entry of its
   "## Required inputs" list, is a handoff input of that stage or waived here
   with a reason.
"""
from __future__ import annotations

import ast
import asyncio
import dataclasses
import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = SR_ROOT.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402

# A declared dependency (strategy-research/config/requirements-mac.txt), and
# run_phase1_research already imports it: a missing SDK fails here, not skips.
from claude_agent_sdk import ClaudeAgentOptions  # noqa: E402
from claude_agent_sdk._internal.transport.subprocess_cli import SubprocessCLITransport  # noqa: E402

_ORCH = SR_ROOT / "workflow" / "run_phase1_research.py"


# --- 1. the helper and the CLI invocation it produces --------------------------

def test_stage_agent_options_are_closed_book():
    opts = rpr._stage_agent_options()
    assert isinstance(opts, ClaudeAgentOptions)
    assert opts.model == rpr._CLAUDE_WORKER_MODEL
    assert opts.tools == []
    assert opts.setting_sources == []
    assert opts.strict_mcp_config is True
    assert opts.allowed_tools == []  # the SDK default; the helper no longer passes it
    # max_turns deliberately unset: with no tool there is no tool-result round
    # trip, so a stage is one turn by construction; num_turns in the audit log
    # is the check, not a second cap.
    assert opts.max_turns is None


def test_auto_memory_is_disabled_through_env():
    """The bundled CLI gates its auto-memory MEMORY.md on this env var (and on
    settings/feature flags), not on --setting-sources."""
    opts = rpr._stage_agent_options()
    assert opts.env == {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}


def test_cwd_is_a_neutral_directory_outside_the_repository():
    opts = rpr._stage_agent_options()
    cwd = Path(opts.cwd).resolve()
    assert cwd.is_dir()
    assert cwd == rpr._STAGE_AGENT_CWD.resolve()
    assert REPO_ROOT.resolve() not in cwd.parents and cwd != REPO_ROOT.resolve()
    # no git root above it, so no repo-keyed memory or project settings
    assert not any((p / ".git").exists() for p in [cwd, *cwd.parents])


def test_stage_agent_options_are_fresh_per_call():
    """ClaudeAgentOptions is a mutable dataclass; a shared instance could be
    changed by one call and leak into the next."""
    a, b = rpr._stage_agent_options(), rpr._stage_agent_options()
    assert a is not b
    assert a.tools is not b.tools and a.setting_sources is not b.setting_sources
    assert a.env is not b.env


def test_installed_sdk_emits_closed_book_cli_invocation():
    """Read the invocation off the installed SDK's own command builder (no
    process is started). Only the options object and its public `cli_path`
    field are used to build it; the builder itself has no public API in
    0.2.82. Pins: tools=[] -> --tools "", setting_sources=[] ->
    --setting-sources= (empty), strict -> --strict-mcp-config."""
    opts = dataclasses.replace(rpr._stage_agent_options(), cli_path="claude")
    cmd = SubprocessCLITransport(prompt="x", options=opts)._build_command()
    i = cmd.index("--tools")
    assert cmd[i + 1] == ""
    assert "--setting-sources=" in cmd
    assert "--strict-mcp-config" in cmd
    assert "--allowedTools" not in cmd
    assert "--max-turns" not in cmd


# --- 2. both call sites pass those options ------------------------------------

class _Capture:
    def __init__(self):
        self.options = []

    async def query(self, prompt, options):
        self.options.append(options)
        yield type("R", (), {"total_cost_usd": 0.0, "num_turns": 1, "usage": {}})()


def _assert_closed_book(opts):
    assert opts.tools == [], f"tools={opts.tools!r} -- None means the CLI default tool set"
    assert opts.setting_sources == [], f"setting_sources={opts.setting_sources!r}"
    assert opts.strict_mcp_config is True
    assert opts.env.get("CLAUDE_CODE_DISABLE_AUTO_MEMORY") == "1"
    assert opts.cwd and Path(opts.cwd).resolve() == rpr._STAGE_AGENT_CWD.resolve()


def test_run_claude_worker_passes_closed_book_options(monkeypatch, tmp_path):
    monkeypatch.chdir(SR_ROOT)  # _build_stage_prompt opens the skill relative to cwd
    run_dir = tmp_path / "runs" / "run_cul336"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    cap = _Capture()
    monkeypatch.setattr(rpr, "query", cap.query)
    handoff = {"required_inputs": [], "optional_inputs": [],
               "injected_context": {"stage_attempt": "0"}}
    asyncio.run(rpr.run_claude_worker("validation", handoff, run_dir))
    assert len(cap.options) == 1
    _assert_closed_book(cap.options[0])


def test_reader_llm_passes_closed_book_options(monkeypatch):
    cap = _Capture()
    monkeypatch.setattr(rpr, "query", cap.query)
    asyncio.run(rpr._invoke_reader_llm("prompt"))
    assert len(cap.options) == 1
    _assert_closed_book(cap.options[0])


# --- 3. one construction site, every query uses it, no other SDK user ---------

def _enclosing_function(tree: ast.AST, target: ast.AST) -> str | None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(child is target for child in ast.walk(node)):
                return node.name
    return None


def test_options_helper_is_the_only_construction_site():
    tree = ast.parse(_ORCH.read_text(encoding="utf-8"))
    ctor_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Name) and n.func.id == "ClaudeAgentOptions"]
    assert len(ctor_calls) == 1, f"{len(ctor_calls)} ClaudeAgentOptions(...) calls; expected 1"
    assert _enclosing_function(tree, ctor_calls[0]) == "_stage_agent_options"

    query_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                   and isinstance(n.func, ast.Name) and n.func.id == "query"]
    assert len(query_calls) == 2, f"expected the two known call sites, found {len(query_calls)}"
    for call in query_calls:
        opts = {kw.arg: kw.value for kw in call.keywords}.get("options")
        assert isinstance(opts, ast.Call) and isinstance(opts.func, ast.Name) \
            and opts.func.id == "_stage_agent_options", \
            f"query(...) at line {call.lineno} does not pass options=_stage_agent_options()"
    assert {_enclosing_function(tree, c) for c in query_calls} == \
        {"run_claude_worker", "_invoke_reader_llm"}


_SKIP_DIRS = {"venv", ".venv", "site-packages", "node_modules", "__pycache__", ".git", ".claude"}


def test_no_other_python_file_imports_the_agent_sdk():
    """A new SDK user elsewhere would not go through the helper. Imports only,
    production code only: test files may import the SDK to stub or inspect it
    (e.g. the E-061 end-to-end test stubs `query` with real SDK message types),
    so every file under a `tests` directory is excluded."""
    importers = []
    for sub in ("strategy-research", "trading-bot"):
        for py in (REPO_ROOT / sub).rglob("*.py"):
            rel = py.relative_to(REPO_ROOT)
            if _SKIP_DIRS.intersection(rel.parts) or "tests" in rel.parts:
                continue
            text = py.read_text(encoding="utf-8", errors="replace")
            if "claude_agent_sdk" not in text:
                continue
            try:
                tree = ast.parse(text)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                mods = []
                if isinstance(node, ast.Import):
                    mods = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    mods = [node.module]
                if any(m == "claude_agent_sdk" or m.startswith("claude_agent_sdk.") for m in mods):
                    importers.append(rel.as_posix())
                    break
    assert importers == ["strategy-research/workflow/run_phase1_research.py"]


# --- 4. what the stages used to open themselves now comes through the handoff --

_QF = "../../workflow_artifacts/skills/quant-fundamentals/SKILL.md"
_REPO_FILES = {
    "../../config/cost_model.yaml": SR_ROOT / "config" / "cost_model.yaml",
    "../../config/coin_universe.yaml": SR_ROOT / "config" / "coin_universe.yaml",
    "../../docs/DATA_AVAILABILITY.md": SR_ROOT / "docs" / "DATA_AVAILABILITY.md",
    _QF: SR_ROOT / "workflow_artifacts" / "skills" / "quant-fundamentals" / "SKILL.md",
}


def _sandbox_run(tmp_path: Path, monkeypatch, run_id: str = "run_cul336") -> Path:
    """A run dir whose ../../ holds copies of the repo reference files, so the
    real handoff-relative paths resolve without touching the real runs/.
    CAMPAIGN_STATE_PATH is pointed into the same sandbox root."""
    root = tmp_path / "root"
    for rel, src in _REPO_FILES.items():
        dst = root / rel.replace("../../", "")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    monkeypatch.setattr(rpr, "ROOT", root)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", root / "campaign_record" / "campaign_state.yaml")
    run_dir = root / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    return run_dir


def _paths(handoff: dict, key: str) -> list[str]:
    return [r["path"] for r in handoff.get(key, [])]


def _all_paths(handoff: dict) -> list[str]:
    return _paths(handoff, "required_inputs") + _paths(handoff, "optional_inputs")


def _complete_backtest(run_dir: Path) -> None:
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(
        yaml.safe_dump({"results": [{"symbol": "BTCUSDT", "core": {"sharpe": 0.1}}]}),
        encoding="utf-8")


def test_table_matches_the_declared_stages():
    assert set(rpr._CLOSED_BOOK_STAGE_INPUTS) == {
        "innovation_expansion", "validation", "backtest_specification",
        "strategy_config_authoring", "verdict_interpreter", "campaign_review"}
    for stage, entries in rpr._CLOSED_BOOK_STAGE_INPUTS.items():
        for path, kind, reason in entries:
            assert kind in ("required", "optional", "refine_only", "after_backtest"), (stage, path)
            assert reason, (stage, path)
            assert "holdout_sealed" not in path


def test_validation_first_pass_gets_only_cost_model(tmp_path, monkeypatch):
    """Minimal context on a first pass: innovation_notes/DATA_AVAILABILITY only
    in a refine loop; never the data policy."""
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    handoff = {"required_inputs": [{"path": "artifacts/expanded_hypothesis_card.yaml",
                                    "reason": "x"}], "optional_inputs": []}
    rpr._apply_closed_book_inputs("validation", handoff, run_dir)
    assert "../../config/cost_model.yaml" in _paths(handoff, "required_inputs")
    assert "artifacts/innovation_notes.yaml" not in _all_paths(handoff)
    assert "../../docs/DATA_AVAILABILITY.md" not in _all_paths(handoff)
    assert not any("campaign_data_policy" in p for p in _all_paths(handoff))


def test_validation_in_a_refine_loop_also_gets_refine_context(tmp_path, monkeypatch):
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    (run_dir / "artifacts" / "refinement_notes.yaml").write_text("decision: {}\n",
                                                                  encoding="utf-8")
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("validation", handoff, run_dir)
    assert {"artifacts/innovation_notes.yaml", "../../docs/DATA_AVAILABILITY.md"} <= \
        set(_paths(handoff, "optional_inputs"))


@pytest.mark.parametrize("stage", sorted(
    ["innovation_expansion", "validation", "backtest_specification",
     "strategy_config_authoring", "verdict_interpreter", "campaign_review"]))
def test_added_inputs_reach_the_assembled_prompt(stage, tmp_path, monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs(stage, handoff, run_dir)
    prompt = rpr._build_stage_prompt(stage, handoff, run_dir)
    for path, kind, _ in rpr._CLOSED_BOOK_STAGE_INPUTS[stage]:
        if kind == "required":
            assert f"--- CONTENT OF {path} ---" in prompt, (stage, path)
            assert _REPO_FILES[path].read_text(encoding="utf-8") in prompt, (stage, path)


def test_quant_fundamentals_goes_to_every_stage_told_to_read_it(tmp_path, monkeypatch):
    """Four skills say 'Read workflow_artifacts/skills/quant-fundamentals/SKILL.md
    before ...'. Derived from the skill text, so a fifth one fails here."""
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    told = set()
    for stage, skill in rpr._SKILL_MAP.items():
        text = (SR_ROOT / "workflow_artifacts" / "skills" / skill / "SKILL.md").read_text(
            encoding="utf-8")
        if "Read workflow_artifacts/skills/quant-fundamentals/SKILL.md" in text:
            told.add(stage)
    assert told == {"backtest_specification", "strategy_config_authoring",
                    "verdict_interpreter", "campaign_review"}
    for stage in told:
        handoff = {}
        rpr._apply_closed_book_inputs(stage, handoff, run_dir)
        assert _QF in _paths(handoff, "required_inputs"), stage


def test_run_artifacts_are_optional_and_present_ones_are_included(tmp_path, monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    (run_dir / "artifacts" / "findings_carryover.yaml").write_text(
        "parameter_bracket: {dimension: lookback, midpoint: 42}\n", encoding="utf-8")
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("backtest_specification", handoff, run_dir)
    # innovation_notes.yaml and run_context.yaml are absent: optional, so no raise
    prompt = rpr._build_stage_prompt("backtest_specification", handoff, run_dir)
    assert "--- CONTENT OF artifacts/findings_carryover.yaml ---" in prompt
    assert "midpoint: 42" in prompt
    assert "--- CONTENT OF artifacts/run_context.yaml ---" not in prompt


def test_missing_required_reference_file_fails_loud(tmp_path, monkeypatch):
    """Unlike B7's skip-if-absent union, a missing tracked reference file is a
    broken checkout: the stage must not run without it."""
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    (run_dir.parent.parent / "config" / "cost_model.yaml").unlink()
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("validation", handoff, run_dir)
    with pytest.raises(FileNotFoundError):
        rpr._build_stage_prompt("validation", handoff, run_dir)


def test_existing_entries_are_not_duplicated(tmp_path, monkeypatch):
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    handoff = {"required_inputs": [{"path": "../../config/cost_model.yaml", "reason": "t"}],
               "optional_inputs": []}
    rpr._apply_closed_book_inputs("validation", handoff, run_dir)
    rpr._apply_closed_book_inputs("validation", handoff, run_dir)
    assert len(_all_paths(handoff)) == len(set(_all_paths(handoff)))
    assert handoff["required_inputs"][0]["reason"] == "t"


def test_required_wins_over_an_existing_optional_entry(tmp_path, monkeypatch):
    """A template that lists a path as optional while the closed-book table
    requires it ends up with the path required only."""
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    handoff = {"required_inputs": [],
               "optional_inputs": [{"path": "../../config/coin_universe.yaml", "reason": "t"},
                                   {"path": "artifacts/other.yaml", "reason": "keep"}]}
    rpr._apply_closed_book_inputs("verdict_interpreter", handoff, run_dir)
    assert "../../config/coin_universe.yaml" in _paths(handoff, "required_inputs")
    assert "../../config/coin_universe.yaml" not in _paths(handoff, "optional_inputs")
    assert "artifacts/other.yaml" in _paths(handoff, "optional_inputs")


def test_pass_rule_evaluation_required_after_a_completed_backtest(tmp_path, monkeypatch):
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    _complete_backtest(run_dir)
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("verdict_interpreter", handoff, run_dir)
    assert "artifacts/pass_rule_evaluation.yaml" in _paths(handoff, "required_inputs")
    assert "artifacts/pass_rule_evaluation.yaml" not in _paths(handoff, "optional_inputs")


def test_pass_rule_evaluation_optional_without_a_completed_backtest(tmp_path, monkeypatch):
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("verdict_interpreter", handoff, run_dir)
    assert "artifacts/pass_rule_evaluation.yaml" in _paths(handoff, "optional_inputs")
    # an empty results list is not a completed backtest either
    (run_dir / "artifacts" / "protocol_result.yaml").write_text("results: []\n",
                                                                encoding="utf-8")
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("verdict_interpreter", handoff, run_dir)
    assert "artifacts/pass_rule_evaluation.yaml" in _paths(handoff, "optional_inputs")


def test_verdict_interpreter_gets_campaign_state_at_its_real_path(tmp_path, monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    rpr.CAMPAIGN_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    rpr.CAMPAIGN_STATE_PATH.write_text("altitude_history: [sentinel_altitude]\n",
                                       encoding="utf-8")
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("verdict_interpreter", handoff, run_dir)
    assert "../../campaign_record/campaign_state.yaml" in _paths(handoff, "optional_inputs")
    prompt = rpr._build_stage_prompt("verdict_interpreter", handoff, run_dir)
    assert "sentinel_altitude" in prompt


def test_verdict_interpreter_gets_the_trade_diagnostics_summary_only(tmp_path, monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    (run_dir / "trade_diagnostics.json").write_text(json.dumps({
        "trades": [{"entry_bar": i, "pnl_bps": "per_trade_row_sentinel"} for i in range(50)],
        "summary": {"per_trade_expectancy_bps": -26.5, "win_rate_net": 0.51},
    }), encoding="utf-8")
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("verdict_interpreter", handoff, run_dir)
    assert rpr._TRADE_DIAGNOSTICS_SUMMARY_REL in _paths(handoff, "optional_inputs")
    prompt = rpr._build_stage_prompt("verdict_interpreter", handoff, run_dir)
    assert "per_trade_expectancy_bps: -26.5" in prompt
    assert "per_trade_row_sentinel" not in prompt


def test_no_trade_diagnostics_file_means_no_summary(tmp_path, monkeypatch):
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("verdict_interpreter", handoff, run_dir)
    assert not (run_dir / rpr._TRADE_DIAGNOSTICS_SUMMARY_REL).exists()


def test_malformed_trade_diagnostics_fails_loud(tmp_path, monkeypatch):
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    (run_dir / "trade_diagnostics.json").write_text(json.dumps({"trades": []}),
                                                    encoding="utf-8")
    with pytest.raises(ValueError):
        rpr._apply_closed_book_inputs("verdict_interpreter", {}, run_dir)


def test_other_stages_are_untouched(tmp_path, monkeypatch):
    run_dir = _sandbox_run(tmp_path, monkeypatch)
    for stage in ("hypothesis_generation", "protocol_execution", "data_availability_gate",
                  "specialist_readers", "regroup_record", "holdout_evaluation"):
        handoff = {"required_inputs": [], "optional_inputs": []}
        rpr._apply_closed_book_inputs(stage, handoff, run_dir)
        assert handoff == {"required_inputs": [], "optional_inputs": []}, stage


def test_verdict_template_has_no_stale_coin_universe_path():
    t = yaml.safe_load((SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" /
                        "protocol_to_verdict_interpreter.yaml").read_text(encoding="utf-8"))
    every = [r["path"] for k in ("required_inputs", "optional_inputs") for r in t.get(k) or []]
    assert "../../coin_universe.yaml" not in every


def test_async_invoke_agent_applies_the_union():
    """Wired at the one place every LLM stage's handoff is assembled."""
    src = _ORCH.read_text(encoding="utf-8")
    body = src[src.index("async def async_invoke_agent("):]
    body = body[:body.index("\ndef ")]
    assert "_apply_closed_book_inputs(stage_name, handoff, RUN_DIR)" in body
    assert body.index("_apply_closed_book_inputs(") < body.index("run_claude_worker(")


# --- 5. drift guard: what a skill names must be delivered or waived ----------

_PATH_RE = re.compile(
    r"(?<![\w/.-])((?:config|docs|artifacts|workflow_artifacts|campaign_record)/"
    r"[\w./-]+\.(?:yaml|yml|md|json|csv))")
_REQUIRED_SECTION_RE = re.compile(r"^## Required inputs\n(.*?)(?=^## )", re.M | re.S)
_REQUIRED_ITEM_RE = re.compile(r"^- `([^`]+)`", re.M)

# Inputs added by flag-gated unions in async_invoke_agent (the template does
# not list them). Kept here, not derived, because they live inside function
# bodies; each is named after its helper.
_FLAG_GATED_INPUTS = {
    "hypothesis_generation": {
        rpr._TRIED_IDEAS_RELATIVE_PATH, rpr._EXCLUSION_DIGEST_RELATIVE_PATH,  # exclusion digest
        *[v for v in rpr._STALE_INPUT_PATH_FIXES["hypothesis_generation"].values()],  # stale-path fix (on)
        "../../config/criterion_menu.yaml", "../../config/cost_model.yaml",  # config-direct authoring
        rpr.CLAIM_TESTS_GUIDE,  # E-068 slice 2 (claim_tests)
    },
    "innovation_expansion": {
        rpr._TRIED_IDEAS_RELATIVE_PATH, rpr._EXCLUSION_DIGEST_RELATIVE_PATH,
        "artifacts/backtest_spec.yaml",  # config-direct authoring
    },
}

# (stage, reference) -> why it is not a handoff input. A reference that is
# neither delivered nor listed here fails the test: either deliver it or add a
# row with the reason.
_WAIVERS = {
    ("hypothesis_generation", "campaign_record/campaign_memory.yaml"):
        "named as the source of tried_ideas.yaml, which is what is delivered",
    ("hypothesis_generation", "config/campaign_config.yaml"):
        "names the orchestrator flag; the skill says the model cannot read it",
    ("innovation_expansion", "campaign_record/campaign_memory.yaml"):
        "named as the source of tried_ideas.yaml, which is what is delivered",
    ("innovation_expansion", "config/campaign_config.yaml"):
        "names the orchestrator flag; the skill says the model cannot read it",
    ("innovation_expansion", "artifacts/variant_patches.yaml"): "this stage's own output",
    ("strategy_config_authoring", "workflow_artifacts/schemas/decision.schema.json"):
        "output schema citation; schemas are not loaded by any code",
    ("backtest_specification", "workflow_artifacts/schemas/backtest_spec.schema.json"):
        "output schema citation; schemas are not loaded by any code",
    ("backtest_specification", "workflow_artifacts/schemas/decision.schema.json"):
        "output schema citation; schemas are not loaded by any code",
    ("backtest_specification", "config/coin_universe.yaml"):
        "cited as where innovation_notes' asset_diversity_audit categories come from; "
        "the stage uses the audit, which is delivered",
    ("verdict_interpreter", "config/criterion_menu.yaml"):
        "cited as the source of the menu-shaped pass_rule, which reaches the stage via "
        "pre_registration.yaml / pass_rule_evaluation.yaml",
    ("verdict_interpreter", "docs/VERIFICATION_DOCTRINE.md"):
        "design rationale citation, not an instruction to read",
    ("verdict_interpreter", "workflow_artifacts/skills/regime-auditor/SKILL.md"):
        "cites the human-run auditor's rules; its output reaches the stage via the "
        "injected regime context",
    ("verdict_interpreter", "post_backtest_routes"):
        "injected into the handoff dict itself, not a file",
    ("verdict_interpreter", "trade_diagnostics.json"):
        "its summary block is delivered as artifacts/trade_diagnostics_summary.yaml; the "
        "per-trade list is deliberately not (size)",
    ("verdict_interpreter", "innovation_notes.yaml"):
        "skill says 'if available in context'; not added (asset gate reads coin_universe)",
    ("verdict_interpreter", "near_miss_scoreboard.yaml"):
        "listed only by _create_remaining_handoffs' fallback; pre-existing gap, not a "
        "closed-book regression -- follow-up",
    ("verdict_interpreter", "grid_evaluation.yaml"):
        "grid artifacts exist only under the specialist_readers flow, where this stage "
        "is unreached",
    ("campaign_review", "workflow_artifacts/skills/verdict-interpreter/SKILL.md"):
        "cross-reference to another skill's Forbidden section, not an input",
    ("campaign_review", "workflow_artifacts/templates/research_brief.yaml"):
        "output-shape citation for a proposed brief",
    ("campaign_review", "campaign_state.yaml"):
        "legacy template's ../../campaign_state.yaml is stale (pre-existing, E-032 S2b "
        "left it: a required stale path means this legacy stage cannot start); the "
        "regroup-flow handoff delivers a memory digest instead",
}


def _norm(path: str) -> str:
    """Handoff path (relative to runs/<id>/) -> the form skills use."""
    if path.startswith("../../../"):
        return "../" + path[len("../../../"):]
    if path.startswith("../../"):
        return path[len("../../"):]
    return path


def _delivered(stage: str) -> set[str]:
    template = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / \
        rpr.STAGE_CONFIGS[stage]["handoff"]
    doc = yaml.safe_load(template.read_text(encoding="utf-8")) if template.exists() else {}
    paths = {r["path"] for k in ("required_inputs", "optional_inputs")
             for r in (doc or {}).get(k) or []}
    if stage in rpr._B7_MANDATORY_INPUT_STAGES:
        paths |= set(rpr._B7_MANDATORY_INPUT_PATHS)
    for path, _, _ in rpr._CLOSED_BOOK_STAGE_INPUTS.get(stage, ()):
        paths.add("../../campaign_record/campaign_state.yaml" if path == "@campaign_state"
                  else path)
    paths |= _FLAG_GATED_INPUTS.get(stage, set())
    # A repo-level path that does not resolve delivers nothing (the stale
    # ../../<name>.yaml entries); run artifacts are checked by name only.
    return {_norm(p) for p in paths
            if _norm(p).startswith("artifacts/") or (SR_ROOT / _norm(p)).exists()}


def _references(stage: str) -> set[str]:
    text = (SR_ROOT / "workflow_artifacts" / "skills" / rpr._SKILL_MAP[stage] /
            "SKILL.md").read_text(encoding="utf-8")
    refs = set(_PATH_RE.findall(text))
    section = _REQUIRED_SECTION_RE.search(text)
    if section:
        refs |= set(_REQUIRED_ITEM_RE.findall(section.group(1)))
    return refs


@pytest.mark.parametrize("stage", sorted(rpr._SKILL_MAP))
def test_every_skill_reference_is_delivered_or_waived(stage):
    """Closed-book, a skill line that names a file the handoff does not carry
    cannot be followed. Prefixed repo paths anywhere in the skill, and every
    item of its '## Required inputs' list (bare names match by basename)."""
    delivered = _delivered(stage)
    basenames = {Path(p).name for p in delivered}
    missing = []
    for ref in sorted(_references(stage)):
        found = ref in delivered if "/" in ref else ref in basenames
        if not found and (stage, ref) not in _WAIVERS:
            missing.append(ref)
    assert not missing, (f"{stage}: skill names {missing} but no handoff input delivers them; "
                         f"add them to the handoff or to _WAIVERS with a reason")


def test_waivers_are_not_stale():
    """A waiver for something now delivered, or no longer referenced, goes."""
    for (stage, ref), reason in _WAIVERS.items():
        assert reason
        assert ref in _references(stage), f"waiver ({stage}, {ref}) no longer referenced"
        delivered = _delivered(stage)
        found = ref in delivered if "/" in ref else ref in {Path(p).name for p in delivered}
        assert not found, f"waiver ({stage}, {ref}) is delivered now; drop the waiver"
