def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change(); r3=cl.pct_change(3)
            sd=r1.rolling(30).std()
            f=pd.DataFrame({"c":c,"w":w,"i":b.index,"ts":b.timestamp,"r1":r1/sd,"r3":r3/sd,
                            "depth":(b.high-cl)/cl/sd,"nxt":cl.shift(-1)/cl-1,"fc":b.forecast,
                            "reg":b.regime.astype(str),"alloc":b.postRebalance_current_allocation,
                            "r10":cl.pct_change(10)/sd,"rng":(b.high-b.low)/cl/sd})
            rows.append(f)
    A=pd.concat(rows,ignore_index=True)
    mu=A.groupby("c").nxt.mean()
    A["ex"]=-(A.nxt-A.c.map(mu))
    A["day"]=pd.to_datetime(A.ts).dt.floor("D")
    out["regime_counts"]=A.reg.value_counts()
    inp=A[(A.reg!="chop")].dropna(subset=["nxt","r3","r1"])
    inp=inp.assign(r3b=pd.cut(inp.r3,[-99,-1.17,-0.65,0,99]),up=inp.r1>0)
    out["inprofile_r3_by_upday"]=inp.groupby(["r3b","up"]).ex.agg(["size","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    cs=A[A.fc<0].dropna(subset=["nxt","r3","depth"]).copy()
    cs["deep3"]=cs.r3<-0.65
    cs["dq"]=pd.qcut(cs.depth.rank(method="first"),2,labels=["lowdepth","hidepth"])
    out["cases_deep3_x_depth"]=cs.groupby(["deep3","dq"]).ex.agg(["size","mean","std"])
    cs["r10b"]=pd.cut(cs.r10,[-99,-5,-3,0,99])
    out["cases_r10b"]=cs.groupby("r10b").agg(n=("ex","size"),mean=("ex","mean"),pnl=(" alloc".strip(),"size"))
    out["cases_r10b_x_deep3"]=cs.groupby(["r10b","deep3"]).ex.agg(["size","mean"])
    # approx books for filters: daily pnl = mean over coins of alloc*nxt - fee
    def book(mask,name):
        s=A.copy(); s["a"]=np.where(mask(s),s.alloc,0.0)
        s["a"]=s["a"].fillna(0)
        s["prev"]=s.groupby(["c","w"]).a.shift(1).fillna(0)
        s["g"]=s.a*s.nxt.fillna(0)-0.0019/2*(s.a-s.prev).abs()
        res=[]
        for w in sorted(s.w.unique(),key=lambda x:int(x[1:])):
            sw=s[s.w==w].pivot_table(index="day",columns="c",values="g",aggfunc="sum")
            res.append(sw.mean(axis=1))
        r=pd.concat(res).reset_index(drop=True)
        v=(1+r).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(r))-1
        return pd.Series({"yr":yr,"dd":dd,"calmar":yr/-dd,"sharpe":r.mean()/r.std()*np.sqrt(365),"active":(s.a!=0).sum()})
    out["book_all"]=book(lambda s:s.fc<0,"all")
    out["book_deep3"]=book(lambda s:(s.fc<0)&(s.r3<-0.65),"d3")
    out["book_not_r10crash"]=book(lambda s:(s.fc<0)&(s.r10>-5),"r10")
    out["book_hirng"]=book(lambda s:(s.fc<0)&(s.rng>1.07),"rng")
    out["book_deep3_hirng"]=book(lambda s:(s.fc<0)&(s.r3<-0.65)&(s.rng>1.07),"both")
    # condition alone: high range, in profile, not signal
    q=inp.assign(hr=inp.rng>1.07,sig=(inp.r1>0)&(inp.r3<0))
    out["inprofile_rng_by_sig"]=q.groupby(["hr","sig"]).ex.agg(["size","mean"])
    # drawdown cases w14/w15
    dd=cs[cs.w.isin(["w14","w15"])]
    out["dd_cases"]=dd.groupby(dd.ex<0).agg(n=("ex","size"),r3=("r3","mean"),r10=("r10","mean"),depth=("depth","mean"),rng=("rng","mean"),alloc=("alloc","mean"))
    return out
