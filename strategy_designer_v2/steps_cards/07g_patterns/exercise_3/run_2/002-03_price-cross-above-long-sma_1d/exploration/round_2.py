def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    D = []
    for c in days:
        for w, df in days[c].items():
            d = df.copy().reset_index(drop=True); d["coin"]=c; d["w"]=w
            d["past7"] = d["close"]/d["close"].shift(7)-1
            D.append(d)
    D = pd.concat(D).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.weekday
    D["yr"] = D["day"].dt.year
    D["sat"] = D.wd==5
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    # cross-coin averaged per day (removes same-day correlation)
    X = D.groupby(["w","day"]).agg(r=("coin_return","mean"), b=("book_return","mean")).reset_index()
    X["wd"] = X["day"].dt.weekday; X["yr"]=X["day"].dt.year
    out["coin-avg daily by weekday"] = X.groupby("wd")["r"].apply(tt).unstack()
    out["book daily by weekday"] = X.groupby("wd")["b"].apply(tt).unstack()
    # Saturday minus other days, per coin (Welch)
    rows=[]
    for c,g in D.groupby("coin"):
        a=g.loc[g.sat,"coin_return"]; b=g.loc[~g.sat,"coin_return"]
        rows.append(dict(coin=c, sat=a.mean(), other=b.mean(), t=stats.ttest_ind(a,b,equal_var=False).statistic))
    out["Sat minus other per coin"] = pd.DataFrame(rows).set_index("coin")
    rows=[]
    for y,g in X.groupby("yr"):
        a=g.loc[g.wd==5,"r"]; b=g.loc[g.wd!=5,"r"]
        rows.append(dict(yr=y, nsat=len(a), sat=a.mean(), other=b.mean(), t=stats.ttest_ind(a,b,equal_var=False).statistic))
    out["Sat minus other by year (coin-avg)"] = pd.DataFrame(rows).set_index("yr")
    # Fri+Sat vs rest per window group
    X["wg"] = X["w"].str[1:].astype(int).apply(lambda k: "w1-6" if k<=6 else "w7-12" if k<=12 else "w13-18" if k<=18 else "w19-24")
    rows=[]
    for gname,g in X.groupby("wg"):
        a=g.loc[g.wd==5,"r"]; b=g.loc[g.wd!=5,"r"]
        rows.append(dict(wg=gname, sat=a.mean(), other=b.mean(), t=stats.ttest_ind(a,b,equal_var=False).statistic))
    out["Sat minus other by window group"] = pd.DataFrame(rows).set_index("wg")
    # Saturday return graded by past 7d return (per coin terciles)
    S = D[D.sat].dropna(subset=["past7"]).copy()
    S["pq"] = S.groupby("coin")["past7"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["Sat return by past7 tercile"] = S.groupby("pq")["coin_return"].apply(tt).unstack()
    # median and hit on Saturday vs others (outlier check)
    out["median/hit Sat vs other"] = D.groupby("sat")["coin_return"].agg(["median", lambda x:(x>0).mean()])
    # Saturday with top 1% days removed
    q = D["coin_return"].quantile(0.99)
    Dt = D[D.coin_return<q]
    out["trimmed top1% by weekday"] = Dt.groupby("wd")["coin_return"].apply(tt).unstack()
    # book largest days: what weekday
    big = X.dropna(subset=["b"])
    hi = big.nlargest(40,"b"); lo = big.nsmallest(40,"b")
    out["book top40 gain weekday counts"] = hi["wd"].value_counts().sort_index()
    out["book top40 loss weekday counts"] = lo["wd"].value_counts().sort_index()
    return out
