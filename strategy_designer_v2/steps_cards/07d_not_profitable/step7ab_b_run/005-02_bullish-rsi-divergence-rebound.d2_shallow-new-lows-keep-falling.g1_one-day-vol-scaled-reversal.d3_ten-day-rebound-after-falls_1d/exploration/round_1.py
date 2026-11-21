def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    out["coins"] = ",".join(coins)
    # book daily: mean of coins per day within window
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    wins = sorted(D.w.unique(), key=lambda s:int(s[1:]))
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wi"]=bk.w.map(lambda s:int(s[1:])); bk=bk.sort_values(["wi","day"]).dropna()
    s=lambda r: r.mean()/r.std()*np.sqrt(365)
    out["sharpe book / hold"] = f"{s(bk.book_return):.3f} / {s(bk.coin_return):.3f}"
    # drawdown chain
    eq=(1+bk.book_return).cumprod().values; peak=np.maximum.accumulate(eq); ddn=eq/peak-1
    i=ddn.argmin(); j=np.argmax(eq[:i+1]==peak[i])
    out["deepest fall"]=f"{ddn[i]:.3f}, from window {bk.w.iloc[j]} to {bk.w.iloc[i]}, {i-j} days"
    heq=(1+bk.coin_return).cumprod().values; hdd=heq/np.maximum.accumulate(heq)-1
    out["holding deepest fall"]=f"{hdd.min():.3f}"
    out["coin chained return during book's deepest fall"]=f"{heq[i]/heq[j]-1:.3f}"
    yr=eq[-1]**(365/len(eq))-1; out["book yearly"]=f"{yr:.4f}"
    # per window book vs hold
    pw=bk.groupby("wi").agg(book=("book_return",lambda r:(1+r).prod()-1),hold=("coin_return",lambda r:(1+r).prod()-1),
                            bookmin=("book_return","min"))
    out["per window book vs hold"]=pw.round(3)
    # bar-level: allocation, trailing returns
    B=[]
    for c in coins:
        dr_all=[]
        for w,b in bars[c].items():
            b=b.copy(); b["ret1"]=b.close.pct_change(); dr_all.append(b["ret1"])
        mu=pd.concat(dr_all).mean()
        for w,b in bars[c].items():
            b=b.reset_index(drop=True).copy(); cl=b.close
            b["ret1"]=cl.pct_change(); b["nxt"]=cl.shift(-1)/cl-1
            b["fwd10"]=cl.shift(-10)/cl-1
            b["r60"]=cl/cl.shift(60)-1; b["r20"]=cl/cl.shift(20)-1
            b["vol20"]=b.ret1.rolling(20).std()
            b["alloc"]=b.postRebalance_current_allocation
            b["gain"]=b.alloc*b.nxt; b["mkt"]=b.alloc*mu
            b["coin"]=c; b["w"]=w; b["pos"]=np.arange(len(b))
            B.append(b)
    B=pd.concat(B)
    out["mean alloc / share bars long"]=f"{B.alloc.mean():.3f} / {(B.alloc>0.01).mean():.3f}"
    out["bar gain mean, market part, timing"]=f"{B.gain.mean():.6f}, {B.mkt.mean():.6f}, {(B.gain-B.mkt).mean():.6f}"
    # gain by trailing 60d return regime (bar level)
    B["r60q"]=pd.qcut(B.r60,4,labels=["q1low","q2","q3","q4high"])
    g=B.dropna(subset=["r60q","nxt"]).groupby("r60q",observed=True).agg(alloc=("alloc","mean"),gain=("gain","mean"),coin=("nxt","mean"),n=("nxt","size"))
    out["bars by 60d return quartile"]=g.round(5)
    # grid cells
    C=B[(B.pos%10==0)&B.fwd10.notna()].copy()
    drift=C.groupby("coin").fwd10.transform("mean"); C["ex"]=C.fwd10-drift
    P=C[C.forecast>0].copy()
    def tt(x): 
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["pos cells excess by 60d ret quartile"]=P.dropna(subset=["r60q"]).groupby("r60q",observed=True).ex.apply(tt).unstack().round(4)
    out["all cells excess by 60d ret quartile"]=C.dropna(subset=["r60q"]).groupby("r60q",observed=True).ex.apply(tt).unstack().round(4)
    P["fq"]=pd.qcut(P.forecast,3,labels=["f1","f2","f3"])
    out["pos cells by forecast tercile"]=P.groupby("fq",observed=True).ex.apply(tt).unstack().round(4)
    P["up"]=np.where(P.r60>0,"r60up","r60down")
    res={}
    for k,gp in P.dropna(subset=["r60"]).groupby("up"):
        sl=stats.linregress(gp.forecast,gp.ex); res[k]=[len(gp),sl.slope,sl.slope/sl.stderr,gp.ex.mean()]
    out["slope by 60d sign"]=pd.DataFrame(res,index=["n","slope","t","meanex"]).T.round(4)
    vq=pd.qcut(P.vol20/P.groupby("coin").vol20.transform("median"),3,labels=["lowvol","mid","highvol"])
    out["pos cells by vol tercile"]=P.groupby(vq,observed=True).ex.apply(tt).unstack().round(4)
    # trades
    T=pd.concat([t.assign(coin=c) for c in coins for t in data["trades"][c].values()])
    out["trades n, mean net %, win share, mean days"]=f"{len(T)}, {T.net_profit_loss_percent.mean():.3f}, {(T.net_profit_loss_percent>0).mean():.3f}, {T.duration_minutes.mean()/1440:.1f}"
    return out
