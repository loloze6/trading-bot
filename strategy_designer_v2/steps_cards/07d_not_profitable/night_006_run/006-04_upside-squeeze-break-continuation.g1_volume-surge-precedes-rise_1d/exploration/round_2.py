def explore(data):
    import pandas as pd, numpy as np
    days=data["days"]; bars=data["bars"]
    coins=list(days.keys())
    wn=lambda w:int(w[1:])
    # daily book per coin with state at prior close
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy(); b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            cl=b.close
            b["r30"]=cl/cl.shift(30)-1; b["r1"]=cl.pct_change(); b["r5"]=cl/cl.shift(5)-1
            b["nxt"]=cl.shift(-1)/cl-1
            b["gain"]=b.postRebalance_current_allocation*b.nxt
            b["coin"]=c; b["w"]=w; b["wn"]=wn(w)
            rows.append(b[["coin","w","wn","r30","r1","r5","nxt","gain","postRebalance_current_allocation","forecast"]])
    X=pd.concat(rows).dropna(subset=["nxt"])
    X["al"]=X.postRebalance_current_allocation
    act=X[X.al>0.01].copy()
    out={}
    act["r30q"]=pd.qcut(act.r30,5,labels=False)
    out["gain_by_r30"]=act.groupby("r30q").agg(n=("gain","size"),r30lo=("r30","min"),r30hi=("r30","max"),gain=("gain","mean"),
        sumgain=("gain","sum"),al=("al","mean"),nxt=("nxt","mean"),t=("nxt",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    act["r1q"]=pd.qcut(act.r1,5,labels=False)
    out["gain_by_r1"]=act.groupby("r1q").agg(n=("gain","size"),lo=("r1","min"),hi=("r1","max"),gain=("gain","mean"),sumgain=("gain","sum"),nxt=("nxt","mean"))
    # drawdown windows 14-16: book loss share by r30 sign
    dd=act[act.wn.isin([14,15,16,3,17])]
    out["dd_windows_by_r30sign"]=dd.groupby([dd.wn,dd.r30>0]).agg(n=("gain","size"),sumgain=("gain","sum"),al=("al","mean")).reset_index()
    out["all_by_r30sign"]=act.groupby(act.r30>0).agg(n=("gain","size"),mean=("gain","mean"),sd=("gain","std"),sumgain=("gain","sum"))
    # interaction r30 sign x r1 sign
    out["r30_x_r1"]=act.groupby([act.r30>0,act.r1>0]).agg(n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean")).reset_index()
    # 3-day grid excess by r30 sign within f>0
    g=[]
    for c in coins:
        for w,b in bars[c].items():
            cl=b.close.values; f=b.forecast.values
            for i in range(0,len(b)-3,3):
                if i>=30: g.append(dict(coin=c,f=f[i],fwd=cl[i+3]/cl[i]-1,r30=cl[i]/cl[i-30]-1))
    G=pd.DataFrame(g); G["ex"]=G.fwd-G.groupby("coin").fwd.transform("mean")
    from scipy import stats
    res={}
    for s,sub in G.groupby(G.r30>0):
        sl=stats.linregress(sub.f,sub.ex); res[str(s)]=pd.Series({"n":len(sub),"npos":(sub.f>0).sum(),"slope":sl.slope,"t":sl.slope/sl.stderr,"fwmean":(sub.ex*sub.f).sum()/sub.f.sum()})
    out["slope_by_r30sign"]=pd.DataFrame(res)
    # simulated: daily book with alloc zeroed when r30<0, Calmar approx (per-coin mean per day not possible w/o day; use per bar per window mean)
    return out
