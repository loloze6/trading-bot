import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for i in range(0, n-5, 5):
                allr.append(c[i+5]/c[i]-1)
        drift[coin] = np.mean(allr) if allr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            z = r1/sd
            r90 = c/c.shift(90)-1
            r30 = c/c.shift(30)-1
            r5p = c/c.shift(5)-1
            fwd = c.shift(-5)/c-1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for i in range(0, len(df)-5, 5):
                rows.append(dict(coin=coin, w=w, yr=yr[i], reg=df["regime"][i],
                    z=z[i], r1=r1[i], sd=sd[i], r90=r90[i], r30=r30[i], r5p=r5p[i],
                    fwd=fwd[i], fc=df["forecast"][i],
                    alloc=df["postRebalance_current_allocation"][i], drift=drift[coin]))
    d = pd.DataFrame(rows)
    d["un"] = d["fwd"]-d["drift"]
    fall = d[d.reg=="mean_reversion"].copy()
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "fwd_mean%": 100*g.fwd.mean(), "unusual%": 100*g.un.mean(),
                          "t_fwd": g.fwd.mean()/(g.fwd.std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out["all grid vs falling regime"] = pd.DataFrame({"all": summ(d), "falling": summ(fall), "rising/other": summ(d[d.reg!="mean_reversion"])})
    fall["zb"] = pd.cut(fall.z, [-99,-2,-1,0,1,2,3,99])
    out["falling: fwd by 1d z"] = fall.groupby("zb").apply(summ)
    oth = d[d.reg!="mean_reversion"].copy(); oth["zb"] = pd.cut(oth.z, [-99,-2,-1,0,1,2,3,99])
    out["not falling: fwd by 1d z"] = oth.groupby("zb").apply(summ)
    f2 = fall.dropna(subset=["r90"]).copy()
    f2["r90b"] = pd.qcut(f2.r90, 4)
    out["falling: fwd by 90d return quartile"] = f2.groupby("r90b").apply(summ)
    fall["r30b"] = pd.cut(fall.r30, [-9,-0.3,-0.15,0,0.15,9])
    out["falling: fwd by 30d return"] = fall.groupby("r30b").apply(summ)
    fall["r5b"] = pd.cut(fall.r5p, [-9,-0.15,-0.05,0,0.05,0.15,9])
    out["falling: fwd by past 5d return"] = fall.groupby("r5b").apply(summ)
    up = fall[fall.z>0].copy()
    up["r30b"] = pd.cut(up.r30, [-9,-0.3,-0.15,0,0.15,9])
    out["falling up-days: fwd by 30d return"] = up.groupby("r30b").apply(summ)
    out["falling: by year"] = fall.groupby("yr").apply(summ)
    # book
    br = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df[["day","book_return","coin_return"]].copy(); br.append(x)
    b = pd.concat(br).groupby("day")[["book_return","coin_return"]].mean().dropna()
    b["yr"] = pd.to_datetime(b.index).year
    out["book by year"] = b.groupby("yr").agg(bm=("book_return","mean"), cm=("coin_return","mean"), n=("book_return","size"))
    # mean allocation and market-rise part
    al = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            al.append(df["postRebalance_current_allocation"].values)
    al = np.concatenate(al)
    out["mean allocation, share of bars short"] = pd.Series({"mean_alloc": np.nanmean(al), "share_short": np.mean(al<-1e-6), "mean_alloc_when_short": np.nanmean(al[al<-1e-6])})
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            tr.append(df)
    t = pd.concat(tr)
    t["days"] = t.duration_minutes/1440
    out["trades"] = pd.Series({"n": len(t), "mean_pl_gross%": t.profit_loss_percent.mean(), "mean_pl_net%": t.net_profit_loss_percent.mean(), "mean_days": t.days.mean(), "win_share": (t.profit_loss_percent>0).mean()})
    return out
