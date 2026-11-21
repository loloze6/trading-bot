def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["days"].keys())
    cases = []; drift = {}
    for k in coins:
        allr = []
        for w, bars in data["bars"][k].items():
            bars = bars.reset_index(drop=True)
            cl = bars.close.values; hi = bars.high.values; lo = bars.low.values
            r18 = np.full(len(cl), np.nan); r18[:-18] = cl[18:]/cl[:-18]-1
            allr.append(r18[::18])
            pmax = pd.Series(hi).shift(1).rolling(12).max().values
            rng = (hi-lo)/cl
            r7 = pd.Series(rng).rolling(42).mean().values; r60 = pd.Series(rng).rolling(360).mean().values
            ret7 = np.r_[np.full(42, np.nan), cl[42:]/cl[:-42]-1]
            al = bars.postRebalance_current_allocation.values
            sma = pd.Series(cl).rolling(180).mean().values
            idx = np.arange(len(cl))
            df = pd.DataFrame({"brk": cl > pmax, "cell": idx//18, "r18": r18, "q": r60/r7,
                "str": (cl-pmax)/cl/r7, "ret7": ret7, "al": al, "above30d": cl/sma-1})
            df = df[df.brk & df.r18.notna()].groupby("cell").first()
            df["coin"] = k; df["w"] = w
            cases.append(df)
        a = np.concatenate(allr); drift[k] = np.nanmean(a)
    X = pd.concat(cases)
    X["u"] = X.r18 - X.coin.map(drift)
    t = lambda s: s.mean()/s.std()*np.sqrt(len(s))
    fall = ["w5","w6","w7","w8","w9","w10"]
    X["infall"] = X.w.isin(fall)
    X["sq"] = pd.qcut(X["str"], 5, labels=False)
    out["str_by_fall"] = X.groupby(["infall","sq"]).agg(mu=("u","mean"), n=("u","size"), t=("u",t), alloc=("al","mean"), tot=("r18","mean"))
    X["qq"] = pd.qcut(X["q"], 3, labels=False)
    X["s3"] = pd.qcut(X["str"], 3, labels=False)
    out["str_x_q"] = X.groupby(["s3","qq"]).agg(mu=("u","mean"), n=("u","size"), t=("u",t))
    X["tq"] = pd.qcut(X["above30d"], 5, labels=False)
    out["by_above30d"] = X.groupby("tq").agg(mu=("u","mean"), x=("above30d","mean"), n=("u","size"), t=("u",t), loss_share=("r18", lambda s: (s<0).mean()))
    out["alloc_vs_str_corr"] = float(X[["al","str"]].corr().iloc[0,1])
    out["alloc_vs_q_corr"] = float(X[["al","q"]].corr().iloc[0,1])
    X["aq"] = pd.qcut(X["al"].rank(method="first"), 5, labels=False)
    out["by_alloc"] = X.groupby("aq").agg(mu=("u","mean"), al=("al","mean"), n=("u","size"), t=("u",t))
    return out
