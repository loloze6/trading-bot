def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "fwd": c.shift(-H) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
                "past30": c / c.shift(30) - 1,
                "lastday": r1,
                "vol20": r1.rolling(20).std(),
                "year": ts.dt.year,
                "w": w,
            })
            df["lastday_z"] = df["lastday"] / df["vol20"]
            g = df.iloc[::H].copy()
            g = g[g["fwd"].notna()]
            per.append(g)
        G = pd.concat(per)
        mu, sd = G["fwd"].mean(), G["fwd"].std()
        G["z"] = (G["fwd"] - mu) / sd
        G["unus"] = G["fwd"] - mu
        G["coin"] = coin
        for f in ["past30", "lastday", "lastday_z"]:
            ok = G[f].notna()
            G.loc[ok, "q_" + f] = pd.qcut(G.loc[ok, f].rank(method="first"), 5, labels=False)
        G["d_lastday_z"] = np.nan
        ok = G["lastday_z"].notna()
        G.loc[ok, "d_lastday_z"] = pd.qcut(G.loc[ok, "lastday_z"].rank(method="first"), 10, labels=False)
        rows.append(G)
    A = pd.concat(rows)
    out = {}
    def tt(x):
        return pd.Series({"mean_z": x.mean(), "n": x.count(), "t": x.mean() / (x.std() / np.sqrt(x.count()))})
    # slopes per year: correlation of z with ranks
    for f in ["past30", "lastday_z"]:
        r = A.dropna(subset=["q_" + f])
        top = r[r["q_" + f] == 4]; bot = r[r["q_" + f] == 0]
        res = {}
        for y, s in r.groupby("year"):
            tp = s[s["q_" + f] == 4]["unus"]; bt = s[s["q_" + f] == 0]["unus"]
            res[y] = {"top_minus_bottom_unus": tp.mean() - bt.mean(), "n_top": len(tp), "n_bot": len(bt),
                      "t": stats.ttest_ind(tp, bt, equal_var=False).statistic if len(tp) > 3 and len(bt) > 3 else np.nan,
                      "spearman": stats.spearmanr(s[f], s["z"]).correlation}
        out["by_year_" + f] = pd.DataFrame(res).T.round(4)
        out["spearman_all_" + f] = pd.Series({"rho": stats.spearmanr(r[f], r["z"]).correlation, "n": len(r)})
        # by coin
        bc = {}
        for cn, s in r.groupby("coin"):
            bc[cn] = {"spearman": stats.spearmanr(s[f], s["z"]).correlation, "n": len(s)}
        bcd = pd.DataFrame(bc).T
        out["coins_positive_rho_" + f] = pd.Series({"positive": (bcd["spearman"] > 0).sum(), "of": len(bcd), "median_rho": bcd["spearman"].median()})
    out["deciles_lastday_z"] = A.dropna(subset=["d_lastday_z"]).groupby("d_lastday_z").apply(lambda s: pd.Series({"unus": s["unus"].mean(), "fwd3": s["fwd3"].mean(), "n": len(s), "t": s["z"].mean() / (s["z"].std() / np.sqrt(len(s)))})).round(4)
    # interaction: lastday quintile within past30 halves
    r = A.dropna(subset=["q_lastday", "past30"]).copy()
    r["p30_half"] = np.where(r.groupby("coin")["past30"].rank(pct=True) > 0.5, "up", "down")
    out["lastday_x_past30"] = r.groupby(["p30_half", "q_lastday"])["unus"].agg(["mean", "count"]).round(4)
    # weekday check by year, daily returns
    dr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            dr.append(pd.DataFrame({"r": c.pct_change(), "wd": ts.dt.weekday, "y": ts.dt.year, "hr": ts.dt.hour}))
    D = pd.concat(dr).dropna()
    out["bar_start_hour_counts"] = D["hr"].value_counts().head(5)
    D["wfs"] = D["wd"].isin([2, 4, 5])
    yy = {}
    for y, s in D.groupby("y"):
        a = s[s.wfs]["r"]; bb = s[~s.wfs]["r"]
        yy[y] = {"diff": a.mean() - bb.mean(), "t": stats.ttest_ind(a, bb, equal_var=False).statistic, "n": len(s)}
    out["wed_fri_sat_minus_rest_by_year"] = pd.DataFrame(yy).T.round(4)
    # book around largest losses: coin return before
    return out
