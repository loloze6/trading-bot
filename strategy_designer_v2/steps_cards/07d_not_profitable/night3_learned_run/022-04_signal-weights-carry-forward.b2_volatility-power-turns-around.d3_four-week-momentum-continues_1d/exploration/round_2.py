def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]; coins = list(bars.keys())
    rows=[]; grid=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy()
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["ret1"]=b["close"].shift(-1)/b["close"]-1
            p=b["postRebalance_current_allocation"]
            b["gl"]=p.clip(lower=0)*b["ret1"]; b["gs"]=p.clip(upper=0)*b["ret1"]; b["g"]=p*b["ret1"]
            b["coin"]=c; b["wn"]=int(w[1:])
            rows.append(b[["day","coin","wn","gl","gs","g"]])
            b["r28"]=b["close"]/b["close"].shift(28)-1
            b["f5"]=b["close"].shift(-5)/b["close"]-1
            b["vr"]=b["close"].pct_change().rolling(20).std()/b["close"].pct_change().rolling(60).std()
            gg=b.iloc[::5]; grid.append(gg[["coin","wn","r28","f5","forecast","vr"]])
    B=pd.concat(rows).dropna(subset=["g"])
    G=pd.concat(grid).dropna(subset=["f5","r28"])
    G["f5d"]=G["f5"]-G.groupby("coin")["f5"].transform("mean")
    dd=B.groupby(["wn","day"])[["gl","gs","g"]].mean().sort_index()
    def stats(s):
        e=(1+s).cumprod(); mdd=(e/e.cummax()-1).min()
        yr=(e.iloc[-1])**(365/len(s))-1
        return pd.Series({"mean_bps":s.mean()*1e4,"sharpe":s.mean()/s.std()*np.sqrt(365),"yearly":yr,"maxdd":mdd,"calmar":yr/-mdd})
    cf=pd.DataFrame({k:stats(dd[k]) for k in ["g","gl","gs"]})
    # per window group short vs long
    dd2=dd.reset_index(); dd2["grp"]=pd.cut(dd2["wn"],[0,1,10,24],labels=["w1","w2-w10","w11-w24"])
    pg=dd2.groupby("grp")[["gl","gs"]].mean()*1e4
    # asymmetric response: forecast quintile -> demeaned f5, n, t
    G["fq"]=pd.qcut(G["forecast"],6,labels=False,duplicates="drop")
    def tt(s): return pd.Series({"n":len(s),"mean_pct":s.mean()*100,"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    q=G.groupby("fq")["f5d"].apply(tt).unstack()
    q["mean_r28"]=G.groupby("fq")["r28"].mean()
    # slope separately on each side
    from scipy import stats as st
    out={}
    for nm,sub in [("rise",G[G["r28"]>0]),("fall",G[G["r28"]<0])]:
        r=st.linregress(sub["r28"],sub["f5d"]); out[nm]=pd.Series({"n":len(sub),"slope":r.slope,"t":r.slope/r.stderr})
    # falls side by vol ratio
    G["vrq"]=pd.qcut(G["vr"],3,labels=False)
    fv=G[G["r28"]<0].groupby("vrq")["f5d"].apply(tt).unstack()
    return {"counterfactual_before_cost":cf.round(4),"per_group_bps":pg.round(2),"by_forecast_sixth":q.round(3),
            "slope_by_side":pd.DataFrame(out).round(4),"falls_by_volratio":fv.round(3)}
