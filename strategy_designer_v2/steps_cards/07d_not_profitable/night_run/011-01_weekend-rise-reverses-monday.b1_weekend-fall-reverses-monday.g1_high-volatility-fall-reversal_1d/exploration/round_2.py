def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            df=pd.DataFrame({"r":r,"nxt":c.shift(-1)/c-1,
                "a":b["postRebalance_current_allocation"].fillna(0),"f":b["forecast"],
                "reg":b["regime"],"zr":r/r.rolling(20).std(),
                "ret5":c/c.shift(5)-1,"ret3":c/c.shift(3)-1,
                "fee":(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"],
                "w":int(w[1:]),"coin":coin})
            df["gain"]=df.a*df.nxt
            df["ret5prior"]=df.ret5-df.r
            rows.append(df)
    B=pd.concat(rows,ignore_index=True)
    out={}
    out["fee/gain per bar"]=f"fee {B.fee.mean():.6f} gain {B.gain.mean():.6f}"
    act=B[B.a>0.001].dropna(subset=["nxt"])
    x=act.copy(); x["fb"]=pd.qcut(x.f,5,duplicates="drop")
    out["fee by f"]=x.groupby("fb",observed=True).agg(fee=("fee","mean"),gain=("gain","mean"),n=("gain","size")).round(5)
    # zr reversal in all bars, by regime
    A=B.dropna(subset=["nxt","zr"]).copy()
    A["zb"]=pd.cut(A.zr,[-99,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,99])
    out["nxt by zr x regime"]=A.pivot_table(index="zb",columns="reg",values="nxt",aggfunc="mean",observed=True).round(4)
    out["n by zr x regime"]=A.pivot_table(index="zb",columns="reg",values="nxt",aggfunc="size",observed=True)
    # among big falls (zr<-1), by prior 5d return before today
    big=A[A.zr<-1].copy(); big["pb"]=pd.qcut(big.ret5prior,4)
    out["big falls by prior4d"]=big.groupby("pb",observed=True).agg(n=("nxt","size"),nxt=("nxt","mean"),
        t=("nxt",lambda s:s.mean()/s.std()*np.sqrt(len(s))),gain=("gain","mean")).round(4)
    # losing active bars: worst decile of gain
    act2=act.copy(); thr=act2.gain.quantile(0.05)
    L=act2[act2.gain<=thr]
    out["worst5% vs all"]=pd.DataFrame({"worst":[L.zr.mean(),L.ret5prior.mean(),L.a.mean(),L.f.mean(),(L.reg=="mean_reversion").mean()],
        "all":[act2.zr.mean(),act2.ret5prior.mean(),act2.a.mean(),act2.f.mean(),(act2.reg=="mean_reversion").mean()]},
        index=["zr","prior4d","alloc","f","share mr"]).round(4)
    out["gain sum by coin"]=act.groupby("coin").agg(gain=("gain","sum"),fee=("fee","sum"),n=("gain","size")).round(4)
    # hold beyond: nxt 2-day after big fall
    return out
