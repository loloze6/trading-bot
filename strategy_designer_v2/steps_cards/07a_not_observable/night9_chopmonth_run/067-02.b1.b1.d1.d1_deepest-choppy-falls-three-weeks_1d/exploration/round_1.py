def explore(data):
    import numpy as np, pandas as pd
    H = 21
    rows = []
    allbars = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            n = len(b)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            ch = (b["regime"] == "mean_reversion")
            allbars.append(dict(coin=coin, window=w, bars=n, choppy_share=ch.mean(),
                                neg_fc_share=(b["forecast"] < 0).mean()))
            for i in range(0, n - H, H):
                f = b["forecast"].iloc[i]
                r = b["close"].iloc[i + H] / b["close"].iloc[i] - 1
                rows.append(dict(coin=coin, window=w, year=int(yr.iloc[i]), fc=f,
                                 ts=str(pd.to_datetime(b["timestamp"].iloc[i]).date()),
                                 choppy=bool(ch.iloc[i]), r=r))
    g = pd.DataFrame(rows)
    ab = pd.DataFrame(allbars)
    neg = g[g.fc < 0].copy()
    neg["r_short"] = -neg["r"]
    q = neg.fc.quantile(0.2)
    deep = neg[neg.fc <= q]
    out = {}
    out["grid cells total / choppy / negfc"] = pd.Series({"cells": len(g), "choppy": int(g.choppy.sum()),
                                                         "neg_fc": len(neg), "deep_fifth": len(deep),
                                                         "deep_distinct_days": deep.ts.nunique(),
                                                         "neg_distinct_days": neg.ts.nunique()})
    out["neg cases by window"] = neg.groupby("window").agg(n=("fc", "size"), days=("ts", "nunique"),
                                                           mean_rs=("r_short", "mean"))
    out["neg cases by coin"] = neg.groupby("coin").agg(n=("fc", "size"), mean_rs=("r_short", "mean"),
                                                       sd=("r_short", "std"))
    out["neg cases by year"] = neg.groupby("year").agg(n=("fc", "size"), days=("ts", "nunique"))
    out["deep by year"] = deep.groupby("year").agg(n=("fc", "size"), days=("ts", "nunique"),
                                                   mean_rs=("r_short", "mean"))
    out["forecast quantiles neg"] = neg.fc.quantile([0, .1, .2, .3, .5, .8, 1.0])
    out["share of bars choppy / negfc by coin"] = ab.groupby("coin")[["choppy_share", "neg_fc_share"]].mean()
    out["cases per day deep"] = deep.groupby("ts").size().value_counts().sort_index()
    out["deep r_short stats"] = pd.Series({"mean": deep.r_short.mean(), "sd": deep.r_short.std(),
                                           "rest_mean": neg[neg.fc > q].r_short.mean(),
                                           "rest_sd": neg[neg.fc > q].r_short.std()})
    return out
