def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            nxt=c.shift(-1)/c-1
            sgn=np.sign(r).shift(1).fillna(0).values
            rv=r.shift(1).fillna(0).values
            dn=[];cum=[];cd=0;cf=0.0
            for s,x in zip(sgn,rv):
                if s<0: cd+=1; cf=(1+cf)*(1+x)-1
                else: cd=0; cf=0.0
                dn.append(cd);cum.append(cf)
            vol=r.rolling(20).std()
            tr60=c/c.shift(60)-1
            df=pd.DataFrame({"coin":coin,"w":w,"ts":b["timestamp"],"r":r,"nxt":nxt,"dn":dn,
                "cumfall":cum,"vol":vol,"tr60":tr60,"inprof":(b["regime"]!="chop"),
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["r","nxt"])
    d["ex"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    def summ(g):
        def f(x):
            s=x.groupby("ts")["ex"].sum(); n=len(x); m=x["ex"].mean()
            se=s.std(ddof=1)*np.sqrt(len(s))/n if len(s)>1 else np.nan
            return pd.Series({"n":n,"days":len(s),"mean_ex%":100*m,"t":m/se if se else np.nan})
        return g.apply(f)
    out={}
    U=d[(d.r>0)&(d.dn>=1)].copy()
    U["fallz"]=-U.cumfall/U.vol
    U["retr"]=U.r/(-U.cumfall)
    P=U[U.inprof].copy(); O=U[~U.inprof].copy()
    P["fq"]=pd.qcut(P.fallz,4,labels=False,duplicates="drop")
    out["prof_upafterdown_by_runfall_z_q"]=summ(P.groupby("fq"))
    P["rq"]=pd.qcut(P.retr,4,labels=False,duplicates="drop")
    out["prof_upafterdown_by_retracement_q"]=summ(P.groupby("rq"))
    O["fq"]=pd.qcut(O.fallz,4,labels=False,duplicates="drop")
    out["out_upafterdown_by_runfall_z_q"]=summ(O.groupby("fq"))
    O["trb"]=pd.cut(O.tr60,[-10,-0.1,0.1,100],labels=["falling","choppy","rising"])
    O["dnb"]=pd.cut(O.dn,[0,1,2,30],labels=["1","2","3+"])
    out["out_upafterdown_by_trend_x_run"]=summ(O.dropna(subset=["trb"]).groupby(["trb","dnb"]))
    A=d.copy(); A["trb"]=pd.cut(A.tr60,[-10,-0.1,0.1,100],labels=["falling","choppy","rising"])
    A["dir"]=np.where(A.r>0,"up","down")
    A["dnb"]=pd.cut(A.dn,[-1,0,1,30],labels=["0","1","2+"])
    out["all_trend_x_dir_x_run"]=summ(A.dropna(subset=["trb"]).groupby(["trb","dir","dnb"]))
    # book: in-position days by coin and windows
    pos=d[d.alloc<0]
    out["book_short_by_coin"]=summ(pos.groupby("coin"))
    return out
