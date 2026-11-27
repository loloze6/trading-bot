def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            st = (c - sma) / sma / sd
            ret1 = r
            ret5d = c.pct_change(5)
            ret20 = c.pct_change(20)
            rng = (b["high"] - b["low"]) / c
            for h in (5, 10):
                fw = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if np.isnan(fw.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ts=b["timestamp"].iloc[i],
                                     reg=b["regime"].iloc[i], st=st.iloc[i], r1=ret1.iloc[i],
                                     r5=ret5d.iloc[i], r20=ret20.iloc[i], rng=rng.iloc[i],
                                     fw=fw.iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fw"].transform("mean")
    df["un"] = df["fw"] - df["drift"]
    df["wd"] = pd.to_datetime(df["ts"]).dt.dayofweek
    df["yr"] = pd.to_datetime(df["ts"]).dt.year
    out["regime counts"] = df[df.h == 5]["reg"].value_counts()

    def tab(d, key):
        g = d.groupby(key)["un"]
        res = g.agg(["mean", "count"])
        res["t"] = g.mean() / (g.std() / np.sqrt(g.count()))
        return res.round(4)

    for h in (5, 10):
        d = df[(df.h == h) & df.st.notna()].copy()
        d["stq"] = pd.qcut(d["st"], 6, labels=False)
        out[f"h{h} stretch sextile x regime"] = tab(d, ["reg", "stq"])
        d["r1q"] = pd.qcut(d["r1"], 5, labels=False)
        out[f"h{h} 1d return quintile x regime"] = tab(d, ["reg", "r1q"])
        d["r20q"] = pd.qcut(d["r20"], 5, labels=False)
        out[f"h{h} 20d return quintile x regime"] = tab(d, ["reg", "r20q"])
        d["rngq"] = pd.qcut(d["rng"], 5, labels=False)
        out[f"h{h} range quintile x regime"] = tab(d, ["reg", "rngq"])
    d5 = df[df.h == 5]
    out["h5 weekday"] = tab(d5, "wd")
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; days.append(x)
    D = pd.concat(days)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book by window"] = D.groupby("w")[["book_return", "coin_return"]].mean().round(5)
    out["book by year"] = D.groupby("yr")[["book_return", "coin_return"]].mean().round(5)
    out["book by coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean().round(5)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades by |entry forecast| quartile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
    return out
