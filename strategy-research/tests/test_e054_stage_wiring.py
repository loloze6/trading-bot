"""
E-054 Layer 2 -- pipeline-stage wiring tests (run_phase1_research.py side).

Covers:
  1. delivery_plan_v26.md s:0.4 item 14 (2026-09-20): the gate now defaults ON
     via config (`orchestrator.data_availability_gate.enabled`, default
     True) -- Decision A registers "data_availability_gate" in STAGE_CONFIGS
     unconditionally, and routing now follows
     `_data_availability_gate_enabled()` (replaces the old
     `E054_DATA_AVAILABILITY_GATE` env var / `_E054_GATE_ENABLED` module
     constant). Explicit `enabled: false` in config reproduces the OLD
     default (env var unset) byte-identically.
  2. run_tool_worker's new "data_availability_gate" branch: invokes the real
     CLI script (subprocess.run, mocked here), copies its output artifact
     into artifacts/, and never crashes on a non-{0,2,3} exit code without
     raising loudly.

Sandboxing: relies on tests/conftest.py's autouse `_sandbox_by_default`
fixture (rpr.ROOT/rpr.CAMPAIGN_STATE_PATH already redirected to a per-test
tmp_path sandbox), same precedent as test_k3_protocol_pinning.py.
"""
import asyncio
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402


# ---------------------------------------------------------------------------
# _data_availability_gate_enabled() -- the one flag that defaults ON
# ---------------------------------------------------------------------------

def _set_dag_flag(root: Path, enabled) -> None:
    """Same shape as test_grid_evaluation.py's _set_grid_flag: enabled=None
    means 'write an empty orchestrator section' (key absent, section
    present) rather than 'omit the file entirely' -- the no-file case is
    covered by its own test below."""
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text("orchestrator: {}\n", encoding="utf-8")
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {"data_availability_gate": {"enabled": bool(enabled)}}}, f)


@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, True)])
def test_data_availability_gate_enabled_reads_flag(enabled, expected):
    """on/off/absent-key-defaults-true -- the inverted default vs every
    other flag in this module (e.g. _grid_evaluation_enabled)."""
    root = rpr.ROOT
    _set_dag_flag(root, enabled)
    assert rpr._data_availability_gate_enabled() is expected


def test_data_availability_gate_enabled_true_when_config_file_absent():
    # deliberately do not create config/campaign_config.yaml (relies on
    # conftest.py's autouse sandbox already pointing rpr.ROOT at an empty
    # tmp_path) -- absent file must default TRUE, the opposite of
    # _grid_evaluation_enabled()'s absent-file default of False.
    assert rpr._data_availability_gate_enabled() is True


def test_gate_explicit_config_off_reproduces_old_env_var_unset_default(monkeypatch):
    """Byte-identity direction required by the dispatch: explicit
    `orchestrator.data_availability_gate.enabled: false` in config must
    reproduce EXACTLY today's (pre-this-change) behavior -- the gate never
    routed to, next_stage stays whatever determine_post_spec_route()
    returned. This does not exercise the old env var (removed along with
    _E054_GATE_ENABLED); it exercises the new function's off-path, which is
    the only way to reach that same behavior now."""
    root = rpr.ROOT
    _set_dag_flag(root, False)
    monkeypatch.delenv("E054_DATA_AVAILABILITY_GATE", raising=False)
    assert rpr._data_availability_gate_enabled() is False
    # Mirrors the exact routing line at the backtest_specification success
    # branch in run_loop: `if _data_availability_gate_enabled(): next_stage
    # = "data_availability_gate"`.
    next_stage = "protocol_execution"  # what determine_post_spec_route() returns for spec_ready
    if rpr._data_availability_gate_enabled():
        next_stage = "data_availability_gate"
    assert next_stage == "protocol_execution", (
        "explicit config-off must leave routing untouched, exactly like the "
        "old unset E054_DATA_AVAILABILITY_GATE env var did"
    )


def test_data_availability_gate_registered_in_stage_configs():
    """Decision A: a real pipeline stage, registered in STAGE_CONFIGS, not an
    inline routing check -- registered regardless of the flag's value."""
    assert "data_availability_gate" in rpr.STAGE_CONFIGS
    assert rpr.STAGE_CONFIGS["data_availability_gate"]["handoff"] == \
        "backtest_spec_to_data_availability_gate.yaml"


def test_data_availability_gate_is_a_tool_stage_no_llm_cost():
    """Must dispatch through run_tool_worker, never an LLM agent -- the
    epic's own framing ('tool, no LLM')."""

    async def _assert_tool_dispatch():
        called = {}

        async def _fake_run_tool_worker(stage_name, run_id):
            called["stage_name"] = stage_name

        import types
        orig = rpr.run_tool_worker
        rpr.run_tool_worker = _fake_run_tool_worker
        try:
            await rpr.async_invoke_agent("data_availability_gate", "run_999")
        finally:
            rpr.run_tool_worker = orig
        return called

    called = asyncio.run(_assert_tool_dispatch())
    assert called.get("stage_name") == "data_availability_gate"


# ---------------------------------------------------------------------------
# run_tool_worker("data_availability_gate", ...) -- the real branch
# ---------------------------------------------------------------------------

def test_run_tool_worker_data_availability_gate_copies_artifact_and_reports_outcome(monkeypatch, capsys):
    root = rpr.ROOT
    _write_protocol(root, "e054_test_protocol.json")
    run_dir = _minimal_run(root, "run_700")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                   {"run_type": "forced_diagnostic", "protocol": "e054_test_protocol.json"})

    captured = {}

    class _FakeCompletedProcess:
        returncode = 0
        stdout = "E-054 Layer 2 outcome: VALIDATE\n"
        stderr = ""

    def _fake_subprocess_run(cmd, *args, **kwargs):
        captured["cmd"] = cmd
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        rpr.save_yaml(out_dir / "data_availability_gate.yaml", {
            "outcome": "validate", "reasons": ["all windows and aux feeds fully available"],
        })
        return _FakeCompletedProcess()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    asyncio.run(rpr.run_tool_worker("data_availability_gate", "run_700"))

    # The protocol passed to the CLI must be exactly the one the shared
    # resolver picked -- no doubling, no substitution.
    protocol_arg = Path(captured["cmd"][3])
    assert protocol_arg == root / "protocols" / "e054_test_protocol.json"

    gate_artifact = run_dir / "artifacts" / "data_availability_gate.yaml"
    assert gate_artifact.exists()
    result = rpr.load_yaml(gate_artifact)
    assert result["outcome"] == "validate"

    out = capsys.readouterr().out
    assert "VALIDATE" in out


def test_run_tool_worker_data_availability_gate_raises_on_genuine_crash(monkeypatch):
    """A non-{0,2,3} exit code is a bug in the gate script itself, not a real
    outcome -- must raise loudly, never be silently treated as a verdict."""
    root = rpr.ROOT
    _write_protocol(root, "e054_crash_protocol.json")
    run_dir = _minimal_run(root, "run_701")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                   {"run_type": "forced_diagnostic", "protocol": "e054_crash_protocol.json"})

    class _FakeCrashedProcess:
        returncode = 1
        stdout = ""
        stderr = "Traceback: boom"

    monkeypatch.setattr(rpr.subprocess, "run", lambda *a, **kw: _FakeCrashedProcess())

    with pytest.raises(RuntimeError, match="crashed"):
        asyncio.run(rpr.run_tool_worker("data_availability_gate", "run_701"))


def test_run_tool_worker_data_availability_gate_decline_exit_code_does_not_raise(monkeypatch):
    """Exit 2 (decline) is a REAL outcome, not a crash -- must not raise."""
    root = rpr.ROOT
    _write_protocol(root, "e054_decline_protocol.json")
    run_dir = _minimal_run(root, "run_702")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                   {"run_type": "forced_diagnostic", "protocol": "e054_decline_protocol.json"})

    class _FakeDeclinedProcess:
        returncode = 2
        stdout = "E-054 Layer 2 outcome: DECLINE\n"
        stderr = ""

    def _fake_subprocess_run(cmd, *args, **kwargs):
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        rpr.save_yaml(out_dir / "data_availability_gate.yaml",
                       {"outcome": "decline", "reasons": ["no data at all"]})
        return _FakeDeclinedProcess()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    asyncio.run(rpr.run_tool_worker("data_availability_gate", "run_702"))  # must not raise

    result = rpr.load_yaml(run_dir / "artifacts" / "data_availability_gate.yaml")
    assert result["outcome"] == "decline"
