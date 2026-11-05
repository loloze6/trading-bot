"""Branch 3 for a validated claim, in the claim's own terms: trade the claim's signal on its bars,
hold for its horizon, pay the cost, and answer "profitable enough after cost" on one fold.
Code only. Usage: python3 steps/profit/profit.py <claims.yaml> <claim_id> <fold> <bar_size> <SYMBOL>
Bars: the same cache and the same seal mask as the judge. Windows reported as W1..W6, never dates.
The bar: net return positive in at least 5 of 6 windows, annualised Sharpe above 1.0 on the fold,
max drawdown no worse than 20%. Written here once, before the result."""
import sys, pathlib, datetime as dt
import numpy as np, pandas as pd, yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "judge"))
import judge as J  # the same bars, seal mask, windows and code runner  # noqa: E402

SHARPE_MIN, DD_MAX, AGREE = 1.0, 0.20, 5


def profit_claim(claims_path, cid, fold, bar_size, symbol, out_path=None, try_name="try_04"):
    """Branch 3 for one claim on one symbol; writes profit_<id>.yaml; appends a trial row; returns the dict."""
    claims_path = pathlib.Path(claims_path).resolve()
    idea = next(i for i in yaml.safe_load(claims_path.read_text())["ideas"] if i["id"] == cid)
    c = idea["claim"]; h = int(c["horizon_bars"])
    df = J.load_bars(symbol, bar_size)
    wn = J.window_numbers(df.index, J.rf.load_fold_windows(fold))
    a, b, signal, feature = J.run_code(c["code"], df)
    # Position: the claim's direction on an event bar, held h bars, flat otherwise; one position at a time.
    pos = pd.Series(0.0, index=df.index); i = 0; idx = np.where(a.values)[0]
    for k in idx:
        if k < i:          # still holding the previous event
            continue
        pos.iloc[k + 1:k + 1 + h] = float(signal.iloc[k])   # enter at the event bar's close, earn the next h bars
        i = k + 1 + h
    r = df["close"].pct_change().fillna(0.0)
    cost = pos.diff().abs().fillna(0.0) * (J.FEE_RT / 2)   # one leg per unit of position change
    net = pos.shift(0) * r - cost
    bars_per_year = {"1h": 24 * 365, "1d": 365}[bar_size]
    rows, agree = [], 0
    for w in range(1, 7):
        x = net[wn == w]
        eq = (1 + x).cumprod(); dd = (eq / eq.cummax() - 1).min()
        tot = float(eq.iloc[-1] - 1)
        rows.append({"window": f"W{w}", "net_return": round(tot, 4), "trades": int((pos.diff().abs()[wn == w] > 0).sum() // 2),
                     "max_drawdown": round(float(dd), 4)})
        agree += tot > 0
    x = net[wn > 0]; eq = (1 + x).cumprod()
    sharpe = float(x.mean() / x.std() * np.sqrt(bars_per_year)) if x.std() > 0 else 0.0
    dd = float((eq / eq.cummax() - 1).min()); tot = float(eq.iloc[-1] - 1)
    exposure = float((pos[wn > 0] != 0).mean())
    checks = {f"net_positive_in_{AGREE}_of_6": agree >= AGREE, f"sharpe_ge_{SHARPE_MIN}": sharpe >= SHARPE_MIN, f"max_drawdown_le_{DD_MAX:.0%}": dd >= -DD_MAX}
    out = {"claim": cid, "symbol": symbol, "bar_size": bar_size, "fold": fold, "cost_per_round_trip": J.FEE_RT,
           "fold_totals": {"net_return": round(tot, 4), "sharpe": round(sharpe, 2), "max_drawdown": round(dd, 4),
                           "time_in_market": round(exposure, 3), "trades": int((pos.diff().abs()[wn > 0] > 0).sum() // 2)},
           "windows": rows, "checks": checks, "verdict": "pass" if all(checks.values()) else "fail"}
    out_path = pathlib.Path(out_path) if out_path else claims_path.parent / f"profit_{cid}.yaml"
    out_path.write_text(yaml.safe_dump(out, sort_keys=False), encoding="utf-8")
    ledger = yaml.safe_load(J.LEDGER.read_text()); ledger["trials"].append(
        {"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "try": try_name, "claim": cid, "symbols": [symbol],
         "bar_size": bar_size, "fold": fold, "verdict": f"profit:{out['verdict']}"})
    J.LEDGER.write_text(yaml.safe_dump(ledger, sort_keys=False))
    print(f"{cid} {symbol}: profit {out['verdict']}  sharpe={sharpe:.2f} net={tot:+.1%} dd={dd:.1%}")
    return out


def main():
    profit_claim(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                 out_path=pathlib.Path(sys.argv[1]).resolve().parent.parent.parent / "try_04" / f"profit_{sys.argv[2]}.yaml")


if __name__ == "__main__":
    main()
