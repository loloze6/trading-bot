import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    coin_mean = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            rs.append(pd.Series(c).pct_change().dropna())
        coin_mean[coin] = pd.concat(rs).mean()
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            r = pd.Series(c).pct_change()
            sd20 = r.rolling(20).std()
            raw = r / sd20
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(n):
                if b.loc[i, "regime"] != "unknown":
                    continue
                f = b.loc[i, "forecast"]
                if not (pd.notna(f) and f < 0):
                    continue
                d = {"coin": coin, "w": w, "year": ts[i].year, "day": ts[i].normalize(),
                     "absf": abs(f), "raw": raw[i], "sd20": sd20[i]}
                for h in (1, 2, 3, 5):
                    d[f"x{h}"] = (c[i+h]/c[i]-1 - h*coin_mean[coin]) if i+h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    out = {}
    def tday(s, sub):
        g = sub.groupby("day")[s].sum()
        nd = sub.groupby("day")[s].count()
        m = sub[s].mean()
        dev = sub[s] - m
        gs = dev.groupby(sub["day"]).sum()
        se = np.sqrt((gs**2).sum())/len(sub[s].dropna())
        return m, m/se if se > 0 else np.nan
    res = {}
    for h in (1,2,3,5):
        sub = df.dropna(subset=[f"x{h}"])
        m, t = tday(f"x{h}", sub)
        res[f"h{h}"] = {"n": len(sub), "mean_excess": m, "t_day": t}
    out["by_horizon"] = pd.DataFrame(res).T
    df["q"] = pd.qcut(df["absf"].rank(method="first"), 5, labels=False)
    q = {}
    for k, sub in df.groupby("q"):
        s = sub.dropna(subset=["x1"])
        m, t = tday("x1", s)
        m3, t3 = tday("x3", sub.dropna(subset=["x3"]))
        q[k] = {"n": len(s), "absf_mean": s.absf.mean(), "raw_mean": s.raw.mean(), "x1": m, "t1": t, "x3": m3, "t3": t3}
    out["by_forecast_quintile"] = pd.DataFrame(q).T
    for key in ("coin", "year", "w"):
        g = {}
        for k, sub in df.groupby(key):
            s = sub.dropna(subset=["x1"])
            if len(s) < 10: continue
            m, t = tday("x1", s)
            g[k] = {"n": len(s), "x1": m, "t1": t}
        out["by_"+key] = pd.DataFrame(g).T
    # vol level: sd20 relative within coin (median split)
    df["agit"] = df.groupby("coin")["sd20"].transform(lambda s: s > s.median())
    g = {}
    for k, sub in df.groupby("agit"):
        s = sub.dropna(subset=["x1"]); m, t = tday("x1", s)
        s3 = sub.dropna(subset=["x3"]); m3, t3 = tday("x3", s3)
        g[str(k)] = {"n": len(s), "x1": m, "t1": t, "x3": m3, "t3": t3}
    out["by_sd20_high"] = pd.DataFrame(g).T
    s = df.dropna(subset=["x1", "raw"])
    out["corr_raw_x1"] = stats.spearmanr(s.raw, s.x1)[0]
    return out
