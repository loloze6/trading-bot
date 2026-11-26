def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                               "z": r / sd30, "nxt": c.shift(-1) / c - 1,
                               "nxt2": c.shift(-2) / c - 1,
                               "tr60": c / c.shift(60) - 1,
                               "ag": sd30.rolling(120, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True),
                               "clo": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                               "sd30": sd30, "pos": np.arange(len(b))})
            df["day"] = df["ts"].dt.floor("D")
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "z", "clo"])
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["prof"] = np.where(d["tr60"] > 0.10, "rising", np.where(d["tr60"] < -0.10, "falling", "choppy"))
    d.loc[d["tr60"].isna(), "prof"] = np.nan
    d["agit"] = np.where(d["ag"] > 0.5, "agit", "calm")
    d.loc[d["ag"].isna(), "agit"] = np.nan
    def ct(g, col="ex"):
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean_%": 100 * m, "t_day": m / se if se > 0 else np.nan})
    out = {}
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["zbin_dayclustered"] = d.groupby("zb").apply(ct)
    dd = d.dropna(subset=["prof", "agit"])
    dd["zb3"] = pd.cut(dd["z"], [-np.inf, -1, 1, np.inf])
    out["prof_agit_zb3"] = dd.groupby(["agit", "prof", "zb3"]).apply(ct)
    # signed reversal: -z * ex, graded test
    d["rev"] = -np.sign(d["z"]) * d["ex"]
    d["az"] = pd.cut(d["z"].abs(), [0, 0.5, 1, 1.5, 2, np.inf])
    da = d.dropna(subset=["agit"])
    out["abs_z_rev_by_agit"] = da.groupby(["agit", "az"]).apply(lambda g: ct(g, "rev"))
    # close location within z sign
    d["clob"] = pd.cut(d["clo"], [-0.001, 0.2, 0.4, 0.6, 0.8, 1.0])
    d["zs"] = np.where(d["z"] > 0, "up", "down")
    out["clo_by_zsign"] = d.groupby(["zs", "clob"]).apply(ct)
    dc = d.dropna(subset=["prof"])
    dc["clo3"] = pd.cut(dc["clo"], [-0.001, 0.25, 0.75, 1.0])
    out["clo3_by_prof"] = dc.groupby(["prof", "clo3"]).apply(ct)
    out["clo3_by_win_lowminushigh"] = d.assign(clo3=pd.cut(d["clo"], [-0.001, 0.25, 0.75, 1.0])).groupby("win").apply(
        lambda g: pd.Series({"low_%": 100 * g.loc[g["clo"] <= 0.25, "ex"].mean(), "high_%": 100 * g.loc[g["clo"] > 0.75, "ex"].mean()}))
    # regression ex/sd30 on z and clo together
    X = np.column_stack([np.ones(len(d)), d["z"].clip(-4, 4), d["clo"] - 0.5])
    y = (d["ex"] / d["sd30"]).values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    XtXi = np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(XtXi) * res.var())
    out["joint_reg_exn"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z", "clo-0.5"])
    # 2-day horizon, non-overlapping grid, big down days
    g2 = d[d["pos"] % 2 == 0].dropna(subset=["nxt2"]).copy()
    g2["ex2"] = g2["nxt2"] - g2.groupby("coin")["nxt2"].transform("mean")
    g2["zb"] = pd.cut(g2["z"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["two_day_zbin"] = g2.groupby("zb").apply(lambda g: ct(g, "ex2"))
    return out
