def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    h = 5
    cases = []
    for c in bars:
        fr = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            fr.append((b["close"].shift(-h)/b["close"]-1).iloc[::h].dropna())
        mu = pd.concat(fr).mean(); sd = pd.concat(fr).std()
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            f = b["close"].shift(-h)/b["close"]-1
            r30 = b["close"]/b["close"].shift(30)-1
            hi = b["high"].rolling(30).max(); lo = b["low"].rolling(30).min()
            nmr = (b["close"]-b["close"].shift(30)).abs()/(hi-lo)
            g = pd.DataFrame({"f": f, "fc": b["forecast"], "r30": r30, "nmr": nmr, "reg": b["regime"],
                              "year": pd.to_datetime(b["timestamp"]).dt.year}).iloc[::h].dropna()
            g["u"] = g["f"]-mu; g["us"] = g["u"]/sd; g["coin"]=c; g["window"]=w
            cases.append(g)
    G = pd.concat(cases)
    G["side"] = np.where(G["r30"]>0, "up", "down")
    G["dm"] = G["u"]*np.sign(G["r30"])
    def summ(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # graded by r30 quintile within side, all bars
    for s in ["up","down"]:
        g = G[G.side==s].copy()
        g["q"] = pd.qcut(g["r30"].abs(), 5, labels=False)
        out[f"{s}: dm by |r30| quintile (all bars)"] = g.groupby("q")["dm"].apply(summ).unstack().round(4)
        g["nq"] = pd.qcut(g["nmr"], 4, labels=False)
        out[f"{s}: dm by nmr quartile"] = g.groupby("nq")["dm"].apply(summ).unstack().round(4)
        out[f"{s}: dm by year"] = g.groupby("year")["dm"].apply(summ).unstack().round(4)
        # slope of u on r30 within side
        sl = stats.linregress(g["r30"], g["u"])
        out[f"{s}: slope u on r30"] = pd.Series({"slope": sl.slope, "t": sl.slope/sl.stderr, "n": len(g)})
    # leave top windows out for up-side
    g = G[G.side=="up"]
    out["up dm leaving out w21,w6,w19"] = summ(g[~g.window.isin(["w21","w6","w19"])]["dm"]).round(4)
    g = G[G.side=="down"]
    out["down dm leaving out w21,w6,w19,w20"] = summ(g[~g.window.isin(["w21","w6","w19","w20"])]["dm"]).round(4)
    # book: long vs short exposure days
    D=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            r=b["close"].shift(-1)/b["close"]-1
            D.append(pd.DataFrame({"g": b["postRebalance_current_allocation"]*r, "al": b["postRebalance_current_allocation"], "window":w,
                                   "year":pd.to_datetime(b["timestamp"]).dt.year}).dropna())
    D=pd.concat(D)
    out["long-bar gain by year"] = D[D.al>0].groupby("year")["g"].agg(["sum","mean","count"]).round(4)
    out["short-bar gain by year"] = D[D.al<0].groupby("year")["g"].agg(["sum","mean","count"]).round(4)
    return out
