def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            tr60 = c / c.shift(60) - 1
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "yr": pd.to_datetime(b["timestamp"]).dt.year,
                              "z": z, "sd": sd, "tr60": tr60,
                              "clv": (c - b["low"]) / (b["high"] - b["low"]),
                              "rc": (b["regime"] == "unknown")})
            for h in [3, 5, 10]:
                d["f%d" % h] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["sdmed"] = D["coin"].map(D.groupby("coin")["sd"].median())
    D["agit"] = D["sd"] > D["sdmed"]
    D["prof"] = np.where(D.tr60 > 0.10, "rising", np.where(D.tr60 < -0.10, "falling", "choppy"))
    D.loc[D.tr60.isna(), "prof"] = "na"
    for h in [3, 5, 10]:
        g = D[D["pos"] % h == 0]
        D["f%dx" % h] = D["f%d" % h] - D["coin"].map(g.groupby("coin")["f%d" % h].mean())

    def ct(x, y, day):
        m = x.notna() & y.notna()
        x, y, day = x[m].values, y[m].values, day[m].values
        if len(x) < 15: return (np.nan, np.nan, len(x))
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for dd in np.unique(day):
            idx = day == dd
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = len(np.unique(day))
        V = XtXi @ meat @ XtXi * G / (G - 1)
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(x))

    out = {}
    res = []
    for h in [3, 5, 10]:
        g = D[D["pos"] % h == 0]
        for prof in ["rising", "choppy", "falling"]:
            for ag in [False, True]:
                for side in ["up", "down"]:
                    s = g[(g.prof == prof) & (g.agit == ag) & ((g.z > 0) if side == "up" else (g.z < 0))]
                    b_, t_, n_ = ct(s["z"], s["f%dx" % h], s["day"])
                    res.append({"h": h, "prof": prof, "agit": ag, "side": side, "slope": b_, "t": t_, "n": n_})
    out["slope_by_profile_proxy"] = pd.DataFrame(res)
    g5 = D[D["pos"] % 5 == 0]
    ch = g5[(g5.prof == "choppy") & (g5.z > 0)]
    res = []
    for y, s in ch.groupby("yr"):
        b_, t_, n_ = ct(s["z"], s["f5x"], s["day"])
        res.append({"yr": y, "slope": b_, "t": t_, "n": n_})
    for cn, s in ch.groupby("coin"):
        b_, t_, n_ = ct(s["z"], s["f5x"], s["day"])
        res.append({"yr": cn, "slope": b_, "t": t_, "n": n_})
    out["choppy_up_by_year_coin"] = pd.DataFrame(res)
    ch2 = ch.copy()
    ch2["zb"] = pd.qcut(ch2["z"], 4)
    tab = ch2.groupby("zb", observed=True)["f5x"].agg(["mean", "count", "std"])
    tab["t"] = tab["mean"] / (tab["std"] / np.sqrt(tab["count"]))
    out["choppy_up_quartiles"] = tab
    # choppy, all bars (overlapping-free per h=5), signed z
    s = g5[g5.prof == "choppy"]
    out["choppy_all_signed"] = pd.Series(dict(zip(["slope", "t", "n"], ct(s["z"], s["f5x"], s["day"]))))
    # rc down-side by year
    rd = g5[g5.rc & (g5.z < 0)]
    res = []
    for y, s in rd.groupby("yr"):
        b_, t_, n_ = ct(s["z"], s["f5x"], s["day"])
        res.append({"yr": y, "slope": b_, "t": t_, "n": n_})
    out["rc_down_by_year"] = pd.DataFrame(res)
    # clv by profile
    res = []
    for prof in ["rising", "choppy", "falling"]:
        s = g5[g5.prof == prof]
        b_, t_, n_ = ct(s["clv"], s["f5x"], s["day"])
        res.append({"prof": prof, "slope": b_, "t": t_, "n": n_})
    out["clv_by_profile"] = pd.DataFrame(res)
    return out
