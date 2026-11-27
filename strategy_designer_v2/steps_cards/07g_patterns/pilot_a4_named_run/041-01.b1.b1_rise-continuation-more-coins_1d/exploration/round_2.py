def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r = c.pct_change()
            hi = b["high"].astype(float); lo = b["low"].astype(float); op = b["open"].astype(float)
            v = b["volume"].astype(float)
            sd30 = r.rolling(30, min_periods=20).std()
            stretch = (c / c.rolling(20, min_periods=10).mean() - 1) / sd30
            r10 = (c / c.shift(10) - 1) / (sd30*np.sqrt(10))
            r60 = c / c.shift(60) - 1
            uw = (hi - np.maximum(op, c)) / (hi - lo)
            vs = np.log(v / v.rolling(30, min_periods=10).median())
            up = (r > 0).astype(int)
            streak = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            vr = sd30 / r.rolling(120, min_periods=60).std()
            n = len(b)
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    rows.append(dict(coin=coin, w=w, h=h, inprof=b["regime"].iloc[i] == "unknown",
                        stretch=stretch.iloc[i], r10=r10.iloc[i], r60=r60.iloc[i], uw=uw.iloc[i],
                        vs=vs.iloc[i], streak=streak.iloc[i], vr=vr.iloc[i],
                        upvs=vs.iloc[i]*(r.iloc[i] > 0),
                        hr=b["timestamp"].iloc[i], ex=fwd.iloc[i] - ((1+mu)**h - 1)))
    df = pd.DataFrame(rows).dropna(subset=["ex"])
    P = df[df.inprof]
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g["ex"].mean(), t=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g) > 2 else np.nan))
    cors = []
    for col in ["stretch", "r10", "r60", "uw", "vs", "upvs", "streak", "vr"]:
        for h in (1, 3, 5, 10):
            s = P[P.h == h].dropna(subset=[col, "ex"])
            if len(s) < 20: continue
            rho, p = stats.spearmanr(s[col], s["ex"])
            hi_ = s[s[col] >= s[col].quantile(0.8)]["ex"]; lo_ = s[s[col] <= s[col].quantile(0.2)]["ex"]
            tw = stats.ttest_ind(hi_, lo_, equal_var=False)
            cors.append(dict(var=col, h=h, n=len(s), rho=rho, p=p, top_mean=hi_.mean(), bot_mean=lo_.mean(), t_top_minus_bot=tw.statistic))
    out["spearman in profile"] = pd.DataFrame(cors)
    out["profile h10"] = P[P.h == 10].groupby("coin").apply(summ)
    out["all profile h10"] = summ(P[P.h == 10])
    # book days around largest losses/gains
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    act = D[D.book_return != 0]
    out["book active days"] = pd.Series(dict(n=len(act), mean=act.book_return.mean(), sd=act.book_return.std(),
        share_pos=(act.book_return > 0).mean(), top10_sum=act.book_return.nlargest(10).sum(), bot10_sum=act.book_return.nsmallest(10).sum(), total=act.book_return.sum()))
    return out
