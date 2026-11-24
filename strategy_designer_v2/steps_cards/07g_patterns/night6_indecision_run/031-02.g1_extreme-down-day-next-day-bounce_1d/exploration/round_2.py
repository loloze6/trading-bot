import pandas as pd, numpy as np

def _tc(df, col):
    d = df.dropna(subset=[col])
    if len(d) < 10: return (len(d), np.nan, np.nan, 0)
    m = d[col].mean()
    s = (d[col] - m).groupby(d["ts"]).sum()
    D = len(s)
    se = np.sqrt((s**2).sum() * D / (D - 1)) / len(d)
    return (len(d), round(m * 100, 3), round(m / se, 2), D)

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, o, h, l = b["close"], b["open"], b["high"], b["low"]
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            sd120 = r.rolling(120, min_periods=60).std()
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "z": r / sd,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "sd": sd, "vrel": sd / sd120,
                "f1": c.shift(-1) / c - 1,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            }))
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["wn"] = D["win"].str[1:].astype(int)
    D["half"] = np.where(D["wn"] <= 12, "w1-12", "w13-24")
    D["sdq"] = D.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    D["vrq"] = D.groupby("coin")["vrel"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    D["clvq"] = D.groupby("coin")["clv"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    D["zq"] = D.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out = {}
    def grp(df, keys):
        res = {k: _tc(g, "x1") for k, g in df.groupby(keys)}
        return pd.DataFrame(res, index=["n", "mean%", "t_day", "days"]).T
    out["clvq, day-clustered"] = grp(D, "clvq")
    out["clvq x half"] = grp(D, ["half", "clvq"])
    out["clvq on up days (z>0)"] = grp(D[D.z > 0], "clvq")
    out["clvq on down days (z<0)"] = grp(D[D.z < 0], "clvq")
    out["zq, day-clustered"] = grp(D, "zq")
    dn = D[D.z <= -1]
    out["z<=-1 by vol quintile, clustered"] = grp(dn, "sdq")
    out["z<=-1 by vol quintile x half"] = grp(dn, ["half", "sdq"])
    out["z<=-1 by vol rel to 120d (tercile)"] = grp(dn, "vrq")
    out["z in (-1,0] by vol quintile"] = grp(D[(D.z > -1) & (D.z <= 0)], "sdq")
    out["z>=1 by vol quintile"] = grp(D[D.z >= 1], "sdq")
    # graded: down-day return times vol
    D["dnr"] = np.minimum(D["z"], 0) * D["sd"]  # raw fall size
    dd = D[D.z <= -1].copy()
    dd["rq"] = dd.groupby("coin")["dnr"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["z<=-1 by raw fall tercile (0=deepest)"] = grp(dd, "rq")
    out["z<=-1 sdq4 by coin"] = grp(dn[dn.sdq == 4], "coin")
    out["z<=-1 sdq4 by year"] = grp(dn[dn.sdq == 4], "yr")
    return out
