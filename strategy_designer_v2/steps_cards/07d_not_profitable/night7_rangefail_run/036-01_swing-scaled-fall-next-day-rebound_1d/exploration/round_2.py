def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); r=cl.pct_change()
            v20=r.rolling(20).std(); z=r/v20
            v30=r.rolling(30).std()
            vrank=v30.expanding(60).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            d=pd.DataFrame({"coin":c,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z":z,"r":r,"fwd":cl.shift(-1)/cl-1,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "vr":r.rolling(10).std()/r.rolling(60).std(),"vrank":vrank,
                "pv":b["postRebalance_total_value"].astype(float)})
            d["bookret"]=d["pv"].shift(-1)/d["pv"]-1
            d["vprev"]=d["vr"].shift(1)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["mu"]=D.groupby("coin")["fwd"].transform("mean"); D["ex"]=D["fwd"]-D["mu"]
    def f(x):
        x=x.dropna(); n=len(x); m=x.mean()
        return pd.Series({"n":n,"mean%":100*m,"t":m/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["agit"]=D["vr"]>1.0
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.5,0,99])
    out["ex_by_z_x_agit(vr10/60)"]=D.groupby(["agit","zb"])["ex"].apply(f).unstack()
    D["ag2"]=D["vrank"]>0.5
    out["ex_by_z_x_agit(30d rank in window)"]=D.groupby(["ag2","zb"])["ex"].apply(f).unstack()
    # vr measured before the fall day (excludes the fall itself)
    D["agp"]=D["vprev"]>1.0
    out["ex_by_z_x_agit_prevday"]=D.groupby(["agp","zb"])["ex"].apply(f).unstack()
    # simulated books: daily per coin pos*fwd - cost*|dpos|, mean across coins per day
    cost=0.0022/2
    def book(pos):
        X=D.assign(p=pos)
        X["dp"]=X.groupby(["coin","w"])["p"].diff().abs().fillna(X["p"].abs())
        X["g"]=X["p"]*X["fwd"]-cost*X["dp"]
        res=[];eqs=[]
        for w in sorted(X["w"].unique(),key=lambda s:int(s[1:])):
            g=X[X["w"]==w].groupby("day")["g"].mean().dropna(); res.append(g)
        s=pd.concat(res); eq=(1+s).cumprod(); mdd=(eq/eq.cummax()-1).min()
        yr=eq.iloc[-1]**(365/len(s))-1
        return {"sharpe":s.mean()/s.std()*np.sqrt(365),"yr%":100*yr,"mdd%":100*mdd,"calmar":yr/-mdd,"inpos":(X["p"].abs()>0).mean()}
    a=D["alloc"].fillna(0)
    sig=(-D["z"]).clip(lower=0).fillna(0)
    out["books"]=pd.DataFrame({
        "actual_alloc":book(a),
        "hold":book(pd.Series(1.0,index=D.index)),
        "alloc_only_z<-1":book(a.where(D["z"]<-1,0)),
        "alloc_only_agit":book(a.where(D["agit"],0)),
        "alloc_z<-1_agit":book(a.where((D["z"]<-1)&D["agit"],0)),
        "alloc_agit_prev":book(a.where(D["agp"],0)),
        "graded_(-z-1)+_x0.5_agit":book(((sig-1).clip(lower=0)*0.5).clip(upper=2).where(D["agit"],0)),
        "graded_(-z-1)+_x0.5":book(((sig-1).clip(lower=0)*0.5).clip(upper=2)),
    }).T
    # deepest falls: book loss days composition
    D["bg"]=D["alloc"]*D["fwd"]
    worst=D[D["bg"]<D["bg"].quantile(0.02)]
    out["worst2%_posgain_by_z_agit"]=worst.groupby(["agit","zb"]).size().unstack()
    out["posgain_sum_by_agit_z"]=D.groupby(["agit","zb"])["bg"].sum().unstack()
    return out
