def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float)
            r=cl.pct_change()
            v=r.rolling(20).std()
            z=r/v
            d=pd.DataFrame({"coin":c,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year":pd.to_datetime(b["timestamp"]).dt.year,
                "z":z,"r":r,"fwd":cl.shift(-1)/cl-1,"fc":b["forecast"].astype(float),
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "tr60":cl/cl.shift(60)-1,"tr20":cl/cl.shift(20)-1,
                "vr":r.rolling(10).std()/r.rolling(60).std(),
                "pv":b["postRebalance_total_value"].astype(float)})
            d["bookret"]=d["pv"].shift(-1)/d["pv"]-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["mu"]=D.groupby("coin")["fwd"].transform("mean")
    D["ex"]=D["fwd"]-D["mu"]
    def summ(g):
        def f(x):
            x=x.dropna()
            n=len(x); m=x.mean()
            return pd.Series({"n":n,"mean_fwd%":100*m if n else np.nan,"t":m/(x.std()/np.sqrt(n)) if n>2 else np.nan})
        return f(g)
    out={}
    D["zb"]=pd.cut(D["z"],[-99,-3,-2,-1.5,-1,-0.5,0,0.5,1,2,99])
    out["fwd_ex_by_z"]=D.groupby("zb")["ex"].apply(summ).unstack()
    out["fwd_raw_by_z"]=D.groupby("zb")["fwd"].apply(summ).unstack()
    D["trb"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    dn=D[D["z"]<-1]
    out["z<-1_by_trend60"]=dn.groupby("trb")["ex"].apply(summ).unstack()
    out["all_by_trend60"]=D.groupby("trb")["ex"].apply(summ).unstack()
    D["vb"]=pd.cut(D["vr"],[0,0.8,1.0,1.25,9],labels=["calm","mid","up","agit"])
    out["z<-1_by_volratio"]=D[D["z"]<-1].groupby("vb")["ex"].apply(summ).unstack()
    out["all_by_volratio"]=D.groupby("vb")["ex"].apply(summ).unstack()
    D["t20b"]=pd.cut(D["tr20"],[-9,-0.15,0,0.15,99])
    out["z<-1_by_tr20"]=D[D["z"]<-1].groupby("t20b")["ex"].apply(summ).unstack()
    out["all_by_tr20"]=D.groupby("t20b")["ex"].apply(summ).unstack()
    # position by z bucket
    out["alloc_by_z"]=D.groupby("zb")["alloc"].agg(["mean",lambda x:(x.abs()>0.01).mean()])
    # book gain decomposition: position gain
    D["pg"]=D["alloc"]*D["fwd"]
    D["pg_beta"]=D["alloc"]*D["mu"]
    out["posgain_by_z"]=D.groupby("zb")[["pg","pg_beta"]].sum()
    # by year book
    out["by_year_z<-1"]=D[D["z"]<-1].groupby("year")["ex"].apply(summ).unstack()
    # book daily returns per window: drawdowns
    dd=[]
    for w,g in D.groupby("w"):
        br=g.groupby("day")["bookret"].mean().dropna()
        eq=(1+br).cumprod()
        mdd=(eq/eq.cummax()-1).min()
        hr=g.groupby("day")["fwd"].mean().dropna()
        dd.append({"w":w,"book_tot%":100*(eq.iloc[-1]-1),"book_mdd%":100*mdd,"hold_tot%":100*((1+hr).prod()-1),
                   "mean_alloc":g["alloc"].mean(),"tr60_mean":g["tr60"].mean()})
    out["windows"]=pd.DataFrame(dd).set_index("w")
    # bookret on days by trend while held
    out["held_pg_by_trend"]=D[D["alloc"]>0.01].groupby("trb")[["pg"]].agg(["mean","count"])
    return out
