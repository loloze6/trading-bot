def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # pooled mean daily return per coin
    mu = {}
    for c in bars:
        r = []
        for w, df in bars[c].items():
            r.append(df["close"].pct_change().dropna())
        mu[c] = pd.concat(r).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            n = len(df)
            raw = df.get("debug_info.components.above_ma.last_history_value")
            r1 = df["close"].pct_change()
            vol20 = r1.rolling(20).std()
            ret20b = df["close"]/df["close"].shift(20)-1
            for h in (5, 20):
                for i in range(0, n-h, h):
                    rows.append(dict(coin=c, w=w, h=h, fc=df["forecast"].iloc[i],
                        raw=raw.iloc[i] if raw is not None else np.nan,
                        r1=r1.iloc[i], vol=vol20.iloc[i], past20=ret20b.iloc[i],
                        alloc=df["postRebalance_current_allocation"].iloc[i],
                        fwd=cl[i+h]/cl[i]-1, ex=cl[i+h]/cl[i]-1-h*mu[c],
                        wd=pd.Timestamp(df["timestamp"].iloc[i]).weekday()))
    S = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                              hit=(g["ex"]>0).mean()))
    s20 = S[S.h==20].copy()
    s20["fcb"] = np.where(s20.fc<=0, "0", pd.cut(s20.fc, [0,5,10,15,20.01], labels=["0-5","5-10","10-15","15-20"]).astype(str))
    out["h20 by forecast bucket"] = s20.groupby("fcb").apply(summ)
    s20r = s20.dropna(subset=["raw"]).copy()
    s20r["rawq"] = pd.qcut(s20r.raw, 6, duplicates="drop")
    out["h20 by raw distance sextile"] = s20r.groupby("rawq").apply(summ)
    s20v = s20.dropna(subset=["vol"]).copy()
    s20v["volq"] = s20v.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["h20 by vol tercile (per coin)"] = s20v.groupby("volq").apply(summ)
    s20p = s20.dropna(subset=["past20"]).copy()
    s20p["pq"] = s20p.groupby("coin")["past20"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["h20 by past20 quintile"] = s20p.groupby("pq").apply(summ)
    s5 = S[S.h==5].dropna(subset=["r1"]).copy()
    s5["r1q"] = s5.groupby("coin")["r1"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["h5 by 1d-move quintile"] = s5.groupby("r1q").apply(summ)
    s5p = s5.dropna(subset=["past20"]).copy()
    s5p["pq"] = s5p.groupby("coin")["past20"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["h5 by past20 quintile"] = s5p.groupby("pq").apply(summ)
    # weekday on daily coin returns, book
    D = []
    for c in days:
        for w, df in days[c].items():
            d = df.copy(); d["coin"]=c; d["w"]=w; D.append(d)
    D = pd.concat(D).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin daily by weekday"] = D.groupby("wd")["coin_return"].agg(["count","mean",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # book decomposition
    al = []
    for c in bars:
        for w, df in bars[c].items():
            a = df["postRebalance_current_allocation"].mean(); al.append(a*mu[c])
    out["book mean daily"] = D.groupby(["w","day"])["book_return"].mean().mean()
    out["market part approx"] = float(np.mean(al))
    # by coin forecast-weighted
    out["h20 by coin, fc>0 vs 0"] = s20.assign(on=s20.fc>0).groupby(["coin","on"]).apply(summ)
    return out
