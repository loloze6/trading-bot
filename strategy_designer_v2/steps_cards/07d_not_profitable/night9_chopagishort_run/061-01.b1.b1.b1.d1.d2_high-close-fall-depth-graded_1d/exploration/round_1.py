def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            for i in range(0,len(b)-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(allr) if allr else np.nan
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            rng=(h-l).replace(0,np.nan)
            cl=(c-l)/rng
            r5=c/c.shift(5)-1
            r1=c/c.shift(1)-1
            fwd=c.shift(-H)/c-1
            for i in range(len(b)):
                if np.isnan(fwd.iloc[i]): continue
                rows.append(dict(coin=coin,w=w,i=i,cell=i//H,day=str(b["timestamp"].iloc[i])[:10],
                    year=str(b["timestamp"].iloc[i])[:4],regime=b["regime"].iloc[i],cl=cl.iloc[i],r5=r5.iloc[i],r1=r1.iloc[i],
                    fwd=fwd.iloc[i],un=-(fwd.iloc[i]-drift[coin])))
    df=pd.DataFrame(rows).dropna(subset=["cl","r5"])
    df["inprof"]=df.regime!="chop"
    def summ(sub):
        # first per cell per coin-window
        s=sub.sort_values("i").groupby(["coin","w","cell"]).first().reset_index()
        if len(s)<3: return pd.Series(dict(n=len(s),days=s.day.nunique() if len(s) else 0,mean_un=np.nan,t=np.nan,mean_short_total=np.nan))
        d=(s.un-s.un.mean()).groupby(s.day).sum()
        se=np.sqrt((d**2).sum())/len(s)
        return pd.Series(dict(n=len(s),days=s.day.nunique(),mean_un=s.un.mean(),t=s.un.mean()/se,mean_short_total=(-s.fwd).mean()))
    g={}
    P=df[df.inprof]; O=df[~df.inprof]
    g["prof_cl75_r5neg (signal)"]=summ(P[(P.cl>=.75)&(P.r5<0)])
    g["prof_cl75_r5pos"]=summ(P[(P.cl>=.75)&(P.r5>=0)])
    g["prof_cl50_75_r5neg"]=summ(P[(P.cl>=.5)&(P.cl<.75)&(P.r5<0)])
    g["prof_cl_lt50_r5neg"]=summ(P[(P.cl<.5)&(P.r5<0)])
    g["prof_all"]=summ(P)
    g["prof_r5neg_any_cl"]=summ(P[P.r5<0])
    g["out_cl75_r5neg"]=summ(O[(O.cl>=.75)&(O.r5<0)])
    g["out_cl75_r5pos"]=summ(O[(O.cl>=.75)&(O.r5>=0)])
    g["out_all"]=summ(O)
    g["out_r5neg"]=summ(O[O.r5<0])
    groups=pd.DataFrame(g).T
    # r5 depth buckets inside profile with cl>=.5
    Q=P[(P.cl>=.5)&(P.r5<0)].copy()
    Q["b"]=pd.qcut(Q.r5,3,labels=["deep","mid","shallow"])
    depth=pd.DataFrame({k:summ(v) for k,v in Q.groupby("b")}).T
    O2=O[(O.cl>=.75)&(O.r5<0)].copy()
    O2["b"]=pd.qcut(O2.r5,3,labels=["deep","mid","shallow"])
    depth_out=pd.DataFrame({k:summ(v) for k,v in O2.groupby("b")}).T
    share=df.groupby("regime").size()/len(df)
    # trades
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; tt["w"]=w; tr.append(tt)
    T=pd.concat(tr)
    T["year"]=T.entry_time.astype(str).str[:4]
    trades=T.groupby("year").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),mean_gross=("profit_loss_percent","mean"),dur_days=("duration_minutes",lambda x:(x/1440).mean()))
    yr=df[df.inprof].groupby("year").size()
    return {"groups":groups,"depth_in_profile_cl50":depth,"depth_outprofile_cl75":depth_out,"regime_share":share,"trades_by_year":trades,"inprof_bars_by_year":yr}
