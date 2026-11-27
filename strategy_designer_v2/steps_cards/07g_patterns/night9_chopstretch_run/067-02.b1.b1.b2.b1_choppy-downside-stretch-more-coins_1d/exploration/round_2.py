def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            z=(c-sma)/sma/sd
            tr60=c/c.shift(60)-1
            sd30=r.rolling(30).std()
            agit=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            pos=b["postRebalance_current_allocation"].astype(float)
            chop=(b["regime"]=="unknown")
            for h in [1,3,5,10]:
                b["r%d"%h]=c.shift(-h)/c-1
            for h in [3,5,10]:
                for i in range(0,len(b),h):
                    rows.append(dict(h=h,coin=coin,w=w,z=z[i],r=b["r%d"%h][i],chop=chop[i],tr=tr60[i],ag=agit[i],
                                     f=b["forecast"][i],pos=pos[i]))
    g=pd.DataFrame(rows).dropna(subset=["r"])
    out={}
    def summ(x):
        s=x["st"].dropna(); return pd.Series(dict(n=len(s),mean=s.mean(),t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan))
    parts=[]
    for h,gh in g.groupby("h"):
        gh=gh.copy()
        dr=gh.groupby("coin")["r"].mean(); us=gh.groupby("coin")["r"].std()
        gh["st"]=(gh["r"]-gh["coin"].map(dr))/gh["coin"].map(us)
        parts.append(gh)
    g=pd.concat(parts)
    c5=g[(g.h==5)&g.chop].dropna(subset=["z"]).copy()
    out["chop5_rawz_neg_vs_forecast_neg"]=pd.DataFrame({
        "z<0":summ(c5[c5.z<0]),"f<0":summ(c5[c5.f<0]),"f<0&z>=0":summ(c5[(c5.f<0)&(c5.z>=0)]),
        "f<0&z<-1":summ(c5[(c5.f<0)&(c5.z<-1)]),"f==0&z<0":summ(c5[(c5.f==0)&(c5.z<0)])}).T
    out["share_forecastneg_with_z_pos"]=float(((c5.f<0)&(c5.z>=0)).sum()/max((c5.f<0).sum(),1))
    c5["tb"]=pd.cut(c5["tr"],[-0.11,-0.03,0.03,0.11])
    out["chop5_z<-0.75_by_trend60"]=c5[c5.z<-0.75].groupby("tb").apply(summ)
    out["chop5_z>0.75_by_trend60"]=c5[c5.z>0.75].groupby("tb").apply(summ)
    c5["agb"]=np.where(c5.ag>0.5,"agitated",np.where(c5.ag.notna(),"calm","na"))
    out["chop5_z<-0.75_by_agit"]=c5[c5.z<-0.75].groupby("agb").apply(summ)
    out["chop5_z>0.75_by_agit"]=c5[c5.z>0.75].groupby("agb").apply(summ)
    for h in [3,10]:
        ch=g[(g.h==h)&g.chop].dropna(subset=["z"]).copy()
        ch["zb"]=pd.cut(ch["z"],[-99,-1.5,-0.5,0.5,1.5,99])
        out["chop_h%d_zbins"%h]=ch.groupby("zb").apply(summ)
        out["chop_h%d_spearman"%h]=float(stats.spearmanr(ch.z,ch.st)[0])
    # tails: z < -1.5 in chop, per coin sign count
    t=c5[c5.z<-1.5]
    out["chop5_z<-1.5_by_coin"]=t.groupby("coin").apply(summ)
    # book on held days, scaled
    out["chop5_pos<0_vs_z"]=c5[c5.pos<0].assign(zb=lambda x:pd.cut(x.z,[-99,-1.5,-0.5,0,99])).groupby("zb").apply(summ)
    return out
