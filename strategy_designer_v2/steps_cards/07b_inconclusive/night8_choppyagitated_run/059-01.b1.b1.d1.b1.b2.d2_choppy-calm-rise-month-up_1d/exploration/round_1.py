def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [3, 7, 14]
    rows = []
    gridrets = {h: {} for h in H}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            f = df["forecast"].fillna(0).values
            ret30 = pd.Series(c).pct_change(30).values
            ret7 = pd.Series(c).pct_change(7).values
            for h in H:
                gridrets[h].setdefault(coin, [])
                for i in range(0, n - h, h):
                    gridrets[h][coin].append(c[i + h] / c[i] - 1)
            for i in range(0, n - 7, 7):
                r = {"coin": coin, "win": w, "i": i, "f": f[i], "ret30": ret30[i], "ret7": ret7[i],
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year, "day": str(df["timestamp"].iloc[i])[:10]}
                for h in H:
                    r["fwd%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    for h in H:
        mu = {k: np.mean(v) for k, v in gridrets[h].items()}
        d["ex%d" % h] = d["fwd%d" % h] - d["coin"].map(mu)
    act = d[d.f > 0].copy()
    allg = d.copy()

    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["active by horizon"] = pd.DataFrame({h: tstat(act["ex%d" % h]) for h in H}).T
    out["by coin ex7"] = act.groupby("coin")["ex7"].apply(tstat).unstack()
    out["by window ex7"] = act.groupby("win")["ex7"].apply(tstat).unstack()
    out["by year ex7"] = act.groupby("year")["ex7"].apply(tstat).unstack()
    act["fq"] = pd.qcut(act["f"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by forecast tercile"] = act.groupby("fq")[["ex7", "ex14", "ex3"]].mean()
    out["tercile counts/f"] = act.groupby("fq")["f"].agg(["count", "mean"])
    act["r30q"] = pd.qcut(act["ret30"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by ret30 tercile"] = act.groupby("r30q")["ex7"].apply(tstat).unstack()
    # all grid bars (no regime) with ret7>0 : the plain situation
    a2 = allg[(allg.ret7 > 0)]
    out["all grid ret7>0 vs <=0 ex7"] = pd.DataFrame({"up": tstat(a2["ex7"]), "down": tstat(allg[allg.ret7 <= 0]["ex7"])}).T
    out["corr f ex7 active"] = float(act[["f", "ex7"]].corr().iloc[0, 1])
    out["share winners"] = float((act["ex7"] > 0).mean())
    out["median ex7"] = float(act["ex7"].median())
    return out
