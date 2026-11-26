def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    cost = 0.0011
    G = []; R = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            fc = b["forecast"].fillna(0)
            a = b["postRebalance_current_allocation"].fillna(0)
            r20 = cl/cl.shift(20)-1
            r60 = cl/cl.shift(60)-1
            r1n = cl.shift(-1)/cl-1
            f3 = cl.shift(-3)/cl-1
            idx = np.arange(0,len(b),3)
            G.append(pd.DataFrame({"coin":c,"w":w,"ts":b["timestamp"].iloc[idx].values,"f3":f3.iloc[idx].values,
                                   "fc":fc.iloc[idx].values,"r20":r20.iloc[idx].values,"r60":r60.iloc[idx].values}))
            var = {"base":a, "r20_pos":a*((r20>0)|r20.isna()), "r60_rise":a*(r60>0.10),
                   "r60_notfall":a*(r60>=-0.10)}
            for k,p in var.items():
                p = p.fillna(0)
                g = p*r1n - cost*p.diff().abs().fillna(p.abs())
                R.append(pd.DataFrame({"w":w,"ts":b["timestamp"],"v":k,"r":g.values,"pos":(p.abs()>0.01).values}))
    out = {}
    R = pd.concat(R).dropna(subset=["r"])
    res=[]; loo=[]
    for k,x in R.groupby("v"):
        d = x.groupby(["w","ts"])["r"].mean().reset_index()
        d["wn"]=d["w"].str[1:].astype(int); d=d.sort_values(["wn","ts"])
        def cal(dd):
            v=(1+dd["r"]).cumprod(); m=(v/v.cummax()-1).min(); y=v.iloc[-1]**(365/len(dd))-1
            return y, m
        y,m = cal(d)
        res.append({"v":k,"sharpe":d["r"].mean()/d["r"].std()*np.sqrt(365),"yearly":y,"mdd":m,"calmar":y/abs(m),"inpos":x["pos"].mean()})
        lw = []
        for w0 in d["w"].unique():
            dd=d[d["w"]!=w0]; lw.append(dd["r"].mean()/dd["r"].std()*np.sqrt(365))
        loo.append({"v":k,"min_loo_sharpe":min(lw),"pos_windows":(d.groupby("w")["r"].mean()>0).sum(),"n_windows":d["w"].nunique()})
    out["variants"]=pd.DataFrame(res).set_index("v")
    out["variants_loo"]=pd.DataFrame(loo).set_index("v")
    G = pd.concat(G).dropna(subset=["f3"])
    drift=G.groupby("coin")["f3"].mean(); G["ex"]=G["f3"]-G["coin"].map(drift)
    G["inp"]=G["fc"]>0
    G["r60b"]=pd.cut(G["r60"],[-9,-0.10,0.10,9],labels=["fall","chop","rise"])
    def agg(x):
        n=len(x)
        dsum=x.groupby("ts")["ex"].sum(); nd=len(dsum)
        tday = x["ex"].mean()/ (dsum.std()*np.sqrt(nd)/n) if nd>2 else np.nan
        return pd.Series({"n":n,"days":nd,"ex":x["ex"].mean(),"t_day":tday})
    out["inp_by_r60"]=G[G["inp"]].dropna(subset=["r60b"]).groupby("r60b").apply(agg)
    out["outp_by_r60"]=G[~G["inp"]].dropna(subset=["r60b"]).groupby("r60b").apply(agg)
    sl={}
    for k,x in G[G["inp"]].dropna(subset=["r60b"]).groupby("r60b"):
        s=stats.linregress(x["fc"],x["ex"]); sl[str(k)]=pd.Series({"n":len(x),"slope":s.slope,"t":s.slope/s.stderr})
    out["slope_fc_by_r60_inp"]=pd.DataFrame(sl).T
    x=G[G["inp"]&(G["r60b"]=="rise")].copy()
    x["fcq"]=pd.qcut(x["fc"],3,labels=["lo","mid","hi"])
    out["rise_calm_by_fcq"]=x.groupby("fcq").apply(agg)
    return out
