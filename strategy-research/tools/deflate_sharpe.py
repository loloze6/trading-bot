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
import math
import argparse
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
    Deduplicate trial records by forecast_hash field (A6.4).

    Trials with no forecast_hash are treated as unique and always kept.
    Returns (deduped_list, n_removed).
    """
    seen_hashes: set[str] = set()
    kept: list[dict] = []
    n_removed = 0

    for rec in records:
        fh = rec.get("forecast_hash")
        if fh is None:
            # No hash — treat as unique; always keep
            kept.append(rec)
        elif fh in seen_hashes:
            n_removed += 1
        else:
            seen_hashes.add(fh)
            kept.append(rec)

    return kept, n_removed


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
) -> dict:
    """
    Compute the Deflated Sharpe Ratio for candidate_sr given a list of trial Sharpes.

    Returns a dict with:
      - dsr: float or None on error
      - expected_max_sharpe: float
      - mu_sr: mean of trial Sharpes
      - sigma_sr: std dev of trial Sharpes
      - n_trials: number of deduplicated trials
      - z: z-score
      - error: str or None
    """
    N = len(trial_sharpes)

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

    mu_sr    = sum(trial_sharpes) / N
    # Population variance (N denominator) for the trial distribution
    var_sr   = sum((s - mu_sr) ** 2 for s in trial_sharpes) / N
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

    # Expected maximum Sharpe (BLP 2014, equation A.6)
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
    dsr_result = compute_dsr(candidate_sr, sharpe_values)

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

    campaign_state = _load_yaml(campaign_state_path)

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
