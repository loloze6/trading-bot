def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows=[]
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b=b.copy()
            r=b["close"].pct_change()
            b["ret1"]=b["close"].shift(-1)/b["close"]-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["vol20"]=r.rolling(20).std()
            b["tr20"]=b["close"]/b["close"].shift(20)-1
            b["tr60"]=b["close"]/b["close"].shift(60)-1
            b["ma100"]=b["close"]/b["close"].rolling(100).mean()-1
            b["fwd10"]=b["close"].shift(-10)/b["close"]-1
            b["idx"]=np.arange(len(b))
            b["coin"]=coin; b["win"]=w
            sh=b.get("debug_info.components.since_high.last_history_value")
            b["since"]=sh if sh is not None else np.nan
            rows.append(b[["coin","win","idx","forecast","pos","ret1","vol20","tr20","tr60","ma100","fwd10","since"]])
    B=pd.concat(rows)
    out["pos_vs_forecast"]=B.groupby(pd.cut(B.forecast,[-0.1,0.01,5,10,15,19.99,20])).pos.agg(["count","mean"])
    out["since_desc"]=B.since.describe()
    A=B[B.pos.abs()>1e-9].dropna(subset=["ret1"]).copy(); A["pnl"]=A.pos*A.ret1
    A["mab"]=pd.cut(A.ma100,[-10,-0.2,0,0.2,0.5,100])
    out["pnl_by_ma100"]=A.groupby("mab").pnl.agg(["count","mean","sum","std"])
    A["t60"]=pd.cut(A.tr60,[-10,-0.2,0,0.3,100])
    out["pnl_by_tr60"]=A.groupby("t60").pnl.agg(["count","mean","sum"])
    # non-overlapping 10-bar fwd return on active bars by ma100 sign
    N=B[(B.idx%10==0)&(B.pos>1e-9)].dropna(subset=["fwd10","ma100"])
    res={}
    for name,g in [("above_ma100",N[N.ma100>0]),("below_ma100",N[N.ma100<=0]),("all",N)]:
        x=g.fwd10*g.pos; res[name]={"n":len(x),"mean":x.mean(),"t":stats.ttest_1samp(x,0).statistic,"q05":x.quantile(0.05)}
    out["nonovl10_ma100"]=pd.DataFrame(res).T
    # by forecast bucket nonoverlap
    N["fb"]=pd.cut(N.forecast,[0,8,15,20])
    out["nonovl10_fc"]=N.groupby("fb").apply(lambda g: pd.Series({"n":len(g),"mean":g.fwd10.mean(),"t":stats.ttest_1samp(g.fwd10,0).statistic}))
    # losing days share from: active pnl tail
    out["worst5pct_days_ma100"]=A[A.pnl<A.pnl.quantile(0.05)].groupby("mab").size()
    return out
