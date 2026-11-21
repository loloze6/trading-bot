def explore(data):
    import numpy as np, pandas as pd
    recs = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values.astype(float); h = df["high"].values.astype(float); l = df["low"].values.astype(float)
            n = len(c)
            if n < 60: continue
            S = pd.Series
            hh = S(h).rolling(12).max().shift(1).values
            ll = S(l).rolling(12).min().shift(1).values
            rng = (hh - ll) / c
            rngmed = S(rng).rolling(180, min_periods=60).median().values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = S(r1).rolling(60, min_periods=30).std().values
            volmed = S(vol).rolling(360, min_periods=120).median().values
            ret180 = c / S(c).shift(180).values - 1
            ret6 = c / S(c).shift(6).values - 1
            barret = c / df["open"].values - 1
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "cell": np.arange(n) // 18,
                "narrow": rng / rngmed, "volr": vol / volmed, "ret180": ret180,
                "ret6z": ret6 / (vol * np.sqrt(6)), "clear": c / hh - 1, "down": c / ll - 1,
                "clearz": (c / hh - 1) / vol, "downz": (c / ll - 1) / vol, "barz": barret / vol,
                "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
            })
            for H in (6, 18, 36):
                f = np.full(n, np.nan); f[:n - H] = c[H:] / c[:-H] - 1
                d["f%d" % H] = f
            recs.append(d)
    A = pd.concat(recs, ignore_index=True)
    for H in (6, 18, 36):
        g = A[A["pos"] % H == 0]
        st = g.groupby("coin")["f%d" % H].agg(["mean", "std"])
        A["dr%d" % H] = A["coin"].map(st["mean"]); A["sd%d" % H] = A["coin"].map(st["std"])
        A["x%d" % H] = A["f%d" % H] - A["dr%d" % H]
        A["s%d" % H] = A["x%d" % H] / A["sd%d" % H]

    def agg(df, by, col="x18", scol="s18"):
        g = df.groupby(by, observed=True)
        out = pd.DataFrame({"n": g[col].count(), "mean_exc": g[col].mean(),
                            "t": g[col].mean() / (g[col].std() / np.sqrt(g[col].count())),
                            "strength": g[scol].mean(),
                            "t_strength": g[scol].mean() / (g[scol].std() / np.sqrt(g[scol].count()))})
        return out.round(4)

    A = A.dropna(subset=["f18"])
    up = A[A["clear"] > 0].groupby(["coin", "win", "cell"]).head(1).copy()
    dn = A[A["down"] < 0].groupby(["coin", "win", "cell"]).head(1).copy()
    up["reg"] = np.where(up["ret180"] > 0, "pos30d", np.where(up["ret180"] <= 0, "neg30d", "na"))
    dn["reg"] = np.where(dn["ret180"] > 0, "pos30d", np.where(dn["ret180"] <= 0, "neg30d", "na"))
    upp = up[up["reg"] == "pos30d"].copy()
    upp["narrow_q"] = pd.qcut(upp["narrow"], 5, labels=False, duplicates="drop")
    upp["clearz_q"] = pd.qcut(upp["clearz"], 5, labels=False, duplicates="drop")
    upp["volr_q"] = pd.qcut(upp["volr"], 5, labels=False, duplicates="drop")
    dn["narrow_q"] = pd.qcut(dn["narrow"], 5, labels=False, duplicates="drop")
    dn["downz_q"] = pd.qcut(dn["downz"], 5, labels=False, duplicates="drop")
    upp["hb"] = upp["hour"]
    res = {}
    res["up_by_regime"] = agg(up, "reg")
    res["down_by_regime(long sign)"] = agg(dn, "reg")
    res["up_pos30d_by_narrow_q"] = agg(upp, "narrow_q")
    res["up_pos30d_by_clearz_q"] = agg(upp, "clearz_q")
    res["up_pos30d_by_volratio_q"] = agg(upp, "volr_q")
    res["up_pos30d_by_hour"] = agg(upp, "hb")
    res["up_pos30d_by_weekday"] = agg(upp, "wd")
    res["down_by_narrow_q"] = agg(dn, ["reg", "narrow_q"])
    res["down_by_depth_q"] = agg(dn, ["reg", "downz_q"])
    hz = []
    for H in (6, 18, 36):
        x = upp["x%d" % H].dropna(); s = upp["s%d" % H].dropna()
        hz.append({"H_bars": H, "n": len(x), "mean_exc": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "strength": s.mean()})
    res["up_pos30d_by_horizon"] = pd.DataFrame(hz).round(4)
    G = A[A["pos"] % 18 == 0].copy()
    G["volr_q"] = pd.qcut(G["volr"], 5, labels=False, duplicates="drop")
    G["ret6z_q"] = pd.qcut(G["ret6z"], 5, labels=False, duplicates="drop")
    G["ret180_q"] = pd.qcut(G["ret180"], 5, labels=False, duplicates="drop")
    G["narrow_q"] = pd.qcut(G["narrow"], 5, labels=False, duplicates="drop")
    res["grid_by_volratio_q"] = agg(G, "volr_q")
    res["grid_by_ret6z_q"] = agg(G, "ret6z_q")
    res["grid_by_ret180_q"] = agg(G, "ret180_q")
    res["grid_by_narrow_q"] = agg(G, "narrow_q")
    G["absf"] = G["f18"].abs() / G["sd18"]
    res["grid_absmove_by_narrow_q"] = G.groupby("narrow_q")["absf"].agg(["count", "mean"]).round(4)
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    T["eh"] = pd.to_datetime(T["entry_time"]).dt.hour
    T["dur_days_q"] = pd.qcut(T["duration_minutes"], 5, labels=False, duplicates="drop")
    tg = T.groupby("dur_days_q")
    res["trades_by_duration_q"] = pd.DataFrame({"n": tg.size(), "med_dur_days": tg["duration_minutes"].median() / 1440,
                                                "mean_net": tg["net_profit_loss_percent"].mean()}).round(3)
    th = T.groupby("eh")
    res["trades_by_entry_hour"] = pd.DataFrame({"n": th.size(), "mean_net": th["net_profit_loss_percent"].mean(),
                                                "t": th["net_profit_loss_percent"].mean() / (th["net_profit_loss_percent"].std() / np.sqrt(th.size()))}).round(3)
    return res
