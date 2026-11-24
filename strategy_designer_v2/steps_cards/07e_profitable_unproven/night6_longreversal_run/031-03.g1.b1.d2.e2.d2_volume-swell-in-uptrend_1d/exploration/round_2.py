def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    def clus_t(y, x, g):
        X = np.column_stack([np.ones(len(x)), x]); n, k = X.shape
        beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((k, k))
        for gg in np.unique(g):
            m = g == gg; s = (X[m] * e[m][:, None]).sum(0); meat += np.outer(s, s)
        G = len(np.unique(g)); V = XtXi @ meat @ XtXi * G/(G-1)*(n-1)/(n-k)
        return beta[1], beta[1]/np.sqrt(V[1, 1]), n
    for h in [7, 14, 21]:
        Gs = []
        for c in bars:
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                cl = b["close"]; v = b["volume"]
                vr = v.rolling(14).mean()/v.rolling(30).mean() - 1
                z = (vr - vr.rolling(60, min_periods=20).mean())/vr.rolling(60, min_periods=20).std()
                r14 = cl/cl.shift(14) - 1
                idx = np.arange(0, len(b), h)
                g = pd.DataFrame({"fr": (cl.shift(-h)/cl - 1).iloc[idx].values, "vr": vr.iloc[idx].values,
                                  "z": z.iloc[idx].values, "r14": r14.iloc[idx].values,
                                  "reg": b["regime"].iloc[idx].values,
                                  "day": pd.to_datetime(b["timestamp"].iloc[idx]).dt.floor("D").values,
                                  "year": pd.to_datetime(b["timestamp"].iloc[idx]).dt.year.values})
                g["coin"] = c; Gs.append(g)
        G = pd.concat(Gs).dropna(subset=["fr", "vr"])
        G["ex"] = G["fr"] - G.groupby("coin")["fr"].transform("mean")
        G["dayk"] = G["day"].astype("int64")
        rows = []
        for name, m in [("all", G.index == G.index), ("trending", G.reg == "trending"), ("unknown", G.reg != "trending")]:
            S = G[m.values if hasattr(m, "values") else m]
            for var in ["vr", "z"]:
                SS = S.dropna(subset=[var])
                b1, t, n = clus_t(SS.ex.values, SS[var].values, SS.dayk.values)
                rows.append({"h": h, "set": name, "var": var, "slope": b1, "t_clus": t, "n": n})
        out[f"h{h} slope ex~vr clustered"] = pd.DataFrame(rows)
        if h == 14:
            G["q"] = pd.qcut(G["vr"], 5, labels=False)
            out["h14 vr quintile x regime"] = G.groupby(["reg", "q"]).agg(mean_ex=("ex", "mean"), mean_vr=("vr", "mean"), n=("ex", "size"),
                                                         t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x))))).reset_index()
            G["up"] = np.sign(G["r14"])
            G["vr_dir"] = G["vr"] * G["up"]
            SS = G.dropna(subset=["vr_dir"])
            b1, t, n = clus_t(SS.ex.values, SS.vr_dir.values, SS.dayk.values)
            out["h14 ex ~ vr x sign(14d return)"] = pd.Series({"slope": b1, "t": t, "n": n})
            out["h14 vr top quintile by sign of 14d return"] = G[G.q == 4].groupby("up").agg(mean_ex=("ex", "mean"), n=("ex", "size"), t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
            yy = []
            for y, S in G.groupby("year"):
                r = stats.spearmanr(S.vr, S.ex)[0]; yy.append({"year": y, "rank_corr": r, "n": len(S)})
            out["h14 rank corr ex~vr by year"] = pd.DataFrame(yy)
            cc = []
            for c, S in G.groupby("coin"):
                cc.append({"coin": c, "rank_corr": stats.spearmanr(S.vr, S.ex)[0], "n": len(S)})
            out["h14 rank corr by coin"] = pd.DataFrame(cc).sort_values("rank_corr")
    return out
