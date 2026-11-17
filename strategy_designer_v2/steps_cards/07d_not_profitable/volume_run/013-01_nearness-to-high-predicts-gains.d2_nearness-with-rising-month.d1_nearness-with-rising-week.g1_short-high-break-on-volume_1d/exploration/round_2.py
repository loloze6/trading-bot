def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]; a = b["postRebalance_current_allocation"]
            r1 = c.shift(-1)/c - 1
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            dist = c/c.rolling(20).max()-1
            vr = b["volume"]/b["volume"].rolling(30).mean()
            ret60 = c/c.shift(60)-1
            ret20 = c/c.shift(20)-1
            f7 = c.shift(-7)/c-1
            df = pd.DataFrame({"coin":coin,"w":w,"i":range(len(b)),"a":a,"r1":r1,"fee":fee,
                "dist":dist,"vr":vr,"ret60":ret60,"ret20":ret20,"f7":f7,
                "nh":b["debug_info.components.near_high.post_pipeline_value"],
                "vv":b["debug_info.components.vol_ratio.post_pipeline_value"],"f":b["forecast"]})
            df["grid"] = (df["i"]%7==0)
            rows.append(df)
    B = pd.concat(rows, ignore_index=True)
    B["g"]=B.a*B.r1
    B["glong"]=B.a.clip(lower=0)*B.r1
    B["feelong"]=np.where(B.a>0,B.fee,0)
    cm = B.groupby("coin")["r1"].mean()
    B["mkt"]=B.a*B.coin.map(cm)
    # per-bar decomposition by side
    B["side"]=np.sign(B.a)
    out["side_decomp"]=B.groupby("side").agg(gain=("g","sum"),mkt=("mkt","sum"),fee=("fee","sum")).assign(timing=lambda x:x.gain-x.mkt)
    # long-only counterfactual book daily (approx at bar level, mean over coins per w,i)
    P = B.groupby(["w","i"]).agg(g=("g","mean"),gl=("glong","mean"),fe=("fee","mean"),fl=("feelong","mean")).reset_index()
    P["wn"]=P.w.str[1:].astype(int); P=P.sort_values(["wn","i"])
    res={}
    for nm,x in [("book",P.g-P.fe),("longonly",P.gl-P.fl)]:
        x=x.fillna(0); eq=(1+x).cumprod(); dd=(eq/eq.cummax()-1).min()
        yr=eq.iloc[-1]**(365/len(x))-1
        res[nm]={"mean":x.mean(),"sharpe":x.mean()/x.std()*np.sqrt(365),"maxdd":dd,"calmar":yr/-dd}
    out["counterfactual"]=pd.DataFrame(res).T
    # 7d grid: f7 by component quintiles
    G=B[B.grid & B.f7.notna()].copy()
    G["ex"]=G.f7-G.coin.map(G.groupby("coin").f7.mean())
    for col in ["nh","vv","f"]:
        q=pd.qcut(G[col],5,labels=False,duplicates="drop")
        out["ex7_by_"+col]=G.groupby(q).agg(n=("ex","size"),ex=("ex","mean"),f7=("f7","mean"))
    # shorts by 60d trend sign
    S=B[B.side==-1].copy()
    S["tr"]=pd.qcut(S.ret60,4,labels=False)
    out["short_by_ret60q"]=S.groupby("tr").agg(n=("g","size"),g=("g","mean"),r1=("r1","mean"),ret60=("ret60","mean"))
    L=B[B.side==1].copy(); L["tr"]=pd.qcut(L.ret60,4,labels=False)
    out["long_by_ret60q"]=L.groupby("tr").agg(n=("g","size"),g=("g","mean"),r1=("r1","mean"),ret60=("ret60","mean"))
    # slope t of ex7 on f within ret60>0 vs <0
    for nm,m in [("up60",G.ret60>0),("dn60",G.ret60<=0)]:
        s=G[m].dropna(subset=["f","ex"]); r=stats.linregress(s.f,s.ex)
        out["slope_"+nm]=pd.Series({"n":len(s),"slope":r.slope,"t":r.slope/r.stderr})
    return out
