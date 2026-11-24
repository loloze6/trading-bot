def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.sort_values("ts").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=15).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": b["ts"], "pos": np.arange(len(b)),
                "wd": b["ts"].dt.weekday, "year": b["ts"].dt.year, "r": r, "vol": vol,
                "z14": (c / c.shift(14) - 1) / (vol * np.sqrt(14)),
                "z7": (c / c.shift(7) - 1) / (vol * np.sqrt(7)),
                "z28": (c / c.shift(28) - 1) / (vol * np.sqrt(28)),
                "z1": r / vol,
                "f1": c.shift(-1) / c - 1,
                "g1": c.shift(-2) / c.shift(-1) - 1,
                "f2": c.shift(-2) / c - 1,
                "h2": c.shift(-4) / c.shift(-2) - 1,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    d1 = D[D["pos"] % 1 == 0].groupby("coin")["f1"].mean()
    d2 = D[D["pos"] % 2 == 0].groupby("coin")["f2"].mean()
    D["x1"] = D["f1"] - D["coin"].map(d1)
    D["y1"] = D["g1"] - D["coin"].map(d1)
    D["x2"] = D["f2"] - D["coin"].map(d2)
    D["xh2"] = D["h2"] - D["coin"].map(d2)

    def slope_t(s, xc, yc):
        s = s.dropna(subset=[xc, yc])
        X = np.column_stack([np.ones(len(s)), s[xc].values]); y = s[yc].values
        beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in s.groupby("ts").indices.items():
            u = X[idx].T @ e[idx]; meat += np.outer(u, u)
        V = XtXi @ meat @ XtXi
        return beta[1], beta[1] / np.sqrt(V[1, 1]), len(s), s["ts"].nunique()

    out = {}
    res = []
    for wd in range(7):
        s = D[D["wd"] == wd]
        for yc in ("x1", "y1"):
            for xc in ("z7", "z14", "z28"):
                b, t, n, nd = slope_t(s, xc, yc)
                res.append({"bar_wd": wd, "outcome": "next day" if yc == "x1" else "day after", "signal": xc, "slope": b, "t": t, "n": n, "days": nd})
    out["slope_by_weekday"] = pd.DataFrame(res)

    f = D[D["wd"] == 4].dropna(subset=["z14", "x1", "y1", "xh2"]).copy()
    f["q"] = pd.qcut(f["z14"], 5, labels=False)
    out["fri_z14_q_sat_sun_montue"] = f.groupby("q")[["z14", "x1", "y1", "xh2"]].mean().assign(n=f.groupby("q").size())
    res = []
    for yc in ("x1", "y1", "xh2"):
        b, t, n, nd = slope_t(f, "z14", yc)
        res.append({"outcome": yc, "slope": b, "t": t, "n": n})
    out["fri_z14_slopes(x1=sat,y1=sun,xh2=mon+tue)"] = pd.DataFrame(res)

    # Sunday conditional on Saturday move (Saturday bar wd5)
    s = D[D["wd"] == 5].dropna(subset=["z1", "x1"]).copy()
    b, t, n, nd = slope_t(s, "z1", "x1")
    s["q"] = pd.qcut(s["z1"], 5, labels=False)
    out["sat_move_then_sun"] = s.groupby("q")[["z1", "x1"]].mean().assign(n=s.groupby("q").size())
    out["sat_move_then_sun_slope"] = pd.DataFrame([{"slope": b, "t": t, "n": n}])

    # Friday bar's own move then Saturday
    s = D[D["wd"] == 4].dropna(subset=["z1", "x1"])
    b, t, n, nd = slope_t(s, "z1", "x1")
    out["fri_move_then_sat_slope"] = pd.DataFrame([{"slope": b, "t": t, "n": n}])
    # by window halves for Friday z14 -> sat
    f["half"] = np.where(f["year"] <= 2021, "<=2021", ">=2022")
    res = []
    for h, ss in f.groupby("half"):
        for yc in ("x1", "y1"):
            b, t, n, nd = slope_t(ss, "z14", yc)
            res.append({"half": h, "outcome": yc, "slope": b, "t": t, "n": n})
    out["fri_z14_by_half"] = pd.DataFrame(res)
    return out
