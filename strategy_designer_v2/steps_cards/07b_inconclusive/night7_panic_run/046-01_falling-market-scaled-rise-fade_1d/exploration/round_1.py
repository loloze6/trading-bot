import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            r60 = c / c.shift(60) - 1
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "r": r, "z": z, "fall_rec": (b["regime"] == "unknown"),
                               "r60": r60, "nxt": nxt, "nxt2": nxt2, "fc": b["forecast"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["ex2"] = d["nxt2"] - 2 * d["coin"].map(drift)
    d["prof"] = np.where(d["r60"] < -0.10, "falling", np.where(d["r60"] > 0.10, "rising", "choppy"))
    d = d.dropna(subset=["z", "ex"])

    def stat(g, col="ex", sign=-1):
        v = sign * g[col].dropna()
        if len(v) < 5: return pd.Series({"n": len(v), "mean%": np.nan, "t": np.nan})
        dd = (sign * g[col]).groupby(g["day"]).sum().dropna()
        t = dd.mean() / (dd.std() / np.sqrt(len(dd))) * 1.0
        return pd.Series({"n": len(v), "mean%": 100 * v.mean(), "t_day": t})

    up = d[d["z"] > 0]; dn = d[d["z"] < 0]
    out = {}
    # fade after up days (short) per profile
    out["up_by_profile_short"] = up.groupby("prof").apply(stat)
    # rebound after down days (long) per profile
    out["down_by_profile_long"] = dn.groupby("prof").apply(lambda g: stat(g, sign=1))
    fu = up[up["fall_rec"]]; fd = dn[dn["fall_rec"]]
    fu = fu.assign(q=pd.qcut(fu["z"], 5, labels=False))
    fd = fd.assign(q=pd.qcut(fd["z"], 5, labels=False))
    out["fall_up_by_zquint_short"] = fu.groupby("q").apply(stat)
    out["fall_up_by_zquint_short_2d"] = fu.groupby("q").apply(lambda g: stat(g, "ex2"))
    out["fall_down_by_zquint_long"] = fd.groupby("q").apply(lambda g: stat(g, sign=1))
    out["fall_up_by_coin"] = fu.groupby("coin").apply(stat)
    out["fall_up_by_year"] = fu.groupby("year").apply(stat)
    out["fall_up_by_win"] = fu.groupby("win").apply(stat)
    # agitation proxy: 30d sd vs its rolling 365 median not avail in short windows; use sd rank within coin
    out["fall_up_all_2d"] = stat(fu, "ex2")
    out["fall_down_all_2d_long"] = stat(fd, "ex2", 1)
    out["drift_daily%"] = 100 * drift
    return out
