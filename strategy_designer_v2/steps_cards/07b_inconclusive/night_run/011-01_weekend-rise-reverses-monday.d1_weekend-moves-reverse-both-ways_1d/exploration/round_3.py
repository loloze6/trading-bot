def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    means = {}
    for coin, wins in bars.items():
        for h in [2,3]:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                vals.extend(list(c[idx+h]/c[idx]-1))
            means[(coin,h)] = np.mean(vals)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(20).std().values
            z = r1.values/vol
            n = len(df)
            for i in range(n):
                if ts.iloc[i].dayofweek != 6 or i+2>=n or not np.isfinite(z[i]): continue
                x2 = c[i+2]/c[i]-1-means[(coin,2)]
                x3 = (c[i+3]/c[i]-1-means[(coin,3)]) if i+3<n else np.nan
                rows.append({"coin":coin,"win":w,"z":z[i],"vol":vol[i],"x2":x2,"x3":x3,"f":df["forecast"].iloc[i]})
    d = pd.DataFrame(rows)
    d["s2"] = -np.sign(d.z)*d.x2
    d["s2v"] = d.s2/d.vol
    d["hit"] = (d.s2>0).astype(float)
    d["q"] = pd.qcut(d.z.abs().rank(method="first"),5,labels=False)
    def tt(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"sd":x.std(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out = {}
    out["s2_volunits_by_absz_q"] = d.groupby("q")["s2v"].apply(tt).unstack()
    out["hit_by_absz_q"] = d.groupby("q")["hit"].mean()
    out["absz_mean_by_q"] = d.groupby("q")["z"].apply(lambda x: x.abs().mean())
    out["f_abs_mean_by_q"] = d.groupby("q")["f"].apply(lambda x: x.abs().mean())
    # top vs bottom third by |f| in vol units and raw
    d["fq"] = pd.qcut(d.f.abs().rank(method="first"),3,labels=["bot","mid","top"])
    out["by_f_third_raw_and_vol"] = pd.DataFrame({"raw":d.groupby("fq")["s2"].mean(),"vol":d.groupby("fq")["s2v"].mean(),"sd_raw":d.groupby("fq")["s2"].std()})
    out["corr_absz_s2v"] = float(np.corrcoef(d.z.abs(), d.s2v)[0,1])
    return out
