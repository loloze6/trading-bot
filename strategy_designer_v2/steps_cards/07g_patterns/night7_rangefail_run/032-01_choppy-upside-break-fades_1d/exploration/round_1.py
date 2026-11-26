def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ph = hi.shift(1).rolling(20).max(); pl = lo.shift(1).rolling(20).min()
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            tr60 = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            fwd = c.shift(-H) / c - 1
            fwd10 = c.shift(-10) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": ts, "pos": np.arange(len(b)),
                "dh": (c / ph - 1) * 100, "dl": (c / pl - 1) * 100,
                "r1": r1, "z1": r1 / vol20, "volratio": vol20 / vol60,
                "tr60": tr60, "tr20": tr20, "fwd": fwd, "fwd10": fwd10,
                "range20": (ph / pl - 1) * 100,
                "wd": ts.dt.weekday, "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    usual = g.groupby("coin")["fwd"].std()
    g["u"] = g["fwd"] - g["coin"].map(drift)
    g["s"] = g["u"] / g["coin"].map(usual)

    def stat(x):
        x = x.dropna(subset=["u"])
        n = len(x)
        if n < 3: return pd.Series({"n": n})
        m = x["u"].mean()
        ds = (x["u"] - m).groupby(x["ts"]).sum()
        se = np.sqrt((ds ** 2).sum()) / n
        return pd.Series({"n": n, "days": ds.size, "mean_u%": 100 * m, "t_cl": m / se if se > 0 else np.nan,
                          "strength": x["s"].mean()})

    def prof(t):
        if pd.isna(t): return "na"
        return "rising" if t > 0.10 else ("falling" if t < -0.10 else "choppy")
    g["prof"] = g["tr60"].map(prof)
    out = {}
    out["drift_usual"] = pd.DataFrame({"drift%": 100 * drift, "usual%": 100 * usual})
    # breakouts up by profile
    up = g[g["dh"] > 0]
    out["break_up_by_prof"] = up.groupby("prof").apply(stat)
    up = up.copy(); up["q"] = pd.qcut(up["dh"], 3, labels=False, duplicates="drop")
    out["break_up_by_size_tercile"] = up.groupby("q").apply(stat)
    dn = g[g["dl"] < 0].copy()
    out["break_dn_by_prof"] = dn.groupby("prof").apply(stat)
    dn["q"] = pd.qcut(dn["dl"], 3, labels=False, duplicates="drop")
    out["break_dn_by_size_tercile"] = dn.groupby("q").apply(stat)
    # position in range
    g["rpos"] = pd.cut(g["dh"], [-1e9, -30, -20, -10, -5, 0, 1e9])
    out["by_dist_from_high"] = g.groupby("rpos").apply(stat)
    # after large 1-day moves
    g["zq"] = pd.cut(g["z1"], [-1e9, -2, -1, 0, 1, 2, 1e9])
    out["by_z1"] = g.groupby("zq").apply(stat)
    # vol regime
    g["vq"] = pd.qcut(g["volratio"], 4, labels=False)
    out["by_volratio_q"] = g.groupby("vq").apply(stat)
    out["by_tr20_q"] = g.assign(q=pd.qcut(g["tr20"], 5, labels=False)).groupby("q").apply(stat)
    out["by_tr60_prof"] = g.groupby("prof").apply(stat)
    out["by_weekday"] = g.groupby("wd").apply(stat)
    out["by_year"] = g.groupby(g["ts"].dt.year).apply(stat)
    # range width
    out["by_range20_q"] = g.assign(q=pd.qcut(g["range20"], 4, labels=False)).groupby("q").apply(stat)
    # book: active share and gain by coin
    act = d[d["alloc"].abs() > 1e-9]
    out["active_bars_by_coin"] = act.groupby("coin").size()
    return out
