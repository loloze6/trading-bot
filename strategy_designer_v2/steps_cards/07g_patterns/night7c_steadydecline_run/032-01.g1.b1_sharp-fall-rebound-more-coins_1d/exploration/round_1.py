def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            vsr = r / vol20.shift(1)
            ret20 = c / c.shift(20) - 1
            ret20v = ret20 / (vol20 * np.sqrt(20))
            rng = (b["high"] - b["low"]) / c
            rngr = rng / rng.rolling(20).mean()
            volr = b["volume"] / b["volume"].rolling(20).mean()
            maxdd = (rng.rolling(20).max()) / rng.rolling(60, min_periods=30).mean()
            ret5 = c / c.shift(5) - 1
            for h in (2, 5):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                     fwd=fwd.iloc[i], vsr=vsr.iloc[i], ret20v=ret20v.iloc[i],
                                     rngr=rngr.iloc[i], volr=volr.iloc[i], vol20=vol20.iloc[i],
                                     ret5=ret5.iloc[i] / (vol20.iloc[i]*np.sqrt(5)) if vol20.iloc[i] else np.nan,
                                     calm=maxdd.iloc[i]))
    df = pd.DataFrame(rows)
    df["un"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    def tab(d, col, q=5):
        d = d.dropna(subset=[col, "un"]).copy()
        d["bin"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        def f(g):
            s = g.groupby("day")["un"].sum()
            dm = g["un"].mean()
            t = s.sum() / len(g) / (s.std(ddof=1) * np.sqrt(len(s)) / len(g)) if len(s) > 2 else np.nan
            return pd.Series(dict(n=len(g), days=len(s), lo=g[col].min(), hi=g[col].max(),
                                  mean_un=dm, t=t))
        out = d.groupby("bin").apply(f)
        sl = stats.spearmanr(d[col], d["un"])
        out.loc["spearman", "mean_un"] = sl.correlation
        out.loc["spearman", "t"] = sl.pvalue
        return out
    res = {}
    for h in (2, 5):
        d = df[df.h == h]
        res[f"h{h}_vsr"] = tab(d, "vsr")
        res[f"h{h}_ret20v"] = tab(d, "ret20v")
        res[f"h{h}_ret5v"] = tab(d, "ret5")
        res[f"h{h}_vol20"] = tab(d, "vol20")
        res[f"h{h}_volr"] = tab(d, "volr")
        res[f"h{h}_rngr"] = tab(d, "rngr")
        res[f"h{h}_wd"] = d.groupby("wd")["un"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # calm decline: ret20v in lowest tercile and calm low
    d = df[(df.h == 5)].dropna(subset=["ret20v", "calm"])
    dec = d[d.ret20v < d.ret20v.quantile(0.3)]
    res["h5_decline_by_calm"] = tab(dec, "calm", 3)
    # book: daily returns by regime / trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    if len(tr):
        res["trades"] = pd.Series(dict(n=len(tr), mean_net=tr.net_profit_loss_percent.mean(),
                                       win=(tr.net_profit_loss_percent > 0).mean(),
                                       t=tr.net_profit_loss_percent.mean()/tr.net_profit_loss_percent.std()*np.sqrt(len(tr))))
    return res
