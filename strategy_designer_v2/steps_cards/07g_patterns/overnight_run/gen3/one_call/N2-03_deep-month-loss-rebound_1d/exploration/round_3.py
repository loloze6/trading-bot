def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    ev = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            s = pd.Series(c); r1 = s.pct_change(); vol = r1.rolling(20).std()
            z = r1 / vol
            vq_thr = None
            last = -10
            for i in range(21, n - 5):
                if z.iloc[i] <= -1 and i - last >= 5:
                    ev.append(dict(coin=coin, w=w, vol=vol.iloc[i], f1=c[i+1]/c[i]-1, f5=c[i+5]/c[i]-1,
                                   f2_5=c[i+5]/c[i+1]-1, f=b["forecast"].iloc[i]))
                    last = i
    E = pd.DataFrame(ev)
    E["vq"] = E.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    def ag(g, col):
        return pd.Series({"n": len(g), "mean": g[col].mean(), "t": stats.ttest_1samp(g[col], 0).statistic, "hit": (g[col] > 0).mean()})
    for col in ["f1", "f5", "f2_5"]:
        out[f"z<=-1 spaced events {col} by vol tercile"] = E.groupby("vq").apply(lambda g: ag(g, col))
    out["z<=-1 events forecast>0 share by vol tercile"] = E.groupby("vq")["f"].apply(lambda s: (s > 0).mean())
    T = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["days"] = T["duration_minutes"] / 1440
    T["eb"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades by entry forecast quartile"] = T.groupby("eb").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"), med_days=("days", "median"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    T["long"] = T["days"] > 15
    out["share of total net pnl, trades >15d"] = T.groupby("long")["net_profit_loss_percent"].sum()
    return out
