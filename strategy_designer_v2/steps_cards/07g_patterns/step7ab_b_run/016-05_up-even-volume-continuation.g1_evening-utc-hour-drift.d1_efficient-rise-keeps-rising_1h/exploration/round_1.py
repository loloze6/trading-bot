def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            if n < 3 * H:
                continue
            lr = np.r_[np.nan, np.diff(np.log(c))]
            s = pd.Series(lr)
            absr = s.abs()
            sumabs = absr.rolling(H).sum()
            maxabs = absr.rolling(H).max()
            top3 = absr.rolling(H).apply(lambda x: np.sort(x)[-3:].sum(), raw=True)
            vs = pd.Series(v)
            vshare = vs.rolling(H).max() / vs.rolling(H).sum()
            ret72 = pd.Series(c) / pd.Series(c).shift(H) - 1
            lr72 = np.log(pd.Series(c) / pd.Series(c).shift(H))
            er = lr72.abs() / sumabs
            rv = s.rolling(H).std()
            rv720 = s.rolling(720).std()
            ret24 = pd.Series(c) / pd.Series(c).shift(24) - 1
            fwd = pd.Series(c).shift(-H) / pd.Series(c) - 1
            fwd24 = pd.Series(c).shift(-24) / pd.Series(c) - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n, H):
                rows.append(dict(coin=coin, w=w, ret72=ret72.iloc[i], er=er.iloc[i],
                                 jump=maxabs.iloc[i] / sumabs.iloc[i] if sumabs.iloc[i] > 0 else np.nan,
                                 top3=top3.iloc[i] / sumabs.iloc[i] if sumabs.iloc[i] > 0 else np.nan,
                                 vshare=vshare.iloc[i], rvratio=rv.iloc[i] / rv720.iloc[i] if rv720.iloc[i] > 0 else np.nan,
                                 ret24=ret24.iloc[i], fwd=fwd.iloc[i], fwd24=fwd24.iloc[i],
                                 dow=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                 fc=b["forecast"].iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd", "ret72"])
    g = d.groupby("coin")["fwd"]
    d["mu"] = g.transform("mean"); d["sd"] = g.transform("std")
    d["ex"] = d["fwd"] - d["mu"]; d["z"] = d["ex"] / d["sd"]
    d["sign"] = np.sign(d["ret72"])
    d["zdir"] = d["z"] * d["sign"]
    d["rz"] = d["ret72"] / d.groupby("coin")["ret72"].transform("std")
    out = {}
    def tab(df, key, val="z", q=5):
        df = df.dropna(subset=[key, val]).copy()
        df["q"] = df.groupby("coin")[key].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        r = df.groupby("q")[val].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["key_mean"] = df.groupby("q")[key].mean()
        return r.drop(columns="std")
    out["z by ret72 quintile"] = tab(d, "ret72")
    up = d[d.ret72 > 0]; dn = d[d.ret72 < 0]
    out["up: z by ER quintile"] = tab(up, "er")
    out["down: z by ER quintile"] = tab(dn, "er")
    out["zdir by jump share quintile (all moves)"] = tab(d, "jump", "zdir")
    out["zdir by top3 share quintile"] = tab(d, "top3", "zdir")
    out["zdir by vol-concentration quintile"] = tab(d, "vshare", "zdir")
    out["z by vol ratio quintile"] = tab(d, "rvratio")
    big = d[d.rz.abs() > 1]
    out["big moves: zdir by jump quintile"] = tab(big, "jump", "zdir")
    # regression: zdir on |rz|, er, jump, vshare
    dd = d.dropna(subset=["er", "jump", "vshare", "zdir"])
    X = np.column_stack([np.ones(len(dd)), dd.rz.abs(), dd.er, dd.jump, dd.vshare])
    beta, *_ = np.linalg.lstsq(X, dd.zdir.values, rcond=None)
    res = dd.zdir.values - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=X.shape[1])
    out["ols zdir ~ |rz|,er,jump,vshare"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
                                                        index=["c", "absrz", "er", "jump", "vshare"])
    out["z by weekday of grid"] = d.groupby("dow")["z"].agg(["mean", "count"])
    out["z by year"] = d.groupby("yr")["z"].agg(["mean", "count"])
    out["up: z by ER, per coin (q-rank corr)"] = up.groupby("coin").apply(lambda x: stats.spearmanr(x.er, x.z, nan_policy="omit")[0])
    out["down: z by ER, per coin"] = dn.groupby("coin").apply(lambda x: stats.spearmanr(x.er, x.z, nan_policy="omit")[0])
    out["coin z by ret72 rank corr"] = d.groupby("coin").apply(lambda x: stats.spearmanr(x.ret72, x.z)[0])
    # book: daily returns, worst/best days context
    dl = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dl.append(x)
    D = pd.concat(dl)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window: mean, holding mean"] = bk.groupby(level=0).mean().assign(n=bk.groupby(level=0).size())
    return out
