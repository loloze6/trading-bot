def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    rows = []; grid = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; n = len(cl)
            al = b["postRebalance_current_allocation"].fillna(0).values
            fc = b["forecast"].fillna(0).values
            nxt = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            brk = np.full(n, np.nan); r60 = np.full(n, np.nan); r20 = np.full(n, np.nan)
            nb20 = np.full(n, np.nan)
            for t in range(n):
                if t >= 20:
                    brk[t] = cl[t] / hi[t-20:t].max() - 1
                    r20[t] = cl[t] / cl[t-20] - 1
                if t >= 60: r60[t] = cl[t] / cl[t-60] - 1
            isb = (brk > 0).astype(float); isb[np.isnan(brk)] = np.nan
            for t in range(n):
                if t >= 40: nb20[t] = np.nansum(isb[t-19:t+1])
            age = np.zeros(n); a = 0
            for t in range(n):
                a = a + 1 if al[t] != 0 else 0
                age[t] = a
            # breakouts in last 20 days at entry of current position
            entry_nb = np.full(n, np.nan); en = np.nan
            for t in range(n):
                if al[t] != 0 and (t == 0 or al[t-1] == 0): en = nb20[t]
                entry_nb[t] = en if al[t] != 0 else np.nan
            df = pd.DataFrame({"coin": c, "win": w, "al": al, "gain": al * nxt, "nxt": nxt, "age": age,
                               "r60": r60, "r20": r20, "nb20": nb20, "entry_nb": entry_nb, "brk": brk})
            rows.append(df)
            for t in range(0, n - 5, 5):
                grid.append({"coin": c, "win": w, "f5": cl[t+5] / cl[t] - 1, "brk": brk[t], "r60": r60[t],
                             "nb20": nb20[t], "r20": r20[t], "fc": fc[t]})
    D = pd.concat(rows); D = D[D.al != 0].dropna(subset=["gain"])
    G = pd.DataFrame(grid)
    drift = G.groupby("coin").f5.mean()
    G["u5"] = G.f5 - G.coin.map(drift)
    def summ(g): 
        return pd.Series({"n": len(g), "mean_gain": g.gain.mean(), "sum_gain": g.gain.sum(),
                          "p01_gain": g.gain.quantile(0.01), "share_days_lt_-3pct": (g.gain < -0.03).mean()})
    D["age_b"] = pd.cut(D.age, [0, 5, 10, 20, 40, 1000])
    out["pos_by_age"] = D.groupby("age_b").apply(summ)
    D["tr60"] = pd.cut(D.r60, [-10, -0.1, 0.1, 0.5, 1.0, 100])
    out["pos_by_r60"] = D.groupby("tr60").apply(summ)
    D["nb_b"] = pd.cut(D.nb20, [-1, 2, 5, 8, 20])
    out["pos_by_nb20_now"] = D.groupby("nb_b").apply(summ)
    D["r20_b"] = pd.cut(D.r20, [-10, 0, 0.2, 0.4, 0.7, 100])
    out["pos_by_r20_now"] = D.groupby("r20_b").apply(summ)
    # condition-alone check on grid: breakout vs not, by r60 trend, by nb20
    G["sig"] = G.brk > 0
    G["tr60"] = pd.cut(G.r60, [-10, -0.1, 0.1, 0.5, 100])
    G["nb_b"] = pd.cut(G.nb20, [-1, 2, 5, 8, 20])
    def tt(g):
        x = g.u5.dropna()
        return pd.Series({"n": len(x), "mean_u5": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["grid_sig_by_r60"] = G.dropna(subset=["r60"]).groupby(["tr60", "sig"]).apply(tt)
    out["grid_sig_by_nb20"] = G.dropna(subset=["nb20"]).groupby(["nb_b", "sig"]).apply(tt)
    S = G[G.sig]
    S["brk_q"] = pd.qcut(S.brk, 4, labels=False)
    out["grid_sig_by_brk_q"] = S.groupby("brk_q").apply(tt)
    return out
