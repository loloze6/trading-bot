"""
E-025 S4 -- one-command two-writer dual-writer demo.

Stitches the trial-ledger writer contract (WRITER_CONTRACT.md,
S4_UNION_MERGE_DESIGN.md, research/E025_S4_DESIGN_v5.md) into a single
runnable narrative, so the whole contract can be proven end to end rather
than only in the per-mechanism unit tests (union_merge_trial_ledgers x7,
check_no_duplicate_trial_ids, check_ledger_is_merged x3). This is the fork's
half of S4's "prove the documented procedure end to end" -- Jeremy's half is
running this one command.

    python strategy-research/tools/dual_writer_demo.py

SYNTHETIC ONLY. Two fabricated writer fixtures (dual_writer_demo_fixtures/) --
master run_NNN, fork run_d_NNN, 900-range so a stray copy can never collide
with a real trial. Touches no market data, never writes the live
campaign_record/campaign_state.yaml, never appends a TRIALS.csv row. The
no-DSR-until-merged proof runs the real check_ledger_is_merged against a
hermetic local git repo (bare origin + clone, no network).

Reuses the existing deflate_sharpe functions verbatim -- this driver adds no
new merge/guard logic, it only demonstrates the ones already shipped.
"""

import copy
import re
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import yaml

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import deflate_sharpe as ds  # noqa: E402

FIXTURE_DIR = _HERE / "dual_writer_demo_fixtures"
DEMO_CAMPAIGN_ID = "e025_s4_demo"
_DEMO_ID_RE = re.compile(r"^run_(d_)?9\d\d$")  # run_9NN (master) / run_d_9NN (fork)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def load_state(name: str) -> dict:
    return yaml.safe_load((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def _rows(state: dict) -> list[dict]:
    return state["trial_sharpes"]


# ---------------------------------------------------------------------------
# Proofs -- each returns {name, passed, detail}
# ---------------------------------------------------------------------------

def proof_fixtures_are_synthetic(master: dict, fork: dict) -> dict:
    checks = []
    for label, state in (("master", master), ("fork", fork)):
        checks.append((f"{label}.synthetic is True", state.get("synthetic") is True))
        checks.append((f"{label}.campaign_id == {DEMO_CAMPAIGN_ID}",
                       state.get("campaign_id") == DEMO_CAMPAIGN_ID))
        bad = [r["trial_id"] for r in _rows(state) if not _DEMO_ID_RE.match(r["trial_id"])]
        checks.append((f"{label} ids all in synthetic 900-range", not bad))
    passed = all(ok for _, ok in checks)
    return {
        "name": "fixtures are obviously synthetic (no live-range ids, no market data)",
        "passed": passed,
        "detail": "; ".join(f"{d}={ok}" for d, ok in checks),
    }


def proof_forecast_hash_contract(fork: dict) -> dict:
    """forecast_hash mandatory on every new row EXCEPT backtest_failed (WRITER_CONTRACT
    rule 1) -- the one path where null is legal, the config itself may be the failure.

    Fixture-shape assertion only: write-side enforcement lives in
    run_phase1_research.py (_compute_forecast_hash, fail-loud) and is not exercised here."""
    null_fh = [(r["trial_id"], r["source"]) for r in _rows(fork) if r.get("forecast_hash") is None]
    illegal = [(t, s) for (t, s) in null_fh if s != "backtest_failed"]
    passed = null_fh == [("run_d_902", "backtest_failed")] and not illegal
    return {
        "name": "forecast_hash mandatory except backtest_failed",
        "passed": passed,
        "detail": f"null-forecast_hash rows={null_fh}; illegal nulls={illegal}",
    }


def proof_union_merges_both(master: dict, fork: dict) -> dict:
    merged = ds.union_merge_trial_ledgers(_rows(master), _rows(fork))
    keys = {(r["trial_id"], r["source"]) for r in merged}
    expected = {
        ("run_900", "prescreen"), ("run_900", "backtest"),
        ("run_901", "prescreen"), ("run_901", "backtest"),
        ("run_d_901", "prescreen"),
        ("run_d_902", "prescreen"), ("run_d_902", "backtest_failed"),
        ("run_d_903", "prescreen"), ("run_d_903", "backtest"),
    }
    ds.check_no_duplicate_trial_ids(merged)  # postcondition
    checks = [
        ("9 rows (shared base once + both sides' novel)", len(merged) == 9),
        ("every expected (trial_id, source) present", keys == expected),
        ("shared run_900 base kept once, not duplicated",
         sum(1 for r in merged if r["trial_id"] == "run_900" and r["source"] == "backtest") == 1),
    ]
    return {
        "name": "union-merge is loss-less on disjoint run_NNN / run_d_NNN",
        "passed": all(ok for _, ok in checks),
        "detail": f"merged rows={len(merged)}; keys match={keys == expected}",
        "merged": merged,
    }


def proof_append_only_and_idempotent(master: dict, fork: dict, merged: list[dict]) -> dict:
    m_rows, f_rows = _rows(master), _rows(fork)
    m_snapshot, f_snapshot = copy.deepcopy(m_rows), copy.deepcopy(f_rows)

    remerged = ds.union_merge_trial_ledgers(merged, f_rows)

    checks = [
        ("master rows appear first, in order, verbatim", merged[: len(m_rows)] == m_rows),
        ("re-merging the fork side changes nothing (idempotent)", remerged == merged),
        ("inputs never mutated by the merge", m_rows == m_snapshot and f_rows == f_snapshot),
    ]
    return {
        "name": "append-only + idempotent re-merge",
        "passed": all(ok for _, ok in checks),
        "detail": "; ".join(f"{d}={ok}" for d, ok in checks),
    }


def proof_duplicate_refusal(master: dict, fork: dict) -> dict:
    """A manufactured true collision: the fork side carries the shared run_900/backtest
    row with a DIFFERENT sharpe (a hand-edit / bug -- disjoint prefixes make it
    impossible from honest writers). union_merge_trial_ledgers must REFUSE, never
    silently pick a side."""
    poisoned = copy.deepcopy(_rows(fork))
    for r in poisoned:
        if (r["trial_id"], r["source"]) == ("run_900", "backtest"):
            r["sharpe"] = 0.999  # was -0.6375 on both sides
    refused = False
    detail = "no refusal (BUG)"
    try:
        ds.union_merge_trial_ledgers(_rows(master), poisoned)
    except ValueError as e:
        refused = True
        msg = str(e)
        detail = f"refused; names key={'run_900' in msg}; names field={'sharpe' in msg}"
    return {
        "name": "manufactured (trial_id, source) collision is refused, not silently merged",
        "passed": refused,
        "detail": detail,
    }


def _dedup_count(rows: list[dict]) -> int:
    kept, _ = ds.deduplicate_trials(rows)
    return len(kept)


def proof_killed_row_counts_toward_N(merged: list[dict]) -> dict:
    """The killed trial (run_d_901 -- a prescreen kill, no backtest) is a real
    recorded attempt: it lands in the merged view and counts toward N (the
    multiple-testing count), while contributing NO Sharpe value to the mu_sr/
    sigma_sr sample (statistic_valid=neither). This is the H1 distinction.

    Scope (CUL-214): this exercises a synthetic prescreen row through the
    dual-writer MERGE/dedup library path only -- it is a demo of the library
    contract, not the end-to-end guarantee. The real end-to-end proof that a
    killed run survives the full write path is the E-025 killed-run gate
    (killed_run_gate.py); CUL-138/CUL-209 own that defect and its fix. Do not
    read a pass here as closing either of those tickets.
    """
    killed_key = ("run_d_901", "prescreen")
    in_merged = any((r["trial_id"], r["source"]) == killed_key for r in merged)

    n_with = _dedup_count(merged)
    without_killed = [r for r in merged if (r["trial_id"], r["source"]) != killed_key]
    n_without = _dedup_count(without_killed)

    sharpe_values, _ = ds.load_sharpe_trials({"trial_sharpes": merged})

    checks = [
        ("killed row present in merged view", in_merged),
        ("killed row counts toward N (drop it => N-1)", n_with == n_without + 1),
        ("killed row absent from the Sharpe-value sample", sorted(sharpe_values) == [-0.6375, 0.18, 0.30]),
    ]
    return {
        "name": "killed prescreen row lands in merged view AND counts toward N",
        "passed": all(ok for _, ok in checks),
        "detail": f"N_merged={n_with}, N_without_killed={n_without}, sharpe_sample={sorted(sharpe_values)}",
    }


@contextmanager
def _hermetic_repo_as_ds_repo():
    """A bare local origin + working clone (real git, no network), installed as
    ds._REPO for the duration so the real check_ledger_is_merged runs against it."""
    saved = ds._REPO
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp).resolve()  # macOS /var -> /private/var, so relative_to matches
        origin, work = tmp / "origin.git", tmp / "work"
        origin.mkdir()
        work.mkdir()
        _git(origin, "init", "--bare", "-b", "master")
        _git(work, "init", "-b", "master")
        _git(work, "config", "user.email", "demo@demo")
        _git(work, "config", "user.name", "demo")
        _git(work, "remote", "add", "origin", str(origin))
        state_dir = work / "strategy-research" / "campaign_record"
        state_dir.mkdir(parents=True)
        ds._REPO = str(work)
        try:
            yield work, state_dir / "campaign_state.yaml", origin
        finally:
            ds._REPO = saved


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def proof_no_dsr_until_merged(master: dict, fork: dict, merged: list[dict]) -> dict:
    """Two halves of the binding rule: (1) computing DSR pre-merge understates N
    (the fork sees only its own attempts); (2) the real check_ledger_is_merged
    mechanically refuses an unmerged ledger and permits the merged one."""
    n_premerge = _dedup_count(_rows(fork))     # fork-only view
    n_merged = _dedup_count(merged)            # after union

    with _hermetic_repo_as_ds_repo() as (work, state_path, _origin):
        # origin/master holds the MERGED ledger -- the authoritative post-PR state.
        state_path.write_text(yaml.safe_dump({"trial_sharpes": merged}), encoding="utf-8")
        _git(work, "add", "-A")
        _git(work, "commit", "-m", "merged ledger")
        _git(work, "push", "origin", "master")

        # Pre-merge: this machine still holds only its fork-side view -> divergent.
        state_path.write_text(yaml.safe_dump({"trial_sharpes": _rows(fork)}), encoding="utf-8")
        refused = False
        try:
            ds.check_ledger_is_merged(state_path)
        except RuntimeError:
            refused = True

        # Post-merge: working copy == origin/master -> the gate permits.
        state_path.write_text(yaml.safe_dump({"trial_sharpes": merged}), encoding="utf-8")
        permitted = True
        try:
            ds.check_ledger_is_merged(state_path)
        except RuntimeError:
            permitted = False

    # Only now, on the merged ledger, is DSR computed -- with the honest N.
    sharpe_values, _ = ds.load_sharpe_trials({"trial_sharpes": merged})
    candidate_sr = max(sharpe_values)
    dsr = ds.compute_dsr(candidate_sr, sharpe_values, n_trials=n_merged)

    checks = [
        ("pre-merge N understates the honest count", n_premerge < n_merged),
        ("check_ledger_is_merged REFUSES the unmerged ledger", refused),
        ("check_ledger_is_merged PERMITS the merged ledger", permitted),
        ("DSR computes on the merged ledger with the honest N", dsr.get("error") is None and dsr["n_trials"] == n_merged),
    ]
    return {
        "name": "no DSR until merged (pre-merge N understated; gate refuses then permits)",
        "passed": all(ok for _, ok in checks),
        "detail": f"N_premerge={n_premerge} < N_merged={n_merged}; refused_unmerged={refused}; "
                  f"permitted_merged={permitted}; dsr={dsr['dsr']:.4f} at N={dsr['n_trials']}",
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_demo() -> list[dict]:
    master = load_state("master_ledger.yaml")
    fork = load_state("fork_ledger.yaml")

    results = [
        proof_fixtures_are_synthetic(master, fork),
        proof_forecast_hash_contract(fork),
    ]
    union = proof_union_merges_both(master, fork)
    merged = union.pop("merged")
    results.append(union)
    results.append(proof_append_only_and_idempotent(master, fork, merged))
    results.append(proof_duplicate_refusal(master, fork))
    results.append(proof_killed_row_counts_toward_N(merged))
    results.append(proof_no_dsr_until_merged(master, fork, merged))
    return results


def main() -> int:
    print("E-025 S4 -- two-writer dual-writer demo (synthetic; no market data)\n")
    results = run_demo()
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"[{mark}] {r['name']}")
        print(f"       {r['detail']}")
    all_pass = all(r["passed"] for r in results)
    print(f"\nVERDICT: {'ALL PROOFS PASS' if all_pass else 'FAILED'} "
          f"({sum(r['passed'] for r in results)}/{len(results)})")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
