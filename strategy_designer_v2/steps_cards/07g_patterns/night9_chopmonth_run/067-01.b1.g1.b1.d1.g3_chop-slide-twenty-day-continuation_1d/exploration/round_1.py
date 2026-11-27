def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def tclust(vals, days):
        s = pd.Series(vals).groupby(pd.Series(days)).sum()
        n = len(vals); m = np.mean(vals)
        dev = (pd.Series(vals) - m).groupby(pd.Series(days)).sum()
        D = len(dev)
        if D < 3: return np.nan, D
        se = np.sqrt((dev**2).sum() * D/(D-1)) / n
        return m/se, D
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            ret1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            r30 = np.full(n, np.nan); r30[30:] = c[30:]/c[:-30]-1
            r60 = np.full(n, np.nan); r60[60:] = c[60:]/c[:-60]-1
            r7 = np.full(n, np.nan); r7[7:] = c[7:]/c[:-7]-1
            vol20 = pd.Series(ret1).rolling(20).std().values
            for h in (5, 10, 20):
                for t in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, t=t, day=str(ts[t].date()),
                        wd=ts[t].dayofweek, fwd=c[t+h]/c[t]-1, r30=r30[t], r60=r60[t], r7=r7[t],
                        r1=ret1[t], vol=vol20[t], reg=df["regime"].iloc[t]))
    R = pd.DataFrame(rows)
    drift = R.groupby(["coin","h"])["fwd"].mean().rename("drift")
    R = R.join(drift, on=["coin","h"]); R["un"] = R["fwd"] - R["drift"]
    out = {}
    # 1. by 30d return quintile, choppy vs not, per horizon
    res = []
    for h in (5,10,20):
        for reg in ["unknown","chop"]:
            S = R[(R.h==h)&(R.reg==reg)].dropna(subset=["r30"]).copy()
            S["q"] = pd.qcut(S["r30"], 5, labels=False)
            for q, g in S.groupby("q"):
                t, D = tclust(g["un"].values, g["day"].values)
                res.append(dict(h=h, reg=reg, q=q, r30=g.r30.mean(), n=len(g), un=g.un.mean(), t=t))
            sp = stats.spearmanr(S.r30, S.un)
            res.append(dict(h=h, reg=reg, q="rho", r30=np.nan, n=len(S), un=sp.correlation, t=sp.pvalue))
    out["r30 quintiles"] = pd.DataFrame(res)
    # 2. by 7d return quintile in choppy and non
    res = []
    for h in (5,10):
        for reg in ["unknown","chop"]:
            S = R[(R.h==h)&(R.reg==reg)].dropna(subset=["r7"]).copy()
            S["z"] = S.r7/ (S.vol*np.sqrt(7))
            S = S.dropna(subset=["z"])
            S["q"] = pd.qcut(S["z"], 5, labels=False)
            for q, g in S.groupby("q"):
                t, D = tclust(g["un"].values, g["day"].values)
                res.append(dict(h=h, reg=reg, q=q, z=g.z.mean(), n=len(g), un=g.un.mean(), t=t))
    out["r7 scaled quintiles"] = pd.DataFrame(res)
    # 3. non-choppy split by 60d sign, r30 quintile, h=10
    res = []
    S = R[(R.h==10)&(R.reg=="chop")].dropna(subset=["r30","r60"]).copy()
    S["tr"] = np.where(S.r60>0, "rising", "falling")
    for tr, G in S.groupby("tr"):
        G = G.copy(); G["q"] = pd.qcut(G.r30, 4, labels=False)
        for q, g in G.groupby("q"):
            t, D = tclust(g["un"].values, g["day"].values)
            res.append(dict(tr=tr, q=q, r30=g.r30.mean(), n=len(g), un=g.un.mean(), t=t))
    out["trend r30 h10"] = pd.DataFrame(res)
    # 4. weekday daily (h=5 grid not useful) -> use daily returns
    dl = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek; d["coin"]=coin
            dl.append(d)
    Dd = pd.concat(dl)
    Dd["cr_dm"] = Dd.coin_return - Dd.groupby("coin").coin_return.transform("mean")
    out["weekday"] = Dd.groupby("wd").agg(n=("cr_dm","count"), mean=("cr_dm","mean"),
        t=("cr_dm", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))), book=("book_return","mean"))
    # 5. book by year
    Dd["yr"] = pd.to_datetime(Dd["day"]).dt.year
    bk = Dd.groupby("day").book_return.mean()
    out["book by year"] = bk.groupby(pd.to_datetime(bk.index).year).agg(["count","mean","std"])
    return out
