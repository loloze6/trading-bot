"""
validate_regime_detector.py — Standalone, deterministic regime detector validation.

Metrics computed (A2.2 additions marked):
  - regime_persistence_median_bars
  - transition_frequency_per_window
  - parameter_sensitivity (all-bars; retained but CANNOT upgrade confidence for rare labels)
  - [A2.2] class_conditional_sensitivity_per_label: for each label, fraction of its own
    bars that change label under ±10% perturbation, plus relative population change.
    Used as the gate metric whenever activation_rate < 0.10 (rare label).
  - trending_activation_rate (first-class metric; must be in plausibility band)
  - [A2.2] activation_band_check: whether activation is within [BAND_MIN, BAND_MAX]
  - zero_trade_slot_pct

Confidence rules (A2.2 revised):
  Gate sensitivity used:
    - activation_rate < 0.10 (rare label) → class_conditional_sensitivity (TRENDING)
    - activation_rate >= 0.10             → all_bars parameter_sensitivity
  Activation band cap: activation outside [BAND_MIN, BAND_MAX] → confidence capped at medium.
  high:   persistence>=24 AND transitions/window<=4 AND gate_sensitivity<=0.15
          AND activation_rate in [BAND_MIN, BAND_MAX]
  medium: persistence>=12 AND gate_sensitivity<=0.25
  low:    otherwise

Retune firewall: detector parameters may ONLY be tuned against intrinsic criteria
(persistence, class-conditional stability, activation-within-band). Strategy PnL,
Sharpe, IC, or any backtest output must never appear in retune acceptance.

Output: campaign-level `regime_detector_report.yaml` (root of strategy-research/).

CLI:
  python strategy-research/tools/validate_regime_detector.py
  python strategy-research/tools/validate_regime_detector.py --config <path/to/strategy_config.json>
  python strategy-research/tools/validate_regime_detector.py --start 2024-01-01 --end 2025-12-31
"""

import sys, os, json, copy, argparse, statistics
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_SR = os.path.dirname(_HERE)
_REPO = os.path.dirname(_SR)
_TBOT = os.path.join(_REPO, "trading-bot")
if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

import pandas as pd
import yaml

from data.data_manager import DataManager
from strategies.regime_engine import ConfigDrivenRegimeEngine
from strategies.strategy_base import MarketRegime


# ---------------------------------------------------------------------------
# Campaign defaults
# ---------------------------------------------------------------------------

_DEFAULT_CONFIG = os.path.join(
    _SR, "runs", "run_033", "artifacts", "candidate_strategy_config.json"
)
_DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT"]
_DEFAULT_TIMEFRAME = "1h"
_DEFAULT_START = "2024-01-01"
_DEFAULT_END = "2025-12-31"  # walk-forward range only, never holdout
_OUTPUT_PATH = os.path.join(_SR, "regime_detector_report.yaml")

# Zero-trade slots from Keltner v2 re-run (Improvement 07 A2.1 seed)
_V2_ZERO_TRADE_MONTHS = {
    "BTCUSDT": [
        "2024-01",
        "2024-09",
        "2024-10",
        "2024-12",
        "2025-03",
        "2025-04",
        "2025-05",
        "2025-09",
        "2025-12",
    ],
    "ETHUSDT": ["2024-01", "2024-03", "2024-11", "2024-12", "2025-02"],
}

# Confidence thresholds
_HIGH_PERSISTENCE = 24
_HIGH_TRANSITIONS = 4
_HIGH_SENSITIVITY = (
    0.15  # gate sensitivity (class-conditional or all-bars per A2.2 rule)
)
_MEDIUM_PERSISTENCE = 12
_MEDIUM_SENSITIVITY = 0.25

# A2.2: activation plausibility band for a trend label on 1h crypto
ACTIVATION_BAND_MIN = 0.10  # 10%
ACTIVATION_BAND_MAX = 0.40  # 40%
RARE_LABEL_THRESHOLD = 0.10  # use class-conditional when activation < this


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _config_hash(detector_cfg: dict) -> str:
    canonical = json.dumps(detector_cfg, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode()).hexdigest()[:8]


def _perturb_thresholds(detector_cfg: dict, factor: float) -> dict:
    """Deep-copy of detector config with all rule threshold values scaled by factor."""
    cfg = copy.deepcopy(detector_cfg)
    for rule in cfg.get("rules", []):
        for cond_set in rule.get("any_of", []):
            for cond in cond_set:
                if "value" in cond:
                    cond["value"] = cond["value"] * factor
                if "low" in cond:
                    cond["low"] = cond["low"] * factor
                if "high" in cond:
                    cond["high"] = cond["high"] * factor
    return cfg


def _run_detector(detector_cfg: dict, bars_df: pd.DataFrame):
    """
    Feed bars one by one to a fresh ConfigDrivenRegimeEngine.
    Returns list of (timestamp, regime_str) for every ready bar.
    """
    engine = ConfigDrivenRegimeEngine(detector_cfg)
    labels = []
    for i in range(1, len(bars_df) + 1):
        window = bars_df.iloc[:i]
        engine.update(window)
        if engine.is_ready():
            regime, _ = engine.classify()
            ts = bars_df.iloc[i - 1]["timestamp"]
            labels.append((ts, regime.value))
    return labels


def _compute_persistence(labels):
    """Median run length in bars for consecutive same-regime segments."""
    if not labels:
        return 0.0
    runs, current, run_len = [], labels[0][1], 1
    for _, regime in labels[1:]:
        if regime == current:
            run_len += 1
        else:
            runs.append(run_len)
            current, run_len = regime, 1
    runs.append(run_len)
    return statistics.median(runs) if runs else 0.0


def _compute_transition_frequency(labels, bars_per_window: int = 720):
    """Mean regime transitions per bars_per_window (~30 days at 1h)."""
    if not labels:
        return 0.0
    windows, transitions = [], 0
    for i in range(1, len(labels)):
        if labels[i][1] != labels[i - 1][1]:
            transitions += 1
        if i % bars_per_window == 0:
            windows.append(transitions)
            transitions = 0
    return statistics.mean(windows) if windows else float(transitions)


def _compute_all_bars_sensitivity(labels_orig, labels_perturbed):
    """Fraction of ALL bars where the label differs (all-bars figure)."""
    n = min(len(labels_orig), len(labels_perturbed))
    if n == 0:
        return 0.0
    diffs = sum(1 for i in range(n) if labels_orig[i][1] != labels_perturbed[i][1])
    return diffs / n


def _compute_class_conditional_sensitivity(
    labels_orig, labels_perturbed, label_name: str
) -> dict:
    """
    A2.2: for bars carrying `label_name` at baseline, compute:
      - class_conditional_sensitivity: fraction that lose that label under perturbation
      - relative_population_change: (perturbed_count - baseline_count) / baseline_count
    Returns None if the label never appears at baseline.
    """
    n = min(len(labels_orig), len(labels_perturbed))
    baseline_indices = [i for i in range(n) if labels_orig[i][1] == label_name]
    baseline_count = len(baseline_indices)

    if baseline_count == 0:
        return None

    lost = sum(1 for i in baseline_indices if labels_perturbed[i][1] != label_name)
    perturbed_total_count = sum(1 for _, r in labels_perturbed[:n] if r == label_name)

    return {
        "baseline_count": baseline_count,
        "lost_count": lost,
        "class_conditional_sensitivity": round(lost / baseline_count, 4),
        "perturbed_count": perturbed_total_count,
        "relative_population_change": round(
            (perturbed_total_count - baseline_count) / baseline_count, 4
        ),
    }


def _compute_per_label_class_conditional(labels_orig, labels_down, labels_up):
    """
    A2.2: compute class-conditional sensitivity for every label that appears at baseline.
    Returns dict keyed by label_name, value = worst-case (max) across both perturbation directions.
    """
    all_labels = {r for _, r in labels_orig}
    result = {}
    for label in all_labels:
        down_stats = _compute_class_conditional_sensitivity(
            labels_orig, labels_down, label
        )
        up_stats = _compute_class_conditional_sensitivity(labels_orig, labels_up, label)
        if down_stats is None and up_stats is None:
            continue
        # worst-case direction = highest class-conditional sensitivity
        if down_stats is None:
            worst = up_stats
            direction = "up"
        elif up_stats is None:
            worst = down_stats
            direction = "down"
        elif (
            down_stats["class_conditional_sensitivity"]
            >= up_stats["class_conditional_sensitivity"]
        ):
            worst = down_stats
            direction = "down"
        else:
            worst = up_stats
            direction = "up"
        result[label] = {
            "baseline_count": worst["baseline_count"],
            "class_conditional_sensitivity": worst["class_conditional_sensitivity"],
            "worst_case_direction": direction,
            "relative_population_change": worst["relative_population_change"],
            "down": down_stats,
            "up": up_stats,
        }
    return result


def _monthly_activation(labels):
    """
    Returns: activation_rate, zero_slot_pct, month_fired dict.
    """
    monthly = defaultdict(list)
    for ts, regime in labels:
        month_key = ts.strftime("%Y-%m") if hasattr(ts, "strftime") else str(ts)[:7]
        monthly[month_key].append(regime)

    trending_total = sum(1 for _, r in labels if r == "trending")
    activation_rate = trending_total / len(labels) if labels else 0.0
    month_fired = {m: any(r == "trending" for r in rs) for m, rs in monthly.items()}
    zero_slot_pct = (
        sum(1 for f in month_fired.values() if not f) / len(month_fired)
        if month_fired
        else 0.0
    )

    return activation_rate, zero_slot_pct, month_fired


def _assign_confidence(
    persistence,
    transitions_per_window,
    all_bars_sensitivity,
    activation_rate,
    class_cond_sens_trending,
    band_min=ACTIVATION_BAND_MIN,
    band_max=ACTIVATION_BAND_MAX,
):
    """
    A2.2 revised confidence rule.
    Gate sensitivity: class-conditional for rare labels (activation < RARE_LABEL_THRESHOLD),
    all-bars otherwise. All-bars figure is RETAINED but CANNOT upgrade confidence.
    Activation outside band caps confidence at medium.
    """
    rare = activation_rate < RARE_LABEL_THRESHOLD
    if rare and class_cond_sens_trending is not None:
        gate_sens = class_cond_sens_trending
        sens_label = f"class_cond_sensitivity(TRENDING)={gate_sens:.3f} [rare label: activation={100 * activation_rate:.2f}%<10%]"
    else:
        gate_sens = all_bars_sensitivity
        sens_label = f"all_bars_sensitivity={gate_sens:.3f}"

    in_band = band_min <= activation_rate <= band_max
    band_note = f"activation={100 * activation_rate:.2f}% in [{100 * band_min:.0f}%,{100 * band_max:.0f}%]"
    band_fail_note = f"activation={100 * activation_rate:.2f}% outside [{100 * band_min:.0f}%,{100 * band_max:.0f}%] (cap: medium)"

    # High requires: persistence, transitions, gate_sensitivity, AND activation in band
    if (
        persistence >= _HIGH_PERSISTENCE
        and transitions_per_window <= _HIGH_TRANSITIONS
        and gate_sens <= _HIGH_SENSITIVITY
        and in_band
    ):
        return "high", (
            f"persistence={persistence:.1f}>=24, transitions={transitions_per_window:.1f}<=4, "
            f"{sens_label}<=0.15, {band_note}"
        )

    # Medium: minimum persistence and gate sensitivity pass
    if persistence >= _MEDIUM_PERSISTENCE and gate_sens <= _MEDIUM_SENSITIVITY:
        blockers = []
        if persistence < _HIGH_PERSISTENCE:
            blockers.append(f"persistence={persistence:.1f}<24")
        if transitions_per_window > _HIGH_TRANSITIONS:
            blockers.append(f"transitions={transitions_per_window:.1f}>4")
        if gate_sens > _HIGH_SENSITIVITY:
            blockers.append(f"{sens_label}>0.15")
        if not in_band:
            blockers.append(band_fail_note)
        return "medium", (
            f"persistence={persistence:.1f}>=12, {sens_label}<=0.25 "
            f"but fails high gate: {'; '.join(blockers)}"
        )

    # Low
    reasons = []
    if persistence < _MEDIUM_PERSISTENCE:
        reasons.append(f"persistence={persistence:.1f}<12")
    if gate_sens > _MEDIUM_SENSITIVITY:
        reasons.append(f"{sens_label}>0.25")
    return "low", "; ".join(reasons) if reasons else "unknown"


def _known_weak_periods(symbol: str, month_fired: dict) -> list:
    seed = set(_V2_ZERO_TRADE_MONTHS.get(symbol, []))
    computed_zero = {m for m, fired in month_fired.items() if not fired}
    return sorted(seed | computed_zero)


# ---------------------------------------------------------------------------
# Main validation function
# ---------------------------------------------------------------------------


def validate(config_path: str, symbols: list, start: str, end: str) -> dict:
    with open(config_path, encoding="utf-8") as f:
        strategy_cfg = json.load(f)

    detector_cfg = strategy_cfg.get("regime_detector")
    if not detector_cfg:
        raise ValueError(f"No 'regime_detector' key in {config_path}")

    det_hash = _config_hash(detector_cfg)
    cfg_down = _perturb_thresholds(detector_cfg, 0.90)
    cfg_up = _perturb_thresholds(detector_cfg, 1.10)

    per_symbol = []
    for symbol in symbols:
        print(f"  {symbol} {start} to {end} ...", end=" ", flush=True)
        dm = DataManager(symbols=[symbol], interval_seconds=3600, mode="backtest")
        df = dm.fetch_historical_data(symbol, start, end)
        if df.empty:
            print("NO DATA -- skipping")
            continue
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)

        labels_orig = _run_detector(detector_cfg, df)
        labels_down = _run_detector(cfg_down, df)
        labels_up = _run_detector(cfg_up, df)

        # All-bars metrics
        persistence = _compute_persistence(labels_orig)
        transitions_pw = _compute_transition_frequency(labels_orig)
        all_bars_sens = max(
            _compute_all_bars_sensitivity(labels_orig, labels_down),
            _compute_all_bars_sensitivity(labels_orig, labels_up),
        )

        # A2.2: class-conditional sensitivity per label
        per_label_cc = _compute_per_label_class_conditional(
            labels_orig, labels_down, labels_up
        )
        cc_trending = (per_label_cc.get("trending") or {}).get(
            "class_conditional_sensitivity"
        )

        # Activation
        activation_rate, zero_slot_pct, month_fired = _monthly_activation(labels_orig)
        in_band = ACTIVATION_BAND_MIN <= activation_rate <= ACTIVATION_BAND_MAX

        confidence, rationale = _assign_confidence(
            persistence,
            transitions_pw,
            all_bars_sens,
            activation_rate,
            cc_trending,
        )
        weak_periods = _known_weak_periods(symbol, month_fired)

        # Summary line
        cc_str = f"{cc_trending:.3f}" if cc_trending is not None else "n/a"
        print(
            f"confidence={confidence}  persistence={persistence:.1f}  "
            f"all_bars_sens={all_bars_sens:.3f}  cc_trending={cc_str}  "
            f"activation={100 * activation_rate:.2f}%  in_band={in_band}  zero_slots={100 * zero_slot_pct:.0f}%"
        )

        per_symbol.append(
            {
                "symbol": symbol,
                "timeframe": "1h",
                "metrics": {
                    "regime_persistence_median_bars": round(persistence, 2),
                    "transition_frequency_per_window": round(transitions_pw, 2),
                    # All-bars figure — retained but CANNOT upgrade confidence for rare labels
                    "parameter_sensitivity": round(all_bars_sens, 4),
                    "trending_activation_rate": round(activation_rate, 4),
                    "zero_trade_slot_pct": round(zero_slot_pct, 4),
                    "agreement_with_reference_labels": None,
                    # A2.2 additions
                    "class_conditional_sensitivity_per_label": {
                        label: {
                            "baseline_count": v["baseline_count"],
                            "class_conditional_sensitivity": v[
                                "class_conditional_sensitivity"
                            ],
                            "worst_case_direction": v["worst_case_direction"],
                            "relative_population_change": v[
                                "relative_population_change"
                            ],
                        }
                        for label, v in per_label_cc.items()
                    },
                    "activation_band_check": {
                        "within_band": in_band,
                        "band_min": ACTIVATION_BAND_MIN,
                        "band_max": ACTIVATION_BAND_MAX,
                        "rare_label_threshold": RARE_LABEL_THRESHOLD,
                        "gate_metric_used": "class_conditional"
                        if (
                            activation_rate < RARE_LABEL_THRESHOLD
                            and cc_trending is not None
                        )
                        else "all_bars",
                    },
                },
                "confidence": confidence,
                "confidence_rationale": rationale,
                "known_weak_periods": weak_periods,
            }
        )

    return {
        "detector_version": det_hash,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "data_range": {"start": start, "end": end},
        "config_source": config_path,
        "per_symbol_per_timeframe": per_symbol,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Validate regime detector standalone.")
    parser.add_argument("--config", default=_DEFAULT_CONFIG)
    parser.add_argument("--symbols", nargs="+", default=_DEFAULT_SYMBOLS)
    parser.add_argument("--start", default=_DEFAULT_START)
    parser.add_argument("--end", default=_DEFAULT_END)
    parser.add_argument("--out", default=_OUTPUT_PATH)
    args = parser.parse_args()

    policy_path = os.path.join(_SR, "config", "campaign_data_policy.yaml")
    if os.path.exists(policy_path):
        with open(policy_path, encoding="utf-8") as f:
            policy = yaml.safe_load(f)
        holdout_start = policy.get("holdout_range", [None, None])[0]
        if holdout_start and args.end >= holdout_start:
            print(
                f"WARNING: --end {args.end} >= holdout_start {holdout_start}. Clamping."
            )
            args.end = holdout_start

    print(f"Regime detector validation: {args.symbols} {args.start} to {args.end}")
    print(f"Config: {args.config}")
    print()

    report = validate(args.config, args.symbols, args.start, args.end)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(
            report, f, allow_unicode=True, sort_keys=False, default_flow_style=False
        )

    print(f"\nWrote: {out_path}")
    print("Summary:")
    for e in report["per_symbol_per_timeframe"]:
        m = e["metrics"]
        cc = (m.get("class_conditional_sensitivity_per_label") or {}).get(
            "trending"
        ) or {}
        ab = m.get("activation_band_check") or {}
        print(
            f"  {e['symbol']}: {e['confidence']}  "
            f"activation={100 * m['trending_activation_rate']:.2f}%  "
            f"in_band={ab.get('within_band')}  "
            f"cc_sensitivity(TRENDING)={cc.get('class_conditional_sensitivity', 'n/a')}  "
            f"rel_pop_change={cc.get('relative_population_change', 'n/a')}"
        )


if __name__ == "__main__":
    main()
