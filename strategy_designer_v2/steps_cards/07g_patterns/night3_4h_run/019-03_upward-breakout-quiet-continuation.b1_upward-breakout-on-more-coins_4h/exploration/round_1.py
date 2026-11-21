def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = 18
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            if n < 220: continue
            rng = (hi - lo) / c
            mrng = rng.rolling(180).mean()
            h12 = hi.shift(1).rolling(12).max(); l12 = lo.shift(1).rolling(12).min()
            stretch = (h12 - l12) / c
            narrow = stretch / mrng  # small = narrow
            r1 = c.pct_change()
            vol = r1.rolling(180).std()
            up = (c - h12).clip(lower=0) / c; dn = (c - l12).clip(upper=0) / c
            bo = np.where(up > 0, 1, np.where(dn < 0, -1, 0))
            f = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "narrow": narrow, "bo": bo, "r1z": r1 / vol, "r6": c / c.shift(6) - 1,
                "r42": c / c.shift(42) - 1, "r180": c / c.shift(180) - 1, "vol": vol,
                "dist_hi": c / hi.rolling(180).max() - 1,
                "hour": ts.dt.hour, "wd": ts.dt.weekday, "f": f})
            df = df.iloc[::H]
            df = df[df["f"].notna()]
            recs.append(df)
        if not recs: continue
        d = pd.concat(recs)
        dr, sd = d["f"].mean(), d["f"].std()
        d["u"] = d["f"] - dr; d["z"] = d["u"] / sd; d["az"] = d["f"].abs() / sd
        d["coin"] = coin
        for col in ["narrow", "r1z", "r6", "r42", "r180", "vol", "dist_hi"]:
            d["q_" + col] = pd.qcut(d[col].rank(method="first"), 5, labels=False) if d[col].notna().sum() > 50 else np.nan
        rows.append(d)
    D = pd.concat(rows)
    def summ(g, col="z"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_z": x.mean(), "mean_u%": g.loc[x.index, "u"].mean() * 100,
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    for col in ["narrow", "r1z", "r6", "r42", "r180", "vol", "dist_hi"]:
        out["fwd18 by quintile of " + col] = D.groupby("q_" + col).apply(summ)
    out["abs move (az) by narrow quintile"] = D.groupby("q_narrow")["az"].agg(["count", "mean"])
    out["fwd by breakout sign"] = D.groupby("bo").apply(summ)
    out["fwd by breakout sign x narrow<=q1"] = D[D["q_narrow"] <= 1].groupby("bo").apply(summ)
    out["fwd by hour"] = D.groupby("hour").apply(summ)
    out["fwd by weekday"] = D.groupby("wd").apply(summ)
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin, win=w))
    B = pd.concat(bk)
    out["book vs coin daily"] = pd.Series({"book_mean": B["book_return"].mean(), "coin_mean": B["coin_return"].mean(),
        "corr": B[["book_return", "coin_return"]].corr().iloc[0, 1]})
    B["cq"] = pd.qcut(B["coin_return"].rank(method="first"), 5, labels=False)
    out["book by coin-day quintile"] = B.groupby("cq")[["book_return", "coin_return"]].mean()
    return out
