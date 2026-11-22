import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        allr = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(allr); usual[coin] = np.std(allr)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            hi = c.rolling(30).max(); lo = c.rolling(30).min()
            rng = (hi - lo)
            pos = 2 * (c - lo) / rng - 1
            flat = 1 - (c - c.shift(29)).abs() / rng
            r30 = c / c.shift(29) - 1
            r10 = c / c.shift(10) - 1
            fwd = c.shift(-H) / c - 1
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                    fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i], pos=pos.iloc[i], flat=flat.iloc[i],
                    r30=r30.iloc[i], r10=r10.iloc[i], fwd=fwd.iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i],
                    un=fwd.iloc[i] - drift[coin], z=(fwd.iloc[i] - drift[coin]) / usual[coin]))
    g = pd.DataFrame(rows)
    out = {}
    cases = g[g.fc <= -2].copy()
    cases["short_un"] = -cases.un
    def summ(x, col="short_un"):
        v = x[col].dropna()
        return pd.Series(dict(n=len(v), mean=v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan))
    out["cases_by_coin"] = cases.groupby("coin").apply(summ)
    out["cases_by_year"] = cases.groupby("year").apply(summ)
    cases["fq"] = pd.qcut(cases.fc.rank(method="first"), 4, labels=["strong", "q2", "q3", "weak"])
    out["cases_by_fc_quartile"] = cases.groupby("fq").apply(summ)
    cases["r30q"] = pd.qcut(cases.r30, 4, labels=False)
    out["cases_by_r30_quartile"] = cases.groupby("r30q").apply(summ)
    cases["r10q"] = pd.qcut(cases.r10, 4, labels=False)
    out["cases_by_r10_quartile"] = cases.groupby("r10q").apply(summ)
    # all grid bars with range info: forward unusual move (long direction) by position and regime
    a = g.dropna(subset=["pos", "fwd"]).copy()
    a["posb"] = pd.cut(a.pos, [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01], labels=["bot", "lo", "mid", "hi", "top"])
    a["flatb"] = pd.qcut(a.flat, 3, labels=["trendy", "mid", "flat"])
    a["long_un"] = a.un
    t = a.groupby(["reg", "posb"]).apply(lambda x: summ(x, "long_un"))
    out["all_long_un_by_regime_pos"] = t
    t2 = a[a.reg == "mean_reversion"].groupby(["flatb", "posb"]).apply(lambda x: summ(x, "long_un"))
    out["mr_long_un_by_flat_pos"] = t2
    # book
    d = pd.concat([df.assign(coin=c, w=w) for c, ws in days.items() for w, df in ws.items()])
    bd = d.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    out["book_by_window"] = bd.groupby("w").agg(book=("br", "mean"), coin=("cr", "mean"), n=("br", "size"))
    out["drift_usual"] = pd.DataFrame(dict(drift=drift, usual=usual))
    out["share_grid_short"] = float((g.alloc < 0).mean())
    return out
