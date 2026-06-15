"""
run_protocol.py — walk-forward protocol runner.

CLI (run from repo root or strategy-research/):
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path>
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path> --holdout --i-understand
"""
import sys
import os
import json
import argparse
import statistics
from datetime import datetime, timezone, date
from hashlib import sha256
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))   # strategy-research/tools/
_SR   = os.path.dirname(_HERE)                        # strategy-research/
_REPO = os.path.dirname(_SR)                          # repo root
_TBOT = os.path.join(_REPO, "trading-bot")            # trading-bot/

if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

from core.launcher import run_backtest

_RESULTS_ROOT = os.path.join(_SR, "results")


def _config_sha(config_path: str):
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"))
    digest = sha256(canonical.encode()).hexdigest()
    return digest, digest[:8]


def _protocol_run_id(sha8: str) -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + sha8


def main():
    parser = argparse.ArgumentParser(description="Walk-forward protocol runner")
    parser.add_argument("config_path",   help="Path to strategy_config.json")
    parser.add_argument("protocol_path", help="Path to protocol JSON spec")
    parser.add_argument("--holdout",      action="store_true")
    parser.add_argument("--i-understand", action="store_true", dest="i_understand")
    args = parser.parse_args()

    # Holdout gate: require BOTH flags or NEITHER
    if args.holdout != args.i_understand:
        print("ERROR: --holdout requires --i-understand (and vice versa). Pass both or neither.",
              file=sys.stderr)
        sys.exit(1)

    with open(args.protocol_path, encoding="utf-8") as f:
        protocol = json.load(f)

    config_sha256, config_sha8 = _config_sha(args.config_path)
    symbols = protocol["symbols"]
    os.makedirs(_RESULTS_ROOT, exist_ok=True)

    run_id = _protocol_run_id(config_sha8)
    out_dir = Path(_RESULTS_ROOT) / "protocols" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # HOLDOUT MODE
    # ------------------------------------------------------------------
    if args.holdout:
        h = protocol["holdout"]
        start = h["start"]
        end   = h["end"] if h["end"] is not None else date.today().isoformat()

        holdout_results = {}
        for symbol in symbols:
            print(f"[holdout] {symbol}  {start} to {end} ...")
            rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT)
            with open(rd / "metrics.json", encoding="utf-8") as f:
                m = json.load(f)
            holdout_results[symbol] = {"run_id": rd.name, "core": m["core"]}

        payload = {
            "protocol_run_id": run_id,
            "config_sha256":   config_sha256,
            "holdout_window":  {"start": start, "end": end},
            "results":         holdout_results,
        }
        (out_dir / "holdout_result.json").write_text(
            json.dumps(payload, indent=2, default=str), encoding="utf-8"
        )
        print(f"Holdout result: {out_dir / 'holdout_result.json'}")

        log_path = Path(_RESULTS_ROOT) / "holdout_log.jsonl"
        line = {
            "utc":             datetime.now(timezone.utc).isoformat(),
            "config_sha256":   config_sha256,
            "protocol_run_id": run_id,
            "symbols_core":    {s: holdout_results[s]["core"] for s in symbols},
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, default=str) + "\n")
        print(f"Appended to {log_path}")
        return

    # ------------------------------------------------------------------
    # NORMAL MODE — walk-forward windows
    # ------------------------------------------------------------------
    budget_path = Path(_RESULTS_ROOT) / "protocol_budget.jsonl"
    prior_runs = 0
    if budget_path.exists():
        with open(budget_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                if entry.get("config_sha256") == config_sha256:
                    prior_runs += entry.get("n_runs", 0)
    n_new = len(symbols) * len(protocol["windows"])
    print(f"Budget used for this config: {prior_runs}/20 scored runs")
    if prior_runs + n_new > 20:
        print(f"WARNING: this run adds {n_new}, bringing total to {prior_runs + n_new}/20 (over budget). Continuing.")

    results = []
    for symbol in symbols:
        for window in protocol["windows"]:
            label = window["label"]
            start = window["test"]["start"]
            end   = window["test"]["end"]
            print(f"  {symbol}  window={label}  {start} to {end} ...")
            rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT)
            with open(rd / "metrics.json", encoding="utf-8") as f:
                m = json.load(f)
            core = m["core"]
            results.append({
                "symbol": symbol,
                "window": label,
                "run_id": rd.name,
                "core":   core,
            })
            print(f"    sharpe={core.get('sharpe', 0):.3f}  trades={core.get('trade_count', 0)}"
                  f"  dd={core.get('max_drawdown_pct', 0):.1f}%")

    # Per-symbol summary
    promo = protocol["promotion"]
    per_symbol = {}
    for symbol in symbols:
        rows     = [r for r in results if r["symbol"] == symbol]
        sharpes  = [r["core"]["sharpe"] for r in rows]
        dds      = [abs(r["core"]["max_drawdown_pct"]) for r in rows]
        trades   = [r["core"]["trade_count"] for r in rows]
        per_symbol[symbol] = {
            "median_sharpe":        round(statistics.median(sharpes), 4),
            "max_abs_drawdown_pct": round(max(dds), 4),
            "min_trade_count":      min(trades),
        }

    def _promote(s):
        p = per_symbol[s]
        return (p["median_sharpe"]        >  promo["median_sharpe_gt"]
                and p["max_abs_drawdown_pct"] <  promo["max_abs_drawdown_pct_lt"]
                and p["min_trade_count"]       >= promo["min_trade_count_gte"])

    def _kill(s):
        return per_symbol[s]["median_sharpe"] < promo["kill_median_sharpe_lt"]

    if all(_promote(s) for s in symbols):
        verdict = "promote"
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}>0"
                 f" max_dd={per_symbol[s]['max_abs_drawdown_pct']:.1f}%<30"
                 f" min_trades={per_symbol[s]['min_trade_count']}>=20"
                 for s in symbols]
        verdict_reason = "; ".join(parts)
    elif all(_kill(s) for s in symbols):
        verdict = "kill"
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}<-1" for s in symbols]
        verdict_reason = "both symbols below kill threshold: " + ", ".join(parts)
    else:
        verdict = "refine"
        parts = []
        for s in symbols:
            p = per_symbol[s]
            fails = []
            if p["median_sharpe"] <= promo["median_sharpe_gt"]:
                fails.append(f"median_sharpe={p['median_sharpe']:.3f}<=0")
            if p["max_abs_drawdown_pct"] >= promo["max_abs_drawdown_pct_lt"]:
                fails.append(f"max_dd={p['max_abs_drawdown_pct']:.1f}%>=30")
            if p["min_trade_count"] < promo["min_trade_count_gte"]:
                fails.append(f"min_trades={p['min_trade_count']}<20")
            if fails:
                parts.append(f"{s}: " + ", ".join(fails))
        verdict_reason = "; ".join(parts) if parts else "mixed — not all pass promote, not all fail at kill"

    summary = {
        "protocol_run_id":    run_id,
        "config_sha256":      config_sha256,
        "protocol_file":      args.protocol_path,
        "results":            results,
        "per_symbol_summary": per_symbol,
        "verdict":            verdict,
        "verdict_reason":     verdict_reason,
    }
    (out_dir / "protocol_summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )
    print(f"\nProtocol summary: {out_dir / 'protocol_summary.json'}")
    print(f"Verdict : {verdict}")
    print(f"Reason  : {verdict_reason}")

    # Task 5.4 — append to budget log
    budget_entry = {
        "utc":             datetime.now(timezone.utc).isoformat(),
        "config_sha256":   config_sha256,
        "protocol_run_id": run_id,
        "n_runs":          n_new,
    }
    with open(budget_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(budget_entry, default=str) + "\n")
    print(f"Budget log: {budget_path}")


if __name__ == "__main__":
    main()
