def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    drows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; n = len(cl)
            hr = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            pos = b["postRebalance_current_allocation"].values
            g = np.r_[pos[:-1] * hr[1:], np.nan]
            s = pd.Series(cl)
            ma30 = s.rolling(720).mean().values
            r30a = np.r_[np.full(720, np.nan), cl[720:] / cl[:-720] - 1]
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            df = pd.DataFrame({"day": day, "g": g, "pos": pos, "r30": r30a, "above": cl > ma30})
            agg = df.groupby("day").agg(g=("g", "sum"), pos=("pos", "mean"), r30=("r30", "first"), above=("above", "first"))
            agg["coin"] = c; agg["w"] = w
            drows.append(agg)
            for i in range(0, n - 72, 72):
                if i < 720: continue
                f = b["forecast"].values[i]
                if f <= 0: continue
                fwd = cl[i + 72] / cl[i] - 1
                vol30 = np.nanstd(hr[i - 719:i + 1])
                recs.append((c, f, cl[i] / cl[i - 720] - 1, cl[i] > ma30[i], vol30, cl[i] / cl[i - 24] - 1, fwd))
    G = pd.DataFrame(recs, columns=["coin", "f", "r30", "above", "vol30", "r24", "fwd"])
    G["fq"] = pd.qcut(G.f, 4, labels=False)
    G["r24z"] = G.r24 / (G.vol30 * np.sqrt(24))
    G["zq"] = pd.qcut(G.r24z, 4, labels=False)
    def st(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "p10": x.quantile(0.1)})
    out["fq_by_above"] = G.groupby(["above", "fq"])["fwd"].apply(st).unstack().round(4)
    out["r24z_quartile"] = G.groupby("zq")["fwd"].apply(st).unstack().round(4)
    out["r24z_by_above"] = G.groupby(["above", "zq"])["fwd"].apply(st).unstack().round(4)
    D = pd.concat(drows)
    D = D[D.r30.notna()]
    out["daily_gain_by_above"] = D.groupby("above").agg(n=("g", "size"), mean_g=("g", "mean"), sd=("g", "std"),
                                                         worst5=("g", lambda x: x.quantile(0.05)), pos=("pos", "mean")).round(5)
    D["r30q"] = pd.qcut(D.r30, 5, labels=False)
    out["daily_gain_by_r30q"] = D.groupby("r30q").agg(n=("g", "size"), mean_g=("g", "mean"), sd=("g", "std"),
                                                      pos=("pos", "mean")).round(5)
    # chained drawdown per variant: book of mean over coins, keeping only above-MA days
    def dd_of(mask):
        X = D.copy(); X["gg"] = np.where(mask(X), X.g, 0.0)
        B = X.groupby(["w", "day"])["gg"].mean().reset_index()
        B["wn"] = B.w.str[1:].astype(int); B = B.sort_values(["wn", "day"])
        eq = np.cumprod(1 + B.gg.values); dd = (eq / np.maximum.accumulate(eq) - 1).min()
        yrs = len(B) / 365; ann = eq[-1] ** (1 / yrs) - 1
        return pd.Series({"ann": ann, "maxdd": dd, "calmar": ann / -dd, "sharpe": B.gg.mean() / B.gg.std() * np.sqrt(365)})
    out["variant_all"] = dd_of(lambda X: np.ones(len(X), bool)).round(4)
    out["variant_above_only"] = dd_of(lambda X: X.above.values).round(4)
    out["variant_below_only"] = dd_of(lambda X: ~X.above.values).round(4)
    return out
