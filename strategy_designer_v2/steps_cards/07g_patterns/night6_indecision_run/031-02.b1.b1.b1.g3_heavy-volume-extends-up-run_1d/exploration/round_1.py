import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["ret6"] = c / c.shift(6) - 1
            d["r1"] = c / c.shift(1) - 1
            d["vr"] = v / v.shift(1).rolling(20).mean() - 1
            d["fwd3"] = c.shift(-3) / c - 1
            rng = (b["high"] - b["low"]) / c
            d["rngr"] = rng / rng.shift(1).rolling(20).mean()
            d["body"] = (b["close"] - b["open"]).abs() / (b["high"] - b["low"]).replace(0, np.nan)
            d["clv"] = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            d["sd20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["sd20"].shift(1)
            d["fc"] = b["forecast"]
            d["grid"] = (np.arange(len(b)) % 3 == 0)
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    g = df[df.grid & df.fwd3.notna()].copy()
    g["ex"] = g.fwd3 - g.groupby("coin").fwd3.transform("mean")
    usual = g.groupby("coin").fwd3.transform("std")
    g["str"] = g.ex / usual
    g["day"] = g.ts.dt.floor("D")
    g["wd"] = g.ts.dt.weekday
    g["year"] = g.ts.dt.year

    def summ(sub):
        x = sub.ex; n = len(x)
        if n < 10: return pd.Series({"n": n})
        m = x.mean(); ds = (x - m).groupby(sub.day).sum()
        se = np.sqrt((ds**2).sum()) / n
        return pd.Series({"n": n, "mean_ex%": 100*m, "t_day": m/se, "strength": sub.str.mean()})

    out = {}
    up = g[g.ret6 > 0]; dn = g[g.ret6 <= 0]
    out["up6 by vr quintile"] = up.groupby(pd.qcut(up.vr, 5, duplicates="drop"), observed=True).apply(summ)
    out["down6 by vr quintile"] = dn.groupby(pd.qcut(dn.vr, 5, duplicates="drop"), observed=True).apply(summ)
    out["all by ret6 decile"] = g.groupby(pd.qcut(g.ret6, 10), observed=True).apply(summ)
    out["by z1 decile (last day move/vol)"] = g.groupby(pd.qcut(g.z1, 10), observed=True).apply(summ)
    out["by rng ratio quintile"] = g.groupby(pd.qcut(g.rngr, 5), observed=True).apply(summ)
    out["by close location quintile"] = g.groupby(pd.qcut(g.clv, 5), observed=True).apply(summ)
    # brief: wide-flat after up run
    wf = g[(g.rngr > 1.5) & (g.body < 0.25)]
    out["wide-flat by run sign"] = wf.groupby(np.sign(wf.ret6)).apply(summ)
    nf = g[(g.rngr < 0.8) & (g.body < 0.25)]
    out["narrow-flat by run sign"] = nf.groupby(np.sign(nf.ret6)).apply(summ)
    out["by weekday"] = g.groupby("wd").apply(summ)
    out["by vol level quintile"] = g.groupby(pd.qcut(g.sd20, 5), observed=True).apply(summ)
    out["up6 heavy vs year"] = up[up.vr > 0].groupby("year").apply(summ)
    out["up6 by vr x sd20 tercile"] = up.groupby([pd.qcut(up.sd20, 3), pd.qcut(up.vr, 3)], observed=True).apply(summ)
    # book largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin))
    dd = pd.concat(dd)
    bk = dd.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    top = bk.book_return.quantile([0.01, 0.05, 0.95, 0.99])
    out["book quantiles"] = top
    out["book share of gain from top 5% days"] = float(bk.book_return[bk.book_return > top[0.95]].sum() / bk.book_return.sum())
    out["corr book vs coin daily"] = float(bk.corr().iloc[0, 1])
    return out
