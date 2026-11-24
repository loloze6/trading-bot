def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=15).std()
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "wd": ts.dt.weekday.values, "yr": ts.dt.year.values, "day": ts.dt.normalize().values,
                "vol": vol, "z14": (c / c.shift(14) - 1) / (vol * np.sqrt(14)),
                "z1": r1 / vol, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "g1": b["postRebalance_current_allocation"].astype(float) * (c.shift(-1) / c - 1),
            }))
    d = pd.concat(rows, ignore_index=True)
    for h in [2, 5]:
        g = d[d["pos"] % h == 0].groupby("coin")[f"f{h}"]
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(g.mean())

    def tday(s, day):
        x = pd.DataFrame({"v": s - s.mean(), "day": day}).dropna().groupby("day")["v"].sum()
        se = np.sqrt((x ** 2).sum()) / len(s.dropna())
        return (s.mean() / se if se > 0 else np.nan), len(x)

    out = {}
    # A. Thu and Fri momentum split by sign of z14, signed drift-removed move in the z14 direction
    res = []
    for wd in [2, 3, 4]:
        s = d[d["wd"] == wd].dropna(subset=["z14", "x2"])
        for side, g in [("up", s[s["z14"] > 0]), ("down", s[s["z14"] < 0])]:
            sg = np.sign(g["z14"])
            v = sg * g["x2"]
            t, n = tday(v, g["day"])
            vg = g["z14"].abs().clip(0, 3) * v
            t2, _ = tday(vg, g["day"])
            res.append({"wd": wd, "side": side, "dir_x2": v.mean(), "t": t, "graded": vg.mean(), "t_graded": t2, "days": n})
    out["Wed/Thu/Fri momentum by side"] = pd.DataFrame(res)
    # B. Thu+Fri graded momentum by year
    s = d[d["wd"].isin([3, 4])].dropna(subset=["z14", "x2"])
    v = s["z14"].clip(-3, 3) * s["x2"]
    res = []
    for y, idx in s.groupby("yr").groups.items():
        t, n = tday(v.loc[idx], s.loc[idx, "day"])
        res.append({"yr": y, "mean": v.loc[idx].mean(), "t": t, "days": n})
    out["Thu+Fri momentum by year"] = pd.DataFrame(res)
    # C. Thu+Fri by coin
    res = []
    for cn, idx in s.groupby("coin").groups.items():
        t, n = tday(v.loc[idx], s.loc[idx, "day"])
        res.append({"coin": cn, "mean": v.loc[idx].mean(), "t": t})
    out["Thu+Fri momentum by coin"] = pd.DataFrame(res)
    # D. large up day -> 5d, by year and graded
    s5 = d[d["pos"] % 5 == 0].dropna(subset=["z1", "x5"])
    res = []
    for y, g in s5.groupby("yr"):
        top = g[g["z1"] > g["z1"].quantile(.8)]
        res.append({"yr": y, "top_x5": top["x5"].mean(), "all_x5": g["x5"].mean(), "n_top": len(top)})
    out["top 1d-move quintile 5d by year"] = pd.DataFrame(res)
    vv = s5["z1"].clip(-3, 3) * s5["x5"]
    out["z1 x x5 graded t, days"] = str(tday(vv, s5["day"]))
    # E. book gain per coin-day: long vs short positions, by weekday of the held bar
    p = d.dropna(subset=["g1"])
    p = p[p["alloc"] != 0].copy()
    p["side"] = np.where(p["alloc"] > 0, "long", "short")
    out["position gain by side and weekday"] = p.groupby(["wd", "side"])["g1"].agg(["mean", "count"]).unstack()
    return out
