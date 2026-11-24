def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts").reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            d["coin"] = coin; d["win"] = w
            d["fwd1"] = c.shift(-1) / c - 1
            d["fwd3"] = c.shift(-3) / c - 1
            d["pos"] = np.arange(len(d))
            vol = r.rolling(30, min_periods=20).std()
            d["vol30"] = vol
            d["z1"] = r / vol
            d["r20"] = c / c.shift(20) - 1
            d["z20"] = d["r20"] / (vol * np.sqrt(20))
            lo = c.rolling(365, min_periods=120).min()
            d["dist_ylo"] = (c / lo - 1) / (vol * np.sqrt(20))
            d["next_wd"] = (d["ts"] + pd.Timedelta(days=1)).dt.weekday
            d["year"] = d["ts"].dt.year
            d["day"] = d["ts"].dt.floor("D")
            d["alloc"] = d["postRebalance_current_allocation"].astype(float)
            d["bookr"] = d["postRebalance_total_value"].astype(float).pct_change()
            rows.append(d[["coin","win","day","year","pos","fwd1","fwd3","z1","z20","vol30","dist_ylo","next_wd","alloc","bookr"]])
    A = pd.concat(rows, ignore_index=True)
    drift1 = A.dropna(subset=["fwd1"]).groupby("coin")["fwd1"].mean()
    drift3 = A[A["pos"] % 3 == 0].dropna(subset=["fwd3"]).groupby("coin")["fwd3"].mean()
    A["ex"] = A["fwd1"] - A["coin"].map(drift1)
    A["ex3"] = A["fwd3"] - A["coin"].map(drift3)

    def ct(s, days):
        n = days.nunique()
        if n < 3: return np.nan
        m = s.mean()
        dev = (s - m).groupby(days).sum()
        se = np.sqrt((dev**2).sum() * n/(n-1)) / len(s)
        return m / se

    def summ(df, key, col="ex"):
        out = []
        for k, g in df.groupby(key, observed=True):
            g = g.dropna(subset=[col])
            out.append({"k": k, "n": len(g), "mean_%": 100*g[col].mean(), "t_day": ct(g[col], g["day"]), "days": g["day"].nunique()})
        return pd.DataFrame(out)

    res = {}
    C = A.dropna(subset=["z1", "ex"]).copy()
    C["z1d"] = pd.qcut(C["z1"], 10, labels=False)
    res["z1_decile_next1"] = summ(C, "z1d")
    C3 = A[A["pos"] % 3 == 0].dropna(subset=["z1", "ex3"]).copy()
    C3["z1q"] = pd.qcut(C3["z1"], 5, labels=False)
    res["z1_quint_next3_nonoverlap"] = summ(C3, "z1q", "ex3")
    low = C[C["z1d"] <= 1]
    res["drop_by_year"] = summ(low, "year")
    res["drop_by_coin"] = summ(low, "coin")
    res["drop_by_nextwd"] = summ(low, "next_wd")
    low = low.copy()
    low["volq"] = low.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    res["drop_by_vol"] = summ(low, "volq")
    L2 = low.dropna(subset=["dist_ylo"]).copy()
    L2["yq"] = pd.qcut(L2["dist_ylo"], 3, labels=False, duplicates="drop")
    res["drop_by_dist_yearlow"] = summ(L2, "yq")
    rho, p = stats.spearmanr(C.loc[C["z1"] < 0, "z1"], C.loc[C["z1"] < 0, "ex"])
    res["spearman_neg_z1_vs_ex"] = f"rho {rho:.4f} p {p:.4g} n {(C['z1']<0).sum()}"
    Y = A.dropna(subset=["dist_ylo", "ex"]).copy()
    Y["yq"] = pd.qcut(Y["dist_ylo"], 5, labels=False, duplicates="drop")
    res["by_dist_yearlow_quint"] = summ(Y, "yq")
    # Saturday: non-forecast Saturdays after 20d loss
    S = A[(A["next_wd"] == 5)].dropna(subset=["z20", "ex"]).copy()
    S["neg"] = (S["z20"] < 0).astype(int)
    res["sat_by_z20_sign"] = summ(S, "neg")
    # book's largest day gains/losses: what preceded
    B = A.dropna(subset=["bookr"]).copy()
    B = B[B["bookr"] != 0]
    B["bq"] = pd.qcut(B["bookr"], 5, labels=False, duplicates="drop")
    res["book_bar_quint_profile"] = B.groupby("bq").agg(n=("bookr", "size"), mean_bookr_pct=("bookr", lambda x: 100*x.mean()),
                                                        mean_z20=("z20", "mean"), mean_z1=("z1", "mean"), mean_vol=("vol30", "mean")).reset_index()
    return res
