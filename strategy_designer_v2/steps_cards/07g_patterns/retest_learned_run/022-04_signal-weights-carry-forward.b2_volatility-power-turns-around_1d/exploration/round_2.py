def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            nxt1 = c.shift(-1) / c - 1
            fwd5 = c.shift(-5) / c - 1
            d = pd.DataFrame({"coin": coin, "win": w, "r1": r1, "nxt1": nxt1, "fwd5": fwd5,
                              "z": r1 / vol20, "wd": ts.dt.weekday, "yr": ts.dt.year,
                              "pos": np.arange(len(b))})
            rows.append(d)
    df = pd.concat(rows)
    # weekday effect on next 1-day return (each day once)
    s = df.dropna(subset=["nxt1"]).copy()
    s["ex1"] = s["nxt1"] - s.groupby("coin")["nxt1"].transform("mean")
    s["nwd"] = (s["wd"] + 1) % 7  # weekday of the day whose return it is
    g = s.groupby("nwd")["ex1"].agg(["mean", "count", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["excess_1d_return_by_weekday_of_return_day"] = g.round(5)
    piv = s.groupby(["coin", "nwd"])["ex1"].mean().unstack().round(4)
    out["by_coin_weekday_mean_1d"] = piv
    piv2 = s.groupby(["yr", "nwd"])["ex1"].mean().unstack().round(4)
    out["by_year_weekday_mean_1d"] = piv2
    # Mon+Tue minus Sat+Sun per year
    s["grp"] = np.where(s["nwd"].isin([0, 1]), "montue", np.where(s["nwd"].isin([5, 6]), "satsun", "mid"))
    yy = s.groupby(["yr", "grp"])["ex1"].mean().unstack()
    yy["diff"] = yy["montue"] - yy["satsun"]
    out["montue_minus_satsun_by_year"] = yy.round(4)
    a = s.loc[s.grp == "montue", "ex1"]; bq = s.loc[s.grp == "satsun", "ex1"]
    out["montue_vs_satsun_welch_t"] = float(stats.ttest_ind(a, bq, equal_var=False)[0])
    # large up day z effect on next 5d, non-overlap grid, by coin and year
    q = df[df["pos"] % 5 == 0].dropna(subset=["fwd5", "z"]).copy()
    q["ex5"] = q["fwd5"] - q.groupby("coin")["fwd5"].transform("mean")
    q["zq"] = q.groupby("coin")["z"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    top = q[q.zq == 4]
    out["top_z_quint_ex5_by_coin"] = top.groupby("coin")["ex5"].agg(["mean", "count"]).round(4)
    out["top_z_quint_ex5_by_year"] = top.groupby("yr")["ex5"].agg(["mean", "count"]).round(4)
    out["z_spearman_pooled"] = float(stats.spearmanr(q["z"], q["ex5"])[0])
    # positive z graded
    pz = q[q.z > 0]
    out["poszonly_spearman"] = float(stats.spearmanr(pz["z"], pz["ex5"])[0])
    out["poszonly_n"] = int(len(pz))
    return out
