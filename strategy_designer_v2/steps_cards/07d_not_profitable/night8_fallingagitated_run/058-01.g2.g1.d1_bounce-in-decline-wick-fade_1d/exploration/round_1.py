def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily, per window
    wins = sorted({w for c in data["days"] for w in data["days"][c]}, key=lambda s:int(s[1:]))
    chains=[]; perwin=[]
    for w in wins:
        cols={}
        for c in data["days"]:
            if w in data["days"][c]:
                d=data["days"][c][w].set_index("day")["book_return"]
                cols[c]=d
        df=pd.DataFrame(cols)
        br=df.mean(axis=1).dropna()
        chains.append(pd.DataFrame({"w":w,"r":br.values}))
        perwin.append({"w":w,"days":len(br),"sum":br.sum(),"min_day":br.min()})
    ch=pd.concat(chains,ignore_index=True)
    v=(1+ch.r).cumprod(); peak=v.cummax(); dd=v/peak-1
    ch["dd"]=dd
    i=dd.idxmin(); j=v[:i+1].idxmax()
    out["deepest_dd"]=pd.Series({"dd":dd.min(),"start_w":ch.w[j],"end_w":ch.w[i],"days":i-j})
    out["perwin"]=pd.DataFrame(perwin)
    # worst days distribution
    out["worst10_days"]=ch.nsmallest(10,"r")[["w","r"]].reset_index(drop=True)
    # case level
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change(); r3=cl.pct_change(3)
            sd=r1.rolling(30).std()
            depth=(b.high-cl)/cl/sd
            nxt=cl.shift(-1)/cl-1
            rng=(b.high-b.low)/cl/sd
            r60=cl.pct_change(60) if len(b)>60 else pd.Series(np.nan,index=b.index)
            f=pd.DataFrame({"c":c,"w":w,"r1":r1/sd,"r3":r3/sd,"depth":depth,"nxt":nxt,"fc":b.forecast,
                            "alloc":b.postRebalance_current_allocation,"rng":rng,"r10":cl.pct_change(10)/sd,
                            "uppct":(cl-b.low)/(b.high-b.low)})
            rows.append(f)
    A=pd.concat(rows,ignore_index=True)
    mu=A.groupby("c").nxt.mean()
    A["ex"]=-(A.nxt-A.c.map(mu))
    A["pnl"]=A.alloc*A.nxt
    cs=A[(A.fc<0)].dropna(subset=["nxt"])
    out["cases_n_mean"]=pd.Series({"n":len(cs),"mean_short_ex":cs.ex.mean(),"t":stats.ttest_1samp(cs.ex,0).statistic,
                                   "sum_pnl":cs.pnl.sum(),"mean_alloc":cs.alloc.mean()})
    def grp(col,q=4):
        g=pd.qcut(cs[col].rank(method="first"),q,labels=False)
        return cs.groupby(g).agg(n=("ex","size"),lo=(col,"min"),hi=(col,"max"),mean_ex=("ex","mean"),
                                 sd=("ex","std"),pnl=("pnl","sum"),worst=("ex","min"))
    for col in ["depth","r1","r3","r10","rng","uppct"]:
        out["by_"+col]=grp(col)
    out["by_coin"]=cs.groupby("c").agg(n=("ex","size"),mean_ex=("ex","mean"),pnl=("pnl","sum"),worst=("ex","min"))
    out["by_win"]=cs.groupby("w").agg(n=("ex","size"),mean_ex=("ex","mean"),pnl=("pnl","sum"))
    # same situation outside profile (fc==0, r1>0, r3<0)
    oth=A[(A.fc==0)&(A.r1>0)&(A.r3<0)].dropna(subset=["nxt","depth"])
    out["outside_profile"]=pd.Series({"n":len(oth),"mean_ex":oth.ex.mean(),"t":stats.ttest_1samp(oth.ex,0).statistic})
    # worst cases features
    out["worst15_cases"]=cs.nsmallest(15,"pnl")[["c","w","r1","r3","r10","depth","rng","ex","alloc","pnl"]].reset_index(drop=True)
    return out
