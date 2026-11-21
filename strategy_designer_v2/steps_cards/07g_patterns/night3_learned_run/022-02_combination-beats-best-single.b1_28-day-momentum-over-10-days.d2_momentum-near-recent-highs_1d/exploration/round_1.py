def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(c).pct_change().values
            r28 = pd.Series(c).pct_change(28).values
            hi60 = pd.Series(c).rolling(60, min_periods=60).max().values
            dist = (hi60 - c) / hi60 * 100
            vol20 = pd.Series(r1).rolling(20, min_periods=20).std().values
            r5 = pd.Series(c).pct_change(5).values
            fc = b["forecast"].astype(float).values
            pos = b["postRebalance_current_allocation"].astype(float).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, fc=fc[i], r28=r28[i],
                                 dist=dist[i], vol=vol20[i], r1=r1[i], r5=r5[i],
                                 pos=pos[i], year=ts[i].year))
            for i in range(n-1):
                daily.append(dict(coin=coin, w=w, nxt=c[i+1]/c[i]-1, r1=r1[i], vol=vol20[i],
                                  wd=ts[i+1].weekday(), pos=pos[i], year=ts[i].year))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    d = pd.DataFrame(daily)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["gain"] = d["pos"] * d["nxt"]
    out = {}
    def bucket(df, col, q=5, y="z"):
        x = df.dropna(subset=[col, y]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        a = x.groupby("b")[y].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["x_mean"] = x.groupby("b")[col].mean()
        return a.drop(columns="std").round(4)
    out["fc_quint_z10"] = bucket(g, "fc")
    out["r28_quint_z10"] = bucket(g, "r28")
    out["dist_quint_z10"] = bucket(g, "dist")
    out["vol_quint_z10"] = bucket(g, "vol")
    out["r5_quint_z10"] = bucket(g, "r5")
    out["r1_quint_z10"] = bucket(g, "r1")
    # dist quintile signed by r28 sign: momentum*sign vs dist
    x = g.dropna(subset=["r28", "dist"]).copy()
    x["sz"] = np.sign(x["r28"]) * x["z"]
    x["db"] = pd.qcut(x["dist"].rank(method="first"), 4, labels=False)
    x["side"] = np.where(x["r28"] > 0, "up28", "dn28")
    a = x.groupby(["side", "db"])["z"].agg(["mean", "count"]).round(4)
    out["z_by_r28side_dist4"] = a
    # regression z on r28, dist, interaction (pooled, standardized)
    y = x.dropna(subset=["vol"])
    X = np.column_stack([np.ones(len(y)), (y.r28-y.r28.mean())/y.r28.std(),
                         (y.dist-y.dist.mean())/y.dist.std(), (y.vol-y.vol.mean())/y.vol.std()])
    beta, *_ = np.linalg.lstsq(X, y.z.values, rcond=None)
    res = y.z.values - X @ beta
    s2 = res @ res / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["reg_z_on_r28_dist_vol"] = pd.DataFrame({"beta": beta, "t": beta/se}, index=["c", "r28", "dist", "vol"]).round(4)
    out["n_reg"] = len(y)
    # daily: next-day by r1 quintile, weekday, vol
    out["d_r1_quint_nextday_bps"] = (bucket(d.assign(exb=d.ex*1e4), "r1", y="exb"))
    wd = d.groupby("wd")["ex"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"])); wd["mean"] *= 1e4
    out["weekday_ex_bps"] = wd.drop(columns="std").round(3)
    # book gain by side and year
    d["side"] = np.sign(d["pos"])
    out["gain_by_side_bps"] = (d.groupby("side")["gain"].agg(["mean", "count"]) * [1e4, 1]).round(3)
    out["gain_by_year_bps"] = (d.groupby("year")["gain"].agg(["mean", "count"]) * [1e4, 1]).round(3)
    out["z10_by_year_fc_sign"] = g.assign(s=np.sign(g.fc)).groupby(["year", "s"])["z"].mean().unstack().round(3)
    return out
