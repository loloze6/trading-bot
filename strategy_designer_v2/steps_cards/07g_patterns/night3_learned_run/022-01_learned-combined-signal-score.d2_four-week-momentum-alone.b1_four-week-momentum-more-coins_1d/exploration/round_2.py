def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            ts = pd.to_datetime(b["timestamp"])
            s = pd.Series(c)
            r1 = (s/s.shift(1)-1).values
            vol20 = s.pct_change().rolling(20, min_periods=15).std()
            vol60 = s.pct_change().rolling(60, min_periods=40).std()
            relv = (vol20/vol60).values
            vol20 = vol20.values
            mom28 = (s/s.shift(28)-1).values
            mom84 = (s/s.shift(84)-1).values
            for h in (5, 10, 20):
                for i in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[i+h]/c[i]-1, r1=r1[i],
                                     r1z=r1[i]/vol20[i] if np.isfinite(vol20[i]) and vol20[i]>0 else np.nan,
                                     relv=relv[i], vol=vol20[i], mom28=mom28[i], mom84=mom84[i], yr=ts[i].year))
    df = pd.DataFrame(rows)
    g = df.groupby(["coin","h"])["fwd"]
    df["ex"] = df["fwd"] - g.transform("mean")
    df["z"] = df["ex"] / g.transform("std")
    out = {}
    def slope(sub, x, y="z", rank=False):
        s = sub[[x,y]].dropna()
        if len(s) < 40: return (np.nan, np.nan, len(s))
        xv = s[x].rank() if rank else s[x]
        xs = (xv-xv.mean())/xv.std()
        r = stats.linregress(xs, s[y])
        return (r.slope, r.slope/r.stderr, len(s))
    def tab(d): return pd.DataFrame(d, index=["slope","t","n"]).T
    # r1 -> fwd 20 robustness
    s20 = df[df.h==20].copy()
    s20["zc"] = s20["z"].clip(-3,3)
    out["r1_20d_variants"] = tab({"raw": slope(s20,"r1"), "rank": slope(s20,"r1",rank=True),
                                  "rank_zclip": slope(s20,"r1","zc",rank=True), "r1z_rank": slope(s20,"r1z",rank=True)})
    out["r1_20d_by_year"] = tab({k: slope(v,"r1",rank=True) for k,v in s20.groupby("yr")})
    s10 = df[df.h==10].copy(); s10["zc"]=s10["z"].clip(-3,3)
    s5 = df[df.h==5].copy(); s5["zc"]=s5["z"].clip(-3,3)
    out["r1_by_h_rank"] = tab({"5": slope(s5,"r1",rank=True), "10": slope(s10,"r1",rank=True), "20": slope(s20,"r1",rank=True)})
    q = s20.dropna(subset=["r1"]).copy()
    q["q"] = pd.qcut(q.r1.rank(method="first"),5,labels=False)
    out["r1_20d_quint"] = q.groupby("q").agg(n=("ex","size"), mean_ex=("ex","mean"), med_ex=("ex","median"), mean_z=("z","mean"))
    # mom28 by vol: relative vol and absolute, rank, clipped, by halves
    for lab, x in [("relv","relv"),("absvol","vol")]:
        s = s5.dropna(subset=[x,"mom28"]).copy()
        s["vt"] = pd.qcut(s[x].rank(method="first"),3,labels=["low","mid","high"])
        out["mom28_5d_by_"+lab] = tab({k: slope(v,"mom28","zc",rank=True) for k,v in s.groupby("vt")})
    s = s5.dropna(subset=["vol","mom28"]).copy()
    s["vt"] = s.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"),3,labels=False))
    s["half"] = np.where(s.yr<=2021,"to2021","from2022")
    out["mom28_5d_coinvol_by_half"] = tab({f"{a}_{b}": slope(v,"mom28","zc",rank=True) for (a,b),v in s.groupby(["half","vt"])})
    # size of the low-vol case: mean ex in top fifth mom28 within low-vol tercile vs all
    lv = s[s.vt==0].copy()
    lv["q"]=pd.qcut(lv.mom28.rank(method="first"),5,labels=False)
    out["lowvol_mom28_quint"] = lv.groupby("q").agg(n=("ex","size"),mean_ex=("ex","mean"),mean_z=("z","mean"))
    # mom84 at 10d robust
    out["mom84_10d"] = tab({"rank": slope(s10,"mom84","zc",rank=True), "to2021": slope(s10[s10.yr<=2021],"mom84","zc",rank=True), "from2022": slope(s10[s10.yr>=2022],"mom84","zc",rank=True)})
    # book: short vs long gain by year
    T=[]
    for coin,wins in bars.items():
        for w,b in wins.items():
            c=b["close"].astype(float).values; a=b["postRebalance_current_allocation"].astype(float).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values[:-1]
            T.append(pd.DataFrame(dict(g=a[:-1]*(c[1:]/c[:-1]-1), a=a[:-1], yr=yr)))
    T=pd.concat(T); T["side"]=np.sign(T.a)
    out["pos_gain_side_year"]=T.groupby(["yr","side"])["g"].mean().unstack()
    return out
