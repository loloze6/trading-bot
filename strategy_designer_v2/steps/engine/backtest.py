"""The engine's backtest of a validated claim: write its strategy config, run trading-bot on every window
of the fold, read the engine's own metrics, apply the profit bar. Code only.
Usage: python3 steps/engine/backtest.py <claims.yaml> <claim_id> <fold> <bar_size> <SYMBOL> [out_dir] [--windows N]
Reused from v1 by hand: trading-bot/core/launcher.run_backtest (the backtester itself, with warmup prefetch,
Kraken commission, per-run trades log, bar-level equity). Windows are reported as W1..W6, never dates."""
import sys, json, pathlib, datetime as dt, time
import numpy as np, yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
TB = ROOT / "trading-bot"
sys.path.insert(0, str(TB)); sys.path.insert(0, str(ROOT / "strategy-research" / "tools"))
import research_folds as rf  # noqa: E402

FEE_PER_LEG = 0.0005          # Kraken 5 bps per leg (engine cost model); slippage is the engine's own
SHARPE_MIN, DD_MAX, AGREE = 1.0, 0.20, 5
LEDGER = ROOT / "strategy_designer_v2" / "records" / "trials.yaml"
INTERVAL = {"1h": 3600, "1d": 86400}


def config_of(idea: dict) -> dict:
    c = idea["claim"]
    return {"aux_feeds": [], "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
            "strategies": {"warmup": 2, "regimes": {"unknown": {"components": [
                {"id": idea["id"], "class": "strategies.claim_event.ClaimEventComponent",
                 "params": {"code": c["code"], "horizon": int(c["horizon_bars"]), "scaling_factor": 10.0, "min_bars": 200},
                 "weight": 1.0, "lookback": 500, "transforms": [{"op": "identity"}]}]},
                "trending": None, "mean_reversion": None, "chop": None}}}


def backtest_claim(claims_path, cid, fold, bar_size, symbol, out_dir=None, max_windows=None):
    from core.launcher import run_backtest  # the engine
    claims_path = pathlib.Path(claims_path).resolve()
    idea = next(i for i in yaml.safe_load(claims_path.read_text())["ideas"] if i["id"] == cid)
    out_dir = (pathlib.Path(out_dir) if out_dir else claims_path.parent / f"engine_{cid}_{symbol}").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = out_dir / "strategy_config.json"; cfg.write_text(json.dumps(config_of(idea), indent=2))
    windows = rf.load_fold_windows(fold)[: max_windows or 6]
    holdout_start = rf.policy_ranges()["holdout"][0]   # the seal, never printed
    rows, agree = [], 0
    for i, w in enumerate(windows, start=1):
        t0 = time.time()
        rd = run_backtest(str(cfg), symbol, w["test"]["start"], w["test"]["end"], str(out_dir / "results"),
                          runs_root=str(out_dir / "results"), interval_seconds=INTERVAL[bar_size], warmup_prefetch=True,
                          holdout_start=holdout_start, commission_rate=FEE_PER_LEG, exchange="kraken",
                          trades_log_file=str(out_dir / "trades.json"), bar_equity=True, market_type="futures")
        m = json.loads((pathlib.Path(rd) / "metrics.json").read_text())
        core, be = m.get("core", {}), m.get("bar_equity", {}) or {}
        ret = float(core.get("net_return_pct", 0.0) or 0.0) / 100.0
        errors = m.get("component_errors") or {}
        row = {"window": f"W{i}", "net_return": round(ret, 4), "trades": int(core.get("trade_count", 0) or 0),
               "sharpe": be.get("sharpe"), "max_drawdown": round(abs(float(be.get("max_drawdown_pct") or 0.0)) / 100.0, 4),
               "exposure_pct": be.get("exposure_pct"), "cost_drag_pct": core.get("cost_drag_pct"),
               "component_errors": int(errors.get("count", errors) if isinstance(errors, (dict, int)) else 0) if errors else 0,
               "run_dir": str(pathlib.Path(rd).relative_to(ROOT)), "seconds": round(time.time() - t0)}
        rows.append(row); agree += ret > 0
        print(f"  {row['window']}: net={ret:+.1%} trades={row['trades']} sharpe={row['sharpe']} dd={row['max_drawdown']} ({row['seconds']}s)")
    tot = float(np.prod([1 + r["net_return"] for r in rows]) - 1)
    sharpes = [r["sharpe"] for r in rows if isinstance(r["sharpe"], (int, float))]
    dds = [float(r["max_drawdown"]) for r in rows if r["max_drawdown"] is not None]
    dd_worst = max(dds) if dds else None
    sharpe_med = float(np.median(sharpes)) if sharpes else None
    checks = {f"net_positive_in_{AGREE}_of_{len(rows)}": agree >= min(AGREE, len(rows)),
              f"median_window_sharpe_ge_{SHARPE_MIN}": (sharpe_med is not None and sharpe_med >= SHARPE_MIN),
              f"worst_window_drawdown_le_{DD_MAX:.0%}": (dd_worst is not None and dd_worst <= DD_MAX)}
    out = {"claim": cid, "symbol": symbol, "bar_size": bar_size, "fold": fold, "engine": "trading-bot run_backtest, warmup prefetch, kraken 5 bps per leg",
           "fold_totals": {"net_return": round(tot, 4), "median_window_sharpe": sharpe_med, "worst_window_drawdown": dd_worst,
                           "trades": sum(r["trades"] for r in rows)}, "windows": rows, "checks": checks,
           "verdict": "pass" if all(checks.values()) else "fail"}
    (out_dir / "engine_verdict.yaml").write_text(yaml.safe_dump(out, sort_keys=False))
    ledger = yaml.safe_load(LEDGER.read_text()); ledger["trials"].append(
        {"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "try": "engine", "claim": cid, "symbols": [symbol],
         "bar_size": bar_size, "fold": fold, "verdict": f"engine:{out['verdict']}", "windows": len(rows)})
    LEDGER.write_text(yaml.safe_dump(ledger, sort_keys=False))
    print(f"{cid} {symbol}: engine {out['verdict']}  net={tot:+.1%} median_sharpe={sharpe_med} worst_dd={dd_worst}")
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mw = int(sys.argv[sys.argv.index("--windows") + 1]) if "--windows" in sys.argv else None
    backtest_claim(*args[:5], out_dir=(args[5] if len(args) > 5 else None), max_windows=mw)
