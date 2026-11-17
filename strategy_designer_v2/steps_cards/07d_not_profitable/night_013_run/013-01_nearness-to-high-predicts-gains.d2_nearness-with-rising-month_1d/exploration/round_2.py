def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out={}
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["nr"]=b.close.shift(-1)/b.close-1
            b["al"]=b.postRebalance_current_allocation
            b["g"]=b.al*b.nr
            b["r30"]=b.close/b.close.shift(30)-1
            b["r7p"]=b.close/b.close.shift(7)-1
            b["vol20"]=b.close.pct_change().rolling(20).std()
            b["nh"]=b["debug_info.components.near_high.last_history_value"]
            b["rs"]=b["debug_info.components.ret30_size.post_pipeline_value"]
            b["np"]=b["debug_info.components.near_high.post_pipeline_value"]
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            b["coin"]=c; b["w"]=w; b["wn"]=int(w[1:])
            rows.append(b)
    B=pd.concat(rows)
    B["side"]=np.sign(B.al).map({1:"long",-1:"short",0:"flat"})
    # coin mean daily return over all windows
    cm=B.groupby("coin").nr.mean()
    B["mkt"]=B.al*B.coin.map(cm)
    B["tim"]=B.g-B.mkt
    out["decomp_by_side"]=B.groupby("side").agg(n=("g","size"),g_sum_share=("g","sum"),mkt=("mkt","sum"),tim=("tim","sum"))
    tr=B[(B.regime=="trending")&(B.side=="short")].dropna(subset=["nh"])
    out["short_bars_near_stats"]=pd.Series({"nh_mean":tr.nh.mean(),"np_mean":tr.np.mean(),"rs_mean":tr.rs.mean(),"r30_mean":tr.r30.mean()})
    # book daily with drawdown episodes
    dd=B.groupby(["wn","day"]).agg(g=("g","mean"),cr=("nr","mean"),al=("al","mean"),
        long_share=("side",lambda s:(s=="long").mean()),short_share=("side",lambda s:(s=="short").mean()),
        vol=("vol20","mean"),r30=("r30","mean"),r7p=("r7p","mean")).dropna(subset=["g"]).reset_index()
    eq=(1+dd.g).cumprod(); dd["dd"]=(eq/eq.cummax()-1).values
    dd["in_dd"]=dd.dd< -0.07
    out["dd_vs_not"]=dd.groupby("in_dd").agg(n=("g","size"),g=("g","mean"),cr=("cr","mean"),al=("al","mean"),longsh=("long_share","mean"),shortsh=("short_share","mean"),vol=("vol","mean"),r30=("r30","mean"),r7p=("r7p","mean"))
    # gain by prior 7d return and by vol state for long bars
    L=B[B.side=="long"].dropna(subset=["r7p","vol20"])
    L["vq"]=pd.qcut(L.vol20,5,labels=False)
    L["pq"]=pd.qcut(L.r7p,5,labels=False)
    out["long_by_vol"]=L.groupby("vq").agg(n=("g","size"),vol=("vol20","mean"),g=("g","mean"),nr=("nr","mean"),al=("al","mean"))
    out["long_by_r7p"]=L.groupby("pq").agg(n=("g","size"),r7p=("r7p","mean"),g=("g","mean"),nr=("nr","mean"))
    # 7-day grid: forward return by nearness pooled all bars (incl unknown) - nearness recomputed
    G=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy(); b["f7"]=b.close.shift(-7)/b.close-1
            b["r30"]=b.close/b.close.shift(30)-1
            b["vol20"]=b.close.pct_change().rolling(20).std()
            b["coin"]=c; G.append(b.iloc[::7][["coin","f7","r30","vol20","regime","debug_info.components.near_high.last_history_value"]])
    G=pd.concat(G).dropna(subset=["f7"])
    G["ex"]=G.f7-G.coin.map(G.groupby("coin").f7.mean())
    gt=G[G.regime=="trending"].dropna(subset=["debug_info.components.near_high.last_history_value","vol20"])
    x=gt["debug_info.components.near_high.last_history_value"]
    s=stats.linregress(x,gt.ex)
    out["near_slope"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(gt)})
    gt["vq"]=pd.qcut(gt.vol20,3,labels=False)
    res={}
    for q,g in gt.groupby("vq"):
        s=stats.linregress(g["debug_info.components.near_high.last_history_value"],g.ex)
        res[q]=(s.slope,s.slope/s.stderr,len(g),g.ex.mean())
    out["near_slope_by_vol"]=pd.DataFrame(res,index=["slope","t","n","ex"]).T
    return out
