def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "inprof": (df["regime"] == "unknown").astype(int),
                              "yr": pd.to_datetime(df["timestamp"]).dt.year})
            for k in [1, 2, 3, 5, 7]:
                d[f"r{k}"] = c / c.shift(k) - 1
            d["r30"] = c / c.shift(30) - 1
            for h in [1, 2, 3, 5, 7]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    drift = {h: A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean() for h in [1, 2, 3, 5, 7]}
    def prep(h, prof):
        g = A[(A.pos % h == 0) & (A.inprof == prof)].copy()
        g["ex"] = g[f"f{h}"] - g.coin.map(drift[h])
        return g
    # spearman matrix past k vs fwd h, in profile and out
    res = []
    for prof in [1, 0]:
        for h in [1, 2, 3, 5, 7]:
            g = prep(h, prof)
            for k in [1, 2, 3, 5, 7]:
                s = g.dropna(subset=["ex", f"r{k}"])
                rho, p = stats.spearmanr(s[f"r{k}"], s.ex)
                res.append({"prof": prof, "h": h, "k": k, "n": len(s), "rho": round(rho, 3), "p": round(p, 3)})
    out["spearman_k_h"] = pd.DataFrame(res).pivot_table(index=["prof", "h"], columns="k", values="rho")
    out["pvals_k_h"] = pd.DataFrame(res).pivot_table(index=["prof", "h"], columns="k", values="p")
    # short side: r3<0 in profile, terciles of r3, horizons 3,5; short gain = -ex
    res = []
    for h in [3, 5]:
        g = prep(h, 1).dropna(subset=["ex", "r3"])
        neg = g[g.r3 < 0].copy()
        neg["q"] = pd.qcut(neg.r3, 3, labels=["deep", "mid", "shallow"])
        for q, s in neg.groupby("q", observed=True):
            res.append({"h": h, "q": q, "n": len(s), "r3": s.r3.mean(), "mean_ex": s.ex.mean(),
                        "t": s.ex.mean() / (s.ex.std() / np.sqrt(len(s)))})
        pos = g[g.r3 >= 0]
        res.append({"h": h, "q": "r3>=0", "n": len(pos), "r3": pos.r3.mean(), "mean_ex": pos.ex.mean(),
                    "t": pos.ex.mean() / (pos.ex.std() / np.sqrt(len(pos)))})
        # graded short signal: weight -r3 on r3<0, gain = (-ex) * (-r3)/mean(-r3); per-day t
        neg["w"] = -neg.r3 / (-neg.r3).mean()
        neg["gain"] = -neg.ex * neg.w
        dd = neg.groupby("day").gain.sum()
        res.append({"h": h, "q": "graded_short_gain_perday", "n": len(dd), "r3": np.nan,
                    "mean_ex": dd.mean(), "t": dd.mean() / (dd.std() / np.sqrt(len(dd)))})
        dd2 = (-neg.ex).groupby(neg.day).sum()
        res.append({"h": h, "q": "flat_short_gain_perday", "n": len(dd2), "r3": np.nan,
                    "mean_ex": dd2.mean(), "t": dd2.mean() / (dd2.std() / np.sqrt(len(dd2)))})
    out["inprof_r3neg_terciles"] = pd.DataFrame(res)
    # by coin and by year, h=5, r3<0, spearman and mean short gain
    g = prep(5, 1).dropna(subset=["ex", "r3"])
    neg = g[g.r3 < 0]
    def summ(s):
        rho = stats.spearmanr(s.r3, s.ex)[0] if len(s) > 5 else np.nan
        return pd.Series({"n": len(s), "short_gain": -s.ex.mean(), "rho_r3_ex": rho})
    out["h5_r3neg_by_coin"] = neg.groupby("coin").apply(summ)
    out["h5_r3neg_by_year"] = neg.groupby("yr").apply(summ)
    # all r3 in profile by coin at h3
    g3 = prep(3, 1).dropna(subset=["ex", "r3"])
    out["h3_all_by_coin_rho"] = g3.groupby("coin").apply(lambda s: pd.Series({"n": len(s), "rho": stats.spearmanr(s.r3, s.ex)[0]}))
    return out
