"""The engine's backtest of a validated claim: write its strategy config, run trading-bot on every window
of the fold, read the engine's own metrics, apply the profit bar. Code only.
Usage: python3 steps/engine/backtest.py <claims.yaml> <claim_id> <fold> <bar_size> <SYMBOL> [out_dir] [--windows N]
Reused from v1 by hand: trading-bot/core/launcher.run_backtest (the backtester itself, with warmup prefetch,
Kraken commission, per-run trades log, bar-level equity). Windows are reported as W1..W6, never dates."""
import sys, re, json, pathlib, datetime as dt, time
import numpy as np, yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
TB = ROOT / "trading-bot"
sys.path.insert(0, str(TB)); sys.path.insert(0, str(ROOT / "strategy-research" / "tools"))
import research_folds as rf  # noqa: E402

FEE_PER_LEG = 0.0005          # Kraken 5 bps per leg (engine cost model); slippage is the engine's own
SHARPE_MIN, DD_MAX, AGREE = 1.0, 0.20, 5
LEDGER = ROOT / "strategy_designer_v2" / "records" / "trials.yaml"
INTERVAL = {"1h": 3600, "1d": 86400}


def min_bars_of(code: str) -> int:
    """History the claim needs: the sum of the window sizes in its code (nested windows add up) plus a margin."""
    wins = [int(n) for n in re.findall(r"(?:rolling|shift|pct_change|diff|span=|window=)\(?\s*(\d+)", code)]
    return max(200, sum(wins) + 50)


SIZING = {"kind": "vol_target", "window": 30, "target_annual_vol": 0.20, "max_allocation": 1.0}   # fixed before any result
STD = {"window": 500, "min_periods": 100, "target": 10.0, "cap": 20.0}   # standardise first, fixed before any result
PERIODS = {"1h": 24 * 365, "1d": 365}


def config_of(idea: dict, bar_size: str = "1h", sized: bool = False) -> dict:
    c = idea["claim"]; mb = min_bars_of(c["code"])
    cfg = _config_of(idea, mb)
    if sized:
        cfg["strategies"]["sizing"] = {**SIZING, "periods_per_year": PERIODS[bar_size]}
    return cfg


def _config_of(idea: dict, mb: int) -> dict:
    c = idea["claim"]
    return {"aux_feeds": [], "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
            "strategies": {"warmup": 2, "regimes": {"unknown": {"components": [
                {"id": idea["id"], "class": "strategies.claim_linear.ClaimStrengthComponent",
                 "params": {"code": c["code"], "horizon": int(c["horizon_bars"]), "min_bars": mb},
                 "weight": 1.0, "lookback": mb + STD["window"] + 100,   # linear: the engine grades the strength, target 10, cap 20
                 "transforms": [{"op": "standardise", "params": dict(STD)}]}]},
                "trending": None, "mean_reversion": None, "chop": None}}}


def _run_size(idea, cid, fold, bar_size, symbol, out_dir, windows, holdout_start, sized):
    from core.launcher import run_backtest  # the engine
    tag = "vol_target" if sized else "full_size"
    cfg = out_dir / f"strategy_config_{tag}.json"; cfg.write_text(json.dumps(config_of(idea, bar_size, sized), indent=2))
    rows, agree = [], 0
    for i, w in enumerate(windows, start=1):
        t0 = time.time()
        rd = run_backtest(str(cfg), symbol, w["test"]["start"], w["test"]["end"], str(out_dir / "results" / tag),
                          runs_root=str(out_dir / "results" / tag), interval_seconds=INTERVAL[bar_size], warmup_prefetch=True,
                          holdout_start=holdout_start, commission_rate=FEE_PER_LEG, exchange="kraken",
                          trades_log_file=str(out_dir / f"trades_{tag}.json"), bar_equity=True, market_type="futures")
        m = json.loads((pathlib.Path(rd) / "metrics.json").read_text())
        core, be = m.get("core", {}), m.get("bar_equity", {}) or {}
        ret = float(core.get("net_return_pct", 0.0) or 0.0) / 100.0
        row = {"window": f"W{i}", "net_return": round(ret, 4), "trades": int(core.get("trade_count", 0) or 0),
               "sharpe": be.get("sharpe"), "max_drawdown": round(abs(float(be.get("max_drawdown_pct") or 0.0)) / 100.0, 4),
               "exposure_pct": be.get("exposure_pct"), "cost_drag_pct": core.get("cost_drag_pct"),
               "run_dir": str(pathlib.Path(rd).relative_to(ROOT)), "seconds": round(time.time() - t0)}
        rows.append(row); agree += ret > 0
        print(f"  [{tag}] {row['window']}: net={ret:+.1%} trades={row['trades']} sharpe={row['sharpe']} dd={row['max_drawdown']} ({row['seconds']}s)")
    tot = float(np.prod([1 + r["net_return"] for r in rows]) - 1)
    sharpes = [r["sharpe"] for r in rows if isinstance(r["sharpe"], (int, float))]
    dds = [float(r["max_drawdown"]) for r in rows if r["max_drawdown"] is not None]
    sharpe_med = float(np.median(sharpes)) if sharpes else None; dd_worst = max(dds) if dds else None
    checks = {f"net_positive_in_{AGREE}_of_{len(rows)}": agree >= min(AGREE, len(rows)),
              f"median_window_sharpe_ge_{SHARPE_MIN}": (sharpe_med is not None and sharpe_med >= SHARPE_MIN),
              f"worst_window_drawdown_le_{DD_MAX:.0%}": (dd_worst is not None and dd_worst <= DD_MAX)}
    verdict = "refused" if sum(r["trades"] for r in rows) == 0 else ("pass" if all(checks.values()) else "fail")
    return {"sizing": (dict(SIZING) if sized else "full size (forecast 10 = 100%)"),
            "fold_totals": {"net_return": round(tot, 4), "median_window_sharpe": sharpe_med, "worst_window_drawdown": dd_worst,
                            "trades": sum(r["trades"] for r in rows)}, "windows": rows, "checks": checks, "verdict": verdict}


def backtest_claim(claims_path, cid, fold, bar_size, symbol, out_dir=None, max_windows=None):
    """Both sizes, every book: full size and a fixed 20% volatility target. Pass if either passes; the record says which."""
    claims_path = pathlib.Path(claims_path).resolve()
    idea = next(i for i in yaml.safe_load(claims_path.read_text())["ideas"] if i["id"] == cid)
    out_dir = (pathlib.Path(out_dir) if out_dir else claims_path.parent / f"engine_{cid}_{symbol}").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    windows = rf.load_fold_windows(fold)[: max_windows or 6]
    holdout_start = rf.policy_ranges()["holdout"][0]   # the seal, never printed
    try:
        full = _run_size(idea, cid, fold, bar_size, symbol, out_dir, windows, holdout_start, sized=False)
        sized = _run_size(idea, cid, fold, bar_size, symbol, out_dir, windows, holdout_start, sized=True) if full["verdict"] != "refused" else None
    except (AssertionError, RuntimeError, ValueError) as exc:   # asked by run n06: AVAX's history before fold A is shorter than the warm-up
        why = re.sub(r"\d{4}-\d{2}-\d{2}", "<date>", f"engine refused: {type(exc).__name__}: {str(exc)[:200]}")   # never a window date in a tracked file
        out = {"claim": cid, "symbol": symbol, "bar_size": bar_size, "fold": fold, "verdict": "refused", "why": why,
               "fold_totals": {"net_return": 0.0, "median_window_sharpe": None, "worst_window_drawdown": None, "trades": 0}}
        (out_dir / "engine_verdict.yaml").write_text(yaml.safe_dump(out, sort_keys=False)); print(f"{cid} {symbol}: {why}")
        return out
    verdicts = [full["verdict"]] + ([sized["verdict"]] if sized else [])
    verdict = "refused" if full["verdict"] == "refused" else ("pass" if "pass" in verdicts else "fail")
    best = sized if (sized and sized["verdict"] == "pass" and full["verdict"] != "pass") else full
    out = {"claim": cid, "symbol": symbol, "bar_size": bar_size, "fold": fold, "engine": "trading-bot run_backtest, warmup prefetch, kraken 5 bps per leg",
           "min_bars": min_bars_of(idea["claim"]["code"]), "verdict": verdict, "passed_as": ("vol_target" if best is sized else "full_size") if verdict == "pass" else None,
           "fold_totals": best["fold_totals"], "full_size": full, "vol_target": sized}
    (out_dir / "engine_verdict.yaml").write_text(yaml.safe_dump(out, sort_keys=False))
    if full["verdict"] != "refused":   # branch 1 from the same folder (lazy import: the judge does not import this step)
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "judge")); import judge
        judge.judge_engine_run(out_dir, claims_path, cid)
    ledger = yaml.safe_load(LEDGER.read_text()); ledger["trials"].append(
        {"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "try": "engine", "claim": cid, "symbols": [symbol],
         "bar_size": bar_size, "fold": fold, "verdict": f"engine:{verdict}", "windows": len(windows), "sizes": len(verdicts)})
    LEDGER.write_text(yaml.safe_dump(ledger, sort_keys=False))
    print(f"{cid} {symbol}: engine {verdict} (full {full['verdict']}" + (f", vol_target {sized['verdict']}" if sized else "") +
          f")  net={best['fold_totals']['net_return']:+.1%} median_sharpe={best['fold_totals']['median_window_sharpe']} worst_dd={best['fold_totals']['worst_window_drawdown']}")
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mw = int(sys.argv[sys.argv.index("--windows") + 1]) if "--windows" in sys.argv else None
    backtest_claim(*args[:5], out_dir=(args[5] if len(args) > 5 else None), max_windows=mw)
