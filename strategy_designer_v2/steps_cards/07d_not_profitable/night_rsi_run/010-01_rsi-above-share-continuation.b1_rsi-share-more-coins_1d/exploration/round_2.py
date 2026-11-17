def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    g = []; A = []
    for c in bars:
        for w, df in bars[c].items():
            d = df.reset_index(drop=True).copy()
            d["f14"] = d["close"].shift(-14)/d["close"] - 1
            d["ret90"] = d["close"]/d["close"].shift(90) - 1
            d["ma100"] = d["close"].rolling(100, min_periods=60).mean()
            d["trend"] = np.where(d["close"] > d["ma100"], "up", np.where(d["close"] < d["ma100"], "down", None))
            d["r1"] = d["close"].shift(-1)/d["close"] - 1
            d["pos"] = d["postRebalance_current_allocation"]
            d["gain"] = d["pos"]*d["r1"]
            d["coin"] = c; d["w"] = w
            A.append(d[["coin","w","pos","r1","gain","trend","ret90"]])
            s = d.iloc[::14].dropna(subset=["f14"])
            g.append(s[["coin","forecast","f14","trend","ret90"]])
    G = pd.concat(g)
    G["ex"] = G["f14"] - G.groupby("coin")["f14"].transform("mean")
    G["fb"] = pd.cut(G["forecast"], [-21,-10,-3,3,10,21])
    G2 = G.dropna(subset=["trend"])
    out["fwd14ex_by_trend_forecast"] = G2.groupby(["trend","fb"], observed=True)["ex"].agg(["count","mean"]).unstack(0)
    res = {}
    for t, s in G2.groupby("trend"):
        s = s.dropna(subset=["forecast","ex"])
        lr = stats.linregress(s["forecast"], s["ex"])
        res[t] = {"n": len(s), "slope": lr.slope, "t": lr.slope/lr.stderr}
    out["slope_by_trend"] = pd.DataFrame(res).T
    B = pd.concat(A).dropna(subset=["r1"])
    B["side"] = np.sign(B["pos"])
    B2 = B.dropna(subset=["trend"])
    out["gain_by_trend_side"] = B2.groupby(["trend","side"]).agg(n=("gain","size"), gain=("gain","mean"), r1=("r1","mean")).reset_index()
    # drawdowns of the pooled book (mean across coins per day, chained by window)
    D = pd.concat([days[c][w].assign(w=w, coin=c) for c in days for w in days[c]])
    P = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"] = P["w"].str[1:].astype(int)
    P = P.sort_values(["wn","day"]).dropna()
    eq = (1+P["book_return"]).cumprod(); dd = eq/eq.cummax()-1
    P["dd"] = dd.values
    out["dd_stats"] = pd.Series({"maxdd": dd.min(), "yearly": eq.iloc[-1]**(365/len(P))-1})
    out["dd_by_window_min"] = P.groupby("wn")["dd"].min()
    return out
