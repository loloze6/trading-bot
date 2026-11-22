def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # --- bar-level gain by side and by trend state
    rows = []
    grid = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r1 = cl.shift(-1)/cl - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            hi = cl.rolling(30, min_periods=30).max(); lo = cl.rolling(30, min_periods=30).min()
            width = (hi-lo)/cl
            ret30 = cl/cl.shift(30)-1
            vol = cl.pct_change().rolling(30, min_periods=20).std()
            trend = ret30.abs()/(vol*np.sqrt(30))
            fwd10 = cl.shift(-10)/cl - 1
            df = pd.DataFrame({"coin":c,"w":w,"gain":pos*r1,"pos":pos,"r1":r1,"fc":b["forecast"].astype(float),
                               "width":width,"trend":trend,"ret30":ret30,"fwd10":fwd10,
                               "year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
            grid.append(df.iloc[::10])
    A = pd.concat(rows); G = pd.concat(grid).dropna(subset=["fwd10","fc"])
    mean10 = G.groupby("coin")["fwd10"].transform("mean")
    G["ex"] = G["fwd10"] - mean10
    A["side"] = np.sign(A["pos"])
    out["bar gain by side"] = A.groupby("side")["gain"].agg(["count","mean","sum"])
    # trend terciles
    G["trend_q"] = pd.qcut(G["trend"], 3, labels=["low","mid","high"])
    G["width_q"] = pd.qcut(G["width"], 3, labels=["narrow","mid","wide"])
    def slope(g):
        g = g.dropna(subset=["fc","ex"])
        if len(g) < 30: return pd.Series({"n":len(g)})
        s = stats.linregress(g["fc"], g["ex"])
        return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr,
                          "ex_long":g.loc[g.fc>0,"ex"].mean(),"ex_short":g.loc[g.fc<0,"ex"].mean(),
                          "raw_long":g.loc[g.fc>0,"fwd10"].mean(),"raw_short":g.loc[g.fc<0,"fwd10"].mean()})
    out["slope by trend tercile"] = G.groupby("trend_q").apply(slope)
    out["slope by width tercile"] = G.groupby("width_q").apply(slope)
    out["slope by coin"] = G.groupby("coin").apply(slope)
    out["slope by year"] = G.groupby("year").apply(slope)
    # forecast buckets
    G["fc_b"] = pd.cut(G["fc"], [-21,-15,-8,-2,2,8,15,21])
    out["fwd10 by forecast bucket"] = G.groupby("fc_b")[["ex","fwd10"]].agg(["count","mean"])
    # bar gain by trend tercile & side
    A["trend_q"] = pd.qcut(A["trend"], 3, labels=["low","mid","high"])
    out["bar gain by trend x side"] = A.groupby(["trend_q","side"])["gain"].agg(["count","mean"]).unstack()
    # --- book daily, drawdown
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"]=c; d["w"]=w; D.append(d)
    D = pd.concat(D)
    wins = sorted(D["w"].unique(), key=lambda s:int(s[1:]))
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna().reset_index()
    bk["wi"] = bk["w"].map({w:i for i,w in enumerate(wins)})
    bk = bk.sort_values(["wi","day"])
    out["by window"] = bk.groupby("wi").agg(book=("book_return","sum"),hold=("coin_return","sum"),n=("book_return","count"))
    eq = (1+bk["book_return"]).cumprod().values
    peak = np.maximum.accumulate(eq); dd = eq/peak-1
    i_tr = int(np.argmin(dd)); i_pk = int(np.argmax(eq[:i_tr+1]))
    out["deepest fall"] = pd.Series({"depth":dd[i_tr],"days":i_tr-i_pk,"window_start":bk["wi"].iloc[i_pk],"window_end":bk["wi"].iloc[i_tr],
                                     "coin_sum_in_fall":bk["coin_return"].iloc[i_pk:i_tr+1].sum(),
                                     "book_sum_in_fall":bk["book_return"].iloc[i_pk:i_tr+1].sum()})
    return out
