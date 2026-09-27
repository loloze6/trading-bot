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

1. The one options helper carries ``tools=[]``, ``setting_sources=[]`` and
   ``strict_mcp_config=True``, and the installed SDK turns them into the
   closed-book CLI flags.
2. Both call sites (``run_claude_worker``, ``_invoke_reader_llm``) pass exactly
   those options to ``query`` -- these two tests fail on the old code.
3. The helper is the only ``ClaudeAgentOptions(...)`` construction in the
   orchestrator, every ``query(...)`` call uses it, and no other Python file in
   the repository imports the SDK.
4. The files the stage skills tell the agent to read, which it can no longer
   open itself, reach the prompt through the handoff
   (``_apply_closed_book_inputs``).
"""
from __future__ import annotations

import ast
import asyncio
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

_ORCH = SR_ROOT / "workflow" / "run_phase1_research.py"


# --- 1. the helper and the CLI flags it produces ------------------------------

def test_stage_agent_options_are_closed_book():
    opts = rpr._stage_agent_options()
    assert opts.model == rpr._CLAUDE_WORKER_MODEL
    assert opts.tools == []
    assert opts.setting_sources == []
    assert opts.strict_mcp_config is True
    assert opts.allowed_tools == []
    # max_turns deliberately unset: with no tool there is no tool-result round
    # trip, so a stage is one turn by construction; num_turns in the audit log
    # is the check, not a second cap.
    assert opts.max_turns is None


def test_stage_agent_options_are_fresh_per_call():
    """ClaudeAgentOptions is a mutable dataclass; a shared instance could be
    changed by one call and leak into the next."""
    a, b = rpr._stage_agent_options(), rpr._stage_agent_options()
    assert a is not b
    assert a.tools is not b.tools and a.setting_sources is not b.setting_sources


def test_installed_sdk_emits_closed_book_cli_flags():
    """Read the flags off the installed SDK's own command builder (no process
    is started). Pins the 0.2.82 mapping: tools=[] -> --tools "",
    setting_sources=[] -> --setting-sources= (empty), strict -> --strict-mcp-config."""
    transport_mod = pytest.importorskip("claude_agent_sdk._internal.transport.subprocess_cli")
    t = transport_mod.SubprocessCLITransport(prompt="x", options=rpr._stage_agent_options())
    t._cli_path = "claude"  # _build_command refuses to run before the CLI is resolved
    cmd = t._build_command()
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
    """A new SDK user elsewhere would not go through the helper. Imports only:
    tests and docs may name the SDK in text."""
    importers = []
    for sub in ("strategy-research", "trading-bot"):
        for py in (REPO_ROOT / sub).rglob("*.py"):
            if _SKIP_DIRS.intersection(py.relative_to(REPO_ROOT).parts):
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
                    importers.append(py.relative_to(REPO_ROOT).as_posix())
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


def _sandbox_run(tmp_path: Path, run_id: str = "run_cul336") -> Path:
    """A run dir whose ../../ holds copies of the repo reference files, so the
    real handoff-relative paths resolve without touching the real runs/."""
    root = tmp_path / "root"
    for rel, src in _REPO_FILES.items():
        dst = root / rel.replace("../../", "")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    run_dir = root / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    return run_dir


def _paths(handoff: dict, key: str) -> list[str]:
    return [r["path"] for r in handoff.get(key, [])]


def test_table_matches_the_declared_stages():
    assert set(rpr._CLOSED_BOOK_STAGE_INPUTS) == {
        "innovation_expansion", "validation", "backtest_specification",
        "strategy_config_authoring", "verdict_interpreter", "campaign_review"}
    for stage, entries in rpr._CLOSED_BOOK_STAGE_INPUTS.items():
        for path, kind, reason in entries:
            assert kind in ("required", "optional") and reason, (stage, path)
            assert "holdout_sealed" not in path


def test_validation_gets_cost_model_and_not_the_data_policy(tmp_path):
    run_dir = _sandbox_run(tmp_path)
    handoff = {"required_inputs": [{"path": "artifacts/expanded_hypothesis_card.yaml",
                                    "reason": "x"}], "optional_inputs": []}
    rpr._apply_closed_book_inputs("validation", handoff)
    assert "../../config/cost_model.yaml" in _paths(handoff, "required_inputs")
    assert {"artifacts/innovation_notes.yaml", "../../docs/DATA_AVAILABILITY.md"} <= \
        set(_paths(handoff, "optional_inputs"))
    every = _paths(handoff, "required_inputs") + _paths(handoff, "optional_inputs")
    assert not any("campaign_data_policy" in p for p in every)


@pytest.mark.parametrize("stage", sorted(
    ["innovation_expansion", "validation", "backtest_specification",
     "strategy_config_authoring", "verdict_interpreter", "campaign_review"]))
def test_added_inputs_reach_the_assembled_prompt(stage, tmp_path, monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path)
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs(stage, handoff)
    prompt = rpr._build_stage_prompt(stage, handoff, run_dir)
    for path, kind, _ in rpr._CLOSED_BOOK_STAGE_INPUTS[stage]:
        if kind == "required":
            assert f"--- CONTENT OF {path} ---" in prompt, (stage, path)
            body = _REPO_FILES[path].read_text(encoding="utf-8")
            assert body in prompt, (stage, path)


def test_quant_fundamentals_goes_to_every_stage_told_to_read_it(tmp_path):
    """Four skills say 'Read workflow_artifacts/skills/quant-fundamentals/SKILL.md
    before ...'. Derived from the skill text, so a fifth one fails here."""
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
        rpr._apply_closed_book_inputs(stage, handoff)
        assert _QF in _paths(handoff, "required_inputs"), stage


def test_run_artifacts_are_optional_and_present_ones_are_included(tmp_path, monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path)
    (run_dir / "artifacts" / "findings_carryover.yaml").write_text(
        "parameter_bracket: {dimension: lookback, midpoint: 42}\n", encoding="utf-8")
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("backtest_specification", handoff)
    # innovation_notes.yaml and run_context.yaml are absent: optional, so no raise
    prompt = rpr._build_stage_prompt("backtest_specification", handoff, run_dir)
    assert "--- CONTENT OF artifacts/findings_carryover.yaml ---" in prompt
    assert "midpoint: 42" in prompt
    assert "--- CONTENT OF artifacts/run_context.yaml ---" not in prompt


def test_missing_required_reference_file_fails_loud(tmp_path, monkeypatch):
    """Unlike B7's skip-if-absent union, a missing tracked reference file is a
    broken checkout: the stage must not run without it."""
    monkeypatch.chdir(SR_ROOT)
    run_dir = _sandbox_run(tmp_path)
    (run_dir.parent.parent / "config" / "cost_model.yaml").unlink()
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_closed_book_inputs("validation", handoff)
    with pytest.raises(FileNotFoundError):
        rpr._build_stage_prompt("validation", handoff, run_dir)


def test_existing_entries_are_not_duplicated():
    handoff = {"required_inputs": [{"path": "../../config/cost_model.yaml", "reason": "t"}],
               "optional_inputs": [{"path": "artifacts/innovation_notes.yaml", "reason": "t"}]}
    rpr._apply_closed_book_inputs("validation", handoff)
    rpr._apply_closed_book_inputs("validation", handoff)
    every = _paths(handoff, "required_inputs") + _paths(handoff, "optional_inputs")
    assert len(every) == len(set(every))
    assert handoff["required_inputs"][0]["reason"] == "t"


def test_other_stages_are_untouched():
    for stage in ("hypothesis_generation", "protocol_execution", "data_availability_gate",
                  "specialist_readers", "regroup_record", "holdout_evaluation"):
        handoff = {"required_inputs": [], "optional_inputs": []}
        rpr._apply_closed_book_inputs(stage, handoff)
        assert handoff == {"required_inputs": [], "optional_inputs": []}, stage


def test_async_invoke_agent_applies_the_union(monkeypatch, tmp_path):
    """Wired at the one place every LLM stage's handoff is assembled."""
    src = _ORCH.read_text(encoding="utf-8")
    body = src[src.index("async def async_invoke_agent("):]
    body = body[:body.index("\ndef ")]
    assert "_apply_closed_book_inputs(stage_name, handoff)" in body
    assert body.index("_apply_closed_book_inputs(") < body.index("run_claude_worker(")
