import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float).rolling(20).max(); lo = df["low"].astype(float).rolling(20).min()
            pos = 2*(c-lo)/(hi-lo)-1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in (1,3,5,10):
                fwd = c.shift(-h)/c-1
                idx = np.arange(0, len(df), h)
                for i in idx:
                    if np.isnan(fwd.iloc[i]) or np.isnan(pos.iloc[i]): continue
                    rows.append(dict(coin=coin, w=w, h=h, pos=pos.iloc[i], f=df["forecast"].iloc[i],
                                     cc=(df["regime"].iloc[i]=="unknown"), r=fwd.iloc[i], yr=yr.iloc[i],
                                     day=str(df["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin","h"])["r"].transform("mean")
    d["x"] = d["r"]-d["drift"]
    d["b"] = pd.cut(d["pos"], [-1.01,-0.6,-0.2,0.2,0.6,1.01], labels=["bot","lowmid","mid","highmid","top"])
    def agg(g):
        n=len(g); m=g["x"].mean(); s=g["x"].std(ddof=1)
        return pd.Series({"n":n,"mean_x%":100*m,"t":m/(s/np.sqrt(n)) if n>1 and s>0 else np.nan})
    out = {}
    out["by_bucket_profile_h5"] = d[d.h==5].groupby(["cc","b"]).apply(agg)
    out["by_bucket_cc_by_h"] = d[d.cc].groupby(["h","b"]).apply(agg)
    s5 = d[(d.h==5)&d.cc&(d.pos<0)]
    out["cc_bottomhalf_by_coin"] = s5.groupby("coin").apply(agg)
    out["cc_bottomhalf_by_year"] = s5.groupby("yr").apply(agg)
    out["cc_bottomhalf_by_window"] = s5.groupby("w").apply(agg)
    sf = d[(d.h==5)&(d.f<0)]
    out["forecast_neg_h5_by_fquint"] = sf.groupby(pd.qcut(sf["f"],4,duplicates="drop")).apply(agg)
    out["corr_pos_x_cc_bottom"] = float(np.corrcoef(s5["pos"], s5["x"])[0,1])
    return out
