"""
Evaluation harness for prereg_whale_footprint_v2.yaml (dispatch W8 step 6;
pointed at v2 and given a new economic-feasibility gate by dispatch W9 step 5).

Reads every threshold from the pre-registration file — none are hardcoded
here — enforces economic feasibility, the minimum-N gate, the coverage floor,
and single-use consumption, and emits a verdict by MECHANICAL application of
the pre-registration's verdict mapping. This module is UNRUN against the real
capture: every test in
`strategy-research/tests/test_whale_footprint_evaluation.py` exercises it on
synthetic, planted-answer fixtures only.

CALL ORDER OF GATES (fixed, matches the pre-registration's stated intent that
"the harness refuses to execute" ahead of computing anything): single-use ->
economic feasibility -> coverage floor -> minimum-N. The first gate that
blocks stops evaluation; no verdict is computed for a blocked run, and a
blocked run does NOT consume the single-use mark (only a run that reaches an
actual verdict does).

ECONOMIC FEASIBILITY (new in v2, dispatch W9 step 4)
-----------------------------------------------------
Data-independent: it reads only `prereg['economic_ic_threshold']`, never the
panels. A pre-registration whose own cost-model derivation shows the required
IC at its registered bar frequency exceeds what a Spearman correlation can
even express (bounded in [-1, 1]) is untradeable BEFORE any data is
collected — no sample size fixes an economically-impossible threshold, so
this gate is checked ahead of (and independent of) the minimum-N sample-size
question. A pre-registration file with no `economic_ic_threshold` key (e.g.
v1) or with `economically_untradeable_at_registered_frequency` false/absent
is unaffected — this gate is backward compatible.

INPUT CONTRACT
--------------
`panels`: Dict[pair_symbol, pandas.DataFrame], one DataFrame per venue pair,
each with columns:
  - one column per name in prereg['features']['names']
  - 'target'   : that bar's forward return (data.target_definition)
  - 'attested' : bool/0-1, whether this bar's feature values are usable
                 (mirrors whale_features.py's whale_attested column)
Rows where attested is falsy are excluded from every statistic below — this
harness never imputes or forward-fills an unattested row.

STATISTICS ARE SHARED, NOT REIMPLEMENTED (dispatch W14, R2/R3)
----------------------------------------------------------------
W13's reconciliation report found this module hand-rolling two things
`tools/prescreen_signal.py` already has shared, correct implementations of:
Spearman correlation with degenerate-input handling, and autocorrelation-
adjusted significance. Both are now imported rather than re-derived here:

  - IC: `performance.signal_statistics.spearman_correlation` (the same shared
    function `prescreen_signal.py` uses) replaces the direct `scipy.stats.
    spearmanr` calls. It returns `None` (never a fabricated 0.0/NaN) on a
    zero-variance input, so the old `nunique() < 2` / `np.isnan(ic)` guards
    are no longer needed and are removed.
  - Significance: `prescreen_signal._block_adjusted_significance` (the same
    Fisher-z, block-24 estimator every 1h prescreen decision in this campaign
    is gated on — `_BLOCK_SIZE_1H = 24`) replaces the raw, unadjusted p-value
    scipy returns. This is a DEFECT FIX, not a style change: an unadjusted
    p-value on autocorrelated 1h bars is anti-conservative (it understates the
    true p, i.e. overstates significance) precisely because it treats every
    bar as an independent draw. The frozen feature parameters
    (`features.bar_seconds: 3600`) are 1h, matching prescreen's own
    `_BLOCK_SIZE_1H` convention, so the same block size applies here.
    `alpha_corrected` — the prereg's own registered Bonferroni threshold — is
    still what a feature is compared against; only the p-value ESTIMATOR
    changes, and only in the conservative direction.

Nothing about the gates, thresholds, or verdict mapping this module enforces
changes as a result — see `gate_rule` in `prereg_whale_footprint_v2.yaml` and
`verdict.mapping` there, both untouched. R4 (routing this harness's IC
computation itself through `prescreen_signal.py`'s forecast-extraction path)
was REJECTED by the director: the pre-registration's hypothesis is univariate
on the raw feature column, while `prescreen_signal.py::_extract_forecasts`
computes a strategy FORECAST — a different, gated subset of the same feature.
Only the two statistics primitives are shared; the evaluation path is not.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import yaml

# ---------------------------------------------------------------------------
# Shared statistics imports (W14 R2/R3, repointed 2026-09-12 -- E-039 step 5).
# Both functions now live in trading-bot/performance/signal_statistics.py,
# the single shared home for this class of function -- prescreen_signal.py
# is being removed (E-039), these are no longer sourced from it.
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent          # strategy-research/tools/
_REPO = _HERE.parent.parent                       # repo root
_TBOT = _REPO / "trading-bot"                     # trading-bot/

for _p in (str(_HERE), str(_TBOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from performance.signal_statistics import spearman_correlation as _spearman  # noqa: E402
from performance.signal_statistics import (  # noqa: E402
    pooled_block_adjusted_significance as _block_adjusted_significance,
)
from timeframe import bars_per_day  # noqa: E402  (sibling module in tools/)

_BLOCK_SIZE_1H = bars_per_day("1h")  # was prescreen_signal._BLOCK_SIZE_1H (=24), now derived

MIN_BARS_FOR_PER_PAIR_SIGN = 30  # prereg verdict.sign_consistency: pairs below this are not meaningfully signed


@dataclass
class EvaluationResult:
    status: str  # "BLOCKED_SINGLE_USE" | "BLOCKED_ECONOMIC_INFEASIBILITY" |
                 # "BLOCKED_COVERAGE_FLOOR" | "BLOCKED_MIN_N" | "VERDICT"
    verdict: Optional[str] = None  # "PASS" | "UNSTABLE" | "NULL", only when status == "VERDICT"
    detail: Dict[str, Any] = field(default_factory=dict)


def load_prereg(path: Path) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _consumption_path(prereg_path: Path) -> Path:
    return prereg_path.with_suffix(prereg_path.suffix + ".consumed.json")


def _read_consumption(prereg_path: Path) -> Optional[Dict[str, Any]]:
    """Consumption state lives in a SIDECAR file next to the frozen prereg,
    never as a mutation of the YAML's thresholds — the pre-registration's
    (a)-(h) content must stay byte-identical for the life of the hypothesis;
    only the sidecar changes on execution."""
    p = _consumption_path(prereg_path)
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _write_consumption(prereg_path: Path, run_id: str, hypothesis_id: str) -> None:
    p = _consumption_path(prereg_path)
    p.write_text(json.dumps({
        "hypothesis_id": hypothesis_id, "run_id": run_id,
        "consumed_at": pd.Timestamp.utcnow().isoformat(),
    }, indent=2), encoding="utf-8")


def _pooled_attested(panels: Dict[str, pd.DataFrame], column: str) -> pd.DataFrame:
    frames = []
    for pair, df in panels.items():
        sub = df[df["attested"].astype(bool)][[column, "target"]].dropna()
        if sub.empty:
            continue
        sub = sub.assign(pair=pair)
        frames.append(sub)
    if not frames:
        return pd.DataFrame(columns=[column, "target", "pair"])
    return pd.concat(frames, ignore_index=True)


def _attestation_fraction(panels: Dict[str, pd.DataFrame]) -> float:
    total = sum(len(df) for df in panels.values())
    attested = sum(int(df["attested"].astype(bool).sum()) for df in panels.values())
    return (attested / total) if total > 0 else 0.0


def _attested_bars_per_pair_avg(panels: Dict[str, pd.DataFrame]) -> float:
    counts = [int(df["attested"].astype(bool).sum()) for df in panels.values()]
    return float(np.mean(counts)) if counts else 0.0


def _sign_consistency(panels: Dict[str, pd.DataFrame], column: str,
                       pooled_sign: int, floor: float = 0.80) -> Dict[str, Any]:
    per_pair_signs = []
    for pair, df in panels.items():
        sub = df[df["attested"].astype(bool)][[column, "target"]].dropna()
        if len(sub) < MIN_BARS_FOR_PER_PAIR_SIGN:
            continue
        # _spearman (performance.signal_statistics.spearman_correlation)
        # returns None -- never a fabricated 0.0/NaN -- on a zero-variance
        # input, which is what the removed nunique()<2 guards existed to
        # detect; the shared function already makes that case unreachable.
        ic = _spearman(sub[column].tolist(), sub["target"].tolist())
        if ic is None:
            continue
        per_pair_signs.append(np.sign(ic))
    if not per_pair_signs:
        return {"holds": False, "agree_fraction": 0.0, "n_pairs_signed": 0}
    agree = sum(1 for s in per_pair_signs if s == pooled_sign) / len(per_pair_signs)
    return {"holds": agree >= floor, "agree_fraction": agree, "n_pairs_signed": len(per_pair_signs)}


def _feature_verdict(panels: Dict[str, pd.DataFrame], column: str,
                      alpha_corrected: float, sign_floor: float) -> Dict[str, Any]:
    pooled = _pooled_attested(panels, column)
    n_attested = len(pooled)
    if n_attested < 3 or pooled[column].nunique() < 2 or pooled["target"].nunique() < 2:
        return {"feature": column, "verdict": "NULL", "ic": None, "p_value": None,
                "reason": "insufficient pooled data"}
    ic = _spearman(pooled[column].tolist(), pooled["target"].tolist())
    if ic is None:
        return {"feature": column, "verdict": "NULL", "ic": None, "p_value": None,
                "reason": "degenerate pooled correlation (zero variance)"}
    # W14 R3: block-24 Fisher-z significance (the same estimator every 1h
    # prescreen decision in this campaign is gated on), NOT the raw scipy
    # p-value -- see the module docstring "STATISTICS ARE SHARED" section.
    # ic_values=[ic] (a single pooled estimate, not multiple window ICs to
    # average) is exactly how prescreen_signal.py itself calls this when it
    # has one pooled IC (run_prescreen: `ic_values_for_sig = [ic_active]`).
    significance = _block_adjusted_significance([ic], n_attested, block_size=_BLOCK_SIZE_1H)
    p_value = significance["p_value"]
    # alpha_corrected is the PREREG's own registered Bonferroni threshold --
    # deliberately NOT prescreen_signal._SIG_THRESHOLD, which is that module's
    # own unrelated routing constant.
    clears = bool(p_value < alpha_corrected)
    if not clears:
        return {"feature": column, "verdict": "NULL", "ic": float(ic), "p_value": float(p_value),
                "significance": significance}
    sc = _sign_consistency(panels, column, int(np.sign(ic)), floor=sign_floor)
    verdict = "PASS" if sc["holds"] else "UNSTABLE"
    return {"feature": column, "verdict": verdict, "ic": float(ic), "p_value": float(p_value),
            "sign_consistency": sc, "significance": significance}


def evaluate(
    prereg: Dict[str, Any],
    panels: Dict[str, pd.DataFrame],
    *,
    prereg_path: Optional[Path] = None,
    run_id: str = "unspecified_run",
    hypothesis_id: str = "whale_footprint_v2",
    force_ignore_consumption: bool = False,
) -> EvaluationResult:
    # 1. single-use
    if prereg_path is not None and not force_ignore_consumption:
        consumed = _read_consumption(prereg_path)
        if prereg.get("single_use", {}).get("fires_exactly_once") and consumed is not None:
            return EvaluationResult(status="BLOCKED_SINGLE_USE", detail={"consumed_by": consumed})

    # 2. economic feasibility -- data-independent, checked before any panel
    # is touched. See module docstring.
    econ = prereg.get("economic_ic_threshold") or {}
    if econ.get("economically_untradeable_at_registered_frequency"):
        return EvaluationResult(
            status="BLOCKED_ECONOMIC_INFEASIBILITY",
            detail={
                "required_ic_at_registered_frequency": econ.get("required_ic_at_registered_frequency"),
                "max_possible_ic": 1.0,
                "finding": econ.get("finding"),
            },
        )

    # 3. coverage floor
    floor = prereg["required_coverage_floor"]["floor"]
    attested_fraction = _attestation_fraction(panels)
    if attested_fraction < floor:
        return EvaluationResult(
            status="BLOCKED_COVERAGE_FLOOR",
            detail={"attested_fraction": attested_fraction, "floor": floor},
        )

    # 4. minimum-N gate
    required_n = prereg["minimum_n_gate"]["required_attested_bars_per_pair"]
    avg_attested = _attested_bars_per_pair_avg(panels)
    if avg_attested < required_n:
        return EvaluationResult(
            status="BLOCKED_MIN_N",
            detail={"attested_bars_per_pair_avg": avg_attested, "required": required_n},
        )

    # 5. mechanical verdict per feature, then the (g) TOTAL mapping
    alpha_corrected = prereg["test_statistic"]["multiple_comparison_correction"]["alpha_corrected"]
    sign_floor = 0.80  # frozen in prereg verdict.sign_consistency; not a tunable input
    feature_names: List[str] = prereg["features"]["names"]
    per_feature = [_feature_verdict(panels, name, alpha_corrected, sign_floor) for name in feature_names]

    if any(f["verdict"] == "PASS" for f in per_feature):
        total = "PASS"
    elif any(f["verdict"] == "UNSTABLE" for f in per_feature):
        total = "UNSTABLE"
    else:
        total = "NULL"

    if prereg_path is not None and not force_ignore_consumption:
        _write_consumption(prereg_path, run_id=run_id, hypothesis_id=hypothesis_id)

    return EvaluationResult(
        status="VERDICT", verdict=total,
        detail={"per_feature": per_feature, "attested_fraction": attested_fraction,
                "attested_bars_per_pair_avg": avg_attested},
    )


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prereg", required=True, type=Path)
    ap.add_argument("--run-id", default="manual_run")
    args = ap.parse_args(argv)
    raise SystemExit(
        "This harness takes real per-pair feature/target panels as a Python "
        "call (see `evaluate()`), not a CLI data source — there is deliberately "
        "no flag here that points at trading-bot/local_data/recorded_reserved/. "
        "Wire a caller that reads the released whale-feature cache explicitly "
        "once a designation exists; do not add one here as a matter of convenience."
    )


if __name__ == "__main__":
    raise SystemExit(main())
