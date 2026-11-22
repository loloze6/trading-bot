def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=15).std().shift(1)
            z = r / vol
            ret90 = c / c.shift(90) - 1
            fall = np.where(ret90.notna(), ret90 < 0, b["regime"].eq("mean_reversion"))
            ret30 = c / c.shift(30) - 1
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "r": r,
                              "fall": fall, "ret30": ret30, "vol": vol,
                              "fc": b["forecast"].astype(float),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "wd": pd.to_datetime(b["timestamp"]).dt.weekday})
            for h in (1, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = {}
    for h in (1, 3, 5):
        g = D[D["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        drift[h] = g
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(g)
    D["vrel"] = D["vol"] / D.groupby("coin")["vol"].transform("median")
    bins = [-np.inf, -3, -2, -1, 1, 2, 3, np.inf]
    D["zb"] = pd.cut(D["z"], bins)
    def summ(df, col):
        x = df[col].dropna()
        n = len(x)
        if n < 3: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    out = {}
    for h in (1, 3, 5):
        S = D[D["pos"] % h == 0]
        t = S.groupby(["fall", "zb"], observed=True).apply(lambda g: summ(g, f"u{h}")).unstack(0) if False else \
            S.groupby(["fall", "zb"], observed=True).apply(lambda g: summ(g, f"u{h}"))
        out[f"unusual fwd {h}d by fall,z"] = t
    # vol level, in falling, bounce z>2 vs all
    S = D.copy()
    S["vb"] = pd.qcut(S["vrel"], 3, labels=["lowvol", "midvol", "highvol"])
    out["fwd1 by vol level,fall"] = S.groupby(["fall", "vb"], observed=True).apply(lambda g: summ(g, "u1"))
    out["fwd1 bounce z>2 in fall by vol level"] = S[(S.fall) & (S.z > 2)].groupby("vb", observed=True).apply(lambda g: summ(g, "u1"))
    out["fwd1 by weekday"] = D.groupby("wd").apply(lambda g: summ(g, "u1"))
    D["ret30b"] = pd.qcut(D["ret30"], 5)
    out["fwd1 bounce z>2 by 30d return quintile"] = D[D.z > 2].groupby("ret30b", observed=True).apply(lambda g: summ(g, "u1"))
    out["fwd5 grid by 30d return quintile"] = D[D.pos % 5 == 0].groupby("ret30b", observed=True).apply(lambda g: summ(g, "u5"))
    # book by window
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    DD = pd.concat(dd)
    bk = DD.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    bw = bk.groupby(level=0).agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "size"))
    bw["book_mean"] *= 100; bw["coin_mean"] *= 100
    out["book by window (% per day)"] = bw
    return out
