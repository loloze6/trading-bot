def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            b["r1"] = cl.pct_change()
            b["nxt"] = cl.shift(-1)/cl-1
            b["loc"] = (cl-b["low"])/(b["high"]-b["low"])
            b["rngratio"] = (b["high"]-b["low"])/(b["high"]-b["low"]).rolling(20,min_periods=10).mean()
            b["ret5"] = cl/cl.shift(5)-1
            b["ret5pre"] = cl.shift(1)/cl.shift(6)-1
            b["prevr"] = b["r1"].shift(1)
            b["upstreak"] = (b["r1"]>0).astype(int).groupby(((b["r1"]<=0)).cumsum()).cumsum()
            b["coin"]=c; b["w"]=w; b["wn"]=int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["inprof"] = b["regime"]!="chop"
            b["sig"] = b["postRebalance_current_allocation"]<-0.01
            rows.append(b)
    A = pd.concat(rows).dropna(subset=["nxt"])
    mu = A.groupby("coin")["nxt"].mean()
    A["un"] = -(A["nxt"]-A["coin"].map(mu))   # short-side unusual move
    P = A[A["inprof"]]
    out["profile bars"] = pd.Series({"n_prof":len(P),"n_sig":int(P["sig"].sum()),"prof_nosig_mean":P.loc[~P["sig"],"un"].mean(),"sig_mean":P.loc[P["sig"],"un"].mean()})
    def cmp(name, cond):
        r = {}
        for lab, m in [("cond&sig", cond & P["sig"]), ("cond&nosig", cond & ~P["sig"]), ("notcond&sig", ~cond & P["sig"])]:
            x = P.loc[m,"un"].dropna()
            r[lab] = {"n":len(x),"mean":x.mean(),"t":(x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan),"tail<-5%":(x<-0.05).mean()}
        return pd.DataFrame(r).T
    out["first up day (prev day down)"] = cmp("first", P["prevr"]<=0)
    out["prior 5d fall < -10% (before the up day)"] = cmp("ret5pre", P["ret5pre"]< -0.10)
    out["prior 5d fall < 0"] = cmp("ret5pre0", P["ret5pre"]< 0)
    out["loc<0.95"] = cmp("loc", P["loc"]<0.95)
    # grading within signal, by prior 5-day fall
    S = P[P["sig"]].copy()
    out["sig by ret5pre q"] = S.groupby(pd.qcut(S["ret5pre"],4),observed=True)["un"].agg(["size","mean","median"])
    out["sig by prevr q"] = S.groupby(pd.qcut(S["prevr"],4),observed=True)["un"].agg(["size","mean","median"])
    # approximate book: per day, sum of alloc*pnl over coins / coins present
    ncoin = A.groupby(["wn","day"])["coin"].nunique()
    S["bc"] = (-S["postRebalance_current_allocation"])*(-S["nxt"])
    def book(mask, lab):
        x = S[mask].groupby(["wn","day"])["bc"].sum()
        r = (x / ncoin.reindex(x.index)).reindex(ncoin.index).fillna(0).sort_index()
        v = (1+r).cumprod(); dd = (v/v.cummax()-1).min()
        yrs = len(r)/365/ (ncoin.index.get_level_values(0).nunique()/ncoin.index.get_level_values(0).nunique())
        ny = len(ncoin)/365
        yr = v.iloc[-1]**(1/ny)-1
        return {"n":int(mask.sum()),"total":v.iloc[-1]-1,"maxdd":dd,"yearly":yr,"calmar":yr/abs(dd) if dd<0 else np.nan}
    out["approx book"] = pd.DataFrame({
        "all": book(S["sig"], "all"),
        "first up day": book(S["prevr"]<=0, "f"),
        "ret5pre<0": book(S["ret5pre"]<0, "r"),
        "first&ret5pre<0": book((S["prevr"]<=0)&(S["ret5pre"]<0), "fr"),
        "loc<0.95": book(S["loc"]<0.95, "l"),
    }).T
    return out
