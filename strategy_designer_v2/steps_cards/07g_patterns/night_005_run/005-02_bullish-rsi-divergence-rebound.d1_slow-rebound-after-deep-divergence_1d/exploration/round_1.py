def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    def tt(x):
        x = pd.Series(x).dropna()
        if len(x) < 3: return (len(x), np.nan, np.nan)
        return (len(x), x.mean(), x.mean()/(x.std(ddof=1)/np.sqrt(len(x))))
    # coin mean returns at horizons on grid
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            r30 = pd.Series(c).pct_change(30).values
            r1 = pd.Series(c).pct_change(1).values
            r5 = pd.Series(c).pct_change(5).values
            vol = pd.Series(r1).rolling(20).std().values
            minprev = pd.Series(c).shift(1).rolling(30).min().values
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 5, 10, 20):
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, t=t, fwd=c[t+h]/c[t]-1,
                        r30=r30[t], r1=r1[t], r5=r5[t], vol=vol[t],
                        newlow=(c[t] < minprev[t]) if not np.isnan(minprev[t]) else np.nan,
                        div=b["regime"].iloc[t] == "mean_reversion",
                        fc=b["forecast"].iloc[t], wd=ts.iloc[t].dayofweek, yr=ts.iloc[t].year))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    # 1) momentum: 30d return terciles -> next h excess
    res = []
    for h in (5, 10, 20):
        d = df[(df.h == h)].dropna(subset=["r30"])
        d = d.assign(q=d.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 3, labels=False)))
        for q in range(3):
            n_, m, t_ = tt(d[d.q == q]["ex"]); res.append(dict(h=h, r30_tercile=q, n=n_, mean_ex=m, t=t_))
        rho, p = stats.spearmanr(d["r30"], d["ex"]); res.append(dict(h=h, r30_tercile="spearman", n=len(d), mean_ex=rho, t=p))
    out["r30 tercile -> fwd excess"] = pd.DataFrame(res)
    # 2) 1-day move quintiles -> next 1d
    d = df[df.h == 1].dropna(subset=["r1"])
    d = d.assign(q=d.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False)))
    out["r1 quintile -> next 1d excess"] = d.groupby("q")["ex"].apply(lambda s: pd.Series(tt(s), index=["n", "mean", "t"])).unstack()
    # 5d move quintiles -> next 5d
    d = df[df.h == 5].dropna(subset=["r5"])
    d = d.assign(q=d.groupby("coin")["r5"].transform(lambda s: pd.qcut(s, 5, labels=False)))
    out["r5 quintile -> next 5d excess"] = d.groupby("q")["ex"].apply(lambda s: pd.Series(tt(s), index=["n", "mean", "t"])).unstack()
    # 3) vol terciles -> fwd 5,20
    res = []
    for h in (5, 20):
        d = df[df.h == h].dropna(subset=["vol"])
        d = d.assign(q=d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False)))
        for q in range(3):
            n_, m, t_ = tt(d[d.q == q]["ex"]); res.append(dict(h=h, vol_tercile=q, n=n_, mean_ex=m, t=t_))
    out["vol tercile -> fwd excess"] = pd.DataFrame(res)
    # 4) weekday next-1d
    d = df[df.h == 1]
    out["weekday 1d excess"] = d.groupby("wd")["ex"].apply(lambda s: pd.Series(tt(s), index=["n", "mean", "t"])).unstack()
    # 5) new lows: div vs no-div, h=20 & 5 grid
    res = []
    for h in (5, 10, 20):
        d = df[(df.h == h) & (df.newlow == True)]
        for k, g in d.groupby("div"):
            n_, m, t_ = tt(g["ex"]); res.append(dict(h=h, div=k, n=n_, mean_ex=m, t=t_))
    out["newlow div vs not"] = pd.DataFrame(res)
    # 6) book daily
    bd = []
    for coin in days:
        for w, dd in days[coin].items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; bd.append(x)
    bd = pd.concat(bd)
    bd["yr"] = pd.to_datetime(bd["day"]).dt.year
    out["book by coin"] = bd.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["book by year"] = bd.groupby("yr")[["book_return", "coin_return"]].mean()
    # coin daily return by year (holding)
    out["share days in position"] = pd.Series({c: float(np.mean(np.concatenate([(b["postRebalance_current_allocation"].fillna(0).abs() > 0).values for b in bars[c].values()]))) for c in bars})
    return out
