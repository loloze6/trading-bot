def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]["XMRUSD"]
    rows = []
    wl = list(bars.keys())
    for i, (w, b) in enumerate(bars.items()):
        b = b.copy().reset_index(drop=True)
        c = b["close"]
        r = c.pct_change()
        vol = r.rolling(30, min_periods=20).std()
        rng = (b["high"]-b["low"]).replace(0, np.nan)
        d = pd.DataFrame({"w": w, "half": "early" if i < len(wl)//2 else "late",
                          "r": r, "z": r/vol, "vol": vol,
                          "n1": c.shift(-1)/c-1, "n2": c.shift(-2)/c-1, "n3": c.shift(-3)/c-1,
                          "clv": (c-b["low"])/rng,
                          "dfh": (b["high"]-c)/c/vol,   # distance from high in usual moves
                          "dfl": (c-b["low"])/c/vol,
                          "rngz": (b["high"]-b["low"])/c/vol,
                          "volu": b["volume"]/b["volume"].rolling(30,min_periods=10).mean(),
                          "yr": pd.to_datetime(b["timestamp"]).dt.year,
                          "pos": np.arange(len(b)),
                          "fc": b["forecast"]})
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["ex1"] = D["n1"] - D["n1"].mean()
    D["s"] = 0.5 - D["clv"]   # positive when close near low
    def summ(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def ols(df, ycol, xcols):
        df = df.dropna(subset=[ycol]+xcols)
        X = np.column_stack([np.ones(len(df))]+[df[x].values for x in xcols])
        y = df[ycol].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X@beta
        s2 = res@res/(len(y)-X.shape[1])
        se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return pd.Series(dict({"n": len(y)}, **{f"b_{x}": beta[k+1] for k,x in enumerate(xcols)}, **{f"t_{x}": beta[k+1]/se[k+1] for k,x in enumerate(xcols)}))
    out["reg_clv_alone"] = ols(D, "ex1", ["s"])
    out["reg_clv_and_z"] = ols(D, "ex1", ["s", "z"])
    out["reg_dfh_dfl"] = ols(D, "ex1", ["dfh", "dfl", "z"])
    out["reg_clv_by_year"] = D.groupby("yr").apply(lambda g: ols(g, "ex1", ["s", "z"]))
    out["reg_clv_by_half"] = D.groupby("half").apply(lambda g: ols(g, "ex1", ["s", "z"]))
    # clv within z sign
    D["zs"] = np.where(D["z"] < 0, "down", "up")
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False)
    out["clv_x_zsign"] = D.groupby(["zs", "clvq"]).apply(summ).unstack(0)
    # on days the book is flat (forecast 0) - new info?
    out["clv_when_book_flat"] = D[D["fc"] <= 0].groupby("clvq").apply(summ)
    # clv with range size
    D["rq"] = pd.qcut(D["rngz"], 3, labels=["narrow","mid","wide"])
    out["clv_x_range"] = D.groupby(["rq", "clvq"]).apply(summ)["mean%"].unstack(0)
    out["reg_clv_by_range"] = D.groupby("rq").apply(lambda g: ols(g, "ex1", ["s"]))
    # horizon 2/3 non-overlap
    for h in [2, 3]:
        G = D[D["pos"] % h == 0].copy()
        G["ex"] = G[f"n{h}"] - G[f"n{h}"].mean()
        out[f"reg_clv_h{h}_grid"] = ols(G, "ex", ["s", "z"])
    # day-clustered size for top/bottom quintile: one coin so days = cases
    lo = D[D["clvq"] == 0]["ex1"].dropna(); hi = D[D["clvq"] == 4]["ex1"].dropna()
    out["welch_low_minus_high"] = pd.Series({"diff%": 100*(lo.mean()-hi.mean()), "t": stats.ttest_ind(lo, hi, equal_var=False).statistic,
                                             "usual_move%": 100*D["n1"].std(), "strength_low": lo.mean()/D["n1"].std()})
    return out
