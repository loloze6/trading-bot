def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        g5 = []
        for w, b in wins.items():
            c = b["close"].values
            n = len(c)
            for i in range(0, n - 5, 5):
                g5.append(c[i+5]/c[i]-1)
        drift[coin] = np.mean(g5)
        usual = np.std(g5, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z = r1 / sd
            fwd5 = c.shift(-5)/c - 1
            r10 = c/c.shift(10)-1
            hi20 = c/c.rolling(20, min_periods=10).max()-1
            n = len(b)
            for i in range(0, n-5, 5):
                rows.append(dict(coin=coin, w=w, z=z.iloc[i], f5=fwd5.iloc[i], ex=fwd5.iloc[i]-drift[coin],
                                 inside=b["regime"].iloc[i]=="unknown", fc=b["forecast"].iloc[i],
                                 r10=r10.iloc[i], hi20=hi20.iloc[i], usual=usual,
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows).dropna(subset=["z","f5"])
    d["zb"] = pd.cut(d["z"], [-99,-1,0,0.5,1,1.5,2,99])
    def summ(x):
        return pd.Series(dict(n=len(x), mean_f5=x.f5.mean(), mean_ex=x.ex.mean(),
                              t_ex=x.ex.mean()/(x.ex.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out = {}
    out["by_z_inside"] = d[d.inside].groupby("zb").apply(summ)
    out["by_z_outside"] = d[~d.inside].groupby("zb").apply(summ)
    di = d[d.inside & (d.z>0)].copy()
    di["r10b"] = pd.qcut(di["r10"], 3, labels=["r10lo","r10mid","r10hi"])
    out["inside_up_by_r10"] = di.groupby("r10b").apply(summ)
    di["hib"] = pd.qcut(di["hi20"], 3, labels=["farbelow","mid","nearhigh"])
    out["inside_up_by_hi20"] = di.groupby("hib").apply(summ)
    out["inside_up_by_year"] = di.groupby("year").apply(summ)
    out["inside_up_by_coin"] = di.groupby("coin").apply(summ)
    # condition alone (outside z>0 vs any) by r10
    do = d[d.inside].copy()
    do["r10b"] = pd.qcut(do["r10"], 3, labels=["r10lo","r10mid","r10hi"])
    out["inside_all_by_r10"] = do.groupby("r10b").apply(summ)
    # book by window
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin, w=w)[["w","day","book_return","coin_return"]])
    bk = pd.concat(bk).dropna()
    daily = bk.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_by_window"] = daily.groupby("w").agg(n=("book_return","size"),
        book_mean=("book_return","mean"), coin_mean=("coin_return","mean"),
        book_sum=("book_return","sum"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin, w=w))
    tr = pd.concat(tr)
    tr["fb"] = pd.qcut(tr["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entry_fc"] = tr.groupby("fb").agg(n=("net_profit_loss_percent","size"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        dur_days=("duration_minutes", lambda x: x.mean()/1440))
    out["trades_total"] = tr[["profit_loss_percent","net_profit_loss_percent"]].describe()
    return out
