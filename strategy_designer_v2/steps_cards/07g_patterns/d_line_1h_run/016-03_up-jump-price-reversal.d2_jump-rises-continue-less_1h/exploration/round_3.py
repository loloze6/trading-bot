def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; H = 72
    rows = []; hr = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float); n = len(cl)
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            for i in range(H, n-H, H):
                past = cl[i]/cl[i-H]-1; fwd = cl[i+H]/cl[i]-1
                rr = r1[i-H+1:i+1]
                g = np.sort(rr[rr>0])[::-1]; l = np.sort(rr[rr<0])
                rows.append(dict(coin=c, w=w, past=past, fwd=fwd,
                    t3g=g[:3].sum() if len(g) else 0, t3l=l[:3].sum() if len(l) else 0))
            ts = pd.to_datetime(b["timestamp"])
            s = pd.Series(r1)
            vol24 = s.rolling(24).std().values
            ret20 = pd.Series(cl).pct_change(20).values
            f2 = np.r_[cl[2:]/cl[:-2]-1, np.nan, np.nan]
            hr.append(pd.DataFrame({"coin":c,"h":ts.dt.hour.values,"vol":vol24,"r20":ret20,"f2":f2}))
    g = pd.DataFrame(rows); g["ex"] = g.fwd - g.groupby("coin").fwd.transform("mean")
    def sp(d,x):
        r = stats.spearmanr(d[x], d["ex"]); return pd.Series({"rho":r[0],"n":len(d),"t":r[0]*np.sqrt((len(d)-2)/(1-r[0]**2))})
    up = g[g.past>0].copy(); up["gs"] = up.t3g/up.past
    out["rises: spearman ex vs top3 gain share, by coin"] = up.groupby("coin").apply(lambda d: sp(d,"gs"))
    out["rises: pooled spearman"] = sp(up,"gs")
    up["half"] = (up.w.str[1:].astype(int)>12).astype(int)
    out["rises: spearman by window half"] = up.groupby("half").apply(lambda d: sp(d,"gs"))
    dn = g[g.past<0].copy(); dn["ls"] = dn.t3l/dn.past
    out["falls: spearman by coin"] = dn.groupby("coin").apply(lambda d: sp(d,"ls"))
    out["falls: pooled spearman"] = sp(dn,"ls")
    hr = pd.concat(hr)
    at20 = hr[hr.h==20].dropna().copy()   # bar starting 20:00; f2 covers 20-21 bars... approx
    at20["vq"] = at20.groupby("coin").vol.transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    a = at20.groupby("vq").f2.agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["2h ret from hour20 bar close, by 24h vol quintile"] = a
    at20["rq"] = at20.groupby("coin").r20.transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    a = at20.groupby("rq").f2.agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["2h ret from hour20 bar close, by prior 20h ret quintile"] = a
    return out
