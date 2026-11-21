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
            ret180 = c / S(c).shift(180).values - 1
            ret6 = c / S(c).shift(6).values - 1
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "half": np.where(int(w[1:]) <= 12, "early", "late"),
                "pos": np.arange(n), "cell": np.arange(n) // 18,
                "narrow": rng / rngmed, "ret180": ret180,
                "ret6z": ret6 / (vol * np.sqrt(6)), "clear": c / hh - 1, "down": c / ll - 1,
                "wd": ts.dt.weekday.values,
            })
            for H in (18, 36):
                f = np.full(n, np.nan); f[:n - H] = c[H:] / c[:-H] - 1
                d["f%d" % H] = f
            recs.append(d)
    A = pd.concat(recs, ignore_index=True)
    for H in (18, 36):
        g = A[A["pos"] % H == 0]
        st = g.groupby("coin")["f%d" % H].agg(["mean", "std"])
        A["dr%d" % H] = A["coin"].map(st["mean"]); A["sd%d" % H] = A["coin"].map(st["std"])
        A["x%d" % H] = A["f%d" % H] - A["dr%d" % H]
        A["s%d" % H] = A["x%d" % H] / A["sd%d" % H]
    A["reg"] = np.where(A["ret180"] > 0, "pos30d", np.where(A["ret180"] <= 0, "neg30d", "na"))

    def agg(df, by, col="x18", scol="s18", tot="f18"):
        g = df.groupby(by, observed=True)
        return pd.DataFrame({"n": g[col].count(), "mean_exc": g[col].mean(),
                             "t": g[col].mean() / (g[col].std() / np.sqrt(g[col].count())),
                             "strength": g[scol].mean(), "total": g[tot].mean()}).round(4)

    def coinshare(df, col="x18"):
        m = df.groupby("coin")[col].mean()
        return pd.Series({"coins": len(m), "share_pos": (m > 0).mean(), "median_coin": m.median()}).round(4)

    res = {}
    A18 = A.dropna(subset=["f18"])
    G = A18[A18["pos"] % 18 == 0].copy()
    G["narrow_q"] = G.groupby("reg")["narrow"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["grid_narrow_by_reg"] = agg(G[G.reg != "na"], ["reg", "narrow_q"])
    res["grid_narrow_by_half"] = agg(G[G.reg != "na"].assign(nq=pd.qcut(G.loc[G.reg != "na", "narrow"], 5, labels=False)), ["half", "nq"])
    G["nar_z"] = np.log(G["narrow"])
    gg = G.dropna(subset=["nar_z"])
    res["grid_narrowest_coinshare"] = coinshare(gg[gg["nar_z"] <= gg["nar_z"].quantile(0.2)])
    # down breaks in falling coins
    dn = A18[A18["down"] < 0].groupby(["coin", "win", "cell"]).head(1).copy()
    dnn = dn[dn.reg == "neg30d"].copy()
    dnn["nq"] = pd.qcut(dnn["narrow"], 5, labels=False, duplicates="drop")
    res["downbreak_neg30d_narrow_by_half"] = agg(dnn, ["half", "nq"])
    res["downbreak_neg30d_narrowest_coinshare"] = coinshare(dnn[dnn.nq == 0])
    res["downbreak_neg30d_narrowest_36bar"] = agg(dnn.dropna(subset=["f36"]), "nq", "x36", "s36", "f36")
    dnp = dn[dn.reg == "pos30d"].copy()
    dnp["nq"] = pd.qcut(dnp["narrow"], 5, labels=False, duplicates="drop")
    res["downbreak_pos30d_narrow_by_half"] = agg(dnp, ["half", "nq"])
    res["downbreak_pos30d_widest_coinshare"] = coinshare(dnp[dnp.nq == 4])
    # 1-day falls
    G["r6q"] = pd.qcut(G["ret6z"], 10, labels=False, duplicates="drop")
    res["grid_ret6z_decile"] = agg(G, "r6q")
    res["grid_ret6z_bottom20_by_reg_half"] = agg(G[G["r6q"] <= 1], ["reg", "half"])
    res["grid_ret6z_bottom20_coinshare"] = coinshare(G[G["r6q"] <= 1])
    # up breakouts pos30d at 36 bars
    up = A[A["clear"] > 0].dropna(subset=["f36"]).groupby(["coin", "win", "cell"]).head(1)
    upp = up[up.reg == "pos30d"]
    res["up_pos30d_36bar_by_half"] = agg(upp, "half", "x36", "s36", "f36")
    res["up_pos30d_36bar_coinshare"] = coinshare(upp, "x36")
    # weekday robustness
    up18 = A18[A18["clear"] > 0].groupby(["coin", "win", "cell"]).head(1)
    res["up_pos30d_weekday_by_half"] = agg(up18[up18.reg == "pos30d"], ["wd", "half"])
    # book around big days
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.reset_index(drop=True).copy()
            dd["next_book"] = dd["book_return"].shift(-1); dd["next_coin"] = dd["coin_return"].shift(-1)
            dd["coin"] = coin
            D.append(dd)
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return"])
    D = D[D["book_return"] != 0]
    D["bq"] = pd.qcut(D["book_return"], 10, labels=False, duplicates="drop")
    gD = D.groupby("bq")
    res["book_day_decile_next"] = pd.DataFrame({"n": gD.size(), "mean_book": gD["book_return"].mean(),
                                                "next_book": gD["next_book"].mean(), "next_coin": gD["next_coin"].mean()}).round(4)
    return res
