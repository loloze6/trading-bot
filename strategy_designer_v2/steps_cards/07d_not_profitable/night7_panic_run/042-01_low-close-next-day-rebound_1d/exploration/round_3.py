def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(b["close"].pct_change().dropna())
        drift=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            rng=(b.high-b.low)
            cl=(b.high-b.close)/rng.replace(0,np.nan)
            rr=rng/b.close
            rrel=rr/rr.rolling(20,min_periods=10).mean().shift(1)
            r1=b.close.shift(-1)/b.close-1
            dret=b.close.pct_change()
            sd20=dret.rolling(20,min_periods=10).std().shift(1)
            lr=np.log(b.close).diff()
            sd30=lr.rolling(30,min_periods=20).std()
            agit=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            tr60=b.close/b.close.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"cl":cl.values,"rrel":rrel.values,"dret":dret.values,
                            "dz":(dret/sd20).values,"tr60":tr60.values,"agit":agit.values,
                            "ex":(r1-drift).values,"alloc":b.postRebalance_current_allocation.values,
                            "day":pd.to_datetime(b.timestamp).dt.floor("D").values,"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["cl","ex","dret","rrel","dz"]).reset_index(drop=True)
    def tday(m):
        s=D.ex[m]; days=D.day[m]
        if len(s)<5: return pd.Series({"mean_bp":np.nan,"t_day":np.nan,"n":len(s),"days":0})
        mu=s.mean(); g=(s-mu).groupby(days.values).sum()
        se=np.sqrt((g**2).sum())/len(s)
        return pd.Series({"mean_bp":mu*1e4,"t_day":mu/se,"n":len(s),"days":len(g)})
    out={}
    D["c3"]=pd.cut(D.cl,[-.01,.2,.8,1.01],labels=["nearHigh","mid","nearLow"])
    D["dq"]=pd.qcut(D.dz,3,labels=["down","flat","up"])
    out["cl_x_dz_n"]=D.pivot_table(index="c3",columns="dq",values="ex",aggfunc="count",observed=False)
    out["cl_x_dz_bp"]=D.pivot_table(index="c3",columns="dq",values="ex",aggfunc="mean",observed=False)*1e4
    res={}
    for q in ["down","flat","up"]:
        X=D[D.dq==q]
        A=np.column_stack([np.ones(len(X)),X.cl,X.dz])
        res[q]=np.linalg.lstsq(A,X.ex.values,rcond=None)[0][1]*1e4
    out["cl_coef_bp_within_dz_tercile"]=pd.Series(res)
    A=np.column_stack([np.ones(len(D)),D.cl,D.dz])
    out["ols_cl_dz_bp"]=pd.Series(np.linalg.lstsq(A,D.ex.values,rcond=None)[0]*1e4,index=["c","cl","dz"])
    big=D.rrel>D.rrel.quantile(2/3); fall=D.tr60<-0.1; low=D.cl>0.8; half=D.cl>0.5
    agt=D.agit>0.5; down=D.dq=="down"
    cells={"all_low":low,"low&big":low&big,"big&notlow":big&~low,"low&notbig":low&~big,
           "low&fall":low&fall,"fall&notlow":fall&~low,"low&notfall":low&~fall,
           "low&agit":low&agt,"agit&notlow":agt&~low,"low&calm":low&~agt,
           "lowhalf":half,"highhalf":~half,"low&down":low&down,"down&notlow":down&~low}
    out["cells"]=pd.DataFrame({k:tday(v) for k,v in cells.items()}).T
    m=low&big
    out["lowbig_by_window_bp"]=D[m].groupby("w").ex.agg(["mean","count"])
    out["low_by_year"]=D[low].groupby(D.day[low].dt.year).ex.agg(["mean","count"])
    D["s"]=(D.cl-0.5).clip(lower=0)*D.rrel
    S=D[D.s>0].copy()
    S["sq"]=pd.qcut(S.s,5,labels=False)
    out["longscore_quintile"]=S.groupby("sq").ex.agg(["mean","count"])
    out["alloc_by_c3"]=D.groupby("c3",observed=False).alloc.mean()
    out["alloc_abs_q"]=D.alloc.abs().quantile([.5,.9,.99])
    D["prof"]=np.where(D.tr60>0.1,"rising",np.where(D.tr60<-0.1,"falling","choppy"))+"_"+np.where(D.agit>0.5,"agit","calm")
    D["ok"]=D.agit.notna()&D.tr60.notna()
    E=D[D.ok]
    out["lowhalf_minus_highhalf_by_profile_bp"]=(E[E.cl>0.5].groupby("prof").ex.mean()-E[E.cl<=0.5].groupby("prof").ex.mean())*1e4
    out["low_by_profile"]=E[E.cl>0.8].groupby("prof").ex.agg(["mean","count"])
    return out
