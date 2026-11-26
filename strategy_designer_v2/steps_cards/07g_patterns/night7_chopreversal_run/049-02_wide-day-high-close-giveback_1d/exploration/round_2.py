def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            rng = (b["high"] - b["low"])
            clv = ((b["close"] - b["low"]) / rng.replace(0, np.nan))
            width = rng / rng.rolling(30, min_periods=20).mean()
            ret1 = b["close"].pct_change()
            vol30 = ret1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "clv": clv, "width": width, "r0": ret1, "z0": ret1 / vol30, "vol30": vol30,
                "r2": b["close"] / b["close"].shift(2) - 1,
                "f1": b["close"].shift(-1) / b["close"] - 1,
                "f2": b["close"].shift(-2) / b["close"] - 1,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2):
        g = D[D["pos"] % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(dr)
    D["volq"] = D.groupby("coin")["vol30"].rank(pct=True)
    D["agit"] = D["volq"] > 0.5

    def tday(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 10: return (np.nan, np.nan, len(s))
        m = s[col].mean(); dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return (m * 100, m / se, len(s))

    def slope(s, xcol, ycol):
        s = s.dropna(subset=[xcol, ycol])
        x = s[xcol] - s[xcol].mean(); y = s[ycol] - s[ycol].mean()
        b = (x * y).sum() / (x * x).sum()
        e = y - b * x
        sc = (x * e).groupby(s["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (x * x).sum()
        return b, b / se, len(s)

    out = {}
    # graded reversal on today's standardized return, agitated vs calm, plus per-coin
    D["zc"] = D["z0"].clip(-4, 4)
    res = []
    for lab, s in [("all", D), ("agit", D[D["agit"]]), ("calm", D[~D["agit"]])]:
        b, t, n = slope(s, "zc", "x1"); res.append({"set": lab, "h": 1, "slope_%perz": b * 100, "t": t, "n": n})
        g2 = s[s["pos"] % 2 == 0]
        b, t, n = slope(g2, "zc", "x2"); res.append({"set": lab, "h": 2, "slope_%perz": b * 100, "t": t, "n": n})
    out["z_slope"] = pd.DataFrame(res)
    res = []
    for c, s in D[D["agit"]].groupby("coin"):
        b, t, n = slope(s, "zc", "x1"); res.append({"coin": c, "slope_%perz": b * 100, "t": t, "n": n})
    out["z_slope_agit_by_coin"] = pd.DataFrame(res)
    res = []
    for w, s in D[D["agit"]].groupby("win"):
        b, t, n = slope(s, "zc", "x1"); res.append({"win": w, "slope_%perz": b * 100, "t": t, "n": n})
    out["z_slope_agit_by_window"] = pd.DataFrame(res)
    # raw return (not z) slope in agitated: graded by size
    D["zq"] = pd.qcut(D["z0"], 10, labels=False)
    res = []
    for q, s in D[D["agit"]].groupby("zq"):
        m, t, n = tday(s, "x1"); res.append({"z_decile": q, "mean_z": s["z0"].mean(), "x1_%": m, "t": t, "n": n})
    out["agit_z_deciles"] = pd.DataFrame(res)
    # low-close graded by width: lowness*width
    D["lowstr"] = (1 - D["clv"]) * D["width"]
    D["highstr"] = D["clv"] * D["width"]
    res = []
    for lab, col in [("low_close_x_width", "lowstr"), ("high_close_x_width", "highstr")]:
        b, t, n = slope(D, col, "x1"); res.append({"var": lab, "slope_%": b * 100, "t": t, "n": n})
    # close location alone vs width interaction, and controlling for z
    out["clv_strength_slopes"] = pd.DataFrame(res)
    # lo-close wide effect per window sign count
    lw = D[(D["clv"] < 0.2) & (D.groupby("coin")["width"].rank(pct=True) > 2/3)]
    res = []
    for w, s in lw.groupby("win"):
        m, t, n = tday(s, "x1"); res.append({"win": w, "x1_%": m, "n": n})
    out["lowclose_wide_by_window"] = pd.DataFrame(res)
    # does the low-close effect survive given z? within agit & z<0
    s = D[D["agit"] & (D["z0"] < 0)]
    out["agit_down_clv_slope"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(s, "clv", "x1")))])
    # book: next-day gain of book in agitated vs calm
    D["alloc"] = pd.concat([data["bars"][c][w].sort_values("timestamp")["postRebalance_current_allocation"].reset_index(drop=True)
                            for c in data["bars"] for w in data["bars"][c]], ignore_index=True)
    D["pg"] = D["alloc"] * D["f1"]
    out["pos_gain_by_vol"] = D.groupby(["agit", np.sign(D["alloc"])])["pg"].agg(["mean", "count"])
    return out
