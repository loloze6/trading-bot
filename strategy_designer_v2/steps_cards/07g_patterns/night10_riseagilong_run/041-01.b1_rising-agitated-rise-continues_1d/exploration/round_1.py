def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "pos": np.arange(len(b)), "reg": b["regime"].astype(str),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r": r, "sr": r / sd30,
                "sr3": c.pct_change(3) / (sd30 * np.sqrt(3)),
                "sr10": c.pct_change(10) / (sd30 * np.sqrt(10)),
                "cl": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c.shift(1) / sd30,
                "dh20": c / c.rolling(20, min_periods=10).max() - 1,
            })
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 5):
        mu = d.groupby("coin")[f"f{h}"].transform(
            lambda s: s.iloc[::1].mean())
        # drift over grid samples
        g = d[d["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(m)
    d["day"] = d["ts"].dt.floor("D")
    d["wd"] = d["ts"].dt.dayofweek
    d["inp"] = d["reg"] == "unknown"

    def ct(s, days):
        s = s.dropna(); dd = days.loc[s.index]
        dev = (s - s.mean()).groupby(dd).sum()
        G = len(dev)
        if G < 3: return np.nan, G
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(s)
        return s.mean() / se, G

    def table(sub, col, h, q=5):
        sub = sub[sub["pos"] % h == 0].dropna(subset=[col, f"x{h}"])
        if len(sub) < 50: return pd.DataFrame()
        sub = sub.assign(b=pd.qcut(sub[col], q, labels=False, duplicates="drop"))
        out = []
        for k, gg in sub.groupby("b"):
            t, G = ct(gg[f"x{h}"], gg["day"])
            out.append({"bin": k, "lo": gg[col].min(), "hi": gg[col].max(),
                        "n": len(gg), "days": G, "mean_x%": 100 * gg[f"x{h}"].mean(), "t": t})
        return pd.DataFrame(out)

    P = d[d["inp"]]
    res = {}
    res["share_in_profile"] = float(d["inp"].mean())
    res["n_in_profile"] = int(d["inp"].sum())
    res["P_sr_h1"] = table(P, "sr", 1)
    res["P_sr_h3"] = table(P, "sr", 3)
    res["P_sr3_h3"] = table(P, "sr3", 3)
    res["P_sr10_h5"] = table(P, "sr10", 5)
    res["P_cl_h1"] = table(P, "cl", 1)
    res["P_rng_h1"] = table(P, "rng", 1)
    res["P_dh20_h3"] = table(P, "dh20", 3)
    res["Out_sr_h1"] = table(d[~d["inp"]], "sr", 1)
    wd = []
    for k, gg in P.dropna(subset=["x1"]).groupby("wd"):
        t, G = ct(gg["x1"], gg["day"])
        wd.append({"wd": k, "n": len(gg), "mean_x%": 100 * gg["x1"].mean(), "t": t})
    res["P_weekday_h1"] = pd.DataFrame(wd)
    yr = []
    for k, gg in P.dropna(subset=["x1"]).groupby(P["ts"].dt.year):
        t, G = ct(gg["x1"], gg["day"])
        yr.append({"yr": k, "n": len(gg), "mean_x%": 100 * gg["x1"].mean(), "t": t})
    res["P_year_h1"] = pd.DataFrame(yr)
    return res
