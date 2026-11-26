def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            df["pos"] = np.arange(len(b))
            prior_hi = c.shift(1).rolling(28).max()
            prior_lo = c.shift(1).rolling(28).min()
            df["dist_hi"] = (c / prior_hi - 1)
            df["dist_lo"] = (c / prior_lo - 1)
            df["ret28"] = c / c.shift(28) - 1
            df["ret5p"] = c / c.shift(5) - 1
            df["ret1"] = r1
            vol20 = r1.rolling(20).std()
            df["vol20"] = vol20
            df["volratio"] = vol20 / r1.rolling(90).std()
            rng = (h - l) / c
            df["rngratio"] = rng.rolling(20).mean() / rng.rolling(90).mean()
            df["vlmratio"] = v.rolling(20).mean() / v.rolling(90).mean()
            df["fwd5"] = c.shift(-5) / c - 1
            df["fwd1"] = c.shift(-1) / c - 1
            df["grid"] = (df["pos"] % 5 == 0)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # normal drift per coin over all windows (grid)
    G = D[D["grid"] & D["fwd5"].notna()].copy()
    drift = G.groupby("coin")["fwd5"].mean()
    sd = G.groupby("coin")["fwd5"].std()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    G["z5"] = G["ex5"] / G["coin"].map(sd)
    G["day"] = G["ts"].dt.floor("D")
    out = {}
    out["drift_sd"] = pd.DataFrame({"drift": drift, "sd": sd})
    def slope_t(x, name, sub=None):
        S = G if sub is None else G[sub]
        S = S[[x, "z5", "day"]].dropna()
        xs = (S[x] - S[x].mean()) / S[x].std()
        S = S.assign(xs=xs)
        # per-day summed regression contribution: slope via sum(x*y)/sum(x^2), cluster by day
        S["xy"] = S["xs"] * S["z5"]; S["xx"] = S["xs"] ** 2
        b = S["xy"].sum() / S["xx"].sum()
        S["e"] = S["xs"] * (S["z5"] - b * S["xs"])
        dd = S.groupby("day")["e"].sum()
        se = np.sqrt((dd ** 2).sum()) / S["xx"].sum()
        return {"slope_z_per_sd": b, "t_day": b / se, "n": len(S), "days": S["day"].nunique()}
    res = {}
    for x in ["dist_hi", "dist_lo", "ret28", "ret5p", "ret1", "volratio", "rngratio", "vlmratio", "vol20"]:
        res[x] = slope_t(x, x)
    out["slopes_all"] = pd.DataFrame(res).T
    # breakout subset (the idea)
    res2 = {}
    res2["breakout_margin"] = slope_t("dist_hi", "", G["dist_hi"] > 0)
    calm = (G["rngratio"] < 1) & (G["volratio"] < 1)
    res2["calm_ret28_neg"] = slope_t("ret28", "", calm & (G["ret28"] < 0))
    res2["violent_ret28_neg"] = slope_t("ret28", "", (~calm) & (G["ret28"] < 0))
    res2["ret28_highvol"] = slope_t("ret28", "", G["volratio"] > 1)
    res2["ret28_lowvol"] = slope_t("ret28", "", G["volratio"] <= 1)
    res2["ret5p_highvol"] = slope_t("ret5p", "", G["volratio"] > 1)
    res2["ret5p_lowvol"] = slope_t("ret5p", "", G["volratio"] <= 1)
    out["slopes_sub"] = pd.DataFrame(res2).T
    # deciles
    for x in ["dist_hi", "ret28", "volratio", "vlmratio"]:
        q = G.groupby(pd.qcut(G[x], 5, duplicates="drop"), observed=True)["ex5"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
        q.index = [f"q{i+1}" for i in range(len(q))]
        out["quint_" + x] = q
    out["breakout_mean_ex5"] = G[G["dist_hi"] > 0]["ex5"].agg(["mean", "count"])
    # weekday on daily returns, excess over coin mean
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    D["wd"] = (D["ts"] + pd.Timedelta(days=1)).dt.dayofweek
    wd = D.groupby("wd")["ex1"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["weekday_next"] = wd
    out["by_win_dist_hi_corr"] = G.groupby("win").apply(lambda s: s[["dist_hi", "z5"]].corr().iloc[0, 1])
    out["by_coin_ret28_corr"] = G.groupby("coin").apply(lambda s: s[["ret28", "z5"]].dropna().corr().iloc[0, 1])
    return out
