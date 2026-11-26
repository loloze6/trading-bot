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
            lr=np.log(b.close).diff()
            sd30=lr.rolling(30,min_periods=20).std()
            agit=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            tr60=b.close/b.close.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"cl":cl,"rrel":rrel,"dret":dret,"tr60":tr60,"agit":agit,
                            "ex":r1-drift,"r1":r1,"alloc":b.postRebalance_current_allocation,
                            "day":pd.to_datetime(b.timestamp).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["cl","ex","dret","rrel"])
    def tday(s,days):
        x=pd.DataFrame({"v":s.values,"d":days.values}).groupby("d").v.sum()
        n=len(x); m=s.mean()
        se=np.sqrt(((x - s.groupby(days.values).count()*m)**2).sum())/len(s)
        return pd.Series({"mean_bp":m*1e4,"t_day":m/se if se>0 else np.nan,"n":len(s),"days":n})
    out={}
    D["c3"]=pd.cut(D.cl,[-.01,.2,.8,1.01],labels=["nearHigh","mid","nearLow"])
    D["dq"]=pd.qcut(D.dret,3,labels=["down","flat","up"])
    out["cl_x_dayret_n"]=D.pivot_table(index="c3",columns="dq",values="ex",aggfunc="count")
    # within dret terciles, grading of cl
    res={}
    for q in ["down","flat","up"]:
        X=D[D.dq==q]
        A=np.column_stack([np.ones(len(X)),X.cl,X.dret])
        res[q]=np.linalg.lstsq(A,X.ex.values,rcond=None)[0][1]*1e4
    out["cl_coef_bp_within_dret_tercile_ctrl_dret"]=pd.Series(res)
    D["big"]=D.rrel>D.rrel.quantile(2/3)
    D["fall"]=D.tr60<-0.1
    D["low"]=D.cl>0.8
    cells={}
    for name,m in {"low&big":D.low&D.big,"big&notlow":D.big&~D.low,"low&notbig":D.low&~D.big,
                   "low&fall":D.low&D.fall,"fall&notlow":D.fall&~D.low,"low&notfall":D.low&~D.fall,
                   "low&big&down":D.low&D.big&(D.dq=="down"),"big&down&notlow":D.big&(D.dq=="down")&~D.low,
                   "down&notlow":(D.dq=="down")&~D.low,"low&down":D.low&(D.dq=="down")}.items():
        cells[name]=tday(D.ex[m],D.day[m])
    out["cells"]=pd.DataFrame(cells).T
    # graded in big range: cl*rrel regression
    D["clxr"]=(D.cl-0.5)*D.rrel
    A=np.column_stack([np.ones(len(D)),D.cl-0.5,D.clxr,D.dret])
    out["ols_cl_clxrange_dret_bp"]=pd.Series(np.linalg.lstsq(A,D.ex.values,rcond=None)[0]*1e4,index=["c","cl","cl_x_rrel","dret"])
    # per window low&big
    m=D.low&D.big
    out["lowbig_by_window"]=D[m].groupby("w").ex.agg(lambda x:x.mean()*1e4).to_frame("bp").join(D[m].groupby("w").ex.count().rename("n"))
    out["lowbig_by_year"]=D[m].groupby(D.day.dt.year).ex.agg(["mean","count"])
    D["ag"]=np.where(D.agit>0.5,"agit","calm")
    out["c3_x_agit_bp"]=D.pivot_table(index="c3",columns="ag",values="ex",aggfunc="mean")*1e4
    out["c3_x_agit_n"]=D.pivot_table(index="c3",columns="ag",values="ex",aggfunc="count")
    # long-only graded payoff by cl*rrel decile
    D["s"]=(D.cl-0.5).clip(lower=0)*D.rrel
    S=D[D.s>0]
    S["sq"]=pd.qcut(S.s,5,labels=False)
    out["longscore_quintile"]=S.groupby("sq").ex.agg(["mean","count"])
    return out
