def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().rolling(60).mean()
            hi = c.shift(1).rolling(60).max(); lo = c.shift(1).rolling(60).min()
            W = (hi - lo) / c / mabs
            brk_up = (c - hi) / c / mabs
            brk_dn = (lo - c) / c / mabs
            brk = np.where(brk_up > 0, brk_up, np.where(brk_dn > 0, -brk_dn, 0.0))
            # position within range, -1 at low, +1 at high (can exceed)
            mid = (hi + lo) / 2
            rpos = (c - mid) / ((hi - lo) / 2)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": ts.dt.normalize(), "year": ts.dt.year, "wd": ts.dt.weekday,
                "W": W, "brk": brk, "rpos": rpos,
                "ret20p_z": (c / c.shift(20) - 1) / (r1.rolling(60).std() * np.sqrt(20)),
                "vol60": r1.rolling(60).std(), "r1": r1,
            })
            for h in (5, 10, 20):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    def cl_t(x, y, d):
        m = pd.DataFrame({"x": x, "y": y, "d": d}).dropna()
        if len(m) < 30: return (np.nan, np.nan, len(m), 0)
        X = np.column_stack([np.ones(len(m)), m["x"].values]); Y = m["y"].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        S = pd.DataFrame(X * e[:, None]).groupby(m["d"].values).sum().values
        V = XtXi @ (S.T @ S) @ XtXi
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(m), m["d"].nunique())

    out = {}
    # weekday, date-clustered: mean over coins per date, then t over dates
    dd = D.dropna(subset=["r1"]).groupby(["ts", "wd", "year"])["r1"].mean().reset_index()
    wd = dd.groupby("wd")["r1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_datemean"] = wd
    fs = dd[dd["wd"].isin([4, 5])].groupby("year")["r1"].agg(["mean", "count"])
    fs["other_mean"] = dd[~dd["wd"].isin([4, 5])].groupby("year")["r1"].mean()
    out["frisat_by_year"] = fs
    # weekday by coin (Fri+Sat minus others)
    tmp = D.dropna(subset=["r1"]).copy(); tmp["fs"] = tmp["wd"].isin([4, 5])
    out["frisat_by_coin"] = tmp.groupby(["coin", "fs"])["r1"].mean().unstack()

    # breakout size vs forward, multiple grid offsets, slope per h, also rpos, and by window halves
    res = []
    for h in (5, 10, 20):
        for off in range(0, h, max(1, h // 5)):
            g = D[(D["pos"] - off) % h == 0].copy()
            g["ex"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
            g["exz"] = g["ex"] / (g["vol60"] * np.sqrt(h))
            for x in ["brk", "rpos", "ret20p_z"]:
                s, t, n, nd = cl_t(g[x], g["exz"], g["ts"])
                res.append({"h": h, "off": off, "x": x, "slope": s, "t": t, "n": n, "dates": nd})
    R = pd.DataFrame(res)
    out["slopes_offsets"] = R.pivot_table(index=["h", "off"], columns="x", values="t")
    # rpos slope by year, h=10 grid 0
    g = D[D["pos"] % 10 == 0].copy()
    g["ex"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
    g["exz"] = g["ex"] / (g["vol60"] * np.sqrt(10))
    yr = []
    for y, gg in g.groupby("year"):
        s, t, n, nd = cl_t(gg["rpos"], gg["exz"], gg["ts"])
        yr.append({"year": y, "slope": s, "t": t, "n": n})
    out["rpos_h10_by_year"] = pd.DataFrame(yr)
    co = []
    for cn, gg in g.groupby("coin"):
        s, t, n, nd = cl_t(gg["rpos"], gg["exz"], gg["ts"])
        co.append({"coin": cn, "slope": s, "t": t, "n": n})
    out["rpos_h10_by_coin"] = pd.DataFrame(co)
    # rpos quintiles, h=10 grid
    g2 = g.dropna(subset=["rpos", "ex"]).copy()
    g2["q"] = pd.qcut(g2["rpos"].rank(method="first"), 5, labels=False)
    out["rpos_quint_ex10"] = g2.groupby("q").agg(rpos=("rpos", "mean"), ex=("ex", "mean"), n=("ex", "count"))
    # interaction: rpos slope in tight vs wide W
    g2["Wt"] = g2["W"] <= g2["W"].median()
    it = []
    for k, gg in g2.groupby("Wt"):
        s, t, n, nd = cl_t(gg["rpos"], gg["exz"], gg["ts"])
        it.append({"tight": k, "slope": s, "t": t, "n": n})
    out["rpos_by_tightness"] = pd.DataFrame(it)

    # book's largest days: weekday distribution and preceding coin moves
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            br.append(pd.DataFrame({"day": pd.to_datetime(d["day"]), "b": d["book_return"], "c": d["coin_return"]}))
    B = pd.concat(br).dropna().groupby("day")[["b", "c"]].mean().reset_index()
    B["wd"] = B["day"].dt.weekday
    q = B["b"].quantile([0.05, 0.95])
    B["grp"] = np.where(B["b"] <= q.iloc[0], "worst5", np.where(B["b"] >= q.iloc[1], "best5", "mid"))
    out["book_extremes_weekday"] = B.groupby(["grp", "wd"]).size().unstack(fill_value=0)
    return out
