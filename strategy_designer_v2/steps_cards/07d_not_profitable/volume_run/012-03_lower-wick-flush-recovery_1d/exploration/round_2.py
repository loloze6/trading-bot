def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    ev = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            wick = (np.minimum(b["open"], b["close"]) - b["low"]) / rng
            clo = (b["close"] - b["low"]) / rng
            r1 = b["close"].pct_change()
            sd = r1.rolling(20).std()
            z = r1 / sd
            vr = b["volume"] / b["volume"].shift(1).rolling(20).median()
            r20 = b["close"] / b["close"].shift(20) - 1
            last = -10
            for i in range(len(b)):
                if b["regime"].iloc[i] == "mean_reversion" and i - last > 3 and i + 3 < len(b):
                    last = i
                    ev.append(dict(coin=coin, w=w, wick=wick.iloc[i], clo=clo.iloc[i], z=z.iloc[i],
                                   vr=vr.iloc[i], r20=r20.iloc[i], alloc=alloc[i], sd=sd.iloc[i],
                                   r1=c[i+1]/c[i]-1, r3=c[i+3]/c[i]-1, g=alloc[i]*(c[i+1]/c[i]-1)))
    E = pd.DataFrame(ev).dropna()
    out["n indep events"] = len(E)
    res = {}
    for x in ["wick", "clo", "z", "vr", "r20", "sd"]:
        for y in ["r1", "r3"]:
            s = stats.linregress(E[x], E[y])
            res[(x, y)] = dict(slope=s.slope, t=s.slope / s.stderr)
    out["regressions"] = pd.DataFrame(res).T
    E["vq"] = pd.qcut(E["vr"], 3, labels=["lo", "mid", "hi"])
    out["by vr tercile"] = E.groupby("vq")[["r1", "r3", "g", "alloc"]].mean().join(E.groupby("vq").size().rename("n"))
    E["tq"] = pd.qcut(E["r20"], 3, labels=["down", "mid", "up"])
    out["by 20d return tercile"] = E.groupby("tq")[["r1", "r3", "g", "alloc"]].mean().join(E.groupby("tq").size().rename("n"))
    E["wq"] = pd.qcut(E["wick"], 3, labels=["lo", "mid", "hi"])
    out["by wick tercile gain"] = E.groupby("wq")[["r1", "r3", "g", "alloc"]].mean()
    out["book gain sum vs equal-size r1 sum"] = pd.Series({"book g sum": E.g.sum(), "mean alloc x mean r1 x n": E.alloc.mean()*E.r1.mean()*len(E), "corr alloc r1": E[["alloc","r1"]].corr().iloc[0,1]})
    D = pd.concat([d for ws in data["days"].values() for d in ws.values()])
    br = D["book_return"].dropna()
    out["book daily"] = pd.Series({"mean": br.mean(), "sd": br.std(), "share nonzero": (br.abs() > 1e-12).mean(), "mean nonzero": br[br.abs() > 1e-12].mean()})
    return out
