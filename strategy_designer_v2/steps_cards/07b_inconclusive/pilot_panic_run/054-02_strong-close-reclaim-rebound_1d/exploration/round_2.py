def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []; drift = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; lo = df["low"].values; hi = df["high"].values; op = df["open"].values
            n = len(df)
            for i in range(0, n - 5, 5): g.append(c[i+5]/c[i]-1)
            low30 = pd.Series(lo).rolling(30, min_periods=30).min().shift(1).values
            infa = (df["regime"] != "chop").values
            fc = df["forecast"].values
            for i in range(n):
                if np.isnan(low30[i]) or not infa[i]: continue
                if lo[i] < low30[i] <= c[i]:
                    rng = hi[i]-lo[i]
                    d = dict(coin=coin, w=w, day=str(df["timestamp"].iloc[i])[:10],
                             rec=(c[i]-low30[i])/rng if rng>0 else np.nan,
                             clv=(c[i]-lo[i])/rng if rng>0 else np.nan,
                             recpct=(c[i]-low30[i])/low30[i],
                             pierce=(low30[i]-lo[i])/low30[i],
                             rngpct=rng/c[i], body=(c[i]-op[i])/op[i],
                             fc=fc[i], gridpos=i % 5)
                    for h in [2,5,7,10]:
                        d[f"r{h}"] = c[i+h]/c[i]-1 if i+h<n else np.nan
                    rows.append(d)
        drift[coin] = np.mean(g)
    ev = pd.DataFrame(rows)
    ev["x5"] = ev["r5"] - ev["coin"].map(drift)
    for h in [2,7,10]:
        ev[f"x{h}"] = ev[f"r{h}"] - ev["coin"].map(drift)*h/5
    def summ(g):
        o = {"n": len(g), "days": g["day"].nunique()}
        for h in [2,5,7,10]:
            x = g[f"x{h}"].dropna()
            o[f"mx{h}"] = x.mean(); o[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(o)
    res = {}
    for col in ["rec","clv","recpct","pierce","rngpct","body","fc"]:
        res[f"corr_{col}_x5"] = float(ev[[col,"x5"]].dropna().corr(method="spearman").iloc[0,1])
        try:
            res[f"by_{col}"] = ev.assign(q=pd.qcut(ev[col].rank(method="first"),2,labels=["low","high"])).groupby("q").apply(summ)
        except Exception as e:
            res[f"by_{col}"] = str(e)
    res["fc_active_share"] = float((ev["fc"]>0).mean())
    res["by_window"] = ev.groupby("w").apply(summ)
    return res
