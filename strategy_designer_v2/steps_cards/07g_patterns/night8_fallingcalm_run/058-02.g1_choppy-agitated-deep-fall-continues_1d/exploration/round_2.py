def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values; v=b["volume"].astype(float).values
            n=len(c)
            s=pd.Series(np.r_[np.nan, c[1:]/c[:-1]-1])
            sd20=s.rolling(20).std().values
            sd30=s.rolling(30).std()
            sdmed=sd30.expanding(30).median().values
            sd30=sd30.values
            vs=pd.Series(v)
            vr=(vs.rolling(5).mean()/vs.rolling(30).mean()).values
            vr10=(vs.rolling(10).mean()/vs.rolling(60).mean()).values
            ts=pd.to_datetime(b["timestamp"]).values
            for t in range(0,n-5,5):
                if t<30: continue
                r30=c[t]/c[t-30]-1
                r60=c[t]/c[t-60]-1 if t>=60 else np.nan
                rows.append(dict(coin=coin,w=w,ts=ts[t],f5=c[t+5]/c[t]-1,r30=r30,r60=r60,
                    z30=r30/(sd20[t]*np.sqrt(30)),vr=vr[t],vr10=vr10[t],
                    agit=(sd30[t]>sdmed[t]) if not np.isnan(sdmed[t]) else np.nan,
                    reg=b["regime"].values[t]))
    g=pd.DataFrame(rows)
    g["ex"]=g["f5"]-g.groupby("coin")["f5"].transform("mean")
    g["trend"]=np.where(g.r60.isna(),"na",np.where(g.r60<-0.10,"falling",np.where(g.r60>0.10,"rising","choppy")))
    def st(y):
        return pd.Series(dict(mean=y.mean(),n=len(y),t=y.mean()/(y.std()/np.sqrt(len(y))) if len(y)>2 else np.nan))
    def dayt(df):
        x=df.groupby("ts")["ex"].sum()
        nd=len(x); m=df["ex"].mean()
        se=np.sqrt((x - df.groupby("ts")["ex"].count()*m).pow(2).sum())/len(df)
        return pd.Series(dict(mean=m,n=len(df),days=nd,t_day=m/se))
    out={}
    fall=g[g.r30<0].copy()
    fall["vq"]=pd.qcut(fall.vr,3,labels=["quiet","mid","heavy"])
    out["falls by volume tercile, day-clustered"]=fall.groupby("vq").apply(dayt)
    out["falls quiet vs heavy by trend"]=fall.groupby(["trend","vq"])["ex"].apply(st).unstack()
    out["falls quiet vs heavy by agitation"]=fall.groupby(["agit","vq"])["ex"].apply(st).unstack()
    out["falls volume tercile by window"]=fall.groupby(["w","vq"])["ex"].mean().unstack()
    out["falls volume tercile by coin"]=fall.groupby(["coin","vq"])["ex"].mean().unstack()
    q=fall[fall.vq=="quiet"].copy()
    q["dq"]=pd.qcut(q.z30,3,labels=["shallow","mid","deep"])
    out["quiet falls by depth"]=q.groupby("dq").apply(dayt)
    hv=fall[fall.vq=="heavy"].copy()
    hv["dq"]=pd.qcut(hv.z30,3,labels=["shallow","mid","deep"])
    out["heavy falls by depth"]=hv.groupby("dq").apply(dayt)
    # graded: correlation of ex with vr among falls, and with z30*quiet
    out["falls corr ex~vr, ex~z30"]=pd.Series(dict(c_vr=fall[["ex","vr"]].corr().iloc[0,1],c_z30=fall[["ex","z30"]].corr().iloc[0,1],
        c_vr10=fall[["ex","vr10"]].corr().iloc[0,1],n=len(fall)))
    # all bars: volume ratio, rises vs falls
    g["vq"]=pd.qcut(g.vr,3,labels=["quiet","mid","heavy"])
    g["side"]=np.where(g.r30<0,"fall","rise")
    out["all: side x volume"]=g.groupby(["side","vq"])["ex"].apply(st).unstack()
    # z30 momentum by trend
    g["zq"]=pd.qcut(g.z30,5,labels=False)
    out["z30 quint x trend"]=g.groupby(["trend","zq"])["ex"].mean().unstack()
    out["z30 quint day-clustered"]=g.groupby("zq").apply(dayt)
    return out
