def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            rr = ((b["high"] - b["low"]) / b["close"]).astype(float)
            mrr = rr.rolling(30, min_periods=20).mean().values
            r1 = pd.Series(c).pct_change().values
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            ts = pd.to_datetime(b["timestamp"])
            reg = b["regime"].values
            fc = b["forecast"].astype(float).values
            n = len(c)
            for t in range(0, n, 3):
                if t + 3 >= n: break
                past3 = c[t] / c[t-3] - 1 if t >= 3 else np.nan
                rows.append(dict(coin=coin, w=w, fwd=c[t+3]/c[t]-1, past3=past3,
                                 sc=past3/mrr[t] if mrr[t] == mrr[t] else np.nan,
                                 r1=r1[t], v=vol30[t], reg=reg[t], fc=fc[t],
                                 wd=ts[t].dayofweek, yr=ts[t].year))
            for t in range(1, n-1):
                daily.append(dict(coin=coin, r=r1[t], nxt=c[t+1]/c[t]-1,
                                  z=r1[t]/vol30[t] if vol30[t] == vol30[t] else np.nan,
                                  reg=reg[t], wd=ts[t].dayofweek))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["un"] = g["fwd"] - g["drift"]
    def summ(df, key):
        a = df.groupby(key)["un"].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.round(4)
    g["inprof"] = (g["reg"] == "unknown")
    g["scq"] = g.groupby("inprof")["sc"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["unusual fwd3 by scaled3 quintile x in falling calm"] = summ(g.dropna(subset=["scq"]), ["inprof", "scq"])
    g["vq"] = g.groupby("coin")["v"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["unusual fwd3 by vol30 quintile"] = summ(g.dropna(subset=["vq"]), "vq")
    out["unusual fwd3 by weekday"] = summ(g, "wd")
    out["unusual fwd3 by regime"] = summ(g, "reg")
    out["unusual fwd3 by year"] = summ(g, "yr")
    d = pd.DataFrame(daily).dropna()
    d["dr"] = d.groupby("coin")["nxt"].transform("mean")
    d["un"] = d["nxt"] - d["dr"]
    d["zq"] = pd.qcut(d["z"], 7, labels=False)
    out["next-day unusual by today's z-move septile"] = summ(d, "zq")
    out["next-day unusual by weekday"] = summ(d, "wd")
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.reset_index(drop=True).copy()
            x["coin"] = coin; x["w"] = w
            x["prev3"] = x["close"] / x["close"].shift(3) - 1
            x["next3"] = x["close"].shift(-3) / x["close"] - 1
            dd.append(x)
    D = pd.concat(dd)
    act = D[D["book_return"].abs() > 1e-12].dropna(subset=["book_return"])
    act = act.assign(bq=pd.qcut(act["book_return"], 5, labels=False))
    out["book active days by return quintile: coin prev3/next3/coinret"] = act.groupby("bq")[["book_return", "coin_return", "prev3", "next3"]].mean().round(4)
    out["book by coin: mean, count active"] = act.groupby("coin")["book_return"].agg(["mean", "count", "sum"]).round(5)
    out["book by window mean"] = act.groupby("w")["book_return"].agg(["mean", "count"]).round(5)
    return out
