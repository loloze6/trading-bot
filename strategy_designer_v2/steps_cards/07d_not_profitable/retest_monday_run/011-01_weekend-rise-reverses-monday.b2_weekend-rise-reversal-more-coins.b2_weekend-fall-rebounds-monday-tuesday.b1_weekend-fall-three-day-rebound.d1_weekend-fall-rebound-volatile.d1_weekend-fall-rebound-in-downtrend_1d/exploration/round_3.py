def explore(data):
    import numpy as np, pandas as pd
    out = {}
    ncoin = {}
    rows = []
    for c, ws in data["bars"].items():
        for wn, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values; n = len(b)
            s = pd.Series(cl)
            r1 = s.pct_change().values; r20 = s.pct_change(20).values
            lr = np.log(s).diff(); vol20 = lr.rolling(20).std().values
            mx20 = s.rolling(20).max().values
            fc = b["forecast"].values; al = b["postRebalance_current_allocation"].values
            for i in range(0, n-3):
                if ts[i].dayofweek == 6:
                    ncoin[(int(wn[1:]), ts[i].normalize())] = ncoin.get((int(wn[1:]), ts[i].normalize()), 0) + 1
                    if fc[i] > 0:
                        rows.append(dict(coin=c, wn=int(wn[1:]), wk=ts[i].normalize(), r1=r1[i], r20=r20[i], vol20=vol20[i],
                                         dfm=cl[i]/mx20[i]-1, fwd=cl[i+3]/cl[i]-1, alloc=al[i], fc=fc[i]))
    C = pd.DataFrame(rows)
    C["nc"] = [ncoin[(a, b)] for a, b in zip(C["wn"], C["wk"])]
    C["z1"] = C["r1"]/C["vol20"]
    def book(sel, name, size="alloc"):
        x = C[sel].copy()
        x["p"] = x[size]*(x["fwd"] - 0.0022)
        wk = x.groupby(["wn","wk"]).agg(p=("p","sum"), nc=("nc","first"))
        wk["r"] = wk["p"]/wk["nc"]
        wk = wk.sort_index()
        v = (1+wk["r"]).cumprod(); dd = (v/v.cummax()-1).min()
        yrs = 7.94
        yr = v.iloc[-1]**(1/yrs)-1
        wmin = wk.groupby(level=0)["r"].sum()
        return dict(cases=int(sel.sum()), mean_fwd=x["fwd"].mean(), yearly=yr, maxdd=dd, calmar=yr/abs(dd) if dd < 0 else np.nan,
                    worst_window=wmin.min(), w2=wmin.get(2, np.nan))
    res = {}
    res["all"] = book(C["fc"] > 0, "all")
    res["strong"] = book((C["dfm"] < -0.2) & (C["r1"] < -0.02), "strong")
    res["dfm_lt_-0.15"] = book(C["dfm"] < -0.15, "d15")
    res["z1_lt_-0.25"] = book(C["z1"] < -0.25, "z")
    res["dfm15_z25"] = book((C["dfm"] < -0.15) & (C["z1"] < -0.25), "dz")
    res["fc_gt_10"] = book(C["fc"] > 10.7, "fc")
    out["books"] = pd.DataFrame(res).T
    # graded by dfm on Sunday weekend falls, unusual over coin drift approx
    x = C.dropna(subset=["dfm"]).copy()
    x["b"] = pd.qcut(x["dfm"], 5)
    g = x.groupby("b", observed=True)["fwd"].agg(["count","mean","std"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["dfm_grade"] = g.reset_index().astype({"b": str})
    # strong case in window 2
    s = C[(C["dfm"] < -0.2) & (C["r1"] < -0.02)]
    out["w2_strong_vs_all"] = pd.DataFrame({"all": C[C["wn"]==2]["fwd"].describe(), "strong": s[s["wn"]==2]["fwd"].describe()})
    return out
