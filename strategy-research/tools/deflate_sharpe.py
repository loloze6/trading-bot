"""
deflate_sharpe.py — Bailey & López de Prado (2014) Deflated Sharpe Ratio.

Implements the DSR correction for selection bias across multiple trials.
See: Bailey, D. H. & López de Prado, M. (2014). The Deflated Sharpe Ratio:
Correcting for Selection Bias, Backtest Overfitting and Non-Normality.
Journal of Portfolio Management, 40(5).

A6.4: Trial deduplication by forecast_hash before DSR computation.

CLI:
  python strategy-research/tools/deflate_sharpe.py <run_id>
  python strategy-research/tools/deflate_sharpe.py <run_id> --campaign-state PATH
"""

import sys
import os
import copy
import math
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from statistics import NormalDist, median, variance

import yaml

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))   # strategy-research/tools/
_SR   = os.path.dirname(_HERE)                        # strategy-research/
_REPO = os.path.dirname(_SR)                          # repo root

if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from workflow_artifact_validation import validate_workflow_artifact  # noqa: E402  (CUL-11 sibling helper)

# ---------------------------------------------------------------------------
# Normal distribution helpers (stdlib only — no scipy)
# ---------------------------------------------------------------------------

_NDIST = NormalDist(0, 1)


def _phi(x: float) -> float:
    """Standard normal CDF."""
    return _NDIST.cdf(x)


def _phi_inv(p: float) -> float:
    """Standard normal quantile (inverse CDF). Clamps input to avoid domain errors."""
    p_clamped = max(1e-10, min(1 - 1e-10, p))
    return _NDIST.inv_cdf(p_clamped)


# ---------------------------------------------------------------------------
# Invalidated-artifact exclusion (F8b, 2026-07-04)
# ---------------------------------------------------------------------------

def exclude_invalidated_trials(records: list[dict]) -> tuple[list[dict], int]:
    """
    Exclude trials explicitly marked `invalidated_artifact: true` — these represent
    ZERO actual hypothesis testing (e.g. run_044: FundingRateMeanReversionComponent's
    threshold=0 divide-by-zero, F5a, silently produced active_n_bars=0 and a
    kill_no_ic verdict that was never a real result). Must run BEFORE deduplication
    and before any count that feeds the multiple-testing correction basis
    (total_hypotheses_tested) or the Sharpe trial distribution — an invalidated
    trial must not inflate either.
    """
    kept = [r for r in records if not r.get("invalidated_artifact")]
    n_excluded = len(records) - len(kept)
    return kept, n_excluded


# ---------------------------------------------------------------------------
# Trial deduplication (A6.4)
# ---------------------------------------------------------------------------

def _reproduces_collapses_onto_present_original(
    rec: dict, reproduces_by_key: dict
) -> bool:
    """
    Resolve a record's `reproduces_trial` chain WITHIN its own source.

    Returns True when the chain terminates at an original present in the input
    (a row with no reproduces_trial of its own) -- the reproduction counts once,
    with that original. Returns False when the chain leaves the input (the
    referenced trial is absent) -- the reproducing row is a real counted attempt
    and must be kept, never silently dropped. Raises ValueError on a
    self-reference or a cycle (A -> B -> A) -- those do not resolve to a clean
    single original. A chain (A -> B -> C, C terminal) resolves transitively and
    collapses (CUL-233 F4): a third-generation reproduction still counts once.

    Same-source throughout: the walk carries rec's source, matching the
    (forecast_hash, source) one-row-per-source convention so a backtest
    reproduction cannot collapse onto a prescreen row of the referenced trial.
    """
    source = rec.get("source")
    origin_id = rec.get("trial_id")
    target_id = rec.get("reproduces_trial")
    if target_id == origin_id:
        raise ValueError(
            f"reproduces_trial self-reference: trial {origin_id!r} names itself "
            f"(CUL-233)."
        )
    seen: set = {(origin_id, source)}
    while True:
        key = (target_id, source)
        if key in seen:
            raise ValueError(
                f"reproduces_trial cycle detected starting at {origin_id!r} "
                f"(revisited {target_id!r}, same source) -- refused (CUL-233)."
            )
        if key not in reproduces_by_key:
            return False  # chain leaves the input -> keep the reproducing row
        seen.add(key)
        next_target = reproduces_by_key[key]
        if next_target is None:
            return True  # terminal original present -> collapse
        target_id = next_target


def deduplicate_trials(records: list[dict]) -> tuple[list[dict], int]:
    """
    Deduplicate trial records by (forecast_hash, source), honouring an explicit
    `reproduces_trial` back-reference (A6.4; #36; CUL-233).

    Two collapse paths, both counting the collapsed row as removed:

    1. reproduces_trial (CUL-233): a row whose `reproduces_trial` chain resolves
       (transitively, within its own source) to an original present in the input
       collapses onto that original -- independent of forecast_hash. This is the
       T036/T038 case: T038 is a byte-identical re-execution of T036, but T036
       predates the forecast_hash field (hashless) while T038 carries a fresh
       hash, so the hash key alone counted them twice in the DSR N. Same-source
       matching preserves the one-row-per-source convention (a backtest
       reproduction must not collapse onto a prescreen row of the referenced
       trial). An absent reference is kept (never silently dropped); a chain of
       reproductions collapses onto the terminal original; self-reference and
       cycles fail loud. See _reproduces_collapses_onto_present_original.

    2. forecast_hash (#36): keying on forecast_hash ALONE collapsed a single
       run's prescreen and backtest rows once forecast_hash was populated (they
       share the hash), silently dropping the backtest Sharpe from the DSR N. The
       key includes source to match the read-side (trial_id, source) convention
       (check_no_duplicate_trial_ids): a run legitimately carries up to one row
       per source. A genuine duplicate is the SAME (forecast_hash, source) twice.
       Trials with no forecast_hash are treated as unique and always kept.

    E-061 C2 S2b (G6): the key is (forecast_hash, sorted symbols or None,
    source). A per-coin variant's row (written by the variant loop) carries
    `symbols`, so an asset variant with the base's exact config on another coin
    stays its own trial (card D). A row without the field keys (hash, None,
    source) -- the same partition as the former (hash, source): every existing
    ledger dedupes exactly as before. So a legacy row without `symbols` and a
    per-coin row for the same config (same hash, same source) count as TWO
    trials, never one -- the conservative direction for the DSR (N can only be
    over-counted, never under-counted). A present but malformed `symbols`
    raises. Lockstep with run_phase1_research._dedupe_trials.

    Returns (deduped_list, n_removed).
    """
    # Pre-pass: index every (trial_id, source) present and the reproduces_trial it
    # declares, so the walk can follow a chain and detect a cycle.
    reproduces_by_key: dict[tuple, object] = {}
    for rec in records:
        reproduces_by_key[(rec.get("trial_id"), rec.get("source"))] = rec.get("reproduces_trial")

    seen_keys: set[tuple] = set()
    kept: list[dict] = []
    n_removed = 0

    for rec in records:
        # A reproduces_trial row that resolves to a present original collapses
        # (short-circuit keeps the raise-on-cycle only for rows that declare the
        # field); an absent reference falls through to the forecast_hash path and
        # is kept -- never silently dropped.
        if rec.get("reproduces_trial") is not None and _reproduces_collapses_onto_present_original(
            rec, reproduces_by_key
        ):
            n_removed += 1
            continue
        fh = rec.get("forecast_hash")
        if fh is None:
            # No hash — treat as unique; always keep
            kept.append(rec)
            continue
        if "symbols" in rec:
            syms = rec["symbols"]
            if not (isinstance(syms, list) and syms
                    and all(isinstance(s, str) and s for s in syms)):
                raise ValueError(f"trial {rec.get('trial_id')!r}: symbols {syms!r} is not a "
                                 f"non-empty list of non-empty strings (E-061 C2 S2b)")
            coins = tuple(sorted(syms))
        else:
            coins = None
        key = (fh, coins, rec.get("source"))
        if key in seen_keys:
            n_removed += 1
        else:
            seen_keys.add(key)
            kept.append(rec)

    return kept, n_removed


# ---------------------------------------------------------------------------
# E-025 S2 (2026-08-16): dual-writer mechanical guards
# ---------------------------------------------------------------------------

def check_no_duplicate_trial_ids(records: list[dict]) -> None:
    """
    Refuse if the ledger contains two rows with the same (trial_id, source) pair.

    A single trial_id legitimately carries up to two rows -- one 'prescreen' (every
    trial, kill or pass, per A6.2) and one 'backtest' (only if it advanced). That is
    not a duplicate. A genuine duplicate is the SAME (trial_id, source) appearing
    twice: the write-side guard in run_phase1_research.py::_record_backtest_trial
    (H3, 2026-08-16) prevents this going forward, but this is the read-side backstop
    for the same invariant -- catching a dual-writer race, a manual ledger edit, or a
    future writer that skips the write-side guard. Raises rather than silently
    dropping a row: which copy is correct is not this function's call to make.
    """
    seen: set[tuple] = set()
    dupes: list[tuple] = []
    for r in records:
        key = (r.get("trial_id"), r.get("source"))
        if key in seen and key not in dupes:
            dupes.append(key)
        seen.add(key)
    if dupes:
        raise ValueError(
            f"campaign_state.yaml contains duplicate (trial_id, source) rows: {dupes}. "
            f"DSR computation refuses to run against a ledger with duplicates -- "
            f"resolve them (a duplicate row skews the trial count) before re-running. "
            f"See strategy-research/engineering/roadmap/E-025/EPIC.md."
        )


def check_ledger_is_merged(campaign_state_path: Path, allow_unmerged: bool = False) -> None:
    """
    Dual-writer protocol's binding rule (E-025, 2026-08-16): no DSR computation until
    both sides' ledgers are merged. A locally-modified or locally-behind
    campaign_state.yaml means this machine's view of "how many trials were run" is
    partial -- exactly the failure the DSR's N exists to prevent (an inflated
    significance claim from an understated trial count). Checked by comparing the
    file's actual content against origin/master's tracked copy, not by trusting a
    "have I merged" claim.

    allow_unmerged is an explicit, named opt-out (this repo's `--no-verify` pattern)
    for a deliberate exception -- e.g. an offline sanity check with no intent to act
    on the promotion_audit.yaml this run produces.
    """
    if allow_unmerged:
        return

    repo_root = Path(_REPO)
    try:
        subprocess.run(
            ["git", "fetch", "origin", "master"],
            cwd=repo_root, check=True, capture_output=True, timeout=30,
        )
    except Exception as e:
        raise RuntimeError(
            f"Could not fetch origin/master to verify the ledger is merged "
            f"(no-DSR-until-merged, E-025): {e}. Pass --allow-unmerged to run anyway "
            f"if this is a deliberate offline exception."
        )

    rel_path = campaign_state_path.resolve().relative_to(repo_root)
    diff = subprocess.run(
        ["git", "diff", "--quiet", "origin/master", "--", str(rel_path)],
        cwd=repo_root, capture_output=True,
    )
    if diff.returncode != 0:
        raise RuntimeError(
            f"{rel_path} differs from origin/master -- this machine's ledger is not "
            f"merged (unpushed local trials, or behind on the other side's). DSR "
            f"computed against an unmerged ledger understates N. Sync first (push/pull, "
            f"or land the pending PR), or pass --allow-unmerged if this is a deliberate "
            f"exception."
        )


def _canonical_equal(x, y) -> bool:
    """
    Canonical value equality for trial-ledger rows: Python-native `==` (so
    0 == 0.0 and True == 1 compare equal) with one carve-out -- a pair of float
    NaNs is treated as EQUAL. The carve-out is applied PER FIELD, recursively,
    because a whole-dict `==` is False whenever ANY NaN is present, which would
    misread "the two rows are byte-identical and happen to hold a NaN" as a
    divergence. Correct for nested dict/list values, though ledger rows are flat
    scalar dicts today. A key present on only one side of a dict => not equal
    (one-sided field enrichment is a real difference, refused upstream).
    """
    if isinstance(x, float) and isinstance(y, float) and math.isnan(x) and math.isnan(y):
        return True
    if isinstance(x, dict) and isinstance(y, dict):
        if x.keys() != y.keys():
            return False
        return all(_canonical_equal(x[k], y[k]) for k in x)
    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return False
        return all(_canonical_equal(xi, yi) for xi, yi in zip(x, y, strict=True))
    return x == y


def _row_field_diff(master_row: dict, fork_row: dict) -> dict:
    """Per-field diff of two rows, {field: (master_value, fork_value)}, for the
    refuse-message. A field present on only one side reports `<absent>`."""
    _MISSING = object()
    diff: dict = {}
    for k in set(master_row) | set(fork_row):
        mv = master_row.get(k, _MISSING)
        fv = fork_row.get(k, _MISSING)
        if mv is _MISSING or fv is _MISSING or not _canonical_equal(mv, fv):
            diff[k] = (
                "<absent>" if mv is _MISSING else mv,
                "<absent>" if fv is _MISSING else fv,
            )
    return diff


def union_merge_trial_ledgers(a: list[dict], b: list[dict]) -> list[dict]:
    """
    Union-merge two trial-ledger row lists (E-025 S4). Pure -- no I/O, no git.

    `a` is master (authoritative: its rows and their order are preserved
    verbatim); `b` is fork. Returns a NEW list -- a's rows in a-order, then each
    of b's rows whose (trial_id, source) key is not already present, in b-order.
    Inputs are never mutated or aliased: every returned row is a deepcopy.

    A key present on both sides is kept once when the two rows are canonically
    equal (a shared-ancestor row -- REQUIRED, else every dual-writer sync would
    refuse on the common base). When the two rows DIFFER, the merge REFUSES with
    a ValueError: this fn is 2-way with no common base, so "which side edited the
    shared row" is undecidable and REFUSE is the only safe answer. That refusal
    is the mechanical signal to sync origin/master and retry (WRITER_CONTRACT
    rule 2/5 -- an honest state arising from an upsert), not evidence of a bug.

    Scoped to the trial_sharpes region only; the full 16-key file resolution is
    the manual procedure in research/E025_S4_DESIGN_v5.md. Independent of
    deduplicate_trials (issue #36): takes no dependency on the forecast_hash key.
    """
    check_no_duplicate_trial_ids(a)
    check_no_duplicate_trial_ids(b)

    merged: list[dict] = [copy.deepcopy(row) for row in a]
    index: dict[tuple, dict] = {}
    for row in merged:
        index[(row.get("trial_id"), row.get("source"))] = row

    for row in b:
        key = (row.get("trial_id"), row.get("source"))
        existing = index.get(key)
        if existing is None:
            new_row = copy.deepcopy(row)
            merged.append(new_row)
            index[key] = new_row
        elif not _canonical_equal(existing, row):
            raise ValueError(
                f"union_merge_trial_ledgers: shared row {key} differs between "
                f"master and fork: {_row_field_diff(existing, row)}. If you have "
                f"not merged origin/master since the other writer's last ledger "
                f"change, sync and retry -- this state arises honestly from an "
                f"upsert (WRITER_CONTRACT rule 2)."
            )
        # key present + canonically equal -> shared ancestor, keep master's copy once

    check_no_duplicate_trial_ids(merged)
    return merged


# ---------------------------------------------------------------------------
# Sharpe trial loading
# ---------------------------------------------------------------------------

def load_sharpe_trials(campaign_state: dict) -> tuple[list[float], dict]:
    """
    Extract Sharpe values from campaign_state["trial_sharpes"].

    Filters to statistic_valid == "sharpe" and sharpe is not None.
    Returns (sharpe_values, excluded_counts).

    excluded_counts keys:
      - no_sharpe_value: statistic_valid=="sharpe" but sharpe field is None
      - non_finite_sharpe: statistic_valid=="sharpe" but sharpe is NaN/inf (a
        contract-legitimate merged row, e.g. a killed-run placeholder) — excluded
        with a visible counter so a single NaN cannot silently corrupt mu_sr/sigma_sr/dsr
      - statistic_expectancy: statistic_valid=="expectancy"
      - statistic_neither: statistic_valid is something else / absent
    """
    records: list[dict] = campaign_state.get("trial_sharpes", [])

    sharpe_values: list[float] = []
    excluded: dict[str, int] = {
        "no_sharpe_value":    0,
        "non_finite_sharpe":  0,
        "statistic_expectancy": 0,
        "statistic_neither":  0,
    }

    for rec in records:
        stat = rec.get("statistic_valid")
        if stat == "sharpe":
            sr = rec.get("sharpe")
            if sr is None:
                excluded["no_sharpe_value"] += 1
            elif not math.isfinite(float(sr)):
                excluded["non_finite_sharpe"] += 1
            else:
                sharpe_values.append(float(sr))
        elif stat == "expectancy":
            excluded["statistic_expectancy"] += 1
        else:
            excluded["statistic_neither"] += 1

    return sharpe_values, excluded


# ---------------------------------------------------------------------------
# Core DSR computation — Bailey & López de Prado (2014)
# ---------------------------------------------------------------------------

_EULER_MASCHERONI = 0.5772156649  # γ


def compute_dsr(
    candidate_sr: float,
    trial_sharpes: list[float],
    n_trials: int | None = None,
) -> dict:
    """
    Compute the Deflated Sharpe Ratio for candidate_sr given a list of trial Sharpes.

    n_trials (H1 fix, 2026-08-16, issue #28): the multiple-testing correction's N --
    how many independent attempts were made, which sets how hard the expected-max-
    Sharpe benchmark it must clear rises -- is a DIFFERENT quantity from
    len(trial_sharpes), the sample of real Sharpe VALUES used to estimate that
    benchmark's mean/variance. Before this fix the two were silently the same number:
    N was len(trial_sharpes), so a prescreen kill or expectancy-only trial (a real
    attempt, recorded, but with no Sharpe value) was invisible to the very correction
    it exists to be counted by. Measured live: 16 real trials, DSR saw N=1.

    Pass n_trials explicitly (the caller's honest total -- e.g. compute_promotion_audit's
    total_hypotheses_tested, every recorded trial of any statistic_valid, deduplicated)
    to count every real attempt toward the correction's strength. trial_sharpes stays
    the real-valued sample for estimating mu_sr/sigma_sr, which genuinely needs numbers,
    not just a count -- a large N with too few real Sharpe values still correctly
    refuses (see the n_sharpe < 2 branch below), because no total count fixes an
    unmeasurable variance. Omitted, n_trials falls back to len(trial_sharpes) --
    byte-identical to every pre-existing caller.

    Returns a dict with:
      - dsr: float or None on error
      - expected_max_sharpe: float
      - mu_sr: mean of trial Sharpes
      - sigma_sr: std dev of trial Sharpes
      - n_trials: the N used for the multiple-testing correction (not necessarily
        len(trial_sharpes) -- see n_trials param above)
      - z: z-score
      - error: str or None
    """
    n_sharpe = len(trial_sharpes)
    N        = n_trials if n_trials is not None else n_sharpe

    # Defensive: N (the multiple-testing count) must be at least as large as n_sharpe
    # (the real-valued sample it's derived from) -- every real attempt with a Sharpe
    # value is necessarily counted in an honest total. compute_promotion_audit's
    # single call site provably satisfies this by construction (sharpe_values is a
    # filtered SUBSET of the same deduped_records total_hypotheses_tested counts), so
    # this never fires there -- it exists for any future caller. Raising, not
    # clamping: a violation here would silently UNDERSTATE the correction (the exact
    # flattering direction this fix exists to close), so it must fail loud rather than
    # guess which number is right.
    if n_trials is not None and N < n_sharpe:
        raise ValueError(
            f"n_trials={N} is smaller than len(trial_sharpes)={n_sharpe} -- every real "
            f"Sharpe value is itself a counted attempt, so N can never be less than the "
            f"real-valued sample it's estimated from. This is a caller bug, not a data "
            f"condition; passing a too-small n_trials would silently understate the "
            f"multiple-testing correction."
        )

    if N < 2:
        return {
            "dsr":               None,
            "expected_max_sharpe": None,
            "mu_sr":             None,
            "sigma_sr":          None,
            "n_trials":          N,
            "z":                 None,
            "error":             f"Insufficient trials: need >= 2, got {N}",
        }

    if n_sharpe < 2:
        return {
            "dsr":               None,
            "expected_max_sharpe": None,
            "mu_sr":             None,
            "sigma_sr":          None,
            "n_trials":          N,
            "z":                 None,
            "error":             (
                f"N={N} trials recorded (multiple-testing count is honest), but only "
                f"{n_sharpe} produced a real Sharpe value -- need >= 2 real Sharpe "
                f"values to estimate the trial distribution's variance. A large N does "
                f"not fix an unmeasurable variance."
            ),
        }

    mu_sr    = sum(trial_sharpes) / n_sharpe
    # Population variance (n_sharpe denominator, NOT N) for the trial distribution --
    # this estimates the SHAPE of the Sharpe-generating process from the real values
    # actually observed, independent of how many total attempts N counts.
    var_sr   = sum((s - mu_sr) ** 2 for s in trial_sharpes) / n_sharpe
    sigma_sr = math.sqrt(var_sr)

    if sigma_sr < 1e-10:
        return {
            "dsr":               None,
            "expected_max_sharpe": None,
            "mu_sr":             mu_sr,
            "sigma_sr":          sigma_sr,
            "n_trials":          N,
            "z":                 None,
            "error":             "No trial variance: all trial Sharpes are identical",
        }

    # Expected maximum Sharpe (BLP 2014, equation A.6). N here IS the multiple-testing
    # count (every real attempt) -- this is the whole point of H1: a larger honest N
    # makes the benchmark harder to clear, exactly as the correction is supposed to.
    # Z_exp_max = (1 - γ) * Φ⁻¹(1 - 1/N) + γ * Φ⁻¹(1 - 1/(e*N))
    gamma   = _EULER_MASCHERONI
    e       = math.e
    arg1    = 1.0 - 1.0 / N
    arg2    = 1.0 - 1.0 / (e * N)
    Z_exp_max    = (1.0 - gamma) * _phi_inv(arg1) + gamma * _phi_inv(arg2)
    E_max_SR     = mu_sr + sigma_sr * Z_exp_max

    z   = (candidate_sr - E_max_SR) / sigma_sr
    dsr = _phi(z)

    return {
        "dsr":               dsr,
        "expected_max_sharpe": E_max_SR,
        "mu_sr":             mu_sr,
        "sigma_sr":          sigma_sr,
        "n_trials":          N,
        "z":                 z,
        "error":             None,
    }


# ---------------------------------------------------------------------------
# Full promotion audit
# ---------------------------------------------------------------------------

def compute_promotion_audit(
    hypothesis_id: str,
    candidate_sr: float | None,
    campaign_state: dict,
    n_trades: int = 0,
    expectancy_bps: float | None = None,
    expectancy_se: float | None = None,
) -> dict:
    """
    Compute promotion audit dict for promotion_audit.yaml.

    candidate_sr: median Sharpe from protocol_result; None triggers sparse-trading path.
    expectancy_bps / expectancy_se: per-trade expectancy stats for sparse path.

    Returns a dict matching promotion_audit.schema.json.
    """
    raw_trial_records: list[dict] = campaign_state.get("trial_sharpes", [])

    # F8b: exclude invalidated-artifact trials FIRST — before dedup, before any count.
    valid_records, n_invalidated = exclude_invalidated_trials(raw_trial_records)

    # A6.4: deduplicate before any computation
    deduped_records, n_removed = deduplicate_trials(valid_records)

    sharpe_values, excluded_counts = load_sharpe_trials(
        {"trial_sharpes": deduped_records}
    )
    excluded_counts["invalidated_artifact"] = n_invalidated
    # #48 F3: the pipeline reports dedup_removed in its excluded-counts dict
    # (run_phase1_research.py) while this path did not, so promotion audits from
    # the two implementations were not field-comparable -- the same drift class
    # as correction_method (#40/#43) and sigma_sr (#56), in the audit SHAPE
    # rather than a value. The count was already computed above; it just was not
    # reported under the shared shape.
    excluded_counts["dedup_removed"] = n_removed

    total_hypotheses_tested = len(deduped_records)
    n_trials_used           = len(sharpe_values)

    # Determine if sparse-trading path
    is_sparse = (candidate_sr is None)

    # Variance across Sharpe trials
    trial_sharpe_variance: float | None = None
    if n_trials_used >= 2:
        trial_sharpe_variance = variance(sharpe_values)

    # ------------------------------------------------------------------
    # Expectancy-based (sparse) path
    # ------------------------------------------------------------------
    expectancy_promotion: dict | None = None

    if is_sparse:
        t_stat: float | None = None
        if expectancy_bps is not None and expectancy_se is not None and expectancy_se > 0:
            t_stat = expectancy_bps / expectancy_se

        # CUL-163: None (not False) when t_stat is unmeasurable (expectancy SE
        # unavailable), matching the pipeline's honest indeterminate. The holdout gate
        # reads passes with `is False`, so collapsing indeterminate to False would
        # terminal-reject a candidate that was never actually evaluated. A real bool
        # is still returned whenever the t-stat could be computed.
        passes_expectancy = None if t_stat is None else (t_stat > 2.0)

        # CUL-193: the format spec below used to sit on the whole conditional
        # expression (`{X if cond else 'N/A':.2f}`), which applies `.2f` even
        # to the 'N/A' string branch and raises ValueError whenever
        # total_hypotheses_tested is 0 (an empty or not-yet-recorded trial
        # ledger -- a real, reachable state, not just a test artifact).
        # Formatting the numeric branch to a string FIRST avoids the trap.
        _strict_t_str = (
            f"{_phi_inv(1.0 - 0.05 / total_hypotheses_tested):.2f}"
            if total_hypotheses_tested >= 1 else "N/A"
        )
        expectancy_promotion = {
            "t_stat":          t_stat,
            "passes":          passes_expectancy,
            "bonferroni_note": (
                f"Strict Bonferroni threshold with N={total_hypotheses_tested} trials "
                f"would be t > {_strict_t_str}. "
                f"Using conservative t > 2.0 as practical threshold."
            ),
        }

        return {
            "hypothesis_id":             hypothesis_id,
            "raw_median_sharpe":         None,
            "total_hypotheses_tested":   total_hypotheses_tested,
            "trial_sharpe_variance":     trial_sharpe_variance,
            "deflated_sharpe_ratio":     None,
            # CUL-163: the sparse path uses a per-trade expectancy t-stat, not the
            # Bailey & Lopez de Prado DSR -- this label was a genuine mislabel. Aligns
            # with the pipeline's honest label (run_phase1_research.py:5295) so both
            # writers lockstep, and the sparse audit validates against the (now
            # two-value) correction_method enum.
            "correction_method":         "expectancy_t_stat_bonferroni",
            "promotion_threshold_raw":   None,
            "promotion_threshold_deflated": 0.95,
            "passes_deflated_threshold": passes_expectancy,
            "excluded_trial_counts":     excluded_counts,
            "n_trials_used":             n_trials_used,
            "expected_max_sharpe":       None,
            "is_sparse_trading":         True,
            "expectancy_promotion":      expectancy_promotion,
            "generated_at":              datetime.now(timezone.utc).isoformat(),
        }

    # ------------------------------------------------------------------
    # Sharpe path
    # ------------------------------------------------------------------
    # H1 fix (2026-08-16, issue #28): feed the HONEST total (every recorded trial --
    # kills, expectancy-only, sharpe, and now backtest_failed rows -- deduplicated) as
    # the multiple-testing N, not the len(sharpe_values) subset that has real numbers.
    # total_hypotheses_tested already computed this correctly (line 328); it was just
    # never passed to the function that needed it.
    dsr_result = compute_dsr(candidate_sr, sharpe_values, n_trials=total_hypotheses_tested)

    dsr_value   = dsr_result.get("dsr")
    E_max_SR    = dsr_result.get("expected_max_sharpe")

    # raw_median_sharpe is the candidate from the current run
    raw_median_sharpe = candidate_sr

    # promotion_threshold_raw: in Sharpe space, the threshold is E_max_SR
    # (only meaningful if DSR computation succeeded)
    promotion_threshold_raw = E_max_SR

    passes = bool(dsr_value is not None and dsr_value > 0.95)

    audit = {
        "hypothesis_id":             hypothesis_id,
        "raw_median_sharpe":         raw_median_sharpe,
        "total_hypotheses_tested":   total_hypotheses_tested,
        "trial_sharpe_variance":     trial_sharpe_variance,
        "deflated_sharpe_ratio":     dsr_value,
        "correction_method":         "bailey_lopezdeprado_2014",
        "promotion_threshold_raw":   promotion_threshold_raw,
        "promotion_threshold_deflated": 0.95,
        "passes_deflated_threshold": passes,
        "excluded_trial_counts":     excluded_counts,
        "n_trials_used":             n_trials_used,
        "expected_max_sharpe":       E_max_SR,
        "is_sparse_trading":         False,
        "expectancy_promotion":      None,
        "generated_at":              datetime.now(timezone.utc).isoformat(),
    }
    # dsr_error parity with run_phase1_research._write_promotion_audit: when
    # compute_dsr could not compute the DSR (insufficient trials, too few real
    # Sharpe values, or zero variance) it returns a diagnostic under "error".
    # The pipeline path exposes that text as "dsr_error"; mirror it here so the
    # two lockstep audits carry the same field. Present only when non-None,
    # matching the pipeline (absent on the happy path).
    if dsr_result.get("error") is not None:
        audit["dsr_error"] = dsr_result["error"]
    return audit


# ---------------------------------------------------------------------------
# E-062 S2b-2a (D-041 / D-046): the whole-test daily DSR -- PURE, not wired
# ---------------------------------------------------------------------------
#
# ONE implementation: S2b-2b's pipeline imports these functions; there is no
# lockstep twin in run_phase1_research. Everything above this section (the
# legacy per-window DSR, its sparse path and its CLI) is untouched and stays on
# the legacy basis until D-043.
#
# Basis: a trial's Sharpe is the whole-test daily Sharpe of its chained
# equal-weight portfolio (tools/portfolio_whole_test.whole_test_sharpe_stats),
# per day, NOT annualised. It lives on a ledger row as a nested `whole_test`
# block (S2B2_FINDINGS G1/Q2) or, for a legacy row recomputed later, as an
# entry of the append-only overlay campaign_record/trial_sharpe_basis_recompute.yaml
# (G8/Q4). A value enters the same-basis sample only on an EXACT basis-string
# match with status "ok", so per-window-median and whole-test values never mix.

import numbers  # noqa: E402
import statistics  # noqa: E402
from collections.abc import Mapping  # noqa: E402

from portfolio_whole_test import WHOLE_TEST_BASIS  # noqa: E402  (tools/ sibling)

WHOLE_TEST_STATUSES = frozenset({"ok", "not_evaluable", "error"})
_BLOCK_STAT_KEYS = ("sr_daily", "n_daily_returns", "skew", "kurtosis")
# The exact key set of a native ledger `whole_test` block (S2B2_FINDINGS Q2) and of
# an overlay entry (Q4). Exact: an unknown key (e.g. a timestamp) raises.
_BLOCK_KEYS = frozenset({"basis", "status", "reason", *_BLOCK_STAT_KEYS})
_OVERLAY_KEYS = _BLOCK_KEYS | {"trial_id", "source", "inputs_sha256", "code_sha256"}
_HEX = frozenset("0123456789abcdef")


def _real(x) -> bool:
    return isinstance(x, numbers.Real) and not isinstance(x, bool)


def _finite(x, what: str) -> float:
    if not _real(x) or not math.isfinite(float(x)):
        raise ValueError(f"{what}: {x!r} is not a finite real number")
    return float(x)


def _int_at_least(x, lo: int, what: str) -> int:
    if isinstance(x, bool) or not isinstance(x, numbers.Integral):
        raise ValueError(f"{what}: {x!r} is not an integer")
    if int(x) < lo:
        raise ValueError(f"{what}: {x!r} is below {lo}")
    return int(x)


def _expected_max_z(n: int) -> float:
    """Z(N) = (1 - g) Phi^-1(1 - 1/N) + g Phi^-1(1 - 1/(e N)), g = Euler-Mascheroni
    (BLP 2014 A.6). N >= 2. No clamping: N is a trial count, so both arguments lie
    in [0.5, 1) for every reachable N."""
    g = _EULER_MASCHERONI
    return ((1.0 - g) * _NDIST.inv_cdf(1.0 - 1.0 / n)
            + g * _NDIST.inv_cdf(1.0 - 1.0 / (math.e * n)))


def compute_dsr_whole_test(candidate_stats, same_basis_srs, n_total: int,
                           min_same_basis: int) -> dict:
    """Deflated Sharpe Ratio on the whole-test daily basis (D-046).

    candidate_stats: {sr_daily, T, skew, kurtosis_raw} as returned by
        portfolio_whole_test.whole_test_sharpe_stats. It may carry
        `status` (default "ok") and `reason`: any status other than "ok" (the
        candidate's own whole-test block is not_evaluable/error) gives
        NOT_EVALUABLE, and then the numeric keys are not read.
    same_basis_srs: the per-day Sharpes of the same-basis sample (K = its
        length; the candidate's own value included -- see
        select_same_basis_sample).
    n_total: N, every counted trial (the existing deduped-valid-row rule;
        never shrinks). N < K raises (caller bug: every same-basis value is a
        counted trial).
    min_same_basis: the floor `dsr_min_same_basis_trials` (>= 2; a parameter
        here, the config key is S2b-2b's).

    SR0 (the benchmark):
        K <  floor: SR0 = sigma_null * Z(N)                          (sigma_source "null")
        K >= floor: SR0 = max(mean_K, 0) + max(sigma_K, sigma_null) * Z(N)
                    (sigma_source "cross" when sigma_K > sigma_null, else "null")
      sigma_null = 1 / sqrt(T - 1); sigma_K = sample stdev (ddof 1) of the
      same-basis values; Z(N) = _expected_max_z(N).
    DSR = Phi((SR - SR0) sqrt(T - 1) / sqrt(1 - skew SR + ((kurt - 1) / 4) SR^2)),
      SR = the candidate's sr_daily, skew / raw kurtosis of its daily returns.

    NOT_EVALUABLE (status "not_evaluable", dsr None, reason set) ONLY when:
    N < 2; the candidate's own block is not "ok"; the denominator's argument is
    <= 0. A small K is never NOT_EVALUABLE (sigma_null takes over). Malformed
    input raises ValueError."""
    n_total = _int_at_least(n_total, 0, "compute_dsr_whole_test: n_total")
    min_same_basis = _int_at_least(min_same_basis, 2, "compute_dsr_whole_test: min_same_basis")
    if isinstance(same_basis_srs, (str, bytes, Mapping)):
        raise ValueError("compute_dsr_whole_test: same_basis_srs must be a sequence of numbers")
    srs = [_finite(s, f"compute_dsr_whole_test: same_basis_srs[{i}]")
           for i, s in enumerate(same_basis_srs)]
    k = len(srs)
    if n_total < k:
        raise ValueError(
            f"compute_dsr_whole_test: n_total={n_total} is smaller than the same-basis "
            f"sample K={k} -- every same-basis value is itself a counted trial. Caller bug: "
            f"a too-small N would understate the multiple-testing correction.")
    if not isinstance(candidate_stats, Mapping):
        raise ValueError(f"compute_dsr_whole_test: candidate_stats {candidate_stats!r} is not "
                         f"a mapping")

    out = {"status": "ok", "reason": None, "dsr": None, "sr0": None, "sigma_used": None,
           "sigma_source": None, "sigma_null": None, "sigma_cross": None,
           "mean_same_basis": None, "z_expected_max": None, "sr_daily": None,
           "K": k, "N": n_total, "T": None, "min_same_basis": min_same_basis}

    def _not_evaluable(reason: str) -> dict:
        out.update(status="not_evaluable", reason=reason, dsr=None)
        return out

    status = candidate_stats.get("status", "ok")
    if status != "ok":
        return _not_evaluable(
            f"the candidate's own whole-test block is {status!r}, not 'ok'"
            + (f": {candidate_stats.get('reason')}" if candidate_stats.get("reason") else ""))
    sr = _finite(candidate_stats.get("sr_daily"), "compute_dsr_whole_test: candidate sr_daily")
    t = _int_at_least(candidate_stats.get("T"), 2, "compute_dsr_whole_test: candidate T")
    skew = _finite(candidate_stats.get("skew"), "compute_dsr_whole_test: candidate skew")
    kurt = _finite(candidate_stats.get("kurtosis_raw"),
                   "compute_dsr_whole_test: candidate kurtosis_raw")
    out.update(sr_daily=sr, T=t)
    if n_total < 2:
        return _not_evaluable(f"N={n_total} counted trial(s); the multiple-testing "
                              f"correction needs N >= 2")

    sigma_null = 1.0 / math.sqrt(t - 1)
    z = _expected_max_z(n_total)
    out.update(sigma_null=sigma_null, z_expected_max=z)
    if k < min_same_basis:
        sigma_used, source, floor_mean = sigma_null, "null", 0.0
    else:
        mean_k = statistics.mean(srs)
        sigma_k = math.sqrt(statistics.variance(srs))
        out.update(mean_same_basis=mean_k, sigma_cross=sigma_k)
        if sigma_k > sigma_null:
            sigma_used, source = sigma_k, "cross"
        else:
            sigma_used, source = sigma_null, "null"
        floor_mean = max(mean_k, 0.0)
    sr0 = floor_mean + sigma_used * z
    out.update(sr0=sr0, sigma_used=sigma_used, sigma_source=source)

    denom_arg = 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * sr * sr
    if not denom_arg > 0.0:
        return _not_evaluable(f"the DSR denominator's argument 1 - skew*SR + ((kurt-1)/4)*SR^2 "
                              f"= {denom_arg!r} is not > 0 (skew={skew!r}, kurtosis_raw={kurt!r}, "
                              f"SR={sr!r})")
    out["dsr"] = _phi((sr - sr0) * math.sqrt(t - 1) / math.sqrt(denom_arg))
    return out


def _check_sha_tree(value, what: str) -> None:
    """A mapping whose leaves are lowercase 64-hex sha256 strings (nested mappings allowed,
    e.g. portfolio_states: {path: sha})."""
    if not isinstance(value, Mapping) or not value:
        raise ValueError(f"{what}: {value!r} is not a non-empty mapping")
    for k, v in value.items():
        if not isinstance(k, str) or not k:
            raise ValueError(f"{what}: key {k!r} is not a non-empty string")
        if isinstance(v, Mapping):
            _check_sha_tree(v, f"{what}.{k}")
        elif not (isinstance(v, str) and len(v) == 64 and set(v) <= _HEX):
            raise ValueError(f"{what}.{k}: {v!r} is not a lowercase sha256 hex digest")


def _check_whole_test_block(block, what: str, keys=_BLOCK_KEYS) -> dict:
    """Validate a `whole_test` block (native, or an overlay entry with keys=_OVERLAY_KEYS):
    exactly `keys`; basis a non-empty string;
    status in WHOLE_TEST_STATUSES; status ok -> reason None, finite sr_daily / skew /
    kurtosis, integer n_daily_returns >= 2; otherwise a non-empty reason. Returns the
    projection onto the block's own keys (basis, status, reason + the four stats)."""
    if not isinstance(block, Mapping):
        raise ValueError(f"{what}: {block!r} is not a mapping")
    if set(block) != keys:
        raise ValueError(f"{what}: keys missing {sorted(keys - set(block))}, "
                         f"unknown {sorted(set(block) - keys)}")
    basis, status, reason = block.get("basis"), block.get("status"), block.get("reason")
    if not isinstance(basis, str) or not basis:
        raise ValueError(f"{what}: basis {basis!r} is not a non-empty string")
    if status not in WHOLE_TEST_STATUSES:
        raise ValueError(f"{what}: status {status!r} is not one of {sorted(WHOLE_TEST_STATUSES)}")
    if status == "ok":
        if reason is not None:
            raise ValueError(f"{what}: status ok with a reason {reason!r}")
        _finite(block.get("sr_daily"), f"{what}: sr_daily")
        _finite(block.get("skew"), f"{what}: skew")
        _finite(block.get("kurtosis"), f"{what}: kurtosis")
        _int_at_least(block.get("n_daily_returns"), 2, f"{what}: n_daily_returns")
    elif not isinstance(reason, str) or not reason:
        raise ValueError(f"{what}: status {status!r} without a non-empty reason")
    return {k: block.get(k) for k in ("basis", "status", "reason", *_BLOCK_STAT_KEYS)}


def validate_basis_overlay(data) -> dict:
    """Validate the recompute overlay's parsed YAML (S2B2_FINDINGS Q4/G8) and index it.

    Shape: None/empty (no overlay yet) or {"entries": [entry, ...]}. Every entry has
    exactly the keys trial_id, source, basis, status, reason, sr_daily,
    n_daily_returns, skew, kurtosis, inputs_sha256, code_sha256 -- an unknown key
    (e.g. a timestamp, which would make two writers' entries differ) raises. The
    block fields follow _check_whole_test_block; inputs_sha256 / code_sha256 are
    non-empty mappings of sha256 digests.

    Append-only and deterministic: the same (trial_id, source, basis) twice is kept
    once when the two entries are canonically equal (both writers appended the same
    bytes) and raises when they differ. Returns {(trial_id, source, basis): entry}."""
    if data is None:
        return {}
    if not isinstance(data, Mapping) or set(data) - {"entries"}:
        raise ValueError(f"basis overlay: top level must be a mapping with only 'entries', "
                         f"got {data!r:.200}")
    entries = data.get("entries")
    if entries is None:
        return {}
    if not isinstance(entries, list):
        raise ValueError("basis overlay: 'entries' is not a list")
    index: dict = {}
    for i, e in enumerate(entries):
        what = f"basis overlay entry {i}"
        _check_whole_test_block(e, what, keys=_OVERLAY_KEYS)
        for f in ("trial_id", "source"):
            if not isinstance(e[f], str) or not e[f]:
                raise ValueError(f"{what}: {f} {e[f]!r} is not a non-empty string")
        _check_sha_tree(e["inputs_sha256"], f"{what}: inputs_sha256")
        _check_sha_tree(e["code_sha256"], f"{what}: code_sha256")
        key = (e["trial_id"], e["source"], e["basis"])
        if key in index:
            if not _canonical_equal(dict(index[key]), dict(e)):
                raise ValueError(f"basis overlay: two different entries for {key}: "
                                 f"{_row_field_diff(dict(index[key]), dict(e))} -- the overlay "
                                 f"is append-only with deterministic entries; refused")
            continue
        index[key] = copy.deepcopy(dict(e))
    return index


def load_basis_overlay(path) -> dict:
    """Read-only: parse and validate the overlay file (validate_basis_overlay). A
    missing file is an empty overlay (nothing has been recomputed yet)."""
    p = Path(path)
    if not p.exists():
        return {}
    return validate_basis_overlay(_load_yaml(p))


def select_same_basis_sample(trial_records, overlay=None, basis: str = WHOLE_TEST_BASIS) -> dict:
    """The same-basis sample of the whole-test DSR (S2B2_FINDINGS G11) and N.

    Rows: F8b invalidated rows out, then deduplicate_trials -- the SAME deduped
    valid rows that define N (so N is exactly today's rule and does not depend on
    the overlay). A deduped row enters the sample when its value on `basis` is
    status "ok": a native `whole_test` block with that exact basis string, else an
    overlay entry for (trial_id, source, basis). A row with neither (a legacy row,
    a prescreen, a backtest_failed, a not_evaluable block) counts in N only. The
    legacy `sharpe` field is never read. The candidate's own row is in the sample
    like any other (its block is ok).

    Precedence: native beats overlay; both present for the same basis and
    different -> ValueError. An overlay entry for a (trial_id, source) absent from
    the ledger raises (the ledger is behind the overlay: not merged).

    overlay: the dict from validate_basis_overlay / load_basis_overlay (or None).
    Returns {"srs": [...], "rows": [{trial_id, source, sr_daily, origin}], "K": len,
    "N": len(deduped valid rows), "basis": basis}."""
    if not isinstance(basis, str) or not basis:
        raise ValueError(f"select_same_basis_sample: basis {basis!r} is not a non-empty string")
    if not isinstance(trial_records, list):
        raise ValueError("select_same_basis_sample: trial_records must be a list of rows")
    overlay = overlay or {}
    for r in trial_records:
        if not isinstance(r, Mapping):
            raise ValueError(f"select_same_basis_sample: ledger row {r!r} is not a mapping")
    ledger_keys = {(r.get("trial_id"), r.get("source")) for r in trial_records}
    orphans = sorted(str(k) for k in overlay if (k[0], k[1]) not in ledger_keys)
    if orphans:
        raise ValueError(f"select_same_basis_sample: overlay entries for rows absent from the "
                         f"ledger: {orphans} -- the ledger is not merged; refused")

    # Precedence / conflict is checked on EVERY ledger row (a conflict is a data error
    # whether or not the row survives dedup).
    for i, r in enumerate(trial_records):
        if "whole_test" in r:
            native = _check_whole_test_block(r["whole_test"],
                                              f"ledger row {i} ({r.get('trial_id')!r}) whole_test")
            ov = overlay.get((r.get("trial_id"), r.get("source"), native["basis"]))
            if ov is None:
                continue
            ov_block = {k: ov[k] for k in _BLOCK_KEYS}
            if not _canonical_equal(native, ov_block):
                raise ValueError(
                    f"select_same_basis_sample: ledger row ({r.get('trial_id')!r}, "
                    f"{r.get('source')!r}) has a native whole_test block and an overlay entry "
                    f"on basis {native['basis']!r} that differ: "
                    f"{_row_field_diff(native, ov_block)}")

    valid, _n_invalidated = exclude_invalidated_trials(trial_records)
    deduped, _n_removed = deduplicate_trials(valid)
    rows = []
    for r in deduped:
        tid, src = r.get("trial_id"), r.get("source")
        block, origin = None, None
        native = r.get("whole_test")
        if native is not None and native.get("basis") == basis:
            block, origin = native, "native"
        elif (tid, src, basis) in overlay:
            block, origin = overlay[(tid, src, basis)], "overlay"
        if block is None or block.get("status") != "ok":
            continue
        rows.append({"trial_id": tid, "source": src, "sr_daily": float(block["sr_daily"]),
                     "origin": origin})
    return {"srs": [x["sr_daily"] for x in rows], "rows": rows, "K": len(rows),
            "N": len(deduped), "basis": basis}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _write_yaml(path: Path, data: dict) -> None:
    validate_workflow_artifact(path, data)  # CUL-11: opt-in schema check (warn-by-default)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute Deflated Sharpe Ratio (Bailey & López de Prado 2014) for a run."
    )
    parser.add_argument(
        "run_id",
        help="Run ID (e.g. run_039). Artifacts read from strategy-research/runs/<run_id>/artifacts/",
    )
    parser.add_argument(
        "--campaign-state",
        default=None,
        help="Path to campaign_state.yaml. Defaults to strategy-research/campaign_record/campaign_state.yaml.",
    )
    parser.add_argument(
        "--allow-unmerged", action="store_true",
        help="E-025: skip the no-DSR-until-merged check against origin/master. Explicit "
             "opt-out for a deliberate exception (e.g. an offline sanity check) -- do "
             "not use to work around a real sync problem.",
    )
    args = parser.parse_args()

    run_id = args.run_id
    artifacts_dir = Path(_SR) / "runs" / run_id / "artifacts"

    # Load campaign state
    if args.campaign_state:
        campaign_state_path = Path(args.campaign_state)
    else:
        campaign_state_path = Path(_SR) / "campaign_record" / "campaign_state.yaml"

    if not campaign_state_path.exists():
        print(f"ERROR: campaign_state.yaml not found at {campaign_state_path}", file=sys.stderr)
        sys.exit(1)

    # E-025: dual-writer binding rule -- refuse on an unmerged ledger before trusting
    # anything it says.
    try:
        check_ledger_is_merged(campaign_state_path, allow_unmerged=args.allow_unmerged)
    except (RuntimeError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    campaign_state = _load_yaml(campaign_state_path)

    # E-025: mechanical duplicate-(trial_id, source) refusal -- the read-side backstop
    # for the write-side idempotency guard (issue #28 H3).
    try:
        check_no_duplicate_trial_ids(campaign_state.get("trial_sharpes", []))
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Load hypothesis_id from hypothesis_card.yaml
    hypothesis_card_path = artifacts_dir / "hypothesis_card.yaml"
    if not hypothesis_card_path.exists():
        print(f"ERROR: hypothesis_card.yaml not found at {hypothesis_card_path}", file=sys.stderr)
        sys.exit(1)

    hypothesis_card = _load_yaml(hypothesis_card_path)
    hypothesis_id   = hypothesis_card.get("hypothesis_id", run_id)

    # Load candidate_sr and trade info from protocol_result.yaml
    protocol_result_path = artifacts_dir / "protocol_result.yaml"
    if not protocol_result_path.exists():
        print(f"ERROR: protocol_result.yaml not found at {protocol_result_path}", file=sys.stderr)
        sys.exit(1)

    protocol_result = _load_yaml(protocol_result_path)

    # Extract candidate_sr: median Sharpe from per_symbol_summary
    # Also check statistic_valid / is_sparse from hypothesis_verdict diagnostics
    candidate_sr:    float | None = None
    n_trades:        int          = 0
    expectancy_bps:  float | None = None
    expectancy_se:   float | None = None

    per_symbol = protocol_result.get("per_symbol_summary", {})
    sharpes = [
        v["median_sharpe"]
        for v in per_symbol.values()
        if isinstance(v, dict) and v.get("median_sharpe") is not None
    ]
    if sharpes:
        candidate_sr = median(sharpes)

    # Check hypothesis_verdict diagnostics for sparse path
    hv = protocol_result.get("hypothesis_verdict") or {}
    diag = hv.get("diagnostics") or {}
    below_floor_pct = diag.get("below_floor_pct", 0.0)

    if below_floor_pct is not None and below_floor_pct > 50.0:
        # Sparse trading path: median_sharpe is null, use per-trade expectancy
        candidate_sr = None
        exp_block    = diag.get("per_trade_expectancy_bps") or {}
        expectancy_bps = exp_block.get("mean")
        expectancy_se  = exp_block.get("se")
        n_trades       = exp_block.get("n", 0)

    # Total trade count from all results
    if n_trades == 0:
        n_trades = sum(
            r.get("core", {}).get("trade_count", 0)
            for r in protocol_result.get("results", [])
        )

    # Compute audit
    audit = compute_promotion_audit(
        hypothesis_id  = hypothesis_id,
        candidate_sr   = candidate_sr,
        campaign_state = campaign_state,
        n_trades       = n_trades,
        expectancy_bps = expectancy_bps,
        expectancy_se  = expectancy_se,
    )

    # Write output
    out_path = artifacts_dir / "promotion_audit.yaml"
    _write_yaml(out_path, audit)

    print(f"[deflate_sharpe] hypothesis_id:           {audit['hypothesis_id']}")
    print(f"[deflate_sharpe] total_hypotheses_tested: {audit['total_hypotheses_tested']}")
    print(f"[deflate_sharpe] n_trials_used:           {audit['n_trials_used']}")
    print(f"[deflate_sharpe] is_sparse_trading:       {audit['is_sparse_trading']}")
    if not audit["is_sparse_trading"]:
        print(f"[deflate_sharpe] raw_median_sharpe:       {audit['raw_median_sharpe']}")
        print(f"[deflate_sharpe] expected_max_sharpe:     {audit['expected_max_sharpe']}")
        print(f"[deflate_sharpe] deflated_sharpe_ratio:   {audit['deflated_sharpe_ratio']}")
    else:
        ep = audit.get("expectancy_promotion") or {}
        print(f"[deflate_sharpe] expectancy t_stat:       {ep.get('t_stat')}")
    print(f"[deflate_sharpe] passes_deflated_threshold: {audit['passes_deflated_threshold']}")
    print(f"[deflate_sharpe] Written to {out_path}")


if __name__ == "__main__":
    main()
