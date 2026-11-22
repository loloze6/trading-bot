def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            fwd = c.shift(-H) / c - 1
            past = c / c.shift(H) - 1
            past6 = c / c.shift(36) - 1
            r1 = c.pct_change()
            vr = v / v.rolling(180, min_periods=45).mean()
            vtrend = v.rolling(6).mean() / v.rolling(18).mean()
            sgn = np.sign(r1).fillna(0)
            run = sgn.groupby((sgn != sgn.shift()).cumsum()).cumcount() + 1
            run = run * sgn
            up18 = (r1 > 0).rolling(18).sum()
            vol = r1.rolling(180, min_periods=45).std()
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.iloc[idx].values, "past": past.iloc[idx].values,
                "past6": past6.iloc[idx].values, "vr": vr.iloc[idx].values, "vtrend": vtrend.iloc[idx].values,
                "run": run.iloc[idx].values, "up18": up18.iloc[idx].values, "vol": vol.iloc[idx].values,
                "fc": b["forecast"].iloc[idx].values, "pos": b["postRebalance_current_allocation"].iloc[idx].values,
                "hour": ts.iloc[idx].dt.hour.values, "wd": ts.iloc[idx].dt.weekday.values,
                "year": ts.iloc[idx].dt.year.values})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"]).reset_index(drop=True)
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    sd = D.groupby("coin")["fwd"].transform("std")
    D["z"] = D["ex"] / sd
    D["pastz"] = D["past"] / sd
    D["past6z"] = D["past6"] / (sd * np.sqrt(2))
    D["volq"] = D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    def tab(g):
        x = g["z"].dropna()
        return pd.Series({"n": len(x), "mean_z": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan,
                          "mean_ex_pct": g["ex"].mean() * 100})
    out = {}
    def safe(name, f):
        try:
            out[name] = f()
        except Exception as e:
            out[name] = "err: " + str(e)[:80]
    def qtab(col, k=5):
        E = D.dropna(subset=[col]).copy()
        E["q"] = pd.qcut(E[col], k, labels=False, duplicates="drop")
        return E.groupby("q").apply(tab)
    safe("by_past3d_quintile", lambda: qtab("pastz"))
    safe("by_past6d_quintile", lambda: qtab("past6z"))
    safe("by_vr_quintile", lambda: qtab("vr"))
    safe("by_up18_count", lambda: D.dropna(subset=["up18"]).groupby(pd.cut(D["up18"], [-1, 5, 7, 8, 9, 10, 12, 18])).apply(tab))
    safe("by_vol_quintile", lambda: D.dropna(subset=["volq"]).groupby("volq").apply(tab))
    def pv():
        E = D.dropna(subset=["pastz", "vtrend"]).copy()
        E["pq"] = pd.qcut(E["pastz"], 3, labels=["down", "mid", "up"])
        E["vq"] = pd.qcut(E["vtrend"], 3, labels=["fade", "mid", "rise"])
        return E.groupby(["pq", "vq"]).apply(tab)
    safe("past3d_x_voltrend", pv)
    def pvr():
        E = D.dropna(subset=["pastz", "vr"]).copy()
        E["pq"] = pd.qcut(E["pastz"], 3, labels=["down", "mid", "up"])
        E["vq"] = pd.qcut(E["vr"], 3, labels=["lowvol", "mid", "highvol"])
        return E.groupby(["pq", "vq"]).apply(tab)
    safe("past3d_x_volratio", pvr)
    def pvq():
        E = D.dropna(subset=["pastz", "volq"]).copy()
        E["pq"] = pd.qcut(E["pastz"], 3, labels=["down", "mid", "up"])
        return E.groupby(["volq", "pq"]).apply(tab)
    safe("volq_x_past3d", pvq)
    safe("by_runlen", lambda: D.groupby(D["run"].clip(-5, 5)).apply(tab))
    safe("by_hour", lambda: D.groupby("hour").apply(tab))
    safe("by_weekday", lambda: D.groupby("wd").apply(tab))
    safe("by_year", lambda: D.groupby("year").apply(tab))
    safe("by_coin", lambda: D.groupby("coin").apply(tab))
    safe("by_forecast_band", lambda: D.groupby(pd.cut(D["fc"], [-0.1, 0.01, 2, 8, 20.1])).apply(tab))
    def sp():
        E = D.dropna(subset=["pastz", "z"])
        r = {"past3d": stats.spearmanr(E["pastz"], E["z"])[0], "n": len(E)}
        E2 = D.dropna(subset=["vr", "z"]); r["vr"] = stats.spearmanr(E2["vr"], E2["z"])[0]
        E3 = D.dropna(subset=["vtrend", "z"]); r["vtrend"] = stats.spearmanr(E3["vtrend"], E3["z"])[0]
        return pd.Series(r)
    safe("spearman", sp)
    def tails():
        dd = []
        for coin, wins in data["days"].items():
            for w, x in wins.items():
                x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
        DD = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
        q = DD["book_return"].quantile([0.01, 0.99])
        DD["bucket"] = np.where(DD["book_return"] <= q.iloc[0], "worst1%", np.where(DD["book_return"] >= q.iloc[1], "best1%", "other"))
        DD["wd"] = pd.to_datetime(DD["day"]).dt.weekday
        return {"tails": DD.groupby("bucket").agg(n=("book_return", "count"), book=("book_return", "mean"), coin=("coin_return", "mean")),
                "book_by_wd": DD.groupby("wd").agg(n=("book_return", "count"), book=("book_return", "mean"), coin=("coin_return", "mean"))}
    try:
        t = tails(); out["book_tails"] = t["tails"]; out["book_by_weekday"] = t["book_by_wd"]
    except Exception as e:
        out["book_tails"] = "err: " + str(e)[:80]
    return out
