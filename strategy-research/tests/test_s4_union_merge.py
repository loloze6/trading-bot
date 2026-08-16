"""
E-025 S4 (2026-08-16) — union-merge procedure verification for
campaign_state.yaml, the trial-ledger dual-writer scenario (issue #28,
CLAUDE.fork.md's six-item precondition, item 3: "append-only, union-on-
conflict merge -- a naive git merge can silently drop one side's trials").

Empirically tested against real hermetic git repos (real clones, real `git
merge`, no mocking of git behaviour). This file went through one real
self-correction worth keeping visible: the first version tested a 3-key toy
fixture (trial_sharpes/runs/updated_at packed with zero separation) and
concluded `merge=union` "corrupts campaign_state.yaml into invalid YAML" --
true for that toy fixture, but re-tested against the REAL file's actual key
order (`runs` is the 3rd top-level key, `updated_at` the 14th, `trial_sharpes`
the last -- see campaign_record/campaign_state.yaml) and the real co-touch
pattern (`update_campaign_state_after_run` appends to `runs` AND
`altitude_history` -- adjacent keys -- in the same save), the claim did NOT
hold: union merge produced valid, correctly-unioned YAML in both cases. The
false claim had already been committed and told to Dorian before this
correction; both were retracted. See research/ledger/win.md's 2026-08-16
entries for the full trail.

Verified findings, current:

1. Plain `git merge` on concurrent campaign_state.yaml touches CONFLICTS
   loudly (does not silently drop either side) -- but is not zero-touch;
   every concurrent dual-writer sync on this file will conflict.
2. The correct manual resolution is "keep both sides' list entries, always"
   -- verified to produce the full union with no duplicate trial_ids.
3. `merge=union`, re-tested against the real file's actual structure (not a
   toy fixture), correctly unions list fields (`runs`, `altitude_history`,
   `trial_sharpes`) even when two list fields are touched together in the
   same commit and sit on adjacent keys. It does NOT corrupt the file under
   any real-shaped scenario tested here.
4. `merge=union` DOES still have one verified real wrinkle: a same-line
   scalar conflict (both sides changing `updated_at` to different values)
   resolves as a duplicate YAML key, which PyYAML's safe_load silently
   collapses to "last one wins" -- no conflict marker, no error, one side's
   write just doesn't survive. Low-stakes for `updated_at` specifically (a
   timestamp nobody depends on for correctness), but it is the same *shape*
   of silent-loss the dual-writer protocol exists to prevent, on a field
   that happens not to matter. And finding #3's safety currently rests on
   this file's key layout keeping list regions apart from scalar edits --
   that is a property of today's file structure, not a guarantee the merge
   driver enforces, so it is not treated as a durable safety proof.

Given #4 and the layout-dependence caveat in #3, the documented procedure
stays: plain git merge (conflict is the expected, correct outcome), manual
resolution keeps every list entry from both sides, `check_no_duplicate_
trial_ids` is the mechanical backstop on the resolved result before any DSR
computation. `merge=union` is not adopted -- not because it was proven to
corrupt the file (it wasn't, on retest), but because its safety here is
contingent on a file layout nobody has committed to preserving, and it has
one demonstrated silent-loss mode already.
"""
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import deflate_sharpe as ds  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent
REAL_CAMPAIGN_STATE = REPO_ROOT / "campaign_record" / "campaign_state.yaml"


def _git(repo, *args, check=True):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=check)


def _write_state(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _load_real_base_state() -> dict:
    """The real campaign_state.yaml's actual key order and structure, trimmed
    to a small number of entries per list for a fast, readable diff -- but
    with the real key ordering and real field shapes (e.g. `runs` is a flat
    list of id strings, not dicts) preserved exactly."""
    d = yaml.safe_load(REAL_CAMPAIGN_STATE.read_text(encoding="utf-8"))
    d["runs"] = d["runs"][:3]
    d["altitude_history"] = d["altitude_history"][:2]
    d["trial_sharpes"] = d["trial_sharpes"][:2]
    return d


@pytest.fixture
def divergent_branches_realistic(tmp_path):
    """A hermetic local repo, real campaign_state.yaml structure/key order,
    two branches diverging from a common base. Both sides append a run_id to
    `runs`, an entry to `altitude_history` (the real co-touch pattern from
    update_campaign_state_after_run), a trial to `trial_sharpes`, and bump
    `updated_at` (unconditional on every _save_campaign_state call)."""
    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-b", "master")
    _git(work, "config", "user.email", "t@t.com")
    _git(work, "config", "user.name", "t")

    state_path = work / "campaign_state.yaml"
    _write_state(state_path, _load_real_base_state())
    _git(work, "add", "-A")
    _git(work, "commit", "-m", "base")

    _git(work, "checkout", "-b", "master-continues")
    d = yaml.safe_load(state_path.read_text())
    d["runs"].append("run_master_new")
    d["altitude_history"].append({"run": "run_master_new", "altitude": "parameter",
                                   "dimension": "x", "family": "f", "outcome": "improved"})
    d["trial_sharpes"].append({"trial_id": "run_master_new", "source": "backtest",
                                "sharpe": 0.3, "statistic_valid": "sharpe", "forecast_hash": "hM"})
    d["updated_at"] = "2026-08-16T09:00:00Z"
    _write_state(state_path, d)
    _git(work, "commit", "-am", "master run")

    _git(work, "checkout", "master")
    _git(work, "checkout", "-b", "fork-branch")
    d = yaml.safe_load(state_path.read_text())
    d["runs"].append("run_d_new")
    d["altitude_history"].append({"run": "run_d_new", "altitude": "parameter",
                                   "dimension": "y", "family": "g", "outcome": "no_improvement"})
    d["trial_sharpes"].append({"trial_id": "run_d_new", "source": "backtest",
                                "sharpe": 0.15, "statistic_valid": "sharpe", "forecast_hash": "hD"})
    d["updated_at"] = "2026-08-16T10:00:00Z"
    _write_state(state_path, d)
    _git(work, "commit", "-am", "fork run")

    _git(work, "checkout", "master-continues")
    return work, state_path


def test_concurrent_trial_additions_conflict_not_silently_drop(divergent_branches_realistic):
    """Finding 1: plain git merge on concurrent campaign_state.yaml edits CONFLICTS
    (exit != 0) rather than silently picking one side. Both sides' new entries
    must be visibly present (inside conflict markers) -- proving neither is
    dropped, just not auto-resolved."""
    work, state_path = divergent_branches_realistic

    result = _git(work, "merge", "fork-branch", "--no-edit", check=False)
    assert result.returncode != 0, "expected a real merge conflict on concurrent trial additions"

    conflicted = state_path.read_text()
    assert "run_master_new" in conflicted
    assert "run_d_new" in conflicted
    assert "<<<<<<<" in conflicted  # loud, not silent

    _git(work, "merge", "--abort")


def test_manual_union_resolution_keeps_both_sides_and_has_no_duplicates(divergent_branches_realistic):
    """Finding 2: the correct resolution procedure -- keep every list entry from
    BOTH sides (never git checkout --ours/--theirs on this file) -- produces the
    full union with no duplicate trial_ids, verified against the mechanical
    backstop that already gates DSR computation."""
    work, state_path = divergent_branches_realistic
    _git(work, "merge", "fork-branch", "--no-edit", check=False)

    base = _load_real_base_state()
    resolved = dict(base)
    resolved["runs"] = base["runs"] + ["run_master_new", "run_d_new"]
    resolved["trial_sharpes"] = base["trial_sharpes"] + [
        {"trial_id": "run_master_new", "source": "backtest", "sharpe": 0.3,
         "statistic_valid": "sharpe", "forecast_hash": "hM"},
        {"trial_id": "run_d_new", "source": "backtest", "sharpe": 0.15,
         "statistic_valid": "sharpe", "forecast_hash": "hD"},
    ]
    resolved["updated_at"] = "2026-08-16T10:00:00Z"
    _write_state(state_path, resolved)
    _git(work, "add", "-A")
    _git(work, "commit", "--no-edit")

    merged = yaml.safe_load(state_path.read_text())
    assert merged["runs"][-2:] == ["run_master_new", "run_d_new"]  # full union, both sides
    trial_ids = [t["trial_id"] for t in merged["trial_sharpes"]]
    assert trial_ids[-2:] == ["run_master_new", "run_d_new"]
    ds.check_no_duplicate_trial_ids(merged["trial_sharpes"])  # must not raise


def test_merge_union_handles_realistic_concurrent_touches_correctly(divergent_branches_realistic):
    """Finding 3 (corrects an earlier, wrong finding -- see module docstring):
    against the REAL file's key order and the real co-touch pattern (runs +
    altitude_history + trial_sharpes all touched together, exactly as
    update_campaign_state_after_run does it), merge=union produces VALID YAML
    with the correct union on every list field. It does not corrupt the file
    here -- the earlier "produces invalid YAML" claim was an artifact of a toy
    3-key fixture with zero separation between fields, not a property of this
    file."""
    work, state_path = divergent_branches_realistic
    (work / ".gitattributes").write_text("campaign_state.yaml merge=union\n", encoding="utf-8")
    _git(work, "add", ".gitattributes")
    _git(work, "commit", "-m", "attr")

    result = _git(work, "merge", "fork-branch", "--no-edit", check=False)
    assert result.returncode == 0

    merged = yaml.safe_load(state_path.read_text())  # must parse cleanly
    assert merged["runs"][-2:] == ["run_master_new", "run_d_new"]
    altitudes = [a["run"] for a in merged["altitude_history"][-2:]]
    assert altitudes == ["run_master_new", "run_d_new"]
    trial_ids = [t["trial_id"] for t in merged["trial_sharpes"][-2:]]
    assert trial_ids == ["run_master_new", "run_d_new"]


def test_merge_union_silently_drops_one_side_of_a_scalar_conflict(divergent_branches_realistic):
    """Finding 4: merge=union's real, verified wrinkle. Both sides change the
    SAME scalar line (`updated_at`) to different values -- union keeps both as
    a duplicate YAML key with no conflict signal, and PyYAML's safe_load
    silently resolves duplicate keys to the last one, so one side's write
    vanishes without any error. Low-stakes for updated_at specifically, but
    it is the same silent-loss shape the dual-writer protocol exists to
    prevent -- the reason merge=union is not adopted, even though finding 3
    shows it doesn't corrupt the file under tested conditions."""
    work, state_path = divergent_branches_realistic
    (work / ".gitattributes").write_text("campaign_state.yaml merge=union\n", encoding="utf-8")
    _git(work, "add", ".gitattributes")
    _git(work, "commit", "-m", "attr")

    raw_before_parse = None
    _git(work, "merge", "fork-branch", "--no-edit", check=False)
    raw_before_parse = state_path.read_text()
    assert raw_before_parse.count("updated_at:") == 2  # duplicate key, both values present in the text

    merged = yaml.safe_load(state_path.read_text())
    assert merged["updated_at"] == "2026-08-16T10:00:00Z"  # last-wins: master's value silently lost
