def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            r = np.full(len(c), np.nan); r[1:] = c[1:]/c[:-1]-1
            allr.append(r[1:])
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            r = np.full(n, np.nan); r[1:] = c[1:]/c[:-1]-1
            nxt = np.full(n, np.nan); nxt[:-1] = c[1:]/c[:-1]-1
            vol = pd.Series(r).rolling(20, min_periods=20).std().values
            df = pd.DataFrame({"coin": coin, "win": w, "r": r, "nxt": nxt - mu,
                               "z": r/vol, "alloc": b["postRebalance_current_allocation"].astype(float).values,
                               "regime": b["regime"].values,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                               "year": pd.to_datetime(b["timestamp"]).dt.year.values})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["r", "nxt"])
    d = d[d["r"] != 0]
    d["rev"] = -np.sign(d["r"]) * d["nxt"]
    d["gain"] = d["alloc"] * d["nxt"]
    d["act"] = d["regime"] == "mean_reversion"
    d["side"] = np.where(d["r"] < 0, "down", "up")
    d["zb"] = pd.cut(d["z"].abs(), [0, 0.5, 1, 1.5, 2, 100])

    def tstat(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["rev by active x side"] = d.groupby(["act", "side"])["rev"].apply(tstat).unstack()
    out["rev by active x |z| bucket x side"] = d.groupby(["act", "zb", "side"], observed=True)["rev"].apply(tstat).unstack()
    a = d[d["act"]]
    out["active down-up by coin"] = a.groupby("coin").apply(lambda g: pd.Series({
        "diff": g.loc[g.side == "down", "rev"].mean() - g.loc[g.side == "up", "rev"].mean(),
        "welch_t": stats.ttest_ind(g.loc[g.side == "down", "rev"], g.loc[g.side == "up", "rev"], equal_var=False).statistic,
        "gain_t": g["gain"].mean()/(g["gain"].std()/np.sqrt(len(g)))}))
    out["active gain by year"] = a.groupby("year")["gain"].apply(tstat).unstack()
    out["active rev by weekday x side"] = a.groupby(["wd", "side"])["rev"].apply(tstat).unstack()
    out["gain by position side"] = a.assign(ps=np.sign(a["alloc"])).groupby("ps")["gain"].apply(tstat).unstack()
    out["inactive rev x z corr"] = d[~d.act].groupby("coin").apply(lambda g: stats.spearmanr(g["z"], g["nxt"], nan_policy="omit")[0])
    return out
