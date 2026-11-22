def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [2, 5]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rs += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ret = pd.Series(c).pct_change()
            vol = ret.rolling(20).std()
            z = (ret / vol).values
            r30 = pd.Series(c).pct_change(30).values
            r90 = pd.Series(c).pct_change(90).values
            prev = np.r_[0, f[:-1]]
            cand = (f - prev <= -2)
            n = len(c)
            for t in np.where(cand)[0]:
                rec = dict(coin=coin, w=w, t=t, cell2=t // 2, cell5=t // 5, f=f[t], z=z[t],
                           r30=r30[t], r90=r90[t], r30z=r30[t] / (vol.values[t] * np.sqrt(30)) if vol.values[t] > 0 else np.nan,
                           year=pd.Timestamp(df["timestamp"].iloc[t]).year)
                for H in [2, 5]:
                    rec[f"ex{H}"] = (-(c[t + H] / c[t] - 1) + drift[(coin, H)]) if t + H < n else np.nan
                rows.append(rec)
    d0 = pd.DataFrame(rows)

    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    for H, cell in [(2, "cell2"), (5, "cell5")]:
        d = d0.drop_duplicates(["coin", "w", cell])
        d = d[d[f"ex{H}"].notna()].copy()
        d["r30q"] = pd.qcut(d["r30"].rank(method="first"), 4, labels=False)
        g = d.groupby("r30q").apply(lambda g: summ(g, f"ex{H}")).join(d.groupby("r30q")["r30"].mean())
        out[f"H{H}_by_r30_quartile"] = g
        lo = d[d.r30q == 0][f"ex{H}"]; hi = d[d.r30q == 3][f"ex{H}"]
        tt = stats.ttest_ind(lo, hi, equal_var=False)
        out[f"H{H}_deepest_minus_shallowest_r30"] = f"diff {100*(lo.mean()-hi.mean()):.3f}% t {tt.statistic:.2f}"
        med = d["r30"].median()
        a = d[d.r30 < med][f"ex{H}"]; b = d[d.r30 >= med][f"ex{H}"]
        out[f"H{H}_deeper_half_minus_shallower_half"] = f"diff {100*(a.mean()-b.mean()):.3f}% t {stats.ttest_ind(a,b,equal_var=False).statistic:.2f} n {len(a)}/{len(b)}"
        out[f"H{H}_spearman_r30_ex"] = str(stats.spearmanr(d["r30"], d[f"ex{H}"]))
        d["r30zq"] = pd.qcut(d["r30z"].rank(method="first"), 4, labels=False)
        out[f"H{H}_by_r30_in_usual_moves_quartile"] = d.groupby("r30zq").apply(lambda g: summ(g, f"ex{H}")).join(d.groupby("r30zq")["r30z"].mean())
        d["half"] = np.where(d.r30 < med, "deep", "shallow")
        out[f"H{H}_by_year_and_half"] = d.groupby(["year", "half"]).apply(lambda g: summ(g, f"ex{H}"))[["n", "mean%"]].unstack()
        d["zq"] = pd.qcut(d["z"].rank(method="first"), 4, labels=False)
        out[f"H{H}_by_z_quartile"] = d.groupby("zq").apply(lambda g: summ(g, f"ex{H}")).join(d.groupby("zq")["z"].mean())
    return out
