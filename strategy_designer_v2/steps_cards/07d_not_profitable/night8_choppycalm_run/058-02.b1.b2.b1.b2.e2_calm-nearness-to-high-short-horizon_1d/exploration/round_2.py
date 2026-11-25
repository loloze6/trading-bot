def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    cost = 0.0011
    R = []
    G = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1n = cl.shift(-1)/cl-1
            fc = b["forecast"].fillna(0)
            a = b["postRebalance_current_allocation"].fillna(0)
            r20 = cl/cl.shift(20)-1
            r10 = cl/cl.shift(10)-1
            hi20 = b["high"].rolling(20).max()
            dist = 1-cl/hi20
            var = {}
            var["base"] = a
            var["no_r20fall"] = a*((r20>=-0.10)|r20.isna())
            var["r20_pos"] = a*((r20>0)|r20.isna())
            var["graded_fc"] = a*np.clip((fc-10)/10,0,1)*2
            var["top_fc12"] = a*(fc>=12)
            var["graded_and_r20pos"] = a*np.clip((fc-10)/10,0,1)*2*((r20>0)|r20.isna())
            for k,p in var.items():
                p = p.fillna(0)
                g = p*r1n - cost*p.diff().abs().fillna(p.abs())
                R.append(pd.DataFrame({"w":w,"i":np.arange(len(b)),"ts":b["timestamp"],"v":k,"r":g.values,"pos":(p.abs()>0.01).values}))
            f3 = cl.shift(-3)/cl-1
            idx = np.arange(0,len(b),3)
            G.append(pd.DataFrame({"coin":c,"w":w,"f3":f3.iloc[idx].values,"fc":fc.iloc[idx].values,
                                   "r20":r20.iloc[idx].values,"r10":r10.iloc[idx].values,"dist":dist.iloc[idx].values}))
    R = pd.concat(R).dropna(subset=["r"])
    out = {}
    res = []
    for k, x in R.groupby("v"):
        d = x.groupby(["w","ts"])["r"].mean().reset_index()
        d["wn"] = d["w"].str[1:].astype(int)
        d = d.sort_values(["wn","ts"])
        v = (1+d["r"]).cumprod()
        mdd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(d))-1
        res.append({"v":k,"sharpe":d["r"].mean()/d["r"].std()*np.sqrt(365),"yearly":yr,"mdd":mdd,
                    "calmar":yr/abs(mdd),"inpos":x["pos"].mean(),"mean":d["r"].mean()})
    out["variants_gross_minus_cost"] = pd.DataFrame(res).set_index("v")
    G = pd.concat(G).dropna(subset=["f3","r20"])
    drift = G.groupby("coin")["f3"].mean()
    G["ex"] = G["f3"]-G["coin"].map(drift)
    G["inp"] = G["fc"]>0
    def agg(x):
        return pd.Series({"n":len(x),"ex":x["ex"].mean(),"t":x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    G["r20pos"] = G["r20"]>0
    G["fcq"] = pd.qcut(G["fc"].where(G["inp"]),3,labels=["lo","mid","hi"])
    out["inp_by_r20pos_fcq"] = G[G["inp"]].groupby(["r20pos","fcq"]).apply(agg)
    out["outp_by_r20pos"] = G[~G["inp"]].groupby("r20pos").apply(agg)
    out["all_by_r20pos"] = G.groupby("r20pos").apply(agg)
    # slope of ex on fc within r20pos subsets (in profile)
    sl = {}
    for k, x in G[G["inp"]].groupby("r20pos"):
        s = stats.linregress(x["fc"], x["ex"]); sl[str(k)] = pd.Series({"n":len(x),"slope":s.slope,"t":s.slope/s.stderr})
    out["slope_fc_by_r20pos"] = pd.DataFrame(sl).T
    G["dq"] = pd.qcut(G["dist"].where(G["inp"]),4,labels=["near","q2","q3","far"])
    out["inp_by_dist_q"] = G[G["inp"]].groupby("dq").apply(agg)
    return out
