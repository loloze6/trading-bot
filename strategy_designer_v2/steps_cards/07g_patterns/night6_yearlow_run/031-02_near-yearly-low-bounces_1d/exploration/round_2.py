import numpy as np, pandas as pd
from scipy import stats

def day_t(d, y):
    # deviations summed per day, then t of daily sums
    s = d.groupby("day")[y].sum()
    return s.mean()/(s.std()/np.sqrt(len(s))), len(s)

def explore(data):
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            prox = b["debug_info.components.low_prox.last_history_value"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            for h in [5, 10, 20]:
                for i in range(0, n - h, h):
                    recs.append(dict(coin=coin, w=w, h=h, day=ts.iloc[i].normalize(), yr=ts.iloc[i].year,
                                     prox=prox[i], fwd=c[i+h]/c[i]-1,
                                     past60=c[i]/c[i-60]-1 if i >= 60 else np.nan))
    df = pd.DataFrame(recs)
    df["D"] = 1/df["prox"] - 1
    df["lD"] = np.log1p(df["D"]/100.0)
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    res = []
    for h in [5, 10, 20]:
        d = df[(df.h == h)].dropna(subset=["lD", "ex"]).copy()
        s = stats.linregress(d["lD"], d["ex"])
        d["q"] = pd.qcut(d["lD"].rank(method="first"), 5, labels=False)
        top = d[d.q == 4]; bot = d[d.q == 0]
        d["sig"] = (d["lD"] - d["lD"].mean())/d["lD"].std()*d["ex"]
        tday, nday = day_t(d, "sig")
        res.append(dict(h=h, n=len(d), slope=s.slope, t=s.slope/s.stderr, t_dayclustered_prod=tday, days=nday,
                        far_minus_near=top.ex.mean()-bot.ex.mean(), near=bot.ex.mean(), far=top.ex.mean()))
    out["ex on log(1+D) by horizon"] = pd.DataFrame(res)
    # by year for h=5 slope t
    d5 = df[df.h == 5].dropna(subset=["lD", "ex"])
    yy = []
    for y, g in d5.groupby("yr"):
        s = stats.linregress(g["lD"], g["ex"]); yy.append(dict(yr=y, n=len(g), slope=s.slope, t=s.slope/s.stderr))
    out["h5 slope by year"] = pd.DataFrame(yy)
    cc = []
    for cn, g in d5.groupby("coin"):
        s = stats.linregress(g["lD"], g["ex"]); cc.append(dict(coin=cn, n=len(g), slope=s.slope, t=s.slope/s.stderr))
    out["h5 slope by coin"] = pd.DataFrame(cc)
    # past60 momentum control at h=5 and 20
    for h in [5, 20]:
        d = df[df.h == h].dropna(subset=["lD", "ex", "past60"])
        X = np.column_stack([np.ones(len(d)), d["lD"], d["past60"]])
        beta, *_ = np.linalg.lstsq(X, d["ex"].values, rcond=None)
        resid = d["ex"].values - X @ beta
        cov = np.linalg.inv(X.T @ X)*resid.var(ddof=3)
        out[f"h{h} ex ~ lD + past60: b_lD,t,b_p60,t,n"] = f"{beta[1]:.4f}, {beta[1]/np.sqrt(cov[1,1]):.2f}, {beta[2]:.4f}, {beta[2]/np.sqrt(cov[2,2]):.2f}, {len(d)}"
    # at new low (prox==1) events vs others, per horizon
    df["atlow"] = df["prox"] >= 0.999
    out["at new low vs rest"] = df.groupby(["h", "atlow"])["ex"].agg(["size", "mean", "std"])
    # weekday, one value per day (mean over coins), t over days
    dd = pd.concat([x.assign(coin=c) for c, ws in data["days"].items() for x in ws.values()])
    dd["day"] = pd.to_datetime(dd["day"])
    m = dd.groupby("day").agg(coin=("coin_return", "mean"), book=("book_return", "mean")).dropna()
    m["wd"] = m.index.dayofweek; m["yr"] = m.index.year
    g = m.groupby("wd")["coin"].agg(["size", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["weekday, day-mean of coins"] = g
    m["sat"] = (m.wd == 5)
    out["Saturday minus other days by year"] = m.groupby("yr").apply(lambda x: pd.Series(dict(sat=x[x.sat].coin.mean(), other=x[~x.sat].coin.mean(), nsat=x.sat.sum())))
    # per coin Saturday t
    dd["wd"] = dd["day"].dt.dayofweek
    pc = dd.dropna(subset=["coin_return"]).groupby("coin").apply(lambda x: pd.Series(dict(
        sat=x[x.wd == 5].coin_return.mean(), oth=x[x.wd != 5].coin_return.mean(),
        t=stats.ttest_ind(x[x.wd == 5].coin_return, x[x.wd != 5].coin_return, equal_var=False).statistic)))
    out["Saturday vs other per coin"] = pc
    return out
