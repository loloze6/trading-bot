def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(180, min_periods=45).std()
            vm = v.rolling(180, min_periods=45).mean()
            ret6 = c / c.shift(6) - 1
            ret18p = c / c.shift(18) - 1
            rng = (b["high"] - b["low"]) / c
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.values[idx],
                "z6": (ret6 / (sd * np.sqrt(6))).values[idx],
                "z18": (ret18p / (sd * np.sqrt(18))).values[idx],
                "vrat1": np.log(v.rolling(1).mean() / vm).values[idx],
                "vrat3": np.log(v.rolling(3).mean() / vm).values[idx],
                "vrat6": np.log(v.rolling(6).mean() / vm).values[idx],
                "vrat12": np.log(v.rolling(12).mean() / vm).values[idx],
                "vrat18": np.log(v.rolling(18).mean() / vm).values[idx],
                "rngr6": np.log(rng.rolling(6).mean() / rng.rolling(180, min_periods=45).mean()).values[idx],
                "wd": ts.dt.dayofweek.values[idx], "year": ts.dt.year.values[idx],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    D["exs"] = D["ex"] / D.groupby("coin")["fwd"].transform("std")
    D = D.replace([np.inf, -np.inf], np.nan)
    out = {}
    def rho(x, col):
        x = x.dropna(subset=[col]); return stats.spearmanr(x[col], x["exs"])[0]
    out["vrat_horizons_rho"] = pd.Series({c: rho(D, c) for c in ["vrat1","vrat3","vrat6","vrat12","vrat18","rngr6"]}).round(4)
    out["vrat6_rho_by_coin"] = D.groupby("coin").apply(lambda x: rho(x, "vrat6")).round(4)
    out["vrat6_rho_by_year"] = D.groupby("year").apply(lambda x: rho(x, "vrat6")).round(4)
    out["rngr6_rho_by_coin"] = D.groupby("coin").apply(lambda x: rho(x, "rngr6")).round(4)
    # vrat6 split by direction of the last day's move
    D["dir"] = np.where(D["z6"] < 0, "down6", "up6")
    x = D.dropna(subset=["vrat6"]).copy()
    x["vq"] = x.groupby("dir")["vrat6"].transform(lambda s: pd.qcut(s, 4, labels=False))
    a = x.groupby(["dir","vq"])["exs"].agg(["mean","count","std"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    a["ex_pct"] = x.groupby(["dir","vq"])["ex"].mean()*100
    out["vrat6_by_dir"] = a.drop(columns="std").round(4)
    out["vrat6_rho_by_dir"] = x.groupby("dir").apply(lambda y: rho(y, "vrat6")).round(4)
    # joint regression on ranks
    y = D.dropna(subset=["vrat6","rngr6","z6","z18"]).copy()
    for c in ["vrat6","rngr6","z6","z18"]:
        y[c+"_r"] = y.groupby("coin")[c].rank(pct=True) - 0.5
    X = np.column_stack([np.ones(len(y))] + [y[c+"_r"].values for c in ["vrat6","rngr6","z6","z18"]])
    beta, res, *_ = np.linalg.lstsq(X, y["exs"].values, rcond=None)
    e = y["exs"].values - X @ beta
    s2 = (e**2).sum()/(len(y)-X.shape[1]); se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["joint_reg"] = pd.DataFrame({"beta": beta, "t": beta/se}, index=["const","vrat6","rngr6","z6","z18"]).round(4)
    out["joint_n"] = len(y)
    # vrat6 quintiles, with each coin's own quintiles
    x = D.dropna(subset=["vrat6"]).copy()
    x["q"] = x.groupby("coin")["vrat6"].transform(lambda s: pd.qcut(s, 5, labels=False))
    a = x.groupby("q")["exs"].agg(["mean","count","std"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    a["ex_pct"] = x.groupby("q")["ex"].mean()*100
    out["vrat6_q_coinwise"] = a.drop(columns="std").round(4)
    hl = x[x.q==4].groupby("coin")["exs"].mean() - x[x.q==0].groupby("coin")["exs"].mean()
    out["vrat6_top_minus_bottom_by_coin"] = hl.round(4)
    # Sunday by coin and year
    D["sun"] = D["wd"] == 6
    out["sunday_minus_rest_by_coin"] = D.groupby("coin").apply(lambda z: z[z.sun]["exs"].mean() - z[~z.sun]["exs"].mean()).round(4)
    out["sunday_minus_rest_by_year"] = D.groupby("year").apply(lambda z: z[z.sun]["exs"].mean() - z[~z.sun]["exs"].mean()).round(4)
    out["sunday_vrat6_mean_vs_rest"] = pd.Series({"sun": D[D.sun]["vrat6"].mean(), "rest": D[~D.sun]["vrat6"].mean()}).round(4)
    return out
