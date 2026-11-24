def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            prox = df["debug_info.components.low_prox.last_history_value"].values
            for h in (10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, ts=df["timestamp"].iloc[i],
                                     fc=df["forecast"].iloc[i], prox=prox[i],
                                     past20=(c[i]/c[i-20]-1) if i >= 20 else np.nan,
                                     ret=c[i+h]/c[i]-1))
    g = pd.DataFrame(rows)
    g["year"] = pd.to_datetime(g["ts"]).dt.year
    g["ex"] = g["ret"] - g.groupby(["coin", "h"])["ret"].transform("mean")
    g["dnum"] = pd.to_datetime(g["ts"]).astype("int64") // 86400_000_000_000
    g["D"] = 1/g["prox"] - 1   # percent above the low

    def mt(d):
        dd = d.groupby("dnum")["ex"].sum()
        m = d["ex"].mean()
        se = np.sqrt((dd**2).sum() - 0) / len(d) if len(d) else np.nan
        return pd.Series(dict(n=len(d), days=len(dd), mean_ex=m, mean_ret=d["ret"].mean(),
                              t=m/se if se else np.nan))
    out = {}
    for h in (10, 20):
        gh = g[g.h == h].copy()
        gh["fbin"] = pd.cut(gh["fc"], [-20.01, -15, -10, -5, -2, -0.5, 0.01])
        out[f"h{h} by forecast bin"] = gh.groupby("fbin", observed=True).apply(mt)
        gh["Dbin"] = pd.cut(gh["D"], [-0.01, 1, 3, 7, 15, 30, 60, 1e9])
        out[f"h{h} by % above 365d low"] = gh.groupby("Dbin", observed=True).apply(mt)
    g20 = g[g.h == 20].copy()
    g20["at_low"] = np.where(g20["D"] <= 3, "within 3% of low", "farther")
    g20["mom"] = np.where(g20["past20"] < 0, "down", "up")
    out["h20 at_low x past20"] = g20.groupby(["at_low", "mom"]).apply(mt)
    out["h20 deep forecast (<=-10) by year"] = g20[g20.fc <= -10].groupby("year").apply(mt)
    out["h20 deep forecast (<=-10) by coin"] = g20[g20.fc <= -10].groupby("coin").apply(mt)
    out["last timestamp year"] = int(pd.to_datetime(g["ts"]).dt.year.max())
    return out
