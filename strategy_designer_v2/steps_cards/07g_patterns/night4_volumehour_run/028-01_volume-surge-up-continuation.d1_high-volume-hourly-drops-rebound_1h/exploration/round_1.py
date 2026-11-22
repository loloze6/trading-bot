def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    # drift per coin per horizon, non-overlapping grid
    def grid_ret(c, h):
        r = c.shift(-h) / c - 1
        return r.iloc[::h].dropna()
    drift = {}
    for coin in bars:
        for h in (1, 3, 6, 24):
            drift[(coin, h)] = pd.concat([grid_ret(df["close"].reset_index(drop=True), h) for df in bars[coin].values()]).mean()
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]; v = df["volume"]
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            z = r1 / sd
            vr = v / v.rolling(720, min_periods=240).mean()
            rv24 = r1.rolling(24).std() / sd
            r24p = (c / c.shift(24) - 1) / (sd * np.sqrt(24))
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)), "z": z, "vr": vr,
                              "rv24": rv24, "r24p": r24p, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                              "alloc": df["postRebalance_current_allocation"]})
            for h in (1, 3, 6, 24):
                d[f"f{h}"] = (c.shift(-h) / c - 1) - drift[(coin, h)]
            rows.append(d)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["z", "vr"])
    def thin(sub, h):
        keep = []
        for (coin, w), g in sub.groupby(["coin", "w"]):
            last = -10**9
            for p, idx in zip(g["pos"].values, g.index.values):
                if p - last >= h:
                    keep.append(idx); last = p
        return sub.loc[keep]
    A["zb"] = pd.cut(A["z"].abs(), [0, 1, 2, 3, 5, 100], labels=["<1", "1-2", "2-3", "3-5", ">5"])
    A["vb"] = pd.cut(A["vr"], [0, 1, 2, 4, 1e9], labels=["v<1", "v1-2", "v2-4", "v>4"])
    A["dir"] = np.where(A["z"] > 0, "up", "down")
    res = []
    for (dr, zb, vb), g in A[A["z"].abs() >= 2].groupby(["dir", "zb", "vb"], observed=True):
        for h in (6, 24):
            t = thin(g.dropna(subset=[f"f{h}"]), h)
            if len(t) < 15: continue
            x = t[f"f{h}"] * np.sign(t["z"])  # continuation sign
            res.append({"dir": dr, "zb": zb, "vb": vb, "h": h, "n": len(t),
                        "cont_mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["continuation_by_dir_z_vol"] = pd.DataFrame(res)
    # past 24h move (standardised) vs next 24h, non-overlapping grid
    G = A[A["pos"] % 24 == 0].dropna(subset=["r24p", "f24"]).copy()
    G["q"] = pd.qcut(G["r24p"], 5, labels=False)
    out["next24_by_past24_quintile"] = G.groupby("q").apply(lambda g: pd.Series({"n": len(g), "mean%": 100*g["f24"].mean(), "t": g["f24"].mean()/(g["f24"].std()/np.sqrt(len(g)))}))
    G["vq"] = pd.qcut(G["rv24"], 5, labels=False)
    out["next24_by_rvol24_quintile"] = G.groupby("vq").apply(lambda g: pd.Series({"n": len(g), "mean%": 100*g["f24"].mean(), "abs%": 100*g["f24"].abs().mean(), "t": g["f24"].mean()/(g["f24"].std()/np.sqrt(len(g)))}))
    H = A.dropna(subset=["f1"])
    out["f1_by_hour"] = H.groupby("hour").apply(lambda g: pd.Series({"mean_bp": 1e4*g["f1"].mean(), "t": g["f1"].mean()/(g["f1"].std()/np.sqrt(len(g)))}))
    G2 = A[A["pos"] % 24 == 0].dropna(subset=["f24"])
    out["f24_by_weekday"] = G2.groupby("wd").apply(lambda g: pd.Series({"n": len(g), "mean%": 100*g["f24"].mean(), "t": g["f24"].mean()/(g["f24"].std()/np.sqrt(len(g)))}))
    # book days
    D = pd.concat([df.assign(coin=c, w=w) for c in data["days"] for w, df in data["days"][c].items()]).dropna(subset=["book_return"])
    D["ex"] = D["book_return"]
    q = D["book_return"].quantile([0.02, 0.98])
    out["book_extreme_days"] = pd.DataFrame({
        "worst2%_book": [D[D.book_return <= q.iloc[0]]["book_return"].mean(), D[D.book_return <= q.iloc[0]]["coin_return"].mean()],
        "best2%_book": [D[D.book_return >= q.iloc[1]]["book_return"].mean(), D[D.book_return >= q.iloc[1]]["coin_return"].mean()]},
        index=["book", "coin"])
    out["mean_alloc"] = float(A["alloc"].mean())
    out["share_in_position"] = float((A["alloc"].abs() > 1e-6).mean())
    return out
