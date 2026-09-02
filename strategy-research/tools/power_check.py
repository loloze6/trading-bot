"""
A8.6: A-priori statistical power check at hypothesis registration.

Formula (episode-clustered, symbol-correlated):
  n_eff_symbols     = n_symbols / (1 + (n_symbols - 1) * rho_bar)
  expected_active_n = activation_rate × n_bars × n_eff_symbols
  expected_n_eff    = expected_active_n / BLOCK_SIZE
  min_detectable_ic = 1 / sqrt(max(expected_n_eff - 3, 1))

For market-wide signals (is_market_wide=True):
  rho_bar is loaded from campaign_config.yaml (symbol_correlation.btc_eth_return_correlation_1h).
  The sqrt(n) heuristic is NOT used — it materially overstates power (A8.6 amendment).

For independent symbols (is_market_wide=False):
  rho_bar = 0  →  n_eff_symbols = n_symbols (fully independent)

Route:
  min_detectable_ic > plausible_ic_upper  → insufficient_power_a_priori
  otherwise                               → power_adequate

Usage:
  python power_check.py --hypothesis-card path/to/hypothesis_card.yaml [--config path/to/campaign_config.yaml] [--out path/to/out.yaml]

Exits 0 on power_adequate, 1 on insufficient_power_a_priori, 2 on missing/incomplete params.
"""

import math
import sys
import contextlib
import json
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

# BLOCK_SIZE was a bare constant 24 until 2026-08-27 -- "1h bars per
# autocorrelation episode (bars per day)". A bare constant cannot vary at all,
# so this mirror was silently 1h-only for every hypothesis it ever checked.
# Now DERIVED per timeframe from the shared tools/timeframe.py, the single
# source the A8.6 gate and prescreen_signal.py also use. See that module for
# why the old lookup/constant approach kept regenerating this bug.
from timeframe import bars_per_day  # noqa: E402  (sibling module in tools/)

# CUL-213: the emoji status prints in this module crash on a Windows cp1252
# console (UnicodeEncodeError) the moment stdout is redirected/piped/captured
# (e.g. run as a captured subprocess). Degrade unencodable glyphs to '?' rather
# than raising — same fix as setup_run.py (CUL-12). getattr because typeshed
# types sys.stdout as TextIO (no reconfigure); contextlib.suppress because a
# captured stream may reject it (OSError) — never crash a context the raw prints
# already survived.
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    with contextlib.suppress(OSError):
        _reconfigure(errors="replace")

BLOCK_SIZE_1H_LEGACY = 24  # retained ONLY as the regression anchor: bars_per_day("1h") must equal this
_DEFAULT_CONFIG = Path(__file__).parent.parent / "config" / "campaign_config.yaml"


def _load_rho(config_path: Path | str | None = None) -> float:
    """Load measured ρ̄ from campaign_config.yaml. Falls back to 0.82 if unavailable."""
    path = Path(config_path) if config_path else _DEFAULT_CONFIG
    try:
        cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return float(cfg.get("symbol_correlation", {}).get("btc_eth_return_correlation_1h", 0.82))
    except Exception:
        return 0.82


def run_power_check(hypothesis_card_path: Path | str,
                    config_path: Path | str | None = None,
                    timeframe=None) -> dict:
    """
    Load a hypothesis_card.yaml and compute A8.6 power metrics.
    Returns a result dict with 'verdict' key.
    """
    card_path = Path(hypothesis_card_path)
    if not card_path.exists():
        return {"verdict": "skip", "reason": f"hypothesis_card.yaml not found: {card_path}"}

    card = yaml.safe_load(card_path.read_text(encoding="utf-8")) or {}
    params = card.get("power_parameters", {})

    if not params:
        return {"verdict": "skip", "reason": "no power_parameters block in hypothesis_card.yaml"}

    activation_rate = params.get("activation_rate")
    plausible_ic_upper = params.get("plausible_ic_upper")

    if activation_rate is None or plausible_ic_upper is None:
        return {
            "verdict": "skip",
            "reason": "power_parameters.activation_rate or plausible_ic_upper is null",
        }

    # Timeframe drives the autocorrelation block. Mirrors the A8.6 gate's own
    # resolution exactly: prefer an explicit argument, else the sibling
    # research_brief.yaml, else 1h (which reproduces this tool's historic
    # behaviour when no brief is present).
    if timeframe is None:
        brief = card_path.parent / "research_brief.yaml"
        if brief.exists():
            timeframe = (yaml.safe_load(brief.read_text(encoding="utf-8")) or {}).get("timeframe", "1h")
        else:
            timeframe = "1h"
    block_size = bars_per_day(timeframe)

    n_bars = params.get("n_bars", 17520)
    n_symbols = params.get("n_symbols", 2)
    is_market_wide = params.get("is_market_wide", False)
    data_requirement = params.get("data_requirement")

    # A8.6 core formula with proper correlation correction
    if is_market_wide:
        rho = _load_rho(config_path)
        n_eff_symbols = n_symbols / (1.0 + (n_symbols - 1) * rho)
    else:
        rho = 0.0
        n_eff_symbols = float(n_symbols)

    expected_active_n = activation_rate * n_bars * n_eff_symbols
    expected_n_eff = expected_active_n / block_size
    min_detectable_ic = 1.0 / math.sqrt(max(expected_n_eff - 3.0, 1.0))

    verdict = (
        "insufficient_power_a_priori"
        if min_detectable_ic > plausible_ic_upper
        else "power_adequate"
    )

    result = {
        "verdict": verdict,
        "expected_active_n": round(expected_active_n, 1),
        "expected_n_eff": round(expected_n_eff, 2),
        "min_detectable_ic": round(min_detectable_ic, 4),
        "plausible_ic_upper": plausible_ic_upper,
        "activation_rate": activation_rate,
        "n_bars": n_bars,
        "n_symbols": n_symbols,
        "n_eff_symbols": round(n_eff_symbols, 3),
        "rho_bar": round(rho, 4) if is_market_wide else None,
        "is_market_wide": is_market_wide,
        "block_size": block_size,
        "timeframe": timeframe,
    }
    if verdict == "insufficient_power_a_priori":
        result["data_requirement"] = data_requirement or "extend data window (e.g. to 2018+)"

    return result


def _main():
    parser = argparse.ArgumentParser(description="A8.6 a-priori power check")
    parser.add_argument("--hypothesis-card", required=True,
                        help="Path to hypothesis_card.yaml")
    parser.add_argument("--config", default=None,
                        help="Path to campaign_config.yaml (default: ../config/campaign_config.yaml)")
    parser.add_argument("--out", default=None,
                        help="Optional path to write result YAML")
    args = parser.parse_args()

    result = run_power_check(args.hypothesis_card, args.config)
    print(json.dumps(result, indent=2))

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(result, f, default_flow_style=False, sort_keys=False)

    verdict = result.get("verdict", "skip")
    if verdict == "insufficient_power_a_priori":
        print(
            f"\n⚡ A8.6 FAIL: min_detectable_ic={result['min_detectable_ic']:.4f} > "
            f"plausible_ic_upper={result['plausible_ic_upper']}\n"
            f"   expected_n_eff={result['expected_n_eff']:.1f} "
            f"(active_n={result['expected_active_n']:.0f} / block={result['block_size']})\n"
            f"   n_eff_symbols={result['n_eff_symbols']:.3f} "
            f"(rho={result['rho_bar']})\n"
            f"   Data requirement: {result.get('data_requirement')}",
            file=sys.stderr,
        )
        sys.exit(1)
    elif verdict == "power_adequate":
        print(
            f"\n✅ A8.6 PASS: min_detectable_ic={result['min_detectable_ic']:.4f} ≤ "
            f"plausible_ic_upper={result['plausible_ic_upper']} "
            f"(expected_n_eff={result['expected_n_eff']:.1f})",
            file=sys.stderr,
        )
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    _main()
