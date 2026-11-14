"""Numeric summary of an engine run's book, per window. Reads only the engine's files.
Usage: python3 steps/analyst/summarise.py <engine_dir>   -> writes <engine_dir>/book_summary.yaml
No dates: windows are W1.., bars are indices into the window's bars.csv."""
import json, pathlib, sys
import numpy as np, pandas as pd, yaml

CAP = 20.0          # the engine's forecast cap (standardise cap)
NEAR0 = 1.0         # |forecast| below this counts as near zero
VAL = "postRebalance_total_value"   # equity per bar
POS = "postRebalance_current_allocation"   # position after rebalance (forecast units)
ALLOC = "previous_allocation"       # allocation going into the bar; allocation_change = the move


def r(x, n=4):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), n)


def horizon_of(engine_dir, claim_id):
    """claim horizon_bars from claims.yaml next to the engine folder; 12 if not found."""
    for p in (engine_dir.parent / "claims.yaml", engine_dir / "claims.yaml"):
        if p.exists():
            for i in yaml.safe_load(p.read_text()).get("ideas", []):
                if i.get("id") == claim_id:
                    return int(i["claim"]["horizon_bars"])
    return 12


def window(row, root, h, ev_col, st_col):
    d = pathlib.Path(root) / row["run_dir"] if not pathlib.Path(row["run_dir"]).is_absolute() else pathlib.Path(row["run_dir"])
    bars = pd.read_csv(d / "bars.csv")
    trades = json.loads((d / "trades.json").read_text())
    m = json.loads((d / "metrics.json").read_text())
    core, be = m["core"], m["bar_equity"]
    v = bars[VAL].astype(float)
    dv = v.diff().fillna(0.0)
    f = bars["forecast"].astype(float)
    nxt = bars.close.pct_change().shift(-1)           # return of the bar after the decision
    fwd = bars.close.shift(-h) / bars.close - 1        # forward return over the claim horizon
    ok = nxt.notna() & (f != 0)
    agree = lambda mask: r((np.sign(f[mask & ok]) == np.sign(nxt[mask & ok])).mean())
    ev = bars[ev_col].fillna(0).astype(float) != 0 if ev_col in bars else pd.Series(False, index=bars.index)
    s = bars[st_col].astype(float) if st_col in bars else pd.Series(np.nan, index=bars.index)
    evf = ev & fwd.notna()
    pnl = [t["net_profit_loss_absolute"] for t in trades]
    pct = [t["net_profit_loss_percent"] for t in trades]
    dur = [t["duration_minutes"] for t in trades]
    bar_min = (pd.to_datetime(bars.timestamp).diff().dropna().dt.total_seconds().median() or 3600) / 60
    q = f.quantile([0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99])
    idx = np.linspace(0, len(v) - 1, 11)[1:].round().astype(int)
    order = dv.sort_values()
    side = lambda mask: {"n": int(mask.sum()), "mean_fwd_ret_pct": r(100 * fwd[mask].mean()), "share_up": r((fwd[mask] > 0).mean())}
    return {
        "bars": len(bars),
        "net_return_pct": core["net_return_pct"], "sharpe_core": core["sharpe"], "sharpe_bar_equity": be["sharpe"],
        "max_drawdown_pct_core": core["max_drawdown_pct"], "max_drawdown_pct_bar_equity": be["max_drawdown_pct"],
        "fees_paid": core["fees_paid"], "gross_pnl": core["gross_pnl"], "net_pnl": core["net_pnl"], "cost_drag_pct": core["cost_drag_pct"],
        "trades": {"count": len(trades), "win_rate_pct": core["win_rate"], "avg_net": core["avg_trade_net_pnl"],
                   "avg_net_pct": r(np.mean(pct)) if pct else None,
                   "largest_win": r(max(pnl)) if pnl else None, "largest_loss": r(min(pnl)) if pnl else None,
                   "avg_hold_bars": r(np.mean(dur) / bar_min, 2) if dur else None,
                   "long_net": r(sum(p for t, p in zip(trades, pnl) if t["side"] == "LONG")),
                   "short_net": r(sum(p for t, p in zip(trades, pnl) if t["side"] != "LONG"))},
        "exposure_pct": be["exposure_pct"], "exposure_pct_recomputed": r(100 * (bars[POS].abs() > 1e-9).mean(), 2),
        "turnover": be["turnover"], "mean_abs_alloc_change": r(bars["allocation_change"].abs().mean()),
        "forecast": {"quantiles_1_10_25_50_75_90_99": [r(x, 2) for x in q], "share_at_cap": r((f.abs() >= CAP - 1e-9).mean()),
                     "share_near_zero": r((f.abs() < NEAR0).mean()), "share_positive": r((f > 0).mean())},
        "sign_agreement_next_bar": {"all_bars": agree(pd.Series(True, index=bars.index)), "event_bars": agree(ev),
                                    "corr_all_bars_core": core["forecast_return_corr_all_bars"]},
        "event_bars": {"count": int(ev.sum()), "horizon_bars": h, "strength_positive": side(evf & (s > 0)), "strength_negative": side(evf & (s < 0))},
        "equity_deciles": [r(v.iloc[i], 2) for i in idx], "start_value": r(v.iloc[0], 2),
        "worst_5_bars": [[int(i), r(x, 2)] for i, x in order.head(5).items()],
        "best_5_bars": [[int(i), r(x, 2)] for i, x in order.tail(5)[::-1].items()],
    }


def summarise_engine_run(engine_dir):
    engine_dir = pathlib.Path(engine_dir).resolve()
    ev = yaml.safe_load((engine_dir / "engine_verdict.yaml").read_text())
    cid = ev["claim"]; h = horizon_of(engine_dir, cid)
    root = engine_dir
    while root != root.parent and not (root / "strategy_designer_v2").exists():
        root = root.parent   # run_dir is relative to the repo root
    ev_col, st_col = f"debug_info.components.{cid}.event", f"debug_info.components.{cid}.strength"
    out = {"claim": cid, "event_horizon_bars": h, "note": "windows W1..; bar indices count from the window's first bar; no dates"}
    for sizing in ("full_size", "vol_target"):
        if isinstance(ev.get(sizing), dict) and ev[sizing].get("windows"):
            out[sizing] = {w["window"]: window(w, root, h, ev_col, st_col) for w in ev[sizing]["windows"]}
    return out


if __name__ == "__main__":
    d = pathlib.Path(sys.argv[1])
    res = summarise_engine_run(d)
    (d / "book_summary.yaml").write_text(yaml.safe_dump(res, sort_keys=False, default_flow_style=None, width=120))
    print(f"wrote {d / 'book_summary.yaml'}")
