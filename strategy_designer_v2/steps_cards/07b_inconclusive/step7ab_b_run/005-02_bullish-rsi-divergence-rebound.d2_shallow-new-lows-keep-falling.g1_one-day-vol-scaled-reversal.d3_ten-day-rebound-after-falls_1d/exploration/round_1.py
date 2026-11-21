import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for H in [1,3,5,10,20]:
                for i in range(0, n-H, H):
                    past20 = c[i]/c[i-20]-1 if i>=20 else np.nan
                    rows.append(dict(coin=coin, win=w, wn=int(w[1:]), H=H, i=i, f=f[i],
                                     ret=c[i+H]/c[i]-1, past20=past20, year=year[i], r1=r1[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin","H"])["ret"].transform("mean")
    d["ex"] = d["ret"]-d["drift"]
    p = d[d.f>0].copy()
    def slope(g):
        if len(g) < 8: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_ex=g.ex.mean()))
        s = stats.linregress(g.f, g.ex)
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope/s.stderr, mean_ex=g.ex.mean(),
                              t_mean=g.ex.mean()/(g.ex.std()/np.sqrt(len(g)))))
    out["by_horizon"] = p.groupby("H").apply(slope)
    p10 = p[p.H==10]
    out["H10_by_coin"] = p10.groupby("coin").apply(slope)
    out["H10_by_year"] = p10.groupby("year").apply(slope)
    p10 = p10.assign(fq=pd.qcut(p10.f, 4, labels=False, duplicates="drop"))
    out["H10_by_fq"] = p10.groupby("fq").agg(n=("ex","size"), fmean=("f","mean"), ex=("ex","mean"), ret=("ret","mean"))
    p10 = p10.assign(trend=np.where(p10.past20>0,"up20","down20"))
    out["H10_by_trend"] = p10.groupby("trend").apply(slope)
    pall = p.assign(trend=np.where(p.past20>0,"up20","down20"))
    out["byH_trend"] = pall.groupby(["H","trend"]).apply(slope)
    # zero-forecast cells comparison
    z = d[(d.H==10)]
    out["H10_pos_vs_zero"] = z.assign(pos=z.f>0).groupby("pos").agg(n=("ex","size"), ex=("ex","mean"))
    out["coin_sd10"] = d[d.H==10].groupby("coin")["ret"].std()
    return out
