import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = 18
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.nanmean(rets)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            low = f[0]; seen = set()
            for i in range(n):
                if f[i] - low >= 2:
                    low = f[i]
                    cell = i // H
                    if cell not in seen:
                        seen.add(cell)
                        pre30 = c[i] / c[i-180] - 1 if i >= 180 else np.nan
                        pre10 = c[i] / c[i-60] - 1 if i >= 60 else np.nan
                        r18 = c[i+18] / c[i] - 1 if i + 18 < n else np.nan
                        rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                         f=f[i], pre30=pre30, pre10=pre10, r18=r18))
                else:
                    low = min(low, f[i])
    d = pd.DataFrame(rows)
    d["u"] = d["r18"] - d["coin"].map(drift)
    d = d.dropna(subset=["u"])
    def summ(g):
        x = g["u"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    res = {}
    p = d.dropna(subset=["pre30"]).copy()
    p["up30"] = p["pre30"] > 0
    res["by_30d_sign"] = p.groupby("up30").apply(summ)
    for flag in (True, False):
        s = p[p["up30"] == flag].copy()
        s["fq"] = pd.qcut(s["f"].rank(method="first"), 4, labels=False)
        res[f"fq_within_up30={flag}"] = s.groupby("fq").apply(summ).join(s.groupby("fq")["f"].mean())
        res[f"year_within_up30={flag}"] = s.groupby("year").apply(summ)
    up = p[p["up30"]]
    res["coins_positive_share_up30"] = (up.groupby("coin")["u"].mean() > 0).mean()
    # 30d return graded: deciles
    p["pd"] = pd.qcut(p["pre30"].rank(method="first"), 10, labels=False)
    res["by_pre30_decile"] = p.groupby("pd").apply(summ).join(p.groupby("pd")["pre30"].mean())
    q = d.dropna(subset=["pre10"]).copy()
    q["pq"] = pd.qcut(q["pre10"].rank(method="first"), 5, labels=False)
    res["by_pre10d_quintile"] = q.groupby("pq").apply(summ).join(q.groupby("pq")["pre10"].mean())
    return res
