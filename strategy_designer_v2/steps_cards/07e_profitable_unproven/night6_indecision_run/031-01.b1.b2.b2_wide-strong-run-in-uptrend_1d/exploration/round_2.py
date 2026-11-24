def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    res = []; qtab = {}; coin_tab = []
    for h in [3, 5, 10, 20]:
        recs = []
        for c in bars:
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                cl = b["close"]
                r60 = cl/cl.shift(60)-1
                r20 = cl/cl.shift(20)-1
                r5 = cl/cl.shift(5)-1
                rng = (b["high"]-b["low"])/cl
                rm = rng/rng.rolling(20).mean()
                vol = cl.pct_change().rolling(20).std()
                fwd = cl.shift(-h)/cl-1
                idx = np.arange(0, len(b), h)
                recs.append(pd.DataFrame({"fwd": fwd.iloc[idx].values, "r60": r60.iloc[idx].values,
                    "r20": r20.iloc[idx].values, "r5": r5.iloc[idx].values, "rm": rm.iloc[idx].values,
                    "vol": vol.iloc[idx].values, "coin": c, "w": w}))
        D = pd.concat(recs).dropna(subset=["fwd"])
        D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
        for col in ["r60", "r20"]:
            E = D.dropna(subset=[col]).copy()
            E["z"] = E[col] / (E["vol"]*np.sqrt({"r60":60,"r20":20}[col]))
            E = E.dropna(subset=["z"])
            rho, p = stats.spearmanr(E["z"], E["ex"])
            up = E[E[col] > 0]
            rho_up, _ = stats.spearmanr(up["z"], up["ex"])
            sl = stats.linregress(E["z"], E["ex"])
            res.append({"h": h, "var": col, "n": len(E), "spearman": rho, "p": p,
                        "spearman_inside_up": rho_up, "n_up": len(up),
                        "slope_pct_per_z": sl.slope*100, "t_slope": sl.slope/sl.stderr})
            if h == 10:
                E["q"] = pd.qcut(E["z"], 5, labels=False)
                qtab[col] = (E.groupby("q")["ex"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"]*100)).round(3)
                for c, g in E.groupby("coin"):
                    s = stats.linregress(g["z"], g["ex"])
                    coin_tab.append({"var": col, "coin": c, "slope_pct": s.slope*100, "t": s.slope/s.stderr, "n": len(g)})
        # range multiple inside up-60d regime at this h
        U = D.dropna(subset=["r60", "rm"]); U = U[(U.r60 > 0) & (U.r5 > 0)]
        rho, p = stats.spearmanr(U["rm"], U["ex"])
        res.append({"h": h, "var": "rm_in_regime", "n": len(U), "spearman": rho, "p": p})
    out["grades"] = pd.DataFrame(res).round(4)
    for k, v in qtab.items():
        out["quintiles_10d_" + k] = v
    out["by_coin_10d"] = pd.DataFrame(coin_tab).round(3)
    # book daily decomposition
    days = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            days.append(d.assign(coin=c, w=w))
    DD = pd.concat(days)
    bk = DD.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_mean_bp"] = float(bk.mean()*1e4)
    s = bk.sort_values(ascending=False)
    out["book_top20days_share"] = float(s.head(20).sum()/s.sum())
    out["book_mean_wo_top20_bp"] = float(s.iloc[20:].mean()*1e4)
    return out
