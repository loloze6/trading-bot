"""
retune_regime_detector.py — One-shot grid search over (ER_enter, ER_exit, min_dwell).

Scoring is exclusively on the four intrinsic criteria:
  1. persistence  >= 24 bars               (2 pts if >=24, 1 pt if >=12)
  2. activation   in [10%, 40%]            (2 pts if in band)
  3. class-conditional sensitivity <0.15   (2 pts if <0.15, 1 pt if <0.25)
  4. transition frequency <= 4/window      (2 pts if <=4, 1 pt if <=8)

Max score = 8.  Ties broken by persistence desc, then cc_sensitivity asc.

Grid:
  ER_enter ∈ {0.20, 0.25, 0.30, 0.35, 0.40, 0.45}
  ER_exit_ratio ∈ {1.00, 0.80}   (exit = enter × ratio; 1.0 = no hysteresis)
  min_dwell ∈ {1, 6, 12, 24}     bars

VR component DROPPED from this grid: with VR>=1.2, max achievable activation on
1h BTC/ETH is ~1%, which is structurally outside the [10%,40%] band. The retune
tests ER-only rules. If the winner requires dwell>1 or hysteresis, a note is
appended to the output about detector extension needed.

CLI:
  python strategy-research/tools/retune_regime_detector.py
  python strategy-research/tools/retune_regime_detector.py --start 2024-01-01 --end 2025-12-31
"""
import sys, os, json, math, statistics, subprocess
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
_SR   = os.path.dirname(_HERE)
_REPO = os.path.dirname(_SR)
_TBOT = os.path.join(_REPO, "trading-bot")
if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

from data.data_manager import DataManager

# Reuse metric helpers from validate_regime_detector
sys.path.insert(0, _HERE)
from validate_regime_detector import (
    _compute_persistence,
    _compute_transition_frequency,
    _compute_class_conditional_sensitivity,
    _monthly_activation,
    ACTIVATION_BAND_MIN, ACTIVATION_BAND_MAX,
)


def _resolve_tbot_python() -> Path:
    """Absolute path to the trading-bot venv interpreter, anchored at the repo root.

    Windows layout is tried first so an upstream checkout resolves to exactly the
    interpreter it always has. A candidate must also be executable: this repo has
    upstream's Windows venv committed, so venv/Scripts/python.exe exists on macOS
    too but cannot run there. Anchored at _REPO rather than CWD-relative because
    this script is documented as run from the repo root yet passes cwd=_SR to the
    subprocess, so only the child ever resolved the old relative path correctly.
    No usable candidate raises rather than falling back to sys.executable — a
    silently wrong interpreter is the worst outcome here.
    """
    candidates = (
        Path(_REPO) / "venv" / "Scripts" / "python.exe",
        Path(_REPO) / ".venv" / "bin" / "python",
    )
    for candidate in candidates:
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate
    raise RuntimeError(
        "No runnable trading-bot interpreter. Tried: "
        + ", ".join(str(c) for c in candidates)
    )


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
_DEFAULT_SYMBOLS   = ["BTCUSDT", "ETHUSDT"]
_DEFAULT_START     = "2024-01-01"
_DEFAULT_END       = "2025-12-31"
_ER_PERIOD         = 24
_ER_SMOOTH         = 5
_BARS_PER_WINDOW   = 720   # 30 days × 24 bars/day

_HIGH_PERSISTENCE   = 24
_HIGH_TRANSITIONS   = 4.0
_HIGH_CC_SENS       = 0.15
_MEDIUM_PERSISTENCE = 12
_MEDIUM_CC_SENS     = 0.25

_GRID_ER_ENTER   = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45]
_GRID_EXIT_RATIO = [1.00, 0.80]   # ER_exit = ER_enter × ratio
_GRID_MIN_DWELL  = [1, 6, 12, 24]

_WINNER_CONFIG_PATH = Path(_SR) / "config" / "regime_retune_winner.json"
_RETUNE_RESULTS_PATH = Path(_SR) / "regime_retune_results.yaml"


# ---------------------------------------------------------------------------
# ER computation (matches EfficiencyRatioRegimeComponent)
# ---------------------------------------------------------------------------

def _compute_er_series(close: pd.Series, period: int = _ER_PERIOD,
                       smooth: int = _ER_SMOOTH) -> pd.Series:
    """Efficiency Ratio: |net move| / zigzag over `period` bars, smoothed."""
    directional = close.diff(period).abs()
    zigzag = close.diff().abs().rolling(period).sum()
    er_raw = directional / zigzag.replace(0, float("nan"))
    return er_raw.rolling(smooth).mean()


# ---------------------------------------------------------------------------
# Stateful classifier with hysteresis + min-dwell
# ---------------------------------------------------------------------------

def _classify_stateful(er_series: pd.Series, timestamps: pd.Series,
                       er_enter: float, er_exit: float, min_dwell: int):
    """
    Stateful regime labels as list of (timestamp, regime_str).

    Hysteresis: enter 'trending' when ER >= er_enter, exit when ER < er_exit.
    Min-dwell: once a regime is entered, stay for at least min_dwell bars before
    switching.
    """
    labels = []
    regime = "unknown"
    bars_in_regime = min_dwell  # allow immediate switch from initial state

    for ts, er_val in zip(timestamps, er_series):
        if pd.isna(er_val):
            # Warmup period — no ER available
            labels.append((ts, "unknown"))
            continue

        # Hysteresis-based candidate
        if regime == "trending":
            candidate = "trending" if er_val >= er_exit else "unknown"
        else:
            candidate = "trending" if er_val >= er_enter else "unknown"

        # Min-dwell guard: can only switch if we've served the minimum
        if candidate != regime and bars_in_regime < min_dwell:
            candidate = regime

        if candidate != regime:
            regime = candidate
            bars_in_regime = 1
        else:
            bars_in_regime += 1

        labels.append((ts, regime))

    return labels


def _classify_with_perturbed_threshold(er_series: pd.Series, timestamps: pd.Series,
                                       er_enter: float, er_exit: float,
                                       min_dwell: int, factor: float):
    """Classify with er_enter and er_exit scaled by `factor` (e.g. 0.90 or 1.10)."""
    return _classify_stateful(er_series, timestamps,
                              er_enter * factor, er_exit * factor, min_dwell)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _score(persistence, transitions, cc_sens, activation):
    """
    Score on four intrinsic criteria only. Max = 8.
    cc_sens: class-conditional sensitivity for TRENDING (None if label absent)
    """
    score = 0.0
    breakdown = {}

    # 1. Persistence
    if persistence >= _HIGH_PERSISTENCE:
        score += 2.0; breakdown["persistence"] = "HIGH"
    elif persistence >= _MEDIUM_PERSISTENCE:
        score += 1.0; breakdown["persistence"] = "MEDIUM"
    else:
        breakdown["persistence"] = "LOW"

    # 2. Activation in band
    if ACTIVATION_BAND_MIN <= activation <= ACTIVATION_BAND_MAX:
        score += 2.0; breakdown["activation"] = "IN_BAND"
    elif activation > ACTIVATION_BAND_MAX:
        breakdown["activation"] = "OVER_BAND"
    else:
        breakdown["activation"] = "UNDER_BAND"

    # 3. Class-conditional sensitivity
    if cc_sens is None:
        breakdown["cc_sens"] = "NO_TRENDING"  # label never fires — worst case
    elif cc_sens < _HIGH_CC_SENS:
        score += 2.0; breakdown["cc_sens"] = "HIGH"
    elif cc_sens < _MEDIUM_CC_SENS:
        score += 1.0; breakdown["cc_sens"] = "MEDIUM"
    else:
        breakdown["cc_sens"] = "LOW"

    # 4. Transition frequency
    if transitions <= _HIGH_TRANSITIONS:
        score += 2.0; breakdown["transitions"] = "HIGH"
    elif transitions <= 8.0:
        score += 1.0; breakdown["transitions"] = "MEDIUM"
    else:
        breakdown["transitions"] = "LOW"

    return score, breakdown


# ---------------------------------------------------------------------------
# Per-symbol evaluation
# ---------------------------------------------------------------------------

def _eval_symbol(symbol: str, df: pd.DataFrame):
    """Load ER series for a symbol. Returns (er_series, timestamps)."""
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    er = _compute_er_series(df["close"])
    return er, df["timestamp"]


def _eval_cell(er: pd.Series, timestamps: pd.Series,
               er_enter: float, er_exit_ratio: float, min_dwell: int) -> dict:
    """Evaluate one grid cell for one symbol. Returns metric dict."""
    er_exit = er_enter * er_exit_ratio

    labels_orig = _classify_stateful(er, timestamps, er_enter, er_exit, min_dwell)
    labels_down = _classify_with_perturbed_threshold(er, timestamps, er_enter, er_exit, min_dwell, 0.90)
    labels_up   = _classify_with_perturbed_threshold(er, timestamps, er_enter, er_exit, min_dwell, 1.10)

    persistence    = _compute_persistence(labels_orig)
    transitions_pw = _compute_transition_frequency(labels_orig, _BARS_PER_WINDOW)

    # Class-conditional sensitivity for TRENDING (worst-case across ±10%)
    cc_down = _compute_class_conditional_sensitivity(labels_orig, labels_down, "trending")
    cc_up   = _compute_class_conditional_sensitivity(labels_orig, labels_up,   "trending")

    if cc_down is None and cc_up is None:
        cc_trending = None
        baseline_count = 0
    else:
        cc_trending = max(
            (cc_down["class_conditional_sensitivity"] if cc_down else 0.0),
            (cc_up["class_conditional_sensitivity"]   if cc_up   else 0.0),
        )
        baseline_count = (cc_down or cc_up)["baseline_count"]

    activation, zero_slot_pct, _ = _monthly_activation(labels_orig)
    score, breakdown = _score(persistence, transitions_pw, cc_trending, activation)

    return {
        "persistence":     round(persistence, 1),
        "transitions_pw":  round(transitions_pw, 2),
        "cc_sens":         round(cc_trending, 4) if cc_trending is not None else None,
        "activation":      round(activation, 4),
        "zero_slot_pct":   round(zero_slot_pct, 4),
        "baseline_count":  baseline_count,
        "score":           score,
        "breakdown":       breakdown,
    }


# ---------------------------------------------------------------------------
# Grid runner
# ---------------------------------------------------------------------------

def run_grid(symbols: list, start: str, end: str) -> list:
    """Run the full grid. Returns list of result dicts sorted by score desc."""
    # Load data once per symbol
    symbol_data = {}
    for sym in symbols:
        print(f"  Loading {sym} {start}–{end} ...", end=" ", flush=True)
        dm = DataManager(symbols=[sym], interval_seconds=3600, mode="backtest")
        df = dm.fetch_historical_data(sym, start, end)
        if df.empty:
            print("NO DATA — skipping")
            continue
        er, ts = _eval_symbol(sym, df)
        symbol_data[sym] = (er, ts)
        print(f"OK ({len(df):,} bars)")

    if not symbol_data:
        raise RuntimeError("No data loaded for any symbol")

    results = []
    n_cells = len(_GRID_ER_ENTER) * len(_GRID_EXIT_RATIO) * len(_GRID_MIN_DWELL)
    cell_idx = 0

    for er_enter in _GRID_ER_ENTER:
        for er_exit_ratio in _GRID_EXIT_RATIO:
            er_exit = er_enter * er_exit_ratio
            for min_dwell in _GRID_MIN_DWELL:
                cell_idx += 1
                # Average metrics across symbols
                sym_metrics = {}
                for sym, (er, ts) in symbol_data.items():
                    sym_metrics[sym] = _eval_cell(er, ts, er_enter, er_exit_ratio, min_dwell)

                # Combined score = min across symbols (conservative: all must pass)
                combined_score = min(m["score"] for m in sym_metrics.values())

                # Report aggregate metrics
                avg_persistence   = statistics.mean(m["persistence"]   for m in sym_metrics.values())
                avg_transitions   = statistics.mean(m["transitions_pw"] for m in sym_metrics.values())
                avg_activation    = statistics.mean(m["activation"]     for m in sym_metrics.values())
                cc_vals = [m["cc_sens"] for m in sym_metrics.values() if m["cc_sens"] is not None]
                avg_cc            = statistics.mean(cc_vals) if cc_vals else None

                is_directly_implementable = (min_dwell == 1 and er_exit_ratio == 1.00)

                record = {
                    "er_enter":              er_enter,
                    "er_exit":               round(er_exit, 3),
                    "er_exit_ratio":         er_exit_ratio,
                    "min_dwell":             min_dwell,
                    "combined_score":        combined_score,
                    "avg_persistence":       round(avg_persistence, 1),
                    "avg_transitions_pw":    round(avg_transitions, 2),
                    "avg_activation":        round(avg_activation, 4),
                    "avg_cc_sens":           round(avg_cc, 4) if avg_cc is not None else None,
                    "directly_implementable": is_directly_implementable,
                    "per_symbol":            sym_metrics,
                }
                results.append(record)

                # Progress line
                band_str = (f"{100*avg_activation:.1f}%"
                            + (" *" if ACTIVATION_BAND_MIN <= avg_activation <= ACTIVATION_BAND_MAX else ""))
                cc_str = f"{avg_cc:.3f}" if avg_cc is not None else "n/a"
                print(
                    f"  [{cell_idx:03d}/{n_cells}]  "
                    f"er={er_enter:.2f}  exit_ratio={er_exit_ratio:.2f}  dwell={min_dwell:2d}  "
                    f"score={combined_score:.1f}  persist={avg_persistence:.1f}  "
                    f"activ={band_str}  cc={cc_str}  trans={avg_transitions:.1f}"
                )

    # Sort: combined_score desc, then avg_persistence desc, then avg_cc asc
    def _sort_key(r):
        cc = r["avg_cc_sens"] if r["avg_cc_sens"] is not None else 1.0
        return (-r["combined_score"], -r["avg_persistence"], cc)

    results.sort(key=_sort_key)
    return results


# ---------------------------------------------------------------------------
# Winner config builder
# ---------------------------------------------------------------------------

def _build_winner_config(er_enter: float) -> dict:
    """
    Build a strategy config dict with an ER-only trending rule.
    Suitable for validate_regime_detector.py when min_dwell=1 and no hysteresis.
    """
    return {
        "regime_detector": {
            "mode": "threshold_rules",
            "components": [
                {
                    "id": "er",
                    "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent",
                    "params": {"period": _ER_PERIOD, "smooth_period": _ER_SMOOTH},
                }
            ],
            "rules": [
                {
                    "regime": "trending",
                    "any_of": [[{"id": "er", "op": "gte", "value": er_enter}]],
                }
            ],
            "default_regime": "unknown",
        }
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbols", nargs="+", default=_DEFAULT_SYMBOLS)
    parser.add_argument("--start",   default=_DEFAULT_START)
    parser.add_argument("--end",     default=_DEFAULT_END)
    parser.add_argument("--skip-validate", action="store_true",
                        help="Skip running validate_regime_detector.py after grid")
    args = parser.parse_args()

    print("=" * 70)
    print("REGIME DETECTOR RETUNE GRID")
    print(f"Symbols: {args.symbols}  Range: {args.start} to {args.end}")
    print(f"Grid: {len(_GRID_ER_ENTER)} ER_enter × {len(_GRID_EXIT_RATIO)} exit_ratios × "
          f"{len(_GRID_MIN_DWELL)} min_dwell = "
          f"{len(_GRID_ER_ENTER)*len(_GRID_EXIT_RATIO)*len(_GRID_MIN_DWELL)} cells")
    print("VR component: DROPPED (VR>=1.2 structurally limits activation to ~1%)")
    print("=" * 70)

    results = run_grid(args.symbols, args.start, args.end)

    print("\n" + "=" * 70)
    print("TOP 10 CELLS (sorted by combined_score desc, then persistence, cc_sens)")
    print("=" * 70)
    header = (f"{'er_in':>5} {'er_out':>6} {'dwell':>5}  "
              f"{'score':>5}  {'persist':>7}  {'activ%':>7}  "
              f"{'cc_sens':>7}  {'trans':>6}  {'direct':>6}")
    print(header)
    print("-" * len(header))
    for r in results[:10]:
        activ_pct = f"{100*r['avg_activation']:.1f}%"
        in_band_marker = "*" if ACTIVATION_BAND_MIN <= r["avg_activation"] <= ACTIVATION_BAND_MAX else " "
        cc_str = f"{r['avg_cc_sens']:.3f}" if r["avg_cc_sens"] is not None else "n/a  "
        direct_str = "YES" if r["directly_implementable"] else "no"
        print(
            f"{r['er_enter']:5.2f} {r['er_exit']:6.3f} {r['min_dwell']:5d}  "
            f"{r['combined_score']:5.1f}  {r['avg_persistence']:7.1f}  "
            f"{activ_pct + in_band_marker:>8}  {cc_str:>7}  "
            f"{r['avg_transitions_pw']:6.1f}  {direct_str:>6}"
        )

    winner = results[0]
    print("\n" + "=" * 70)
    print(f"WINNER: er_enter={winner['er_enter']:.2f}  er_exit={winner['er_exit']:.3f}  "
          f"min_dwell={winner['min_dwell']}")
    print(f"  Score={winner['combined_score']:.1f}/8  "
          f"Persistence={winner['avg_persistence']:.1f}  "
          f"Activation={100*winner['avg_activation']:.2f}%  "
          f"CC-sens={winner['avg_cc_sens']}  "
          f"Transitions={winner['avg_transitions_pw']:.1f}")
    print(f"  Directly implementable (no engine extension): "
          f"{'YES' if winner['directly_implementable'] else 'NO - requires min_dwell/hysteresis support'}")

    # Per-symbol breakdown for winner
    for sym, m in winner["per_symbol"].items():
        print(f"  {sym}: score={m['score']:.1f}  persist={m['persistence']}  "
              f"activ={100*m['activation']:.2f}%  cc={m['cc_sens']}  "
              f"trans={m['transitions_pw']}  breakdown={m['breakdown']}")

    # Write results YAML
    _RETUNE_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "symbols": args.symbols,
        "data_range": {"start": args.start, "end": args.end},
        "grid_dimensions": {
            "er_enter": _GRID_ER_ENTER,
            "er_exit_ratios": _GRID_EXIT_RATIO,
            "min_dwell": _GRID_MIN_DWELL,
        },
        "vr_dropped": True,
        "vr_drop_rationale": (
            "VR>=1.2 (canonical config) limits activation to ~1%, "
            "structurally outside [10%,40%] band. ER-only rules tested."
        ),
        "winner": {
            "er_enter": winner["er_enter"],
            "er_exit": winner["er_exit"],
            "er_exit_ratio": winner["er_exit_ratio"],
            "min_dwell": winner["min_dwell"],
            "combined_score": winner["combined_score"],
            "avg_persistence": winner["avg_persistence"],
            "avg_activation": winner["avg_activation"],
            "avg_cc_sens": winner["avg_cc_sens"],
            "avg_transitions_pw": winner["avg_transitions_pw"],
            "directly_implementable": winner["directly_implementable"],
            "requires_extension": not winner["directly_implementable"],
            "per_symbol": winner["per_symbol"],
        },
        "all_results": [
            {k: v for k, v in r.items() if k != "per_symbol"}
            for r in results
        ],
    }
    with open(_RETUNE_RESULTS_PATH, "w", encoding="utf-8") as f:
        yaml.dump(output, f, allow_unicode=True, sort_keys=False)
    print(f"\nWrote: {_RETUNE_RESULTS_PATH}")

    # -----------------------------------------------------------------------
    # Run validate_regime_detector.py with winner config
    # -----------------------------------------------------------------------
    if not args.skip_validate:
        # For validate_regime_detector.py, use the best DIRECTLY IMPLEMENTABLE cell.
        # If the overall winner needs engine extension, the direct cell is a separate pick.
        direct_results = [r for r in results if r["directly_implementable"]]
        if direct_results:
            direct_winner = direct_results[0]  # already sorted by score desc, then persistence
        else:
            direct_winner = winner

        if not winner["directly_implementable"]:
            print(
                "\nWARNING: Overall winner requires min_dwell or hysteresis. "
                f"Running validate_regime_detector.py with best directly-implementable cell "
                f"(er_enter={direct_winner['er_enter']:.2f}, score={direct_winner['combined_score']:.1f}) "
                "to get the official report."
            )

        # Write the winner config (ER-only, no dwell/hysteresis in engine)
        winner_cfg = _build_winner_config(direct_winner["er_enter"])
        _WINNER_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(_WINNER_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(winner_cfg, f, indent=2)
        print(f"\nWrote: {_WINNER_CONFIG_PATH}")

        print(f"\nRunning validate_regime_detector.py with winner config ...")
        TBOT_PYTHON = _resolve_tbot_python()
        cmd = [
            str(TBOT_PYTHON),
            str(Path(_HERE) / "validate_regime_detector.py"),
            "--config", str(_WINNER_CONFIG_PATH),
            "--start", args.start,
            "--end", args.end,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=_SR)
        print(result.stdout)
        if result.returncode != 0:
            print(f"WARNING: validate_regime_detector.py failed:\n{result.stderr}")
        else:
            print("regime_detector_report.yaml updated with winner config.")
            if not winner["directly_implementable"]:
                print(
                    "   NOTE: official report shows ER-only (stateless) results. "
                    f"Adding min_dwell={winner['min_dwell']} in the engine would "
                    "improve persistence further - see regime_retune_results.yaml for projected numbers."
                )


if __name__ == "__main__":
    main()
