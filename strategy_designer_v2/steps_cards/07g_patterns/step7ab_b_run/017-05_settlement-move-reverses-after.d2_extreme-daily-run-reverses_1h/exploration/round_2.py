import numpy as np, pandas as pd

def tstat(s):
    s = pd.Series(s).dropna()
    return s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.log(c[1:]/c[:-1])
            vol = pd.Series(np.r_[np.nan, r1]).rolling(168, min_periods=84).std().values
            ret24 = np.r_[np.full(24, np.nan), c[24:]/c[:-24]-1]
            z = ret24/(vol*np.sqrt(24))
            for h in [24, 72]:
                idx = np.arange(0, len(c)-h, h)
                fr = c[idx+h]/c[idx]-1
                for i, v in zip(idx, fr):
                    rows.append((coin, w, h, z[i], v, vol[i], ret24[i], ts.iloc[i].year))
    df = pd.DataFrame(rows, columns=["coin","w","h","z","fr","vol","r24","yr"]).dropna()
    df["drift"] = df.groupby(["coin","h"])["fr"].transform("mean")
    df["ex"] = df["fr"]-df["drift"]
    df["s_ex"] = -np.sign(df["z"])*df["ex"]
    df["vb"] = df.groupby(["coin","h"])["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    df["zq"] = pd.cut(df["z"], [-99,-1.5,-0.5,0.5,1.5,99], labels=["<-1.5","-1.5..-0.5","mid","0.5..1.5",">1.5"])
    for h in [24, 72]:
        d = df[df.h==h]
        g = d.groupby(["vb","zq"], observed=True)["ex"]
        out[f"h{h}: excess bps by vol tercile x z bin"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat), "n": g.count()})
    d = df[(df.h==24)&(df.vb==2)]
    g = d.groupby("vb")
    # graded within top vol: signed reversal vs |z| quartile
    d = d.assign(aq=pd.qcut(d["z"].abs(), 4, labels=False))
    g = d.groupby("aq")["s_ex"]
    out["h24 top vol: signed reversal by |z| quartile"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat), "n": g.count()})
    # stability: top vol tercile, signed reversal x |z|, by coin and by year
    dd = df[(df.h==24)&(df.vb==2)&(df.z.abs()>1)]
    g = dd.groupby("coin")["s_ex"]
    out["top vol |z|>1 reversal by coin"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat), "n": g.count()})
    g = dd.groupby("yr")["s_ex"]
    out["top vol |z|>1 reversal by year"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat), "n": g.count()})
    g = dd.groupby(np.sign(dd["z"]))["s_ex"]
    out["top vol |z|>1 reversal by run sign"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat), "n": g.count()})
    # graded vol: signed reversal of |z|>1 by vol quintile
    d2 = df[(df.h==24)&(df.z.abs()>1)].copy()
    d2["v5"] = d2.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False))
    g = d2.groupby("v5")["s_ex"]
    out["|z|>1 reversal by vol quintile"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat), "n": g.count()})
    # hour 21-22 effect stability
    hr = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            hr.append(pd.DataFrame({"hour": ts.dt.hour, "yr": ts.dt.year, "r": r, "coin": coin}))
    H = pd.concat(hr).dropna()
    H["r"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    H["blk"] = np.where(H.hour.isin([21,22]), "21-22", np.where(H.hour.isin([1,2,3]), "01-03", "other"))
    g = H.groupby(["blk","yr"])["r"]
    out["hour block by year bps"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat)}).unstack(0)
    g = H.groupby(["blk","coin"])["r"]
    out["hour block by coin bps"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.apply(tstat)}).unstack(0)
    return out
