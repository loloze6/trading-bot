"""Diagnosis of the full-data verdicts (not a verdict). For three plans, the signed excess forward return of the
in-position blocks against two references: the mean of the same window (what the plans use) and the coin's mean over
all its windows; and the raw in-position minus flat difference. Also each coin's book and hold log-returns.
Run from 04_backtest/full_data_run/backtests with the venv's Python."""
import pandas as pd, numpy as np, glob, os
H = 10
for plan in ["002-01_sma-golden-cross-upward-drift_1d", "002-03_price-cross-above-long-sma_1d", "002-02_sma-death-cross-downward-drift_1d"]:
    print("==", plan)
    rows = []
    for c in sorted(os.listdir(plan)):
        if not os.path.isdir(f"{plan}/{c}"): continue
        book = hold = 0.0; act = []
        for f in sorted(glob.glob(f"{plan}/{c}/w*/bars.csv.gz"), key=lambda p: int(p.split("/")[-2][1:])):
            d = pd.read_csv(f, low_memory=False)
            fw = d.close.shift(-H) / d.close - 1
            g = pd.DataFrame({"f": d.forecast.iloc[::H].values, "fw": fw.iloc[::H].values, "wmean": fw.mean(), "coin": c})
            rows.append(g.dropna())
            book += np.log(d.portfolio_value.iloc[-1] / d.portfolio_value.iloc[0]); hold += np.log(d.close.iloc[-1] / d.close.iloc[0])
            act.append((d.forecast != 0).mean())
        print(f"  {c}: book log-return {book:+.2f}, hold {hold:+.2f}, active {np.mean(act):.0%}")
    g = pd.concat(rows); side = np.sign(g.f); on, off = g[side != 0], g[side == 0]
    pooled = g.groupby("coin").fw.transform("mean")
    t = lambda x: x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    ex_w = (on.fw - on.wmean) * np.sign(on.f); ex_p = (on.fw - pooled[side != 0]) * np.sign(on.f)
    print(f"  signed excess vs window mean: {ex_w.mean():+.4f} t {t(ex_w):+.2f}; vs coin's all-window mean: {ex_p.mean():+.4f} t {t(ex_p):+.2f}")
    print(f"  in-position minus flat (raw): {on.fw.mean() - off.fw.mean():+.4f}")
