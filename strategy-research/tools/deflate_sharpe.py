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

def deduplicate_trials(records: list[dict]) -> tuple[list[dict], int]:
    """
    Deduplicate trial records by (forecast_hash, source) (A6.4; #36).

    Keying on forecast_hash ALONE collapsed a single run's prescreen and backtest
    rows once forecast_hash was populated (they share the hash), silently dropping
    the backtest Sharpe from the DSR N. The key includes source to match the
    read-side (trial_id, source) convention (check_no_duplicate_trial_ids): a run
    legitimately carries up to one row per source. A genuine duplicate is the SAME
    (forecast_hash, source) twice.

    Trials with no forecast_hash are treated as unique and always kept.
    Returns (deduped_list, n_removed).
    """
    seen_keys: set[tuple] = set()
    kept: list[dict] = []
    n_removed = 0

    for rec in records:
        fh = rec.get("forecast_hash")
        if fh is None:
            # No hash — treat as unique; always keep
            kept.append(rec)
            continue
        key = (fh, rec.get("source"))
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
      - statistic_expectancy: statistic_valid=="expectancy"
      - statistic_neither: statistic_valid is something else / absent
    """
    records: list[dict] = campaign_state.get("trial_sharpes", [])

    sharpe_values: list[float] = []
    excluded: dict[str, int] = {
        "no_sharpe_value":    0,
        "statistic_expectancy": 0,
        "statistic_neither":  0,
    }

    for rec in records:
        stat = rec.get("statistic_valid")
        if stat == "sharpe":
            sr = rec.get("sharpe")
            if sr is None:
                excluded["no_sharpe_value"] += 1
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

        passes_expectancy = bool(t_stat is not None and t_stat > 2.0)

        expectancy_promotion = {
            "t_stat":          t_stat,
            "passes":          passes_expectancy,
            "bonferroni_note": (
                f"Strict Bonferroni threshold with N={total_hypotheses_tested} trials "
                f"would be t > {_phi_inv(1.0 - 0.05 / max(total_hypotheses_tested, 1)) if total_hypotheses_tested >= 1 else 'N/A':.2f}. "
                f"Using conservative t > 2.0 as practical threshold."
            ),
        }

        return {
            "hypothesis_id":             hypothesis_id,
            "raw_median_sharpe":         None,
            "total_hypotheses_tested":   total_hypotheses_tested,
            "trial_sharpe_variance":     trial_sharpe_variance,
            "deflated_sharpe_ratio":     None,
            "correction_method":         "bailey_lopezdeprado_2014",
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

    return {
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


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _write_yaml(path: Path, data: dict) -> None:
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
