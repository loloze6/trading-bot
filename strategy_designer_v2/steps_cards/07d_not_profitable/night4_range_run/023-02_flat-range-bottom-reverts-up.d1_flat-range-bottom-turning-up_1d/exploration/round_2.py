import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"]; hi = b["high"].rolling(30).max(); lo = b["low"].rolling(30).min()
            net = (cl - cl.shift(29)).abs()/(hi-lo)
            pos = (cl - (hi+lo)/2)/((hi-lo)/2)
            r10 = cl/cl.shift(10)-1
            r10z = (r10 - r10.rolling(60, min_periods=20).mean())/r10.rolling(60, min_periods=20).std()
            r30 = cl/cl.shift(29)-1
            n = len(b)
            for i in range(0, n-5, 5):
                recs.append((c, w, net.iloc[i], pos.iloc[i], r10.iloc[i], r10z.iloc[i], r30.iloc[i],
                             cl.iloc[i+5]/cl.iloc[i]-1, b["forecast"].iloc[i], b["regime"].iloc[i]))
    R = pd.DataFrame(recs, columns=["coin","window","net","pos","r10","r10z","r30","r5","f","regime"])
    m5 = R.groupby("coin")["r5"].mean(); sd5 = R.groupby("coin")["r5"].std()
    R["ex"] = R.r5 - R.coin.map(m5); R["z"] = R.ex/R.coin.map(sd5)
    R = R.dropna(subset=["net","pos","r10"])
    R["flat"] = np.where(R.net<=0.3, "flat", "trend")
    R["side"] = np.where(R.pos<0, "below", "above")
    def reg(g, x):
        g = g.dropna(subset=[x])
        if len(g) < 20: return pd.Series(dict(n=len(g)))
        s = stats.linregress(g[x], g.ex)
        return pd.Series(dict(n=len(g), ex=g.ex.mean(), slope=s.slope, t=s.slope/s.stderr))
    out["ex_on_r10_by_state"] = R.groupby(["flat","side"]).apply(lambda g: reg(g,"r10"))
    out["ex_on_pos_by_state"] = R.groupby(["flat"]).apply(lambda g: reg(g,"pos"))
    fb = R[(R.flat=="flat")&(R.side=="below")].copy()
    fb["r10q"] = pd.qcut(fb.r10, 5, labels=False)
    out["flat_below_by_r10_quintile"] = fb.groupby("r10q").agg(n=("ex","size"), r10=("r10","mean"), ex=("ex","mean"), z=("z","mean"))
    fb["posq"] = pd.qcut(fb.pos, 4, labels=False)
    out["flat_below_by_pos_quartile"] = fb.groupby("posq").agg(n=("ex","size"), pos=("pos","mean"), ex=("ex","mean"), z=("z","mean"))
    R["netq"] = pd.qcut(R.net, 5, labels=False)
    R["sgn"] = -np.sign(R.pos)
    R["rev"] = R.ex*R.sgn
    out["reversion_toward_mid_by_net_quintile"] = R.groupby("netq").agg(n=("rev","size"), net=("net","mean"), rev=("rev","mean"),
        t=("rev", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # deepest falls of book
    chain=[]; meta=[]
    per = {}
    for c in coins:
        for w,d in days[c].items():
            per.setdefault(w,[]).append(d.set_index("day")["book_return"].rename(c))
    for w in sorted(per,key=lambda x:int(x[1:])):
        df = pd.concat(per[w],axis=1)
        chain.append(df.mean(axis=1).dropna()); meta += [w]*len(chain[-1])
    s = pd.concat(chain, ignore_index=True); mw = pd.Series(meta)
    v=(1+s).cumprod(); dd=v/v.cummax()-1
    out["dd_by_window_min"] = dd.groupby(mw).min().sort_values().head(6)
    # contributions per coin to worst 20 book days
    worst = s.nsmallest(20)
    out["worst20_days_mean"] = worst.mean()
    # coin contributions: collect per day per coin
    allc=[]
    for w in sorted(per,key=lambda x:int(x[1:])):
        allc.append(pd.concat(per[w],axis=1).dropna(how="all"))
    C = pd.concat(allc, ignore_index=True)
    out["worst20_coin_contrib"] = C.loc[worst.index].mean()/6
    return out
