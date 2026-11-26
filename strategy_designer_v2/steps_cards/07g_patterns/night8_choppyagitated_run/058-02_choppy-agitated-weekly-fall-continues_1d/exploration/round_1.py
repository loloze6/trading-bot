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
            f7 = c.shift(-7) / c - 1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            ret1s = r1 / sd30
            rng = (b["high"] - b["low"]) / c / sd30
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "inprof": (b["regime"] == "unknown").values,
                               "s7": s7, "f7": f7, "f3": f3, "f1": f1, "r1s": ret1s,
                               "rng": rng, "clo": clo, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    out["share_in_profile"] = d["inprof"].mean()
    drift7 = d.loc[d.pos % 7 == 0, "f7"].mean()
    out["drift7_all"] = drift7
    g = d[(d.pos % 7 == 0)].dropna(subset=["s7", "f7"]).copy()
    g["unus"] = g["f7"] - drift7
    def tab(x, col, by):
        t = x.groupby(by)[col].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t
    g["s7q"] = pd.qcut(g["s7"], 5, labels=False)
    out["f7 by s7 quintile, in profile"] = tab(g[g.inprof], "unus", "s7q")
    out["f7 by s7 quintile, out profile"] = tab(g[~g.inprof], "unus", "s7q")
    out["s7 quintile edges"] = pd.Series(g["s7"].quantile([0, .2, .4, .6, .8, 1]).values)
    ip = g[g.inprof]
    out["corr s7 f7 in/out"] = pd.Series({"in": stats.spearmanr(ip.s7, ip.f7)[0], "n_in": len(ip),
                                          "out": stats.spearmanr(g[~g.inprof].s7, g[~g.inprof].f7)[0], "n_out": int((~g.inprof).sum())})
    g3 = d[d.pos % 3 == 0].dropna(subset=["r1s", "f3", "rng", "clo"]).copy()
    dr3 = g3["f3"].mean(); g3["u3"] = g3["f3"] - dr3
    g3["r1q"] = pd.qcut(g3["r1s"], 5, labels=False)
    out["f3 by 1-day scaled return quintile, all"] = tab(g3, "u3", "r1q")
    out["f3 by 1d quintile, in profile"] = tab(g3[g3.inprof], "u3", "r1q")
    g3["rngq"] = pd.qcut(g3["rng"], 5, labels=False)
    out["f3 by range quintile"] = tab(g3, "u3", "rngq")
    g3["cloq"] = pd.qcut(g3["clo"], 5, labels=False)
    out["f3 by close location quintile"] = tab(g3, "u3", "cloq")
    g1 = d.dropna(subset=["f1"]).copy()
    g1["u1"] = g1["f1"] - g1["f1"].mean()
    out["f1 by weekday"] = tab(g1, "u1", "wd")
    out["f7 in-profile by year"] = tab(ip, "unus", "year")
    return out
