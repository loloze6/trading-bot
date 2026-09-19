"""
E-025 S1/S2 (2026-08-16, issue #28 H3) regression tests.

Covers the write-side fix (forecast_hash emission + the (trial_id, source)-keyed
idempotency guard on _record_backtest_trial, run_phase1_research.py) and the
read-side backstops (the mechanical duplicate-(trial_id, source) refusal and the
no-DSR-until-merged git check, deflate_sharpe.py).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))

import deflate_sharpe as ds  # noqa: E402
import run_phase1_research as rpr  # noqa: E402


# ---------------------------------------------------------------------------
# _compute_forecast_hash
# ---------------------------------------------------------------------------


def _write_config(tmp_path, obj, name="candidate_strategy_config.json"):
    p = tmp_path / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    return p


def test_forecast_hash_identical_for_identical_content(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    a = _write_config(tmp_path / "a", {"strategy": "x", "weight": 1.0})
    b = _write_config(tmp_path / "b", {"weight": 1.0, "strategy": "x"})  # key order swapped
    assert rpr._compute_forecast_hash(a) == rpr._compute_forecast_hash(b)


def test_forecast_hash_differs_for_different_content(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    a = _write_config(tmp_path / "a", {"strategy": "x", "weight": 1.0})
    b = _write_config(tmp_path / "b", {"strategy": "x", "weight": 2.0})
    assert rpr._compute_forecast_hash(a) != rpr._compute_forecast_hash(b)


def test_forecast_hash_missing_config_fails_loud(tmp_path):
    with pytest.raises(FileNotFoundError, match="forecast_hash"):
        rpr._compute_forecast_hash(tmp_path / "does_not_exist.json")


# ---------------------------------------------------------------------------
# _record_backtest_trial: forecast_hash emission + (trial_id, source) idempotency
# ---------------------------------------------------------------------------


_MINIMAL_SUMMARY = {
    "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 0.0}},
    "per_symbol_summary": {
        "BTCUSDT": {"median_sharpe": 1.23, "trade_count": 50},
    },
}


@pytest.fixture
def campaign_env(tmp_path, monkeypatch):
    """Isolated campaign_state.yaml + a real candidate_strategy_config.json, with
    load/save monkeypatched onto the tmp path so no test touches the real ledger."""
    state_path = tmp_path / "campaign_state.yaml"
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", state_path)
    config_path = tmp_path / "candidate_strategy_config.json"
    config_path.write_text(json.dumps({"strategy": "x"}), encoding="utf-8")
    return state_path, config_path


def test_record_backtest_trial_writes_forecast_hash(campaign_env):
    state_path, config_path = campaign_env
    rpr._record_backtest_trial("run_900", _MINIMAL_SUMMARY, config_path)
    state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    (row,) = state["trial_sharpes"]
    assert row["forecast_hash"] == rpr._compute_forecast_hash(config_path)


def test_record_backtest_trial_reentry_is_idempotent(campaign_env):
    """H3: calling _record_backtest_trial twice for the same run_id (simulating a
    resume/retry re-entering protocol_execution) must not duplicate the row --
    this is the exact defect measured live on run_054/run_059 (3x each) before
    this fix."""
    state_path, config_path = campaign_env
    rpr._record_backtest_trial("run_901", _MINIMAL_SUMMARY, config_path)
    rpr._record_backtest_trial("run_901", _MINIMAL_SUMMARY, config_path)
    state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    backtest_rows = [t for t in state["trial_sharpes"]
                      if t["trial_id"] == "run_901" and t["source"] == "backtest"]
    assert len(backtest_rows) == 1


def test_record_backtest_trial_not_suppressed_by_existing_prescreen_row(campaign_env):
    """The guard must be keyed on (trial_id, source), not trial_id alone -- issue #28
    warned a naive trial_id-only guard would wrongly suppress a legitimate backtest
    row when a prescreen row for the same run_id already exists (which is the normal
    case: every trial gets a prescreen row, and only those that advance also get a
    backtest row)."""
    state_path, config_path = campaign_env
    state_path.write_text(yaml.safe_dump({
        "trial_sharpes": [
            {"trial_id": "run_902", "source": "prescreen", "statistic_valid": "neither"},
        ]
    }), encoding="utf-8")

    rpr._record_backtest_trial("run_902", _MINIMAL_SUMMARY, config_path)

    state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    sources = sorted(t["source"] for t in state["trial_sharpes"] if t["trial_id"] == "run_902")
    assert sources == ["backtest", "prescreen"]


# ---------------------------------------------------------------------------
# deflate_sharpe.check_no_duplicate_trial_ids
# ---------------------------------------------------------------------------


def test_check_no_duplicate_trial_ids_passes_on_clean_ledger():
    records = [
        {"trial_id": "run_1", "source": "prescreen"},
        {"trial_id": "run_1", "source": "backtest"},  # legitimate: same trial, 2 stages
        {"trial_id": "run_2", "source": "prescreen"},
    ]
    ds.check_no_duplicate_trial_ids(records)  # must not raise


def test_check_no_duplicate_trial_ids_raises_on_real_duplicate():
    records = [
        {"trial_id": "run_1", "source": "backtest"},
        {"trial_id": "run_1", "source": "backtest"},  # the actual H3 shape
    ]
    with pytest.raises(ValueError, match=r"run_1.*backtest"):
        ds.check_no_duplicate_trial_ids(records)


# ---------------------------------------------------------------------------
# deflate_sharpe.check_ledger_is_merged
# ---------------------------------------------------------------------------


def _git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture
def merged_repo(tmp_path):
    """A hermetic local origin + working clone, both real git repos, no network.
    Returns (repo_root, campaign_state_path) with origin/master already tracking
    campaign_state.yaml's initial content."""
    origin = tmp_path / "origin.git"
    origin.mkdir()
    _git(origin, "init", "--bare", "-b", "master")

    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-b", "master")
    _git(work, "config", "user.email", "t@t.com")
    _git(work, "config", "user.name", "t")
    _git(work, "remote", "add", "origin", str(origin))

    campaign_dir = work / "strategy-research" / "campaign_record"
    campaign_dir.mkdir(parents=True)
    state_path = campaign_dir / "campaign_state.yaml"
    state_path.write_text(yaml.safe_dump({"trial_sharpes": []}), encoding="utf-8")
    _git(work, "add", "-A")
    _git(work, "commit", "-m", "initial ledger")
    _git(work, "push", "origin", "master")

    return work, state_path


def test_check_ledger_is_merged_passes_when_in_sync(merged_repo, monkeypatch):
    repo_root, state_path = merged_repo
    monkeypatch.setattr(ds, "_REPO", str(repo_root))
    ds.check_ledger_is_merged(state_path)  # must not raise


def test_check_ledger_is_merged_raises_on_local_divergence(merged_repo, monkeypatch):
    """Simulates the exact dual-writer race this check exists for: a local trial
    added but not yet pushed/merged."""
    repo_root, state_path = merged_repo
    monkeypatch.setattr(ds, "_REPO", str(repo_root))

    state_path.write_text(
        yaml.safe_dump({"trial_sharpes": [{"trial_id": "run_d_001", "source": "backtest"}]}),
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="not merged"):
        ds.check_ledger_is_merged(state_path)


def test_check_ledger_is_merged_allow_unmerged_short_circuits(merged_repo, monkeypatch):
    """--allow-unmerged must skip the check entirely -- proven by making any git call
    fail, so a pass here can only mean the function returned before shelling out."""
    repo_root, state_path = merged_repo
    monkeypatch.setattr(ds, "_REPO", str(repo_root))

    def _boom(*a, **k):
        raise AssertionError("git must not be invoked when allow_unmerged=True")

    monkeypatch.setattr(ds.subprocess, "run", _boom)
    ds.check_ledger_is_merged(state_path, allow_unmerged=True)  # must not raise
