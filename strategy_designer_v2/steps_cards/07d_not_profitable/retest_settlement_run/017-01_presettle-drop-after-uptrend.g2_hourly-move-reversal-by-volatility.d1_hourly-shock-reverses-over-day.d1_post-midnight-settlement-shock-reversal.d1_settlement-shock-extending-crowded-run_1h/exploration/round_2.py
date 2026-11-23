import pandas as pd, numpy as np

def explore(data):
    out = {}
    rows=[]; ctrl=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values); ts = pd.to_datetime(b["timestamp"])
            r1 = cl.pct_change(); vol24 = r1.rolling(24).std(); vol7d = r1.rolling(168).std()
            p23 = cl.shift(1)/cl.shift(24)-1; p7d = cl/cl.shift(168)-1
            fwd = cl.shift(-24)/cl-1
            f = b["forecast"].values; al = b["postRebalance_current_allocation"].values
            hr = ts.dt.hour.values
            for i in range(170, len(b)-24):
                if hr[i]!=0: continue
                if not (vol24[i]>0 and vol7d[i]>0): continue
                rec = {"coin":c,"w":int(w[1:]),"day":ts[i].floor("D"),"year":ts[i].year,
                       "h1z":r1[i]/vol24[i],"p23":p23[i],"p7d":p7d[i],"vr":vol24[i]/vol7d[i],
                       "vol7d":vol7d[i],"fwd":fwd[i],"fc":f[i],"alloc":al[i]}
                rows.append(rec)
    A = pd.DataFrame(rows).dropna(subset=["fwd","p23"])
    A["aligned"] = np.sign(A["h1z"])==np.sign(A["p23"])
    A["fade"] = -np.sign(A["h1z"])*A["fwd"]
    # vol-ratio quartile edges from aligned cases
    C = A[A["aligned"]&(A["fc"]!=0)].copy()
    q = C["vr"].quantile([.25,.5,.75]).values
    A["vrq"] = np.digitize(A["vr"], q)
    def s(g): return pd.Series({"n":len(g),"mean":g.mean(),"t":g.mean()/g.std()*np.sqrt(len(g)),"sd":g.std()})
    out["fade_by_vrq_aligned_vs_not"] = A.groupby(["aligned","vrq"])["fade"].apply(s).unstack()
    # vol level quartile (vol7d) within coin
    A["v7q"] = A.groupby("coin")["vol7d"].transform(lambda x: pd.qcut(x,4,labels=False))
    C = A[A["aligned"]&(A["fc"]!=0)].copy()
    C["side"]=np.sign(C["fc"]); C["contrib"]=C["alloc"]*C["fwd"]
    out["case_by_vol7d_q"] = C.groupby("v7q")["fade"].apply(s).unstack()
    out["contrib_by_vol7d_q"] = C.groupby("v7q")["contrib"].apply(s).unstack()
    out["absalloc_by_vol7d_q"] = C.groupby("v7q")["alloc"].apply(lambda x: x.abs().mean())
    # proxy book: per (w,day) mean over coins of contrib (0 if no case), chained
    def proxy(mask):
        X = A[["coin","w","day"]].copy()
        X["c"] = 0.0
        sel = A["aligned"]&(A["fc"]!=0)&mask
        X.loc[sel,"c"] = (A.loc[sel,"alloc"]*A.loc[sel,"fwd"]).values
        P = X.groupby(["w","day"])["c"].mean().sort_index()
        v = (1+P).cumprod(); dd = (v/v.cummax()-1).min()
        yrs = len(P)/365
        yr = v.iloc[-1]**(1/yrs)-1
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":P.mean()/P.std()*np.sqrt(365),"share_cases":sel.sum()})
    T = {}
    T["all"] = proxy(pd.Series(True,index=A.index))
    T["long_only"] = proxy(A["fc"]>0)
    T["short_only"] = proxy(A["fc"]<0)
    T["drop_vr_q0q1"] = proxy(A["vrq"]>=2)
    T["drop_vol7d_top"] = proxy(A["v7q"]<3)
    T["drop_vol7d_low"] = proxy(A["v7q"]>0)
    T["absh1z_gt_median"] = proxy(A["h1z"].abs()>C["h1z"].abs().median())
    out["proxy_books"] = pd.DataFrame(T).T
    # in deepest fall (w11-w14) cases
    F = C[(C["w"]>=11)&(C["w"]<=14)]
    out["fall_w11_14_by_side"] = F.groupby("side")["contrib"].apply(s).unstack()
    out["fall_w11_14_by_v7q"] = F.groupby("v7q")["contrib"].apply(s).unstack()
    F2 = C[(C["w"]>=5)&(C["w"]<=6)]
    out["fall_w5_6_by_side"] = F2.groupby("side")["contrib"].apply(s).unstack()
    out["fall_w5_6_by_vrq"] = F2.groupby(pd.cut(F2["vr"],[0,*q,99],labels=False))["contrib"].apply(s).unstack()
    return out
