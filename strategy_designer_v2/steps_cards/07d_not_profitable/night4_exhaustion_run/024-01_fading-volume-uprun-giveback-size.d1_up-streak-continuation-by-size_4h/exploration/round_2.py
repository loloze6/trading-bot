def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # book day returns by coin's trailing 30-day return (known at previous day's close)
    rows=[]
    for c in coins:
        for w,d in days[c].items():
            t=d[["day","book_return","coin_return","close"]].copy()
            t["ret30_prev"]=(t["close"]/t["close"].shift(30)-1).shift(1)
            t["coin"]=c; t["wn"]=int(w[1:])
            b=bars[c][w].copy()
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            al=b.groupby("day")["postRebalance_current_allocation"].mean().rename("alloc").reset_index()
            t["day"]=pd.to_datetime(t["day"])
            t=t.merge(al,on="day",how="left")
            rows.append(t)
    D=pd.concat(rows).dropna(subset=["book_return","ret30_prev"])
    D["state"]=pd.qcut(D["ret30_prev"].rank(method="first"),4,labels=False)
    out["coin-day by 30d return quartile"]=D.groupby("state").agg(r30=("ret30_prev","mean"),book=("book_return","mean"),coin=("coin_return","mean"),alloc=("alloc","mean"),book_sd=("book_return","std"),n=("book_return","size"),share_neg_days=("book_return",lambda x:(x<0).mean()))
    D["up"]=D["ret30_prev"]>0
    out["coin-day by sign of 30d return"]=D.groupby("up").agg(book=("book_return","mean"),coin=("coin_return","mean"),alloc=("alloc","mean"),n=("book_return","size"))
    # what book would be if only in when ret30_prev>0 (diagnostic for the falls)
    D["book_up"]=np.where(D["up"],D["book_return"],0.0)
    bk=D.groupby(["wn","day"]).agg(b=("book_return","mean"),bu=("book_up","mean")).reset_index().sort_values(["wn","day"])
    res={}
    for col in ["b","bu"]:
        r=bk[col].values; eq=np.cumprod(1+r); mdd=(eq/np.maximum.accumulate(eq)-1).min()
        yr=eq[-1]**(365/len(r))-1
        res[col]={"mean":r.mean(),"sharpe":r.mean()/r.std()*np.sqrt(365),"mdd":mdd,"calmar":yr/abs(mdd)}
    out["diagnostic book all vs only-up-30d"]=pd.DataFrame(res).T
    # grid cases: ex return by ret30 graded, t-stats, and ret30 x vratio
    cases=[]
    for c in coins:
        allr=[]
        for w,b in bars[c].items():
            cl=b["close"].values; idx=np.arange(0,len(cl)-18,18); allr.append(cl[idx+18]/cl[idx]-1)
        drift=np.concatenate(allr).mean()
        for w,b in bars[c].items():
            cl=b["close"].values; v=b["volume"].values; f=b["forecast"].values
            for i in range(180,len(cl)-18,18):
                if not f[i]>0: continue
                L=0
                while i-L>=1 and cl[i-L]>cl[i-L-1]: L+=1
                cases.append({"coin":c,"ex":cl[i+18]/cl[i]-1-drift,"ret30":cl[i]/cl[i-180]-1,
                              "vr":v[i-L+1:i+1].mean()/v[i-180:i].mean() if L>0 else np.nan})
    C=pd.DataFrame(cases)
    C["q"]=pd.qcut(C["ret30"].rank(method="first"),5,labels=False)
    out["ex by ret30 quintile"]=C.groupby("q").agg(r30=("ret30","mean"),ex=("ex","mean"),n=("ex","size"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    a=C[C.ret30>0]["ex"]; bb=C[C.ret30<=0]["ex"]
    out["welch up30 minus down30"]=f"diff {a.mean()-bb.mean():.5f} t {stats.ttest_ind(a,bb,equal_var=False).statistic:.2f} n {len(a)}/{len(bb)}"
    out["corr ret30 ex (spearman)"]=f"{stats.spearmanr(C.ret30,C.ex).correlation:.4f}"
    C2=C.dropna(subset=["vr"])
    C2["vq"]=pd.qcut(C2["vr"].rank(method="first"),2,labels=["vlow","vhigh"])
    C2["up"]=np.where(C2.ret30>0,"up30","down30")
    out["ex by trend x volume"]=C2.groupby(["up","vq"]).agg(ex=("ex","mean"),n=("ex","size"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["ex up30 by coin"]=C[C.ret30>0].groupby("coin").agg(ex=("ex","mean"),n=("ex","size"))
    out["ex down30 by coin"]=C[C.ret30<=0].groupby("coin").agg(ex=("ex","mean"),n=("ex","size"))
    return out
