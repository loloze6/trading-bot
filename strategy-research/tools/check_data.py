"""
check_data.py — data availability check + holdout overlap guard.

Usage:
  # Basic data check (extended range):
  python strategy-research/tools/check_data.py

  # Protocol-aware check (validates data AND rejects holdout overlap):
  python strategy-research/tools/check_data.py --protocol strategy-research/protocols/baseline_v2.json

  # Override the data policy file:
  python strategy-research/tools/check_data.py --protocol <proto> --policy <path/to/campaign_data_policy.yaml>

Exit codes:
  0  — all checks pass
  1  — holdout overlap detected (hard rejection)
  2  — data gap > 1 day detected
"""
import sys
import os
import json
import argparse
import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))   # strategy-research/tools/
_SR   = os.path.dirname(_HERE)                        # strategy-research/
_REPO = os.path.dirname(_SR)                          # repo root
_TBOT = os.path.join(_REPO, "trading-bot")

if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

import pandas as pd
from data.data_manager import DataManager

_DEFAULT_POLICY = os.path.join(_SR, "config", "campaign_data_policy.yaml")

# Default data check range (covers all baseline_v2 walk-forward windows).
_DEFAULT_START = "2024-01-01"
_DEFAULT_END   = "2025-12-31"
INTERVAL_SECONDS = 3600  # 1h
MAX_GAP_SECONDS  = 86400  # 1 day


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_date(s: str) -> datetime.date:
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()


def _load_policy(policy_path: str) -> dict:
    try:
        import yaml
        with open(policy_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        # Minimal YAML parse for simple key: value / list structures.
        # Falls back to a best-effort plain reader if PyYAML is unavailable.
        raise RuntimeError(
            "PyYAML is required for loading campaign_data_policy.yaml. "
            "Install it with: pip install pyyaml"
        )


def _load_protocol(protocol_path: str) -> dict:
    with open(protocol_path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Holdout overlap guard
# ---------------------------------------------------------------------------

def check_holdout_overlap(protocol: dict, policy: dict) -> bool:
    """Return True (safe) if no protocol window overlaps holdout_range; False otherwise."""
    holdout = policy.get("holdout_range")
    if not holdout or len(holdout) < 2:
        print("WARNING: holdout_range not defined in campaign_data_policy.yaml — skipping overlap check.")
        return True

    h_start = _parse_date(holdout[0])
    h_end   = _parse_date(holdout[1])

    windows = protocol.get("windows", [])
    violations = []
    for w in windows:
        test = w.get("test", {})
        w_start = _parse_date(test["start"])
        w_end   = _parse_date(test["end"])
        # Overlap: intervals [a,b) and [c,d) overlap iff a < d and c < b
        if w_start < h_end and h_start < w_end:
            violations.append(w.get("label", f"{test['start']}–{test['end']}"))

    if violations:
        print("ERROR: Protocol window(s) overlap the frozen holdout range "
              f"[{holdout[0]}, {holdout[1]}]:")
        for v in violations:
            print(f"  - {v}")
        print("Action: remove overlapping windows or choose a different protocol.")
        return False

    # Also check if the protocol's own holdout field overlaps
    proto_holdout = protocol.get("holdout", {})
    if proto_holdout:
        ph_start_s = proto_holdout.get("start")
        ph_end_s   = proto_holdout.get("end")
        if ph_start_s and ph_end_s:
            ph_start = _parse_date(ph_start_s)
            ph_end   = _parse_date(ph_end_s)
            if ph_start != h_start or ph_end != h_end:
                print(f"WARNING: Protocol holdout [{ph_start_s}, {ph_end_s}] does not match "
                      f"policy holdout [{holdout[0]}, {holdout[1]}].")

    print(f"OK: No protocol window overlaps holdout range [{holdout[0]}, {holdout[1]}].")
    return True


# ---------------------------------------------------------------------------
# Data availability check
# ---------------------------------------------------------------------------

def check_data_availability(symbols: list, start: str, end: str) -> bool:
    start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_dt   = datetime.datetime.strptime(end,   "%Y-%m-%d")
    expected_bars = int((end_dt - start_dt).total_seconds() / INTERVAL_SECONDS)

    print(f"\nData availability check: {start} to {end} (1h)")
    print(f"Expected bars (per symbol): {expected_bars}")
    print()

    any_large_gap = False

    for symbol in symbols:
        dm = DataManager(symbols=[symbol], interval_seconds=INTERVAL_SECONDS, mode="backtest")
        df = dm.fetch_historical_data(symbol, start, end)

        if df.empty:
            print(f"{symbol}: NO DATA RETURNED -- cannot proceed")
            any_large_gap = True
            continue

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)

        actual_bars = len(df)
        diff = df["timestamp"].diff().dropna()
        expected_delta = pd.Timedelta(seconds=INTERVAL_SECONDS)
        gaps = diff[diff > expected_delta * 1.5]

        print(f"{symbol}:")
        print(f"  actual bars  : {actual_bars:,}")
        print(f"  expected bars: {expected_bars:,}")
        print(f"  gap count    : {len(gaps)}")

        if gaps.empty:
            print("  gaps         : none")
        else:
            for idx in gaps.index:
                gap_start = df.loc[idx - 1, "timestamp"]
                gap_end   = df.loc[idx,     "timestamp"]
                duration  = gap_end - gap_start
                dur_h     = duration.total_seconds() / 3600
                flag = " *** > 1 DAY ***" if duration.total_seconds() > MAX_GAP_SECONDS else ""
                print(f"  gap: {gap_start} to {gap_end}  ({dur_h:.1f}h){flag}")
                if duration.total_seconds() > MAX_GAP_SECONDS:
                    any_large_gap = True
        print()

    return not any_large_gap


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Data availability check + holdout overlap guard.")
    parser.add_argument(
        "--protocol", metavar="PATH",
        help="Protocol JSON file to validate against holdout_range and use for symbol/date derivation."
    )
    parser.add_argument(
        "--policy", metavar="PATH", default=_DEFAULT_POLICY,
        help=f"campaign_data_policy.yaml path (default: {_DEFAULT_POLICY})"
    )
    parser.add_argument(
        "--skip-data-check", action="store_true",
        help="Only run holdout overlap check, skip the data availability download."
    )
    args = parser.parse_args()

    # --- Step 1: holdout overlap guard ---
    if args.protocol:
        if not os.path.exists(args.protocol):
            print(f"ERROR: protocol file not found: {args.protocol}")
            sys.exit(1)
        if not os.path.exists(args.policy):
            print(f"ERROR: data policy file not found: {args.policy}")
            print(f"Expected at: {args.policy}")
            print("Create config/campaign_data_policy.yaml first (see Improvement 07).")
            sys.exit(1)

        protocol = _load_protocol(args.protocol)
        policy   = _load_policy(args.policy)

        print(f"Checking holdout overlap for protocol: {args.protocol}")
        overlap_ok = check_holdout_overlap(protocol, policy)
        if not overlap_ok:
            sys.exit(1)

        # Derive symbols and date range from protocol windows
        symbols = protocol.get("symbols", ["BTCUSDT", "ETHUSDT"])
        windows = protocol.get("windows", [])
        if windows:
            starts = [w["test"]["start"] for w in windows]
            ends   = [w["test"]["end"]   for w in windows]
            data_start = min(starts)
            data_end   = max(ends)
        else:
            data_start = _DEFAULT_START
            data_end   = _DEFAULT_END
    else:
        symbols    = ["BTCUSDT", "ETHUSDT"]
        data_start = _DEFAULT_START
        data_end   = _DEFAULT_END

    # --- Step 2: data availability check ---
    if args.skip_data_check:
        print("Data availability check skipped (--skip-data-check).")
        sys.exit(0)

    ok = check_data_availability(symbols, data_start, data_end)
    if not ok:
        print("STOP: gap > 1 day detected. Report above. Do not proceed until user decides.")
        sys.exit(2)
    else:
        print("OK: no gap > 1 day. Safe to proceed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
