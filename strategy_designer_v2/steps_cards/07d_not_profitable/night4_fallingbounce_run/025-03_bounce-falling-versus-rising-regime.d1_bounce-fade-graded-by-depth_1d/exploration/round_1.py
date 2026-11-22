def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = b["close"].astype(float).reset_index(drop=True)
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            z1 = r1 / sd
            r90 = c / c.shift(90) - 1
            r30 = c / c.shift(30) - 1
            z30 = r30 / (sd * np.sqrt(30))
            r60 = c / c.shift(60) - 1
            f5 = c.shift(-5) / c - 1
            fc = b["forecast"].reset_index(drop=True)
            alloc = b["postRebalance_current_allocation"].reset_index(drop=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z1": z1, "r90": r90, "r60": r60, "z30": z30,
                               "f5": f5, "fc": fc, "alloc": alloc, "pos": np.arange(len(c)), "n": len(c)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    grid = d[(d.pos % 5 == 0) & d.f5.notna()].copy()
    drift = grid.groupby("coin").f5.mean()
    usual = grid.groupby("coin").f5.std()
    grid["u5"] = grid.f5 - grid.coin.map(drift)
    out = {}
    out["window length bars"] = d.groupby("coin").n.describe()
    out["share bars r90 known"] = d.r90.notna().mean()
    out["drift and usual 5d"] = pd.DataFrame({"drift": drift, "usual": usual})
    # rises by threshold and regime
    res = []
    for th in [0.5, 1.0, 1.5, 2.0]:
        for reg, m in [("r90<0", grid.r90 < 0), ("r90>0", grid.r90 > 0), ("r60<0", grid.r60 < 0)]:
            g = grid[(grid.z1 >= th) & m]
            n = len(g)
            t = g.u5.mean() / (g.u5.std() / np.sqrt(n)) if n > 2 else np.nan
            res.append({"th": th, "reg": reg, "n": n, "mean f5": g.f5.mean(), "mean unusual": g.u5.mean(), "t": t})
    out["rises 5d after (grid)"] = pd.DataFrame(res)
    # all bars in falling regime, graded by z30
    g = grid[grid.r90 < 0].copy()
    g["q"] = pd.qcut(g.z30, 5, labels=False, duplicates="drop")
    out["r90<0 all bars by z30 quintile"] = g.groupby("q").agg(n=("u5", "size"), z30=("z30", "mean"), u5=("u5", "mean"), f5=("f5", "mean"))
    g2 = grid[(grid.r90 < 0) & (grid.z1 >= 1.0)].copy()
    if len(g2) > 20:
        g2["q"] = pd.qcut(g2.z30, 3, labels=False, duplicates="drop")
        out["r90<0 rise>=1 by z30 tercile"] = g2.groupby("q").agg(n=("u5", "size"), z30=("z30", "mean"), u5=("u5", "mean"))
    # falling regime by z1 bins
    g3 = grid[grid.r90 < 0].copy()
    g3["b"] = pd.cut(g3.z1, [-99, -2, -1, 0, 1, 2, 99])
    out["r90<0 by z1 bin"] = g3.groupby("b").agg(n=("u5", "size"), u5=("u5", "mean"), f5=("f5", "mean"))
    g4 = grid[grid.r90 > 0].copy()
    g4["b"] = pd.cut(g4.z1, [-99, -2, -1, 0, 1, 2, 99])
    out["r90>0 by z1 bin"] = g4.groupby("b").agg(n=("u5", "size"), u5=("u5", "mean"), f5=("f5", "mean"))
    # book activity
    out["share bars in position"] = (d.alloc.abs() > 1e-6).groupby(d.coin).mean()
    out["bars with fc<0 per coin"] = (d.fc < 0).groupby(d.coin).sum()
    tr = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)], ignore_index=True)
    if len(tr):
        out["trades"] = tr.groupby(["coin", "side"]).agg(n=("net_profit_loss_percent", "size"),
                     gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
                     dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    return out
