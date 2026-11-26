def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    feats = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            cl = b["close"]
            b["tr60"] = cl/cl.shift(60)-1
            b["r5"] = cl.shift(-5)/cl-1
            b["r1f"] = cl.shift(-1)/cl-1
            b["ret20p"] = cl/cl.shift(20)-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["r1f"]
            b["dchg"] = b["pos"].diff().abs().fillna(b["pos"].abs())
            b["coin"] = c; b["wn"] = int(w[1:]); b["i"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["calm"] = b["regime"] != "chop"
            feats.append(b[["coin","wn","i","day","forecast","tr60","r5","r1f","ret20p","pos","gain","dchg","calm"]])
    F = pd.concat(feats)
    F["trend"] = pd.cut(F["tr60"], [-np.inf,-0.1,0.1,np.inf], labels=["falling","choppy","rising"])
    # trend at the bar the position was entered: use trend of the bar (proxy)
    cost = 0.0019/2
    def book(mask, name):
        g = np.where(mask, F["gain"] - F["dchg"]*cost, 0.0)
        tmp = F[["wn","day"]].copy(); tmp["g"] = g
        tmp = tmp[~np.isnan(tmp["g"])]
        bd = tmp.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        v = (1+bd["g"]).cumprod()
        mdd = (v/v.cummax()-1).min()
        yrs = len(bd)/365
        yr = v.iloc[-1]**(1/yrs)-1
        sh = bd["g"].mean()/bd["g"].std()*np.sqrt(365)
        return pd.Series({"sharpe":sh,"yearly":yr,"maxdd":mdd,"calmar":yr/abs(mdd),
                          "worst_window_chain":bd.groupby("wn")["g"].apply(lambda s:(1+s).prod()-1).min()})
    allm = np.ones(len(F), bool)
    rising = (F["trend"]=="rising").values
    notfall = (F["trend"]!="falling").values
    up20 = (F["ret20p"]>0).values
    out["book_variants"] = pd.DataFrame({"all":book(allm,"all"),"rising":book(rising,"r"),
        "not_falling":book(notfall,"nf"),"ret20_pos":book(up20,"u20")})
    G = F[(F["i"]%5==0)&F["calm"]].dropna(subset=["r5","tr60"]).copy()
    drift = F[F["i"]%5==0].groupby("coin")["r5"].mean()
    G["ex"] = G["r5"]-G["coin"].map(drift)
    G["sig"] = G["forecast"]>0
    res = {}
    for tr in ["falling","choppy","rising"]:
        for s in [True, False]:
            x = G[(G["trend"]==tr)&(G["sig"]==s)]
            dsum = x.groupby("day")["ex"].sum()
            n = x["ex"].count()
            t = x["ex"].mean()/(dsum.std(ddof=1)*np.sqrt(len(dsum))/n) if len(dsum)>2 else np.nan
            res[(tr,s)] = {"mean":x["ex"].mean(),"n":n,"days":len(dsum),"t_day":t}
    out["grid_trend_sig_t"] = pd.DataFrame(res).T
    S = G[G["sig"]&(G["trend"]=="rising")]
    out["rising_slope"] = pd.Series(stats.linregress(S["forecast"], S["ex"])._asdict())
    out["rising_by_window"] = G[G["trend"]=="rising"].groupby(["wn","sig"])["ex"].mean().unstack()
    return out
