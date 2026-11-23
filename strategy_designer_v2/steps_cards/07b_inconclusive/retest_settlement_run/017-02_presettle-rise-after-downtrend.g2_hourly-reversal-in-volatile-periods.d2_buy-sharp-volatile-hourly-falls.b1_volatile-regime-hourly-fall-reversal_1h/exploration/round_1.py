def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[6,12,24,48]
    rec=[]; prc=[]
    for coin,wins in data["bars"].items():
        # coin mean per horizon over grids of all windows
        mean_h={}
        for h in H:
            rs=[]
            for w,b in wins.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rs.append(c[idx+h]/c[idx]-1)
            mean_h[h]=np.nanmean(np.concatenate(rs))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); n=len(c)
            f=b["forecast"].fillna(0).values
            ts=pd.to_datetime(b["timestamp"])
            r1=pd.Series(c).pct_change()
            v24=r1.rolling(24).std(); us=v24.rolling(720,min_periods=200).mean()
            z=(r1/us).values; vr=(v24/us).values
            df_=np.r_[0,np.diff(f)]
            cell=np.arange(n)//24
            # strategy cases
            seen=set()
            for i in np.where((f>=2)&(df_>=2))[0]:
                if cell[i] in seen or i+24>=n: continue
                seen.add(cell[i])
                d={"coin":coin,"w":int(w[1:]),"year":ts[i].year,"hour":ts[i].hour,"f":f[i],"vr":vr[i],"z":z[i]}
                for h in H:
                    d[f"x{h}"]=(c[i+h]/c[i]-1-mean_h[h]) if i+h<n else np.nan
                rec.append(d)
            # price cases: sharp falls any regime
            seen=set()
            for i in np.where(z<=-2)[0]:
                if cell[i] in seen or i+24>=n: continue
                seen.add(cell[i])
                prc.append({"coin":coin,"vr":vr[i],"z":z[i],"hour":ts[i].hour,"x24":c[i+24]/c[i]-1-mean_h[24]})
    R=pd.DataFrame(rec); P=pd.DataFrame(prc)
    def agg(g,col="x24"):
        x=g[col].dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["all_by_horizon"]=pd.DataFrame({h:agg(R,f"x{h}") for h in H}).T
    out["by_coin"]=R.groupby("coin").apply(agg)
    out["by_year"]=R.groupby("year").apply(agg)
    out["forecast_desc"]=R["f"].describe()
    R["fq"]=pd.qcut(R["f"].rank(method="first"),4,labels=False)
    out["by_forecast_q"]=R.groupby("fq").apply(agg)
    R["vq"]=pd.qcut(R["vr"],4,labels=False)
    out["by_volratio_q"]=R.groupby("vq").apply(agg)
    R["settle"]=R["hour"].isin([23,7,15,0,8,16])
    out["by_near_settle"]=R.groupby("settle").apply(agg)
    P["vb"]=pd.cut(P["vr"],[0,0.8,1.0,1.3,1.8,10])
    out["price_falls_by_vr"]=P.groupby("vb").apply(agg)
    P["zb"]=pd.cut(P["z"],[-100,-6,-4,-3,-2])
    out["price_falls_by_z"]=P.groupby("zb").apply(agg)
    out["price_by_coin"]=P.groupby("coin").apply(agg)
    return out
