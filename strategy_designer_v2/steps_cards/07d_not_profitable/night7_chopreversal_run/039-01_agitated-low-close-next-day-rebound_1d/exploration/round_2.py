def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            rng=(b.high-b.low).replace(0,np.nan)
            b["cl"]=(b.high-b.close)/rng
            b["r1"]=b.close.shift(-1)/b.close-1
            b["r2"]=b.close.shift(-2)/b.close-1
            b["ret1d"]=b.close/b.close.shift(1)-1
            b["rngpct"]=rng/b.close
            b["tr60"]=b.close/b.close.shift(60)-1
            b["pos"]=b.postRebalance_current_allocation
            b["agit"]=b.regime!="chop"
            b["coin"]=coin; b["w"]=w; b["i"]=np.arange(len(b))
            b["vol20"]=b.ret1d.rolling(20).std()
            rows.append(b[["coin","w","i","cl","r1","r2","ret1d","rngpct","tr60","pos","agit","forecast","vol20"]])
    A=pd.concat(rows,ignore_index=True)
    A["x1"]=A.r1-A.r1.mean()
    A["z1"]=A.x1/A.vol20
    out={}
    ag=A[A.agit].copy()
    out["abs_pos_by_agit"]=A.groupby("agit").pos.apply(lambda s:s.abs().mean())
    out["abs_pos_active_quant"]=A[A.pos.abs()>1e-9].pos.abs().describe()
    ag["clq"]=pd.cut(ag.cl,[-0.01,0.15,0.85,1.01],labels=["high","mid","low"])
    ag["d1"]=pd.cut(ag.ret1d,[-9,-0.03,0.03,9],labels=["down","flat","up"])
    out["agit_x1_clq_by_day1"]=ag.groupby(["d1","clq"]).x1.agg(["count","mean",lambda s:stats.ttest_1samp(s.dropna(),0).statistic]).round(5)
    ag["rq"]=pd.qcut(ag.rngpct,3,labels=["small","mid","large"])
    out["agit_x1_clq_by_range"]=ag.groupby(["rq","clq"]).x1.agg(["count","mean"]).unstack(1)
    out["agit_z1_clq_by_range"]=ag.groupby(["rq","clq"]).z1.mean().unstack(1)
    ag["tr"]=pd.cut(ag.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    out["agit_x1_clq_by_trend60"]=ag.groupby(["tr","clq"]).x1.agg(["count","mean"]).unstack(1)
    # signed excess for extreme cl in agitated: low -> long, high -> short
    ex=ag[ag.clq!="mid"].copy()
    ex["s"]=np.where(ex.clq=="low",1,-1)
    out["extreme_signed_x1"]=pd.Series({"n":len(ex),"mean":(ex.s*ex.x1).mean(),"t":stats.ttest_1samp((ex.s*ex.x1).dropna(),0).statistic,
        "mean2d":(ex.s*(ex.r2-A.r2.mean())).mean(),"share_bars":len(ex)/len(ag)})
    mid=ag[ag.clq=="mid"]
    out["mid_signed_by_fc"]=pd.Series({"n":len(mid),"mean":(np.sign(mid.forecast)*mid.x1).mean(),"t":stats.ttest_1samp((np.sign(mid.forecast)*mid.x1).dropna(),0).statistic})
    # slope agitated vs calm
    for k,g in A.groupby("agit"):
        g=g.dropna(subset=["cl","x1"])
        r=stats.linregress(g.cl,g.x1)
        out[f"slope_agit_{k}"]=pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(g)})
    return out
