import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=7
    rows=[]
    for coin,wins in data["bars"].items():
        g7=[]
        for w,b in wins.items():
            c=b["close"].values.astype(float)
            for i in range(0,len(c)-H,H):
                g7.append(c[i+H]/c[i]-1)
        drift=np.mean(g7); usual=np.std(g7,ddof=1)
        allv=[]
        for w,b in wins.items():
            c=b["close"].astype(float).reset_index(drop=True)
            allv.append(c.pct_change().rolling(30).std())
        allv=pd.concat(allv).dropna().values
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            r30=c/c.shift(30)-1
            v30=r1.rolling(30).std()
            ts=pd.to_datetime(b["timestamp"])
            alloc=b["postRebalance_current_allocation"].astype(float)
            for i in range(0,len(c)-H,H):
                f=c.iloc[i+H]/c.iloc[i]-1
                vr=(allv<=v30.iloc[i]).mean() if not np.isnan(v30.iloc[i]) else np.nan
                rows.append(dict(coin=coin,w=w,wn=int(w[1:]),day=ts.iloc[i].normalize(),
                    yr=ts.iloc[i].year,r30=r30.iloc[i],vr=vr,
                    chop=b["regime"].iloc[i]=="unknown",fc=b["forecast"].iloc[i],
                    al=alloc.iloc[i],ex=f-drift,exz=(f-drift)/usual))
    G=pd.DataFrame(rows).dropna(subset=["r30","vr"])
    G["agit"]=G["vr"]>0.5
    def ct(df,col):
        s=df.groupby("day")[col].sum(); m=df[col].mean(); k=len(s)
        if k<3: return pd.Series(dict(n=len(df),days=k,mean=m,t=np.nan))
        se=np.sqrt((s-m*df.groupby("day")[col].size()).pow(2).sum()*k/(k-1))/len(df)
        return pd.Series(dict(n=len(df),days=k,mean=m,t=m/se))
    def slope(d,x="r30",y="exz"):
        if len(d)<10: return pd.Series(dict(n=len(d),slope=np.nan,t=np.nan))
        s=stats.linregress(d[x],d[y]); return pd.Series(dict(n=len(d),slope=s.slope,t=s.slope/s.stderr))
    out={}
    C=G[G.chop].copy()
    C["side"]=np.where(C.r30<0,"fall","rise")
    C["cont"]=C["ex"]*np.sign(C["r30"])
    out["chop_cont_by_agit_side"]=C.groupby(["agit","side"]).apply(lambda d:ct(d,"cont"))
    out["chop_slope_by_agit_side"]=C.groupby(["agit","side"]).apply(slope)
    C["half"]=np.where(C.wn<=12,"w7-12","w13-18")
    out["chop_fall_agit_by_half"]=C[(C.side=="fall")&C.agit].groupby("half").apply(lambda d:ct(d,"cont"))
    out["chop_fall_calm_by_half"]=C[(C.side=="fall")&~C.agit].groupby("half").apply(lambda d:ct(d,"cont"))
    out["chop_fall_agit_by_year"]=C[(C.side=="fall")&C.agit].groupby("yr").apply(lambda d:ct(d,"cont"))
    F=C[(C.side=="fall")&C.agit].copy()
    F["tq"]=pd.qcut(F["r30"],3,labels=["deep","mid","shallow"])
    out["chop_agit_fall_terciles_cont"]=F.groupby("tq").apply(lambda d:ct(d,"cont"))
    out["chop_agit_fall_by_coin"]=F.groupby("coin").apply(lambda d:ct(d,"cont"))
    # cases of the forecast
    K=C[C.fc<=-2]
    out["cases_fc_by_agit"]=K.groupby("agit").apply(lambda d:ct(d,"cont"))
    # nonchop for comparison, falls, agitated
    N=G[~G.chop].copy(); N["cont"]=N["ex"]*np.sign(N["r30"])
    N["side"]=np.where(N.r30<0,"fall","rise")
    out["nonchop_cont_by_agit_side"]=N.groupby(["agit","side"]).apply(lambda d:ct(d,"cont"))
    out["agit_share_chop"]=float(C.agit.mean())
    return out
