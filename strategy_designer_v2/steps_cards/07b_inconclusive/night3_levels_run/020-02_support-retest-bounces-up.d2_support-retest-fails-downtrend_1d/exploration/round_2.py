import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    out = {}
    def tt(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    for h in [5,10,20]:
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values; n = len(c)
                fc = df["forecast"].values
                fl = df.get("debug_info.components.fall90.last_history_value")
                fl = fl.values if fl is not None else np.full(n, np.nan)
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                for i in range(0, n, h):
                    if i+h >= n: continue
                    rows.append({"coin":coin,"fc":fc[i],"fall":fl[i],"year":yr[i],
                                 "r":c[i+h]/c[i]-1,
                                 "rd": (c[i+h]/c[i+1]-1) if i+1+h <= n-1 and i+1<n else np.nan})
        g = pd.DataFrame(rows)
        g["d"] = g.groupby("coin")["r"].transform("mean")
        g["x"] = -(g["r"]-g["d"])
        g["xd"] = -(g["rd"]-g["d"])
        a = g[g.fc < 0].copy()
        out[f"h{h}_active"] = tt(a["x"])
        out[f"h{h}_active_from_next_close"] = tt(a["xd"])
        out[f"h{h}_inactive"] = tt(g[g.fc==0]["x"])
        out[f"h{h}_by_coin"] = a.groupby("coin")["x"].apply(tt).unstack()
        out[f"h{h}_by_year"] = a.groupby("year")["x"].apply(tt).unstack()
        a["fq"] = pd.qcut(a.fall.rank(method="first"), 3, labels=False)
        out[f"h{h}_by_fall_tercile_low_is_deeper"] = a.groupby("fq")["x"].apply(tt).unstack()
        out[f"h{h}_fall_tercile_median"] = a.groupby("fq")["fall"].median()
        a["cq"] = pd.qcut((-a.fc).rank(method="first"), 3, labels=False)
        out[f"h{h}_by_fc_tercile"] = a.groupby("cq")["x"].apply(tt).unstack()
        out[f"h{h}_drift_mean"] = g.groupby("coin")["r"].mean()
    return out
