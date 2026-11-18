def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    def tt(x):
        x = pd.Series(x).dropna()
        if len(x) < 3: return pd.Series([len(x), np.nan, np.nan], index=["n","mean","t"])
        return pd.Series([len(x), x.mean(), x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))], index=["n","mean","t"])
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values); n = len(c)
            r1 = c.pct_change(1); r30 = c.pct_change(30); r10 = c.pct_change(10)
            vol = r1.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 2, 5, 10):
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, wi=int(w[1:]), h=h, fwd=c[t+h]/c[t]-1,
                        r1=r1[t], z1=r1[t]/vol[t] if vol[t] > 0 else np.nan,
                        r30=r30[t], r10=r10[t], wd=ts.iloc[t].dayofweek, yr=ts.iloc[t].year))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin","h"])["fwd"].transform("mean")
    df["half"] = np.where(df.wi <= 12, "w1-12", "w13-24")
    # momentum r30 at 5d: by coin, by half, quintiles
    d = df[df.h == 5].dropna(subset=["r30"])
    res = []
    for k, g in list(d.groupby("coin")) + list(d.groupby("half")):
        rho, p = stats.spearmanr(g["r30"], g["ex"]); res.append(dict(grp=k, n=len(g), rho=rho, p=p))
    for k, g in d.groupby("yr"):
        rho, p = stats.spearmanr(g["r30"], g["ex"]); res.append(dict(grp=str(k), n=len(g), rho=rho, p=p))
    out["r30 -> 5d spearman by group"] = pd.DataFrame(res)
    d = d.assign(q=d.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False)))
    out["r30 quintile -> 5d ex"] = d.groupby("q")["ex"].apply(tt).unstack()
    d10 = df[df.h == 10].dropna(subset=["r10"])
    rho, p = stats.spearmanr(d10["r10"], d10["ex"])
    out["r10 -> 10d spearman"] = pd.Series({"n": len(d10), "rho": rho, "p": p})
    # 1d reversal: z-scored, by coin/half, 1d and 2d
    res = []
    for h in (1, 2):
        dd = df[df.h == h].dropna(subset=["z1"])
        for k, g in [("all", dd)] + list(dd.groupby("coin")) + list(dd.groupby("half")):
            rho, p = stats.spearmanr(g["z1"], g["ex"]); res.append(dict(h=h, grp=k, n=len(g), rho=rho, p=p))
    out["z1 -> next h spearman"] = pd.DataFrame(res)
    dd = df[df.h == 1].dropna(subset=["z1"])
    dd = dd.assign(q=pd.cut(dd["z1"], [-np.inf, -2, -1, 0, 1, 2, np.inf]))
    out["z1 bucket -> next 1d ex"] = dd.groupby("q", observed=True)["ex"].apply(tt).unstack()
    # Wednesday by coin and half
    d1 = df[df.h == 1]
    out["wed by coin/half"] = d1[d1.wd == 2].groupby(["coin","half"])["ex"].apply(tt).unstack()
    # trades
    tr = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    out["trades"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median",lambda s:(s>0).mean()])
    out["trade duration days"] = (tr["duration_minutes"]/1440).describe()
    return out
