def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            df = pd.DataFrame({"coin": coin, "win": w, "r": r, "z": z,
                               "fc": b["forecast"].astype(float),
                               "inprof": (b["regime"] == "unknown"),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year})
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["pos"] = np.arange(len(df))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["f1"].mean()
    d["d1"] = d["f1"] - d["coin"].map(drift)
    for h in (2, 3, 5):
        dr = d[d["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        d[f"d{h}"] = d[f"f{h}"] - d["coin"].map(dr)
    p = d[d["inprof"] & d["z"].notna() & d["d1"].notna()].copy()

    def st(x):
        x = x.dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    p["zb"] = pd.cut(p["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    out = {}
    out["in_profile_next1_unusual_by_z"] = p.groupby("zb")["d1"].apply(st).unstack()
    for h in (2, 3, 5):
        q = p[p["pos"] % h == 0]
        out[f"next{h}_unusual_by_z"] = q.groupby("zb")[f"d{h}"].apply(st).unstack()
    up = p[p["z"] > 0]
    out["up_by_coin_d1"] = up.groupby("coin")["d1"].apply(st).unstack()
    out["up_by_win_d1"] = up.groupby("win")["d1"].apply(st).unstack()
    big = p[p["z"] > 1]
    out["bigup_by_year_d1"] = big.groupby("yr")["d1"].apply(st).unstack()
    out["corr_z_d1_up"] = float(up[["z", "d1"]].corr().iloc[0, 1])
    out["corr_z_d1_all_profile"] = float(p[["z", "d1"]].corr().iloc[0, 1])
    # outside profile for comparison
    o = d[(~d["inprof"]) & d["z"].notna() & d["d1"].notna()].copy()
    o["zb"] = pd.cut(o["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["outside_profile_d1_by_z"] = o.groupby("zb")["d1"].apply(st).unstack()
    out["share_inprof"] = float(d["inprof"].mean())
    return out
