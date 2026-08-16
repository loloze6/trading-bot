"""
E-025 S4 (2026-08-16) — union-merge procedure verification for
campaign_state.yaml, the trial-ledger dual-writer scenario (issue #28,
CLAUDE.fork.md's six-item precondition, item 3: "append-only, union-on-
conflict merge -- a naive git merge can silently drop one side's trials").

Empirically tested against a real hermetic git repo (two real clones, real
`git merge`, no mocking of git behaviour) rather than assumed. Three findings:

1. Plain `git merge` does NOT silently drop either side's trials when both
   sides concurrently append to campaign_state.yaml's trial_sharpes/runs
   lists -- it CONFLICTS loudly, because both additions attach at the same
   last common line. This is the safe direction (a human must act), but it
   is not zero-touch: every concurrent dual-writer sync on this file will
   conflict, not merge silently.
2. The correct resolution is "keep both sides' list entries, always" -- never
   `git checkout --ours`/`--theirs` on this file. That produces the full
   union with no duplicate trial_ids, verified against
   deflate_sharpe.check_no_duplicate_trial_ids.
3. A `merge=union` .gitattributes driver -- the obvious "automate the
   resolution" idea -- was tried and is UNSAFE: it does resolve the
   trial_sharpes/runs list conflicts without a manual step, but it also
   interleaves the unrelated `updated_at` scalar line with the `runs` list
   lines it happened to sit beside in the conflict hunk, producing a
   campaign_state.yaml that no longer parses as YAML at all. Auto-merges
   with exit 0 and no error -- exactly the silent-corruption shape the
   dual-writer protocol exists to prevent, just one layer down (structural
   corruption instead of a dropped trial). Do not adopt merge=union for
   this file.

Procedure this landed on: plain git merge (conflict is the expected,
correct outcome on concurrent touches), manual resolution keeps every list
entry from both sides, `check_no_duplicate_trial_ids` is the mechanical
backstop on the resolved result before any DSR computation.
"""
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import deflate_sharpe as ds  # noqa: E402


def _git(repo, *args, check=True):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=check)


def _write_state(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


_BASE_STATE = {
    "trial_sharpes": [
        {"trial_id": "run_060", "source": "backtest", "sharpe": 0.1,
         "statistic_valid": "sharpe", "forecast_hash": "h60"},
        {"trial_id": "run_061", "source": "backtest", "sharpe": 0.2,
         "statistic_valid": "sharpe", "forecast_hash": "h61"},
    ],
    "runs": [
        {"run_id": "run_060", "status": "done"},
        {"run_id": "run_061", "status": "done"},
    ],
    "updated_at": "2026-08-15T00:00:00Z",
}


@pytest.fixture
def divergent_branches(tmp_path):
    """A hermetic local repo with two branches diverging from a common base --
    'master-continues' (a master-side campaign run appending run_062) and
    'fork-branch' (a fork-side campaign run appending run_d_001, the S3
    disjoint-ID scheme). Returns (work_dir, state_path)."""
    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-b", "master")
    _git(work, "config", "user.email", "t@t.com")
    _git(work, "config", "user.name", "t")

    state_path = work / "campaign_state.yaml"
    _write_state(state_path, _BASE_STATE)
    _git(work, "add", "-A")
    _git(work, "commit", "-m", "base")

    _git(work, "checkout", "-b", "master-continues")
    master_state = yaml.safe_load(state_path.read_text())
    master_state["trial_sharpes"].append(
        {"trial_id": "run_062", "source": "backtest", "sharpe": 0.3,
         "statistic_valid": "sharpe", "forecast_hash": "h62"}
    )
    master_state["runs"].append({"run_id": "run_062", "status": "done"})
    master_state["updated_at"] = "2026-08-16T09:00:00Z"
    _write_state(state_path, master_state)
    _git(work, "commit", "-am", "master: run_062")

    _git(work, "checkout", "master")
    _git(work, "checkout", "-b", "fork-branch")
    fork_state = yaml.safe_load(state_path.read_text())
    fork_state["trial_sharpes"].append(
        {"trial_id": "run_d_001", "source": "backtest", "sharpe": 0.15,
         "statistic_valid": "sharpe", "forecast_hash": "hd1"}
    )
    fork_state["runs"].append({"run_id": "run_d_001", "status": "done"})
    fork_state["updated_at"] = "2026-08-16T10:00:00Z"
    _write_state(state_path, fork_state)
    _git(work, "commit", "-am", "fork: run_d_001")

    _git(work, "checkout", "master-continues")
    return work, state_path


def test_concurrent_trial_additions_conflict_not_silently_drop(divergent_branches):
    """Finding 1: plain git merge on concurrent campaign_state.yaml edits CONFLICTS
    (exit != 0) rather than silently picking one side. Both sides' new trial_ids
    must be visibly present (inside conflict markers) -- proving neither is
    dropped, just not auto-resolved."""
    work, state_path = divergent_branches

    result = _git(work, "merge", "fork-branch", "--no-edit", check=False)
    assert result.returncode != 0, "expected a real merge conflict on concurrent trial additions"

    conflicted = state_path.read_text()
    assert "run_062" in conflicted  # master's addition is present, not dropped
    assert "run_d_001" in conflicted  # fork's addition is present, not dropped
    assert "<<<<<<<" in conflicted  # loud, not silent

    _git(work, "merge", "--abort")  # leave repo clean for other tests


def test_manual_union_resolution_keeps_both_sides_and_has_no_duplicates(divergent_branches):
    """Finding 2: the correct resolution procedure -- keep every list entry from
    BOTH sides (never git checkout --ours/--theirs on this file) -- produces the
    full union with no duplicate trial_ids, verified by the mechanical backstop
    (check_no_duplicate_trial_ids) that already gates DSR computation."""
    work, state_path = divergent_branches
    _git(work, "merge", "fork-branch", "--no-edit", check=False)

    resolved = dict(_BASE_STATE)
    resolved["trial_sharpes"] = _BASE_STATE["trial_sharpes"] + [
        {"trial_id": "run_062", "source": "backtest", "sharpe": 0.3,
         "statistic_valid": "sharpe", "forecast_hash": "h62"},
        {"trial_id": "run_d_001", "source": "backtest", "sharpe": 0.15,
         "statistic_valid": "sharpe", "forecast_hash": "hd1"},
    ]
    resolved["runs"] = _BASE_STATE["runs"] + [
        {"run_id": "run_062", "status": "done"},
        {"run_id": "run_d_001", "status": "done"},
    ]
    resolved["updated_at"] = "2026-08-16T10:00:00Z"
    _write_state(state_path, resolved)
    _git(work, "add", "-A")
    _git(work, "commit", "--no-edit")

    merged = yaml.safe_load(state_path.read_text())
    trial_ids = [t["trial_id"] for t in merged["trial_sharpes"]]
    assert trial_ids == ["run_060", "run_061", "run_062", "run_d_001"]  # full union, both sides
    ds.check_no_duplicate_trial_ids(merged["trial_sharpes"])  # must not raise


def test_merge_union_attribute_is_unsafe_for_this_file(divergent_branches):
    """Finding 3: a `merge=union` .gitattributes driver -- the tempting
    'automate the conflict away' shortcut -- resolves WITHOUT a conflict (exit
    0) but interleaves the unrelated `updated_at` scalar with the `runs` list's
    lines, producing campaign_state.yaml that fails to parse as YAML at all.
    Regression-pins the rejection: if this ever starts parsing cleanly, the
    file's structure changed enough that the finding needs re-verifying before
    anyone reconsiders merge=union."""
    work, state_path = divergent_branches

    (work / ".gitattributes").write_text("campaign_state.yaml merge=union\n", encoding="utf-8")
    _git(work, "add", ".gitattributes")
    _git(work, "commit", "-m", "attr")
    # "union" is one of git's built-in low-level merge drivers (no merge.union.driver
    # config needed) -- it keeps all non-identical lines from both sides instead of
    # conflict-marking them.

    result = _git(work, "merge", "fork-branch", "--no-edit", check=False)
    assert result.returncode == 0  # auto-resolves -- looks successful

    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(state_path.read_text())  # ...but the result is not valid YAML
