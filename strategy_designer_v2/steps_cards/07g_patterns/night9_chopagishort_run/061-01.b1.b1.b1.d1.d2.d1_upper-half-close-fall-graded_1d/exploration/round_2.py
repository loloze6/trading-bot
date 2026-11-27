def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            n = len(b)
            if n < 20: continue
            c = b["close"].values
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            loc = ((b["close"] - b["low"]) / rng).values
            s = pd.Series(c)
            ret5 = s.pct_change(5).values
            ret60 = s.pct_change(60).values
            vol30 = s.pct_change().rolling(30, min_periods=20).std().values
            ts = pd.to_datetime(b["timestamp"])
            inprof = (b["regime"] != "chop").values
            for h in (1, 2, 3):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=ts[i].normalize(), year=ts[i].year,
                                     loc=loc[i], ret5=ret5[i], ret60=ret60[i], vol=vol30[i],
                                     inprof=inprof[i], fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["unus"] = d["fwd"] - d["drift"]
    def tst(g):
        s = g.groupby("day")["unus"].sum()
        m = g["unus"].mean(); se = np.sqrt((s ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=len(s), mean=round(m, 4), t=round(m / se, 2) if se else np.nan))
    out = {}
    o = d[~d.inprof].dropna(subset=["loc", "ret5"]).copy()
    o["trend"] = np.select([o.ret60 > 0.10, o.ret60 < -0.10, o.ret60.notna()], ["rising", "falling", "choppy"], "na")
    o["locb"] = pd.cut(o["loc"], [-0.01, 0.25, 0.5, 0.75, 0.9, 1.01], labels=["q1", "q2", "q3", "q4a", "q4b"])
    neg = o[o.ret5 < 0]
    for h in (1, 2, 3):
        out[f"other r5neg h{h} by loc"] = neg[neg.h == h].groupby("locb", observed=True).apply(tst)
    x = neg[(neg.h == 2) & (neg["loc"] > 0.75)]
    out["other r5neg top-quarter h2 by trend"] = x.groupby("trend").apply(tst)
    out["other r5neg top-quarter h2 by year"] = x.groupby("year").apply(tst)
    x = x.assign(dq=pd.qcut(x["ret5"], 3, labels=["deep", "mid", "shallow"]))
    out["other r5neg top-quarter h2 by ret5 depth"] = x.groupby("dq", observed=True).apply(tst)
    x2 = x.dropna(subset=["vol"]).copy()
    x2["vq"] = pd.qcut(x2["vol"], 3, labels=["lowvol", "midvol", "highvol"])
    out["other r5neg top-quarter h2 by vol tercile"] = x2.groupby("vq", observed=True).apply(tst)
    pos = o[(o.ret5 >= 0) & (o.h == 2)]
    out["other r5pos h2 by loc"] = pos.groupby("locb", observed=True).apply(tst)
    # book concentration
    br = pd.concat([dd.assign(coin=c, w=w) for c, ws in data["days"].items() for w, dd in ws.items()])
    book = br.groupby(["w", "day"])["book_return"].mean().dropna()
    srt = book.sort_values()
    out["book total sum"] = float(book.sum())
    out["book top5 days sum"] = float(srt.tail(5).sum())
    out["book bottom5 days sum"] = float(srt.head(5).sum())
    out["book sum excl w16"] = float(book.drop("w16", level=0).sum())
    tr = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    out["trades by window"] = tr.groupby("w")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades win share"] = float((tr["net_profit_loss_percent"] > 0).mean())
    return out
