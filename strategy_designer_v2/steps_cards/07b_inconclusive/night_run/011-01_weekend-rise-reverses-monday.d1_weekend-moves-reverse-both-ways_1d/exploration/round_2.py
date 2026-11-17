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
            vol = r1.rolling(20).std()
            z = (r1/vol).values
            v = df["volume"].values
            # weekend volume (Sat+Sun) relative to 28-bar mean daily volume
            v2 = pd.Series(v).rolling(2).sum().values/2
            vm = pd.Series(v).rolling(28).mean().values
            n = len(df)
            for i in range(n):
                if ts.iloc[i].dayofweek != 6: continue
                rec = {"coin":coin,"f":df["forecast"].iloc[i],"z":z[i],
                       "relvol":v[i]/vm[i] if vm[i]>0 else np.nan,
                       "relwk":v2[i]/vm[i] if vm[i]>0 else np.nan}
                for h in [2,3]:
                    rec[f"x{h}"] = (c[i+h]/c[i]-1-means[(coin,h)]) if i+h<n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows).dropna(subset=["x2","z","relvol"])
    d["s2"] = -np.sign(d.z)*d.x2
    d["s3"] = -np.sign(d.x3)*0 + (-np.sign(d.z)*d.x3)
    d["v3"] = d.f/10*d.x3
    def tt(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out = {}
    d["vq"] = pd.qcut(d.relvol.rank(method="first"),5,labels=False)
    out["s2_by_relvol_quint"] = d.groupby("vq")["s2"].apply(tt).unstack()
    out["s3_by_relvol_quint"] = d.groupby("vq")["s3"].apply(tt).unstack()
    d["wq"] = pd.qcut(d.relwk.rank(method="first"),5,labels=False)
    out["s2_by_relwk_quint"] = d.groupby("wq")["s2"].apply(tt).unstack()
    d["zq"] = pd.qcut(d.z.abs().rank(method="first"),3,labels=["smallz","midz","bigz"])
    d["vt"] = pd.qcut(d.relvol.rank(method="first"),3,labels=["lowv","midv","highv"])
    out["s2_z_by_vol"] = d.groupby(["vt","zq"])["s2"].apply(tt).unstack()
    out["s3_by_absz_quint"] = d.groupby(pd.qcut(d.z.abs().rank(method="first"),5,labels=False))["s3"].apply(tt).unstack()
    # graded score: |z| / relvol
    d["score"] = d.z.abs()/d.relvol
    out["s2_by_score_quint"] = d.groupby(pd.qcut(d.score.rank(method="first"),5,labels=False))["s2"].apply(tt).unstack()
    out["corr_relvol_s2"] = float(np.corrcoef(d.relvol.rank(), d.s2)[0,1])
    out["corr_relvol_absz"] = float(np.corrcoef(d.relvol.rank(), d.z.abs().rank())[0,1])
    out["main_v3"] = tt(d.v3)
    return out
