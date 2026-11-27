def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    drifts = {}
    for coin, wins in data["bars"].items():
        for h in [1, 2, 3, 5]:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                rr += [c[i + h] / c[i] - 1 for i in range(0, len(c) - h, h)]
            drifts[(coin, h)] = np.mean(rr) if rr else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; hi = b["high"].values; lo = b["low"].values
            rng = hi - lo
            cl = np.where(rng > 0, (hi - c) / np.where(rng > 0, rng, 1), np.nan)
            rp = pd.Series(rng / c)
            relr = (rp / rp.rolling(30, min_periods=10).mean().shift(1)).values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd = pd.Series(r1).rolling(30, min_periods=10).std().shift(1).values
            fc = b["forecast"].values; reg = b["regime"].astype(str).values
            sig = (reg == "mean_reversion") & (fc < 0)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in [1, 2, 3, 5]:
                for k in range(0, len(b), h):
                    idx = [i for i in range(k, min(k + h, len(b))) if sig[i]]
                    if not idx: continue
                    i = idx[0]
                    if i + h >= len(b): continue
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, yr=yr[i], fc=fc[i], cl=cl[i], relr=relr[i],
                                     z1=r1[i] / sd[i] if sd[i] > 0 else np.nan,
                                     u=-(r - drifts[(coin, h)]), tot=-r))
    df = pd.DataFrame(rows)
    def summ(g):
        x = g["u"].dropna(); n = len(x)
        return pd.Series(dict(n=n, mean_u=x.mean(), t=x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                              mean_total=g["tot"].mean()))
    out["strategy cases by h"] = df.groupby("h").apply(summ).round(4)
    d3 = df[df.h == 3].copy()
    out["h3 cases by coin"] = d3.groupby("coin").apply(summ).round(4)
    out["h3 cases by year"] = d3.groupby("yr").apply(summ).round(4)
    d3["z1q"] = pd.qcut(d3.z1, 3, labels=["deep fall", "mid", "mild fall"])
    out["h3 by own-day fall in usual swings"] = d3.groupby("z1q").apply(summ).round(4)
    d3["rq"] = pd.qcut(d3.relr, 3, labels=["narrow", "mid", "wide"])
    out["h3 by range vs its 30-day mean"] = d3.groupby("rq").apply(summ).round(4)
    out["h3 by range, ZEC only"] = d3[d3.coin == "ZECUSD"].groupby("rq").apply(summ).round(4)
    out["h3 by fc half"] = d3.groupby(pd.qcut(d3.fc.abs(), 2, labels=["smaller", "larger"])).apply(summ).round(4)
    g = d3.dropna(subset=["z1", "relr"])
    out["h3 spearman z1, relr, cl vs u"] = pd.DataFrame({k: stats.spearmanr(g[k], g.u) for k in ["z1", "relr", "cl"]},
                                                         index=["rho", "p"]).round(4)
    return out
