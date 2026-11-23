def explore(data):
    import pandas as pd, numpy as np
    out = {}
    recs=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            sun=(ts.dt.dayofweek==6).values
            vr=(r.rolling(20).std()/r.rolling(60).std()).values
            ret20=(cl/cl.shift(20)-1).values
            ret60=(cl/cl.shift(60)-1).values
            alloc=b["postRebalance_current_allocation"].fillna(0).values
            n=len(b); last=-1; sv=np.full(n,np.nan); sr=np.full(n,np.nan); s20=np.full(n,np.nan); s60=np.full(n,np.nan)
            for i in range(n):
                if sun[i]: last=i
                if last>=0:
                    sv[i]=vr[last]; sr[i]=r.values[last]; s20[i]=ret20[last]; s60[i]=ret60[last]
            nxt=np.append(cl.values[1:]/cl.values[:-1]-1,np.nan)
            recs.append(pd.DataFrame({"coin":c,"wn":int(w[1:]),"i":np.arange(n),"day":ts.dt.floor("D").values,
                "alloc":alloc,"nxt":nxt,"sv":sv,"sr":sr,"s20":s20,"s60":s60,"hold":r.values}))
    R=pd.concat(recs)
    R=R.dropna(subset=["nxt"])
    def book(mask,name,scale=None):
        a=np.where(mask,R["alloc"],0.0)
        if scale is not None: a=a*scale
        da=np.abs(np.diff(np.concatenate([[0],a])))
        g=a*R["nxt"].values-0.0011*da
        X=pd.DataFrame({"wn":R["wn"].values,"day":R["day"].values,"g":g})
        Bk=X.groupby(["wn","day"])["g"].mean().sort_index()
        v=(1+Bk).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(Bk))-1
        sh=Bk.mean()/Bk.std()*np.sqrt(365)
        w2=(1+Bk.loc[2]).prod()-1
        return {"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":sh,"w2_ret":w2,"days_in_pos":(a!=0).mean()}
    allm=np.ones(len(R),bool)
    res={}
    res["actual_approx"]=book(allm,"all")
    res["vr_gt_0.9"]=book(R["sv"].values>0.9,"")
    res["vr_gt_1"]=book(R["sv"].values>1.0,"")
    res["fall_gt_1.7pct"]=book(R["sr"].values<-0.0172,"")
    res["ret20_lt_-10pct"]=book(R["s20"].values<-0.10,"")
    res["vr_gt_0.9_and_fall"]=book((R["sv"].values>0.9)&(R["sr"].values<-0.0172),"")
    sc=np.clip(np.nan_to_num(R["sv"].values,nan=0)-0.7,0,None)/0.3
    res["scaled_by_vr_minus_0.7"]=book(allm,"",scale=np.minimum(sc,2))
    out["books"]=pd.DataFrame(res).T.round(4)
    # worst days of the actual book: what was held, coin state
    a=R["alloc"].values; g=a*R["nxt"].values
    X=R.assign(g=g)
    Bk=X.groupby(["wn","day"]).agg(g=("g","mean"),coin=("nxt","mean"),inpos=("alloc",lambda x:(x>0).mean()),
                                   sv=("sv","mean"),s60=("s60","mean"),sr=("sr","mean")).reset_index()
    out["worst10_days"]=Bk.sort_values("g").head(10).drop(columns="day").round(4).reset_index(drop=True)
    return out
