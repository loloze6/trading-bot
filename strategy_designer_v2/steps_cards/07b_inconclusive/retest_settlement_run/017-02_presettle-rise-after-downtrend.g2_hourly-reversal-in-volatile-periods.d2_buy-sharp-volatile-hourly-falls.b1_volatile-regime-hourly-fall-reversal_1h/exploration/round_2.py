def explore(data):
    import numpy as np, pandas as pd
    rec=[]
    for coin,wins in data["bars"].items():
        rs=[]
        for w,b in wins.items():
            c=b["close"].values.astype(float); idx=np.arange(0,len(c)-24,24); rs.append(c[idx+24]/c[idx]-1)
        m24=np.nanmean(np.concatenate(rs))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); n=len(c)
            ts=pd.to_datetime(b["timestamp"])
            r1=pd.Series(c).pct_change()
            v24=r1.rolling(24).std(); us=v24.rolling(720,min_periods=200).mean()
            z=(r1/us).values; vr=(v24/us).values
            cell=np.arange(n)//24; seen=set()
            for i in np.where(z<=-1.5)[0]:
                if cell[i] in seen or i+24>=n or np.isnan(vr[i]): continue
                seen.add(cell[i])
                rec.append({"coin":coin,"year":ts[i].year,"vr":vr[i],"z":z[i],"x":c[i+24]/c[i]-1-m24,"vol24":v24[i]*np.sqrt(24)})
    P=pd.DataFrame(rec)
    def agg(g):
        x=g["x"]; return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"strength":(x/g["vol24"]).mean()})
    out={}
    P["vb"]=pd.cut(P["vr"],[0,1.0,1.3,1.6,2.0,2.5,20])
    out["falls_by_vr_fine"]=P.groupby("vb").apply(agg)
    H=P[P.vr>=1.3].copy()
    out["hi_vr_by_coin"]=H.groupby("coin").apply(agg)
    out["hi_vr_by_year"]=H.groupby("year").apply(agg)
    H["zb"]=pd.cut(H["z"],[-100,-4,-3,-2,-1.5])
    out["hi_vr_by_z"]=H.groupby("zb").apply(agg)
    P["prod"]=(-P["z"])*P["vr"]
    P["pq"]=pd.qcut(P["prod"],5,labels=False)
    out["by_z_times_vr_q"]=P.groupby("pq").apply(agg)
    out["corr_x_vr_spearman"]=float(P[["x","vr"]].corr("spearman").iloc[0,1])
    return out
