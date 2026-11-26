def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    H = [3, 5, 10]
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            act = (df["regime"] == "unknown").values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for k in [2, 3, 5]:
                rk = c / c.shift(k) - 1
                sk = rk / (sd * np.sqrt(k))
                for h in H:
                    for start in range(0, n, h):
                        for t in range(start, min(start + h, n)):
                            if act[t] and rk.iloc[t] > 0 and t + h < n and not np.isnan(sk.iloc[t]):
                                ret = c.iloc[t + h] / c.iloc[t] - 1
                                m, s = drift[(coin, h)]
                                rows.append(dict(coin=coin, w=w, k=k, h=h, day=str(df["timestamp"].iloc[t])[:10],
                                                 year=yr[t], sk=sk.iloc[t], unus=-(ret - m), tot=-ret,
                                                 strength=-(ret - m) / s))
                                break
    d = pd.DataFrame(rows)

    def clt(g):
        x = g["unus"]; mu = x.mean()
        dev = (x - mu).groupby(g["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(x) if D > 1 else np.nan
        med = g["sk"].median()
        hi = g[g.sk > med]["unus"].mean(); lo = g[g.sk <= med]["unus"].mean()
        return pd.Series(dict(n=len(x), days=D, mean_unus=mu, t=mu / se if se else np.nan,
                              mean_tot=g["tot"].mean(), strength=g["strength"].mean(),
                              hi_minus_lo=hi - lo, corr=g[["sk", "unus"]].corr().iloc[0, 1]))
    out = {}
    out["by_k_h"] = d.groupby(["k", "h"]).apply(clt)
    d35 = d[(d.k == 3) & (d.h == 5)].copy()
    d35["q"] = pd.qcut(d35["sk"], 4, labels=False)
    out["k3h5_by_quartile"] = d35.groupby("q").apply(clt)
    out["k3h5_by_year"] = d35.groupby("year").apply(clt)
    out["k3h5_by_coin"] = d35.groupby("coin").apply(clt)
    d310 = d[(d.k == 3) & (d.h == 10)].copy()
    out["k3h10_by_year"] = d310.groupby("year").apply(clt)
    return out
