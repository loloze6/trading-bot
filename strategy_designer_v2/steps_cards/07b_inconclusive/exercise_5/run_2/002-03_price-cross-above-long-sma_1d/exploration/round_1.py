import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        dr = []
        for w, df in wins.items():
            c = df["close"].values
            dr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(dr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            f = df["forecast"].values
            raw = df.get("debug_info.components.above_ma.last_history_value", pd.Series(np.nan, index=df.index)).values
            # past 20-day return and 60-day vol
            r1 = pd.Series(c).pct_change()
            vol60 = r1.rolling(60).std().values
            ret60 = (pd.Series(c) / pd.Series(c).shift(60) - 1).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [5, 10, 20, 40, 60]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], f=f[i], raw=raw[i],
                                     vol=vol60[i], r60=ret60[i],
                                     ex=c[i+h]/c[i]-1 - h*mu))
    R = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.ex.mean(), t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan, hit=(g.ex>0).mean()))
    out = {}
    R["fb"] = pd.cut(R.f, [-0.1, 0.001, 5, 10, 15, 20.1], labels=["0","0-5","5-10","10-15","15-20"])
    out["by_h_fbin"] = R.groupby(["h","fb"]).apply(summ).reset_index()
    R20 = R[R.h==20]
    pos = R20[R20.f>0]
    out["h20_pos_by_coin"] = pos.groupby("coin").apply(summ)
    out["h20_zero_by_coin"] = R20[R20.f==0].groupby("coin").apply(summ)
    out["h20_pos_by_year"] = pos.groupby("year").apply(summ)
    out["h20_zero_by_year"] = R20[R20.f==0].groupby("year").apply(summ)
    # raw distance bins (all bars incl. below)
    R20 = R20.copy()
    R20["rawq"] = pd.qcut(R20.raw, 5, duplicates="drop")
    out["h20_by_rawq"] = R20.groupby("rawq").apply(summ)
    pos = pos.copy()
    pos["volq"] = pd.qcut(pos.vol, 3, labels=["lowvol","mid","highvol"])
    pos["r60q"] = pd.qcut(pos.r60, 3, labels=["lowr60","mid","highr60"])
    out["h20_pos_by_vol"] = pos.groupby("volq").apply(summ)
    out["h20_pos_by_r60"] = pos.groupby("r60q").apply(summ)
    out["corr_f_ex_pos_byh"] = R[R.f>0].groupby("h").apply(lambda g: pd.Series(dict(rho=stats.spearmanr(g.f, g.ex)[0], n=len(g))))
    return out
