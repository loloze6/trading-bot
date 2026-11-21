import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; H = 26
    rows = []
    for coin in bars:
        allr = []
        for w, b in bars[coin].items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i+H]/c[i]-1)
        mu = np.mean(allr); sd = np.std(allr)
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"]; f = b["forecast"]
            vol = c.pct_change().rolling(30).std()
            r7 = c/c.shift(7)-1
            for i in range(0, len(c)-H, H):
                if f.iloc[i] < 0:
                    ret = c.iloc[i+H]/c.iloc[i]-1
                    rows.append(dict(coin=coin, half="h1" if int(w[1:])<=12 else "h2",
                                     ex=-(ret-mu), z=-(ret-mu)/sd, tot=-ret, absf=abs(f.iloc[i]),
                                     vol=vol.iloc[i], r7=r7.iloc[i]))
    d = pd.DataFrame(rows)
    d["big"] = np.where(d["absf"] >= d["absf"].median(), "big", "small")
    def agg(g):
        return pd.Series(dict(n=len(g), ex=g["ex"].mean(), t_ex=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))),
                              tot=g["tot"].mean(), z=g["z"].mean()))
    out["big_by_coin"] = d.groupby(["big","coin"]).apply(agg)
    out["big_by_half"] = d.groupby(["big","half"]).apply(agg)
    sp = stats.spearmanr(d["absf"], d["ex"])
    out["spearman_absf_ex"] = pd.Series(dict(rho=sp[0], p=sp[1], n=len(d)))
    dv = d.dropna(subset=["vol"])
    sv = stats.spearmanr(dv["vol"], dv["ex"])
    out["spearman_vol_ex"] = pd.Series(dict(rho=sv[0], p=sv[1], n=len(dv)))
    dv["lowvol"] = np.where(dv["vol"] <= dv["vol"].median(), "low", "high")
    out["vol_by_half"] = dv.groupby(["lowvol","half"]).apply(agg)
    dr = d.dropna(subset=["r7"])
    sr = stats.spearmanr(dr["r7"], dr["ex"])
    out["spearman_r7_ex"] = pd.Series(dict(rho=sr[0], p=sr[1], n=len(dr)))
    return out
