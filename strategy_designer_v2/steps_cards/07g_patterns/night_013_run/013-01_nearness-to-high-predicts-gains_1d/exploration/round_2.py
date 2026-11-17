def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values)
            vo = pd.Series(b["volume"].values)
            n = len(b)
            r1 = cl.pct_change()
            r7p = cl.pct_change(7)
            vol20 = r1.rolling(20).std()
            vrel = vo / vo.rolling(30).mean()
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (7, 30):
                for t in range(0, n - h, h):
                    rows.append(dict(c=c, w=w, h=h, yr=yr.iloc[t], fwd=cl[t+h]/cl[t]-1,
                                     r1=r1.iloc[t], r7p=r7p.iloc[t],
                                     z7=r7p.iloc[t]/(vol20.iloc[t]*np.sqrt(7)) if vol20.iloc[t]>0 else np.nan,
                                     z1=r1.iloc[t]/vol20.iloc[t] if vol20.iloc[t]>0 else np.nan,
                                     vrel=vrel.iloc[t],
                                     sv=np.sign(r1.iloc[t])*np.log(vrel.iloc[t]) if vrel.iloc[t]>0 else np.nan))
    S = pd.DataFrame(rows)
    S["ex"] = S["fwd"] - S.groupby(["c","h"])["fwd"].transform("mean")
    def slope(df, x):
        d = df[[x,"ex"]].dropna()
        if len(d) < 15: return (np.nan, np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["ex"])
        rho = stats.spearmanr(d[x], d["ex"])[0]
        return (round(r.slope,5), round(r.slope/r.stderr,2), round(rho,3), len(d))
    res = {}
    for h in (7,30):
        for x in ["r1","r7p","z7","z1","vrel","sv"]:
            res[f"h{h}_{x}"] = slope(S[S.h==h], x)
    out["slopes(slope,t,rho,n)"] = pd.DataFrame(res, index=["slope","t","rho","n"]).T
    # winsorised r7p (clip 1/99 pct)
    s7 = S[S.h==7].dropna(subset=["r7p"]).copy()
    lo, hi = s7["r7p"].quantile([0.01,0.99])
    s7["r7w"] = s7["r7p"].clip(lo,hi); s7["exw"] = s7["ex"].clip(*s7["ex"].quantile([0.01,0.99]))
    r = stats.linregress(s7["r7w"], s7["exw"])
    out["h7_r7p_winsor"] = pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(s7)}).round(4)
    pc = {}
    for c,g in S[S.h==7].groupby("c"):
        pc[c] = slope(g,"r7p") + slope(g,"z7")
    out["h7_percoin_r7p_z7"] = pd.DataFrame(pc, index=["s","t","rho","n","sz","tz","rhoz","nz"]).T
    py = {}
    for y,g in S[S.h==7].groupby("yr"):
        py[y] = slope(g,"z7")
    out["h7_byyear_z7"] = pd.DataFrame(py, index=["s","t","rho","n"]).T
    s7 = S[S.h==7].dropna(subset=["z7"]).copy()
    s7["q"] = s7.groupby("c")["z7"].transform(lambda v: pd.qcut(v.rank(method="first"),5,labels=False))
    out["h7_z7_quintile"] = s7.groupby("q").agg(z7=("z7","mean"), ex=("ex","mean"), med=("ex","median"), n=("ex","size"), sd=("ex","std")).round(4)
    s30 = S[S.h==30].dropna(subset=["r1"]).copy()
    s30["q"] = pd.qcut(s30["r1"].rank(method="first"),5,labels=False)
    out["h30_r1_quintile"] = s30.groupby("q").agg(r1=("r1","mean"), ex=("ex","mean"), med=("ex","median"), n=("ex","size")).round(4)
    # weekday robustness
    D=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            d=d.copy(); d["c"]=c; D.append(d)
    D=pd.concat(D); dt=pd.to_datetime(D["day"]); D["wd"]=dt.dt.dayofweek; D["yr"]=dt.dt.year
    D["sat"]=(D.wd==5)
    tab={}
    for y,g in D.groupby("yr"):
        a=g[g.sat]["coin_return"].dropna(); b2=g[~g.sat]["coin_return"].dropna()
        tab[y]=(round(a.mean()-b2.mean(),5), round(stats.ttest_ind(a,b2,equal_var=False)[0],2), len(a))
    out["sat_minus_rest_by_year"]=pd.DataFrame(tab,index=["diff","t","n"]).T
    tab={}
    for c,g in D.groupby("c"):
        a=g[g.sat]["coin_return"].dropna(); b2=g[~g.sat]["coin_return"].dropna()
        tab[c]=(round(a.mean()-b2.mean(),5), round(stats.ttest_ind(a,b2,equal_var=False)[0],2), len(a))
    out["sat_minus_rest_by_coin"]=pd.DataFrame(tab,index=["diff","t","n"]).T
    return out
