import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            ret7 = c / c.shift(7) - 1
            s7 = ret7 / (sd30 * np.sqrt(7))
            ret60 = c / c.shift(60) - 1
            f7 = c.shift(-7) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "inprof": (b["regime"] == "unknown").values, "s7": s7, "ret7": ret7,
                "ret60": ret60, "sd30": sd30, "f7": f7, "year": ts.dt.year,
                "dayn": (ts - pd.Timestamp("2000-01-01", tz=ts.dt.tz)).dt.days}))
    d = pd.concat(rows, ignore_index=True)
    drift7 = d.loc[d.pos % 7 == 0, "f7"].mean()
    d["unus"] = d["f7"] - drift7
    out = {}
    g = d[(d.pos % 7 == 0)].dropna(subset=["s7", "f7"])
    ip = g[g.inprof].copy()
    def clus_t(x):
        s = x.groupby("dayn")["unus"].sum()
        n = len(x); m = x["unus"].mean()
        dev = x.groupby("dayn").apply(lambda z: (z["unus"] - m).sum())
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return pd.Series({"mean": m, "n": n, "days": G, "t_clus": m / se})
    out["in-profile grid, all"] = clus_t(ip)
    ip["side"] = np.where(ip.s7 < 0, "fall", "rise")
    out["in-profile by 7d side"] = ip.groupby("side").apply(clus_t)
    out["in-profile by coin"] = ip.groupby("coin").apply(lambda z: pd.Series({"mean": z.unus.mean(), "n": len(z)}))
    out["in-profile by window"] = ip.groupby("w").apply(lambda z: pd.Series({"mean": z.unus.mean(), "n": len(z)}))
    # every in-profile bar (overlapping), grouped by window to see breadth
    a = d[d.inprof].dropna(subset=["f7"])
    out["all in-profile bars by window"] = a.groupby("w").apply(lambda z: pd.Series({"mean": z.unus.mean(), "bars": len(z), "coins": z.coin.nunique()}))
    # grading within profile: ret60 and sd30 position
    ip["r60q"] = pd.qcut(ip["ret60"], 3, labels=False)
    out["in-profile by 60d return tercile"] = ip.groupby("r60q").apply(clus_t)
    # outside profile: choppy (|ret60|<0.1) any agitation, by s7 sign
    ch = g[(g.ret60.abs() < 0.1) & (~g.inprof)].copy()
    ch["s7q"] = pd.qcut(ch["s7"], 4, labels=False)
    out["choppy not-in-profile by s7 quartile"] = ch.groupby("s7q").apply(clus_t)
    return out
