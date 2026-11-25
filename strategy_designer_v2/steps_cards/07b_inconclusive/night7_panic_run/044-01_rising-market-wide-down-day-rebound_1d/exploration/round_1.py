import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for H in (1,3,5,10):
            rr=[]
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c)-H, H)
                rr += list(c[idx+H]/c[idx]-1)
            drift[(coin,H)] = (np.mean(rr), np.std(rr))
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30).std()
            rng = (b["high"]-b["low"])/c/sd
            reg = b["regime"].astype(str)
            n = len(b)
            for H in (1,3,5,10):
                for i in range(1, n-H):
                    if i % H != 0: continue
                    rising = reg[i] != "chop"
                    if not rising or np.isnan(rng[i]): continue
                    fr = c[i+H]/c[i]-1
                    rows.append(dict(coin=coin, w=w, H=H, down=r[i]<0, rng=rng[i],
                                     ex=fr-drift[(coin,H)][0], fc=b["forecast"][i],
                                     sd30=sd[i], d=i))
    df = pd.DataFrame(rows)
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.ex.mean(), t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g)))))
    out["by_H_side"] = df.groupby(["H","down"]).apply(summ)
    d3 = df[df.H==3].copy()
    d3["q"] = d3.groupby("down")["rng"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["H3_side_rangeq"] = d3.groupby(["down","q"]).apply(summ)
    dd = d3[d3.down]
    out["H3_down_coin"] = dd.groupby("coin").apply(summ)
    out["H3_down_window"] = dd.groupby("w").apply(summ)
    d5 = df[(df.H==5)&df.down].copy()
    d5["q"]=pd.qcut(d5.rng,5,labels=False)
    out["H5_down_rangeq"] = d5.groupby("q").apply(summ)
    d1 = df[(df.H==1)&df.down].copy()
    d1["q"]=pd.qcut(d1.rng,5,labels=False)
    out["H1_down_rangeq"] = d1.groupby("q").apply(summ)
    return out
