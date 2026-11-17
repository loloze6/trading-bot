import pandas as pd, numpy as np
from scipy import stats

def s2(x):
    x = pd.Series(x).dropna()
    return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    # daily reversal deeper: decile of today's return scaled by trailing 20d vol, next 1 day and next 3 days (non-overlap 3d grid)
    drows = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.reset_index(drop=True)
            c = d["close"]; cr = d["coin_return"]
            sd = cr.rolling(20).std().shift(1)
            n = len(d)
            f3 = c.shift(-3)/c - 1
            pos = np.arange(n)
            drows.append(pd.DataFrame(dict(coin=coin, w=w, r=cr, z=cr/sd, sd=sd, nxt=cr.shift(-1), f3=f3, pos=pos,
                regime=None, year=pd.to_datetime(d["day"]).dt.year,
                wd=pd.to_datetime(d["day"]).dt.dayofweek)))
    D = pd.concat(drows, ignore_index=True)
    # regime per day from bars (1d bars => same)
    regs = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            regs.append(pd.DataFrame(dict(coin=coin, w=w, pos=np.arange(len(df)), reg=df["regime"].values,
                                          volr=(df["volume"]/df["volume"].rolling(20).mean().shift(1)).values)))
    R = pd.concat(regs, ignore_index=True)
    D = D.merge(R, on=["coin","w","pos"], how="left")
    Dz = D.dropna(subset=["z","nxt"]).copy()
    Dz["zq"] = Dz.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    out["nextday_by_z_decile"] = Dz.groupby("zq")["nxt"].apply(s2).unstack()
    neg = Dz[Dz.z < 0].copy()
    out["corr_negz_next_spearman"] = float(stats.spearmanr(neg.z, neg.nxt).correlation)
    out["nextday_lowdecile_by_coin"] = Dz[Dz.zq==0].groupby("coin")["nxt"].apply(s2).unstack()
    out["nextday_lowdecile_by_year"] = Dz[Dz.zq==0].groupby("year")["nxt"].apply(s2).unstack()
    out["nextday_lowdecile_by_regime"] = Dz[Dz.zq<=1].groupby("reg")["nxt"].apply(s2).unstack()
    # 3-day forward, non-overlapping grid pos%3==0
    G3 = Dz[(Dz.pos % 3 == 0)].dropna(subset=["f3"]).copy()
    G3["ex"] = G3["f3"] - G3.groupby("coin")["f3"].transform("mean")
    G3["zq5"] = G3.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["f3_ex_by_z_quint_grid3"] = G3.groupby("zq5")["ex"].apply(s2).unstack()
    # low volume on the 7d grid: by coin and by regime
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True); c = df["close"].values; n=len(df)
            v = df["volume"]
            vr = (v.rolling(7).mean()/v.rolling(60).mean()).values
            vr1 = (v/v.rolling(20).mean()).values
            for i in range(0, n-7, 7):
                rows.append(dict(coin=coin, fwd=c[i+7]/c[i]-1, vr7=vr[i], vr1=vr1[i], reg=df["regime"].iloc[i]))
    g = pd.DataFrame(rows); g["ex"] = g.fwd - g.groupby("coin").fwd.transform("mean")
    for col in ["vr1","vr7"]:
        gg = g.dropna(subset=[col]).copy()
        gg["q"] = gg.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["7d_ex_by_"+col] = gg.groupby("q")["ex"].apply(s2).unstack()
        out["7d_ex_"+col+"_q0_by_coin"] = gg[gg.q==0].groupby("coin")["ex"].apply(s2).unstack()
    # weekday Saturday by year
    out["sat_coinret_by_year"] = D[D.wd==5].groupby("year")["r"].apply(s2).unstack()
    out["weekday_coinret_ex_by_coin_sat"] = D[D.wd==5].groupby("coin")["r"].apply(s2).unstack()
    return out
