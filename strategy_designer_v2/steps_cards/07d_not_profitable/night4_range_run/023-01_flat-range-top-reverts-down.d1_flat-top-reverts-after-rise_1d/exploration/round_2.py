import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = 5
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
            hi = c.rolling(30).max(); lo = c.rolling(30).min()
            rng = hi - lo
            pos = 2 * (c - lo) / rng - 1
            flat = 1 - (c - c.shift(29)).abs() / rng
            widthv = rng / c / (c.pct_change().rolling(30).std() * np.sqrt(30))
            fwd = c.shift(-H) / c - 1
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 reg=b["regime"].iloc[i], pos=pos.iloc[i], flat=flat.iloc[i],
                                 wv=widthv.iloc[i], fwd=fwd.iloc[i], un=fwd.iloc[i] - dr,
                                 z=(fwd.iloc[i] - dr) / us))
    g = pd.DataFrame(rows).dropna(subset=["pos", "flat", "fwd"])
    def summ(x, col="un"):
        v = x[col].dropna()
        return pd.Series(dict(n=len(v), mean=v.mean(), tot=x["fwd"].mean(), z=x["z"].mean(),
                              t=v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan))
    out = {}
    g["flatq"] = pd.qcut(g.flat, 5, labels=["f1trend", "f2", "f3", "f4", "f5flat"])
    g["posb"] = pd.cut(g.pos, [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01], labels=["bot", "lo", "mid", "hi", "top"])
    out["mr_flatq_pos"] = g[g.reg == "mean_reversion"].groupby(["flatq", "posb"]).apply(summ)
    out["unk_flatq_pos"] = g[g.reg == "unknown"].groupby(["flatq", "posb"]).apply(summ)
    # graded: slope of un on pos*flat within flattest two quintiles vs others
    for nm, sub in [("flat45", g[g.flatq.isin(["f4", "f5flat"])]), ("flat123", g[~g.flatq.isin(["f4", "f5flat"])])]:
        x = sub.pos.values; y = sub.un.values
        b1 = np.polyfit(x, y, 1)[0]
        r = np.corrcoef(x, y)[0, 1]; n = len(x)
        out["slope_un_on_pos_" + nm] = f"slope {b1:.4f}, corr {r:.3f}, t {r*np.sqrt((n-2)/(1-r*r)):.2f}, n {n}"
    ft = g[(g.flatq.isin(["f4", "f5flat"]))]
    ft = ft.assign(side=np.sign(-ft.pos), sun=-np.sign(ft.pos) * ft.un, stot=-np.sign(ft.pos) * ft.fwd,
                   absq=pd.qcut(ft.pos.abs(), 3, labels=["near", "midd", "far"]))
    out["flat45_reversion_by_dist"] = ft.groupby("absq").apply(lambda x: pd.Series(dict(
        n=len(x), un=x.sun.mean(), tot=x.stot.mean(), t=x.sun.mean() / (x.sun.std() / np.sqrt(len(x))))))
    out["flat45_far_rev_by_year"] = ft[ft.absq == "far"].groupby("year").apply(lambda x: pd.Series(dict(
        n=len(x), un=x.sun.mean(), t=x.sun.mean() / (x.sun.std() / np.sqrt(len(x))))))
    out["flat45_far_rev_by_coin"] = ft[ft.absq == "far"].groupby("coin").apply(lambda x: pd.Series(dict(
        n=len(x), un=x.sun.mean(), t=x.sun.mean() / (x.sun.std() / np.sqrt(len(x))))))
    tr = g[g.flatq.isin(["f1trend", "f2"])]
    tr = tr.assign(mun=np.sign(tr.pos) * tr.un, mtot=np.sign(tr.pos) * tr.fwd,
                   absq=pd.qcut(tr.pos.abs(), 3, labels=["near", "midd", "far"]))
    out["trend12_momentum_by_dist"] = tr.groupby(["reg", "absq"]).apply(lambda x: pd.Series(dict(
        n=len(x), un=x.mun.mean(), tot=x.mtot.mean(), t=x.mun.mean() / (x.mun.std() / np.sqrt(len(x))))))
    return out
