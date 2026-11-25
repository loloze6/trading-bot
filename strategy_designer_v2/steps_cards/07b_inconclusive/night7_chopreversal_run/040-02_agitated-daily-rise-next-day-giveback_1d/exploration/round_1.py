def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            # 60-day mean abs move for standardised size
            mabs = r.abs().rolling(60, min_periods=20).mean()
            z = r / mabs
            for h in (1, 2, 3):
                b[f"f{h}"] = c.shift(-h) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "r": r, "z": z,
                               "agit": (b["regime"] != "chop").values,
                               "pos": b["postRebalance_current_allocation"].astype(float),
                               "f1": b["f1"], "f2": b["f2"], "f3": b["f3"],
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "ts": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["r", "f1"])
    drift = d.groupby("coin")["f1"].mean()
    d["x1"] = d["f1"] - d["coin"].map(drift)
    out = {}
    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    # grading: bins of z among up days, agitated vs calm; fade gain = -x1 on up, +x1 on down
    d["fade"] = -np.sign(d["r"]) * d["x1"]
    d["zbin"] = pd.cut(d["z"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    g = d.groupby(["agit", "zbin"], observed=True)["fade"].apply(tstat).unstack()
    out["fade gain by agit and size bin (z = move / 60d mean abs)"] = g
    # regression slope next-day excess on z, by agit and side
    res = []
    for a in (True, False):
        for side, m in (("up", d["r"] > 0), ("down", d["r"] < 0)):
            s = d[(d["agit"] == a) & m].dropna(subset=["z"])
            sl = stats.linregress(s["z"], s["x1"])
            res.append({"agit": a, "side": side, "n": len(s), "slope_bp_per_z": 1e4*sl.slope, "t": sl.slope/sl.stderr})
    out["slope next-day excess on z"] = pd.DataFrame(res)
    au = d[(d["agit"]) & (d["r"] > 0)]
    out["agit up fade by coin"] = au.groupby("coin")["fade"].apply(tstat).unstack()
    out["agit up fade by window"] = au.groupby("win")["fade"].apply(tstat).unstack()
    out["agit down fade by coin"] = d[(d["agit"]) & (d["r"] < 0)].groupby("coin")["fade"].apply(tstat).unstack()
    # horizons on agit up days: return over 2,3 days minus drift
    hz = {}
    for h in (1, 2, 3):
        dr = d.groupby("coin")[f"f{h}"].mean()
        hz[h] = tstat(-(au[f"f{h}"] - au["coin"].map(dr)))
    out["agit up fade over h days (overlapping)"] = pd.DataFrame(hz).T
    # book gain by coin on position bars
    pb = d[d["pos"] != 0]
    out["position x next-day return by coin"] = pb.assign(g=pb["pos"]*pb["f1"]).groupby("coin")["g"].apply(tstat).unstack()
    return out
