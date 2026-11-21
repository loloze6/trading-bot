import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            if n < 130: continue
            r1 = c.pct_change()
            ret30 = c / c.shift(30) - 1
            ret5 = c / c.shift(5) - 1
            vol20 = r1.rolling(20).std()
            vol90 = r1.rolling(90).std()
            hi90 = c.shift(1).rolling(90).max()
            lo90 = c.shift(1).rolling(90).min()
            newhi = (c > hi90) & (c.shift(1) <= hi90.shift(1))
            newlo = (c < lo90) & (c.shift(1) >= lo90.shift(1))
            dist_hi = c / hi90 - 1
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            fc = df["forecast"].astype(float).reset_index(drop=True)
            for h in (5, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, fwd=c[i+h]/c[i]-1,
                        ret30=ret30[i], ret5=ret5[i], r1=r1[i], volratio=vol20[i]/vol90[i] if vol90[i] else np.nan,
                        newhi=bool(newhi[i]), newlo=bool(newlo[i]), dist_hi=dist_hi[i],
                        wd=ts[i].weekday(), active=fc[i] != 0))
    d = pd.DataFrame(rows)
    out = {}
    for h in (5, 20):
        x = d[d.h == h].copy()
        x["un"] = x["fwd"] - x.groupby("coin")["fwd"].transform("mean")
        x["sd"] = x.groupby("coin")["fwd"].transform("std")
        x["z"] = x["un"] / x["sd"]
        def summ(g):
            return pd.Series(dict(n=len(g), mean_un=g.un.mean(), z=g.z.mean(),
                                  t=g.z.mean()/(g.z.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan))
        y = x.dropna(subset=["ret30"]).copy()
        y["q30"] = y.groupby("coin")["ret30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out[f"h{h}_by_ret30_quintile"] = y.groupby("q30").apply(summ)
        y["q5"] = y.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out[f"h{h}_by_ret5_quintile"] = y.groupby("q5").apply(summ)
        y2 = y.dropna(subset=["volratio"]).copy()
        y2["qv"] = y2.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out[f"h{h}_by_volratio_quintile"] = y2.groupby("qv").apply(summ)
        y3 = y.dropna(subset=["dist_hi"]).copy()
        y3["qd"] = y3.groupby("coin")["dist_hi"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out[f"h{h}_by_dist_to_90d_high_q"] = y3.groupby("qd").apply(summ)
        if h == 20:
            y["up30"] = y.ret30 > 0
            out["h20_newhi_by_up30"] = y.groupby(["newhi", "up30"]).apply(summ)
            out["h20_newlo_by_up30"] = y.groupby(["newlo", "up30"]).apply(summ)
            out["h20_by_coin_ret30_corr"] = y.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g), rho=stats.spearmanr(g.ret30, g.un)[0])))
        else:
            out["h5_by_weekday"] = x.groupby("wd").apply(summ)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            dd.append(df.assign(coin=coin, win=w))
    D = pd.concat(dd)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(coin=coin))
    T = pd.concat(tr)
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "count"), mean=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    return out
