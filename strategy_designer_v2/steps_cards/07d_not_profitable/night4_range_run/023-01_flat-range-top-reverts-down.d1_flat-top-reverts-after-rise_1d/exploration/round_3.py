import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; H = 5
    rows = []
    for coin, ws in bars.items():
        allr = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        dr = np.mean(allr); us = np.std(allr)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            hi = c.rolling(30).max(); lo = c.rolling(30).min(); rng = hi - lo
            pos = 2 * (c - lo) / rng - 1
            flat = 1 - (c - c.shift(29)).abs() / rng
            fwd = c.shift(-H) / c - 1
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 reg=b["regime"].iloc[i], fc=b["forecast"].iloc[i], pos=pos.iloc[i],
                                 flat=flat.iloc[i], fwd=fwd.iloc[i], un=fwd.iloc[i] - dr,
                                 z=(fwd.iloc[i] - dr) / us))
    g = pd.DataFrame(rows).dropna(subset=["pos", "flat", "fwd"])
    edges = g.flat.quantile([0, .2, .4, .6, .8, 1]).values
    edges[0] -= 1e-9; edges[-1] += 1e-9
    g["flatq"] = pd.cut(g.flat, edges, labels=["f1trend", "f2", "f3", "f4", "f5flat"])
    out = {}
    cases = g[g.fc <= -2]
    out["cases_share_by_flatq"] = cases.groupby("flatq").apply(lambda x: pd.Series(dict(
        n=len(x), share=len(x) / len(cases), short_un=-x.un.mean(),
        t=-x.un.mean() / (x.un.std() / np.sqrt(len(x))))))
    def st(x, col):
        v = x[col]
        return pd.Series(dict(n=len(v), mean=v.mean(), z=x.z.mean() * np.sign(v.mean()) if len(v) else np.nan,
                              t=v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan))
    top = g[(g.pos > 0.2)].copy()
    top["short_un"] = -top.un
    top["short_z"] = -top.z
    out["above_mid_short_un_by_reg_flatq"] = top.groupby(["reg", "flatq"]).apply(lambda x: pd.Series(dict(
        n=len(x), un=x.short_un.mean(), z=x.short_z.mean(),
        t=x.short_un.mean() / (x.short_un.std() / np.sqrt(len(x))))))
    f5 = top[top.flatq == "f5flat"]
    out["f5_above_mid_by_year"] = f5.groupby("year").apply(lambda x: pd.Series(dict(
        n=len(x), un=x.short_un.mean())))
    out["f5_above_mid_by_coin"] = f5.groupby("coin").apply(lambda x: pd.Series(dict(
        n=len(x), un=x.short_un.mean())))
    g["dev"] = g.pos * g.flat ** 3
    g["dq"] = pd.qcut(g.dev, 5, labels=False)
    out["un_by_flatcubed_dev_quintile_mr"] = g[g.reg == "mean_reversion"].groupby("dq").apply(lambda x: pd.Series(dict(
        n=len(x), un=x.un.mean(), t=x.un.mean() / (x.un.std() / np.sqrt(len(x))))))
    mr = g[(g.reg == "mean_reversion") & (g.flatq.isin(["f1trend", "f2"]))].copy()
    mr["mom"] = np.sign(mr.pos) * mr.un
    mr["mtot"] = np.sign(mr.pos) * mr.fwd
    out["mr_trend_momentum_by_year"] = mr.groupby("year").apply(lambda x: pd.Series(dict(
        n=len(x), un=x.mom.mean(), tot=x.mtot.mean())))
    return out
