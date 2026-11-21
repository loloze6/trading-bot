import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    days = data["days"]; out = {}
    dl = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            d["yr"] = pd.to_datetime(d["day"]).dt.year
            d["next"] = d["coin_return"].shift(-1)
            d["next3"] = d["close"].shift(-3)/d["close"]-1
            d["r3"] = d["close"]/d["close"].shift(3)-1
            dl.append(d)
    D = pd.concat(dl).dropna(subset=["coin_return","next"])
    D["sd"] = D.groupby("coin")["coin_return"].transform("std")
    D["z"] = D["coin_return"]/D["sd"]
    D["nex"] = D["next"] - D.groupby("coin")["coin_return"].transform("mean")
    D["nexz"] = D["nex"]/D["sd"]
    # reversal after falls, per coin
    rows = []
    for coin, g in D.groupby("coin"):
        f = g[g.z < 0]
        big = g[g.z <= -2]; bigu = g[g.z >= 2]
        rows.append(dict(coin=coin, n_fall=len(f), rho_fall=stats.spearmanr(f.z, f.nex).correlation,
                         p_fall=stats.spearmanr(f.z, f.nex).pvalue,
                         n_big=len(big), big_nex=big.nex.mean(), t_big=stats.ttest_1samp(big.nex,0).statistic,
                         n_bigu=len(bigu), bigu_nex=bigu.nex.mean(), t_bigu=stats.ttest_1samp(bigu.nex,0).statistic))
    out["reversal_percoin"] = pd.DataFrame(rows)
    # by year
    rows=[]
    for yr, g in D.groupby("yr"):
        big = g[g.z <= -2]; f = g[g.z<0]
        rows.append(dict(yr=yr, n_big=len(big), big_nex=big.nex.mean() if len(big) else np.nan,
                         t_big=stats.ttest_1samp(big.nex,0).statistic if len(big)>2 else np.nan,
                         rho_fall=stats.spearmanr(f.z,f.nex).correlation))
    out["reversal_year"] = pd.DataFrame(rows)
    # graded bins of the fall
    D["zb"] = pd.cut(D["z"], [-99,-3,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,3,99])
    out["graded"] = D.groupby("zb", observed=True).agg(n=("nex","count"), nex=("nex","mean"), nexz=("nexz","mean"),
                    t=("nex", lambda x: stats.ttest_1samp(x,0).statistic))
    # 3-day falls -> 3-day rebound, non-overlapping grid
    G = []
    for coin, ws in days.items():
        for w, d in ws.items():
            c = d["close"].values.astype(float)
            for t in range(3, len(c)-3, 3):
                G.append(dict(coin=coin, r3=c[t]/c[t-3]-1, f3=c[t+3]/c[t]-1))
    G = pd.DataFrame(G)
    G["ex"] = G.f3 - G.groupby("coin").f3.transform("mean")
    G["z3"] = G.r3/G.groupby("coin").r3.transform("std")
    G["zb"] = pd.cut(G.z3, [-99,-2,-1,0,1,2,99])
    out["r3_graded"] = G.groupby("zb", observed=True).agg(n=("ex","count"), ex=("ex","mean"),
                    t=("ex", lambda x: stats.ttest_1samp(x,0).statistic))
    # weekday per coin (excess), and by year
    D["cex"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["weekday_coin"] = D.pivot_table(index="wd", columns="coin", values="cex", aggfunc="mean")
    out["sat_by_year"] = D[D.wd==5].groupby("yr").agg(n=("cex","count"), cex=("cex","mean"),
                    t=("cex", lambda x: stats.ttest_1samp(x,0).statistic))
    # is the post-fall rebound concentrated on weekdays?
    big = D[D.z <= -1.5]
    out["rebound_by_weekday"] = big.groupby("wd").agg(n=("nex","count"), nex=("nex","mean"))
    return out
