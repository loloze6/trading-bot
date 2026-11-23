def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    # book daily returns: per window, per day, mean over coins
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().reset_index().sort_values(["wn","day"])
    v = (1+B["book_return"]).cumprod()
    peak = v.cummax(); ddn = v/peak-1
    B["dd"] = ddn.values
    # deepest fall: trough and peak
    ti = ddn.idxmin() if False else int(np.argmin(ddn.values))
    pi = int(np.argmax(v.values[:ti+1]))
    out["deepest fall"] = pd.Series({"depth": ddn.values[ti], "days": ti-pi,
        "peak_window": B["wn"].iloc[pi], "trough_window": B["wn"].iloc[ti],
        "book ret in fall": v.values[ti]/v.values[pi]-1,
        "coins ret in fall": (1+B["coin_return"].iloc[pi+1:ti+1]).prod()-1})
    # per window book & coin
    g = B.groupby("wn")
    out["by window"] = pd.DataFrame({"book": g["book_return"].apply(lambda x:(1+x).prod()-1),
        "coins": g["coin_return"].apply(lambda x:(1+x).prod()-1),
        "min_dd": g["dd"].min()}).round(3)
    # per-bar features per coin: trend 60d, vol ratio, and forward 3d return grid
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.pct_change()
            f = b["debug_info.components.rise5.post_pipeline_value"]
            alloc = b["postRebalance_current_allocation"]
            ret60 = cl/cl.shift(60)-1
            ma50 = cl/cl.rolling(50).mean()-1
            vol20 = r1.rolling(20).std(); vol120 = r1.rolling(120).std()
            fwd3 = cl.shift(-3)/cl-1
            gain = alloc*(cl.shift(-1)/cl-1)
            df = pd.DataFrame({"coin":c,"w":w,"pos":np.arange(len(b)),"f":f,"alloc":alloc,
                "ret60":ret60,"ma50":ma50,"volr":vol20/vol120,"fwd3":fwd3,"gain":gain})
            recs.append(df)
    X = pd.concat(recs)
    drift = X[X.pos%3==0].groupby("coin")["fwd3"].mean()
    X["ex3"] = X["fwd3"] - X["coin"].map(drift)
    G = X[(X.pos%3==0)].dropna(subset=["fwd3"])
    def summ(s):
        s = s.dropna()
        return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    tab = {}
    for name, cond in [("ma50>0", G.ma50>0), ("ma50<=0", G.ma50<=0), ("ret60>0",G.ret60>0),("ret60<=0",G.ret60<=0),
                       ("volr>1.2",G.volr>1.2),("volr<=1.2",G.volr<=1.2)]:
        for sname, sc in [("signal", G.f>0), ("nosig", G.f<=0)]:
            tab[f"{name}|{sname}"] = summ(G.loc[cond & sc, "fwd3"])
    out["fwd3 by state (total move)"] = pd.DataFrame(tab).T.round(4)
    # daily position gain by state (all bars held)
    H = X[X.alloc.abs()>0].dropna(subset=["gain"])
    tab2 = {}
    for name, cond in [("ma50>0", H.ma50>0), ("ma50<=0", H.ma50<=0),("ret60>0",H.ret60>0),("ret60<=0",H.ret60<=0),("volr>1.2",H.volr>1.2),("volr<=1.2",H.volr<=1.2)]:
        s = H.loc[cond,"gain"]
        tab2[name] = pd.Series({"n":len(s),"mean":s.mean(),"std":s.std(),"sum":s.sum(),"worst5%":s.quantile(0.05)})
    out["held gain by state"] = pd.DataFrame(tab2).T.round(5)
    # forecast quintile vs fwd3
    S = G[G.f>0].copy()
    S["q"] = pd.qcut(S.f, 4, labels=False, duplicates="drop")
    out["fwd3 by forecast quartile"] = S.groupby("q")["ex3"].agg(["count","mean","std"]).round(4)
    return out
