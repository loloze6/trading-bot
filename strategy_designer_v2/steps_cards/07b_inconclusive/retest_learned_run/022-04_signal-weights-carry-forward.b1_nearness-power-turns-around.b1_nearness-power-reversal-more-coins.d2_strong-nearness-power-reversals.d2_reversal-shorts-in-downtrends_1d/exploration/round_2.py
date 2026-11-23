def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = 5
    for coin, wins in bars.items():
        allr, cases = [], []
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.excess_power.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            for i in range(0, len(df) - H, H):
                r = c[i + H] / c[i] - 1
                allr.append(r)
                if f[i] <= -2:
                    r20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                    r5p = c[i] / c[i - 5] - 1 if i >= 5 else np.nan
                    cases.append((w, abs(f[i]), r, r20, r5p, raw[i]))
        if len(allr) < 3:
            continue
        m = np.mean(allr); sd = np.std(allr, ddof=1)
        for w, fa, r, r20, r5p, rw in cases:
            rows.append(dict(coin=coin, w=w, f=fa, ex=-(r - m), wex=-(r - m) * fa / 10,
                             st=-(r - m) / sd, r20=r20, r5p=r5p, raw=rw))
    d = pd.DataFrame(rows)

    def summ(g):
        n = len(g)
        out = dict(n=n, mean_ex=g.ex.mean(),
                   t_ex=stats.ttest_1samp(g.ex, 0).statistic if n > 2 else np.nan,
                   t_w=stats.ttest_1samp(g.wex, 0).statistic if n > 2 else np.nan,
                   strength=g.st.mean())
        med = g.f.median()
        hi, lo = g[g.f > med].ex, g[g.f < med].ex
        out["supp_hi_minus_lo"] = hi.mean() - lo.mean()
        out["supp_t"] = stats.ttest_ind(hi, lo, equal_var=False).statistic if len(hi) > 2 and len(lo) > 2 else np.nan
        out["spearman_f_ex"] = stats.spearmanr(g.f, g.ex).correlation if n > 5 else np.nan
        return pd.Series(out)

    d["saturated"] = d.f >= 19.99
    d["r20_band"] = pd.cut(d.r20, [-1, -0.2, -0.11, -0.044, 0], labels=["<-20%", "-20..-11%", "-11..-4%", "-4..0%"])
    d["r5_sign"] = np.where(d.r5p < 0, "prior5d_down", "prior5d_up")
    dr = d.dropna(subset=["raw"]).copy()
    dr["raw_abs_q"] = pd.qcut(dr.raw.abs().rank(method="first"), 4, labels=False)
    return {
        "all": summ(d),
        "by_saturation": d.groupby("saturated").apply(summ),
        "by_r20_band": d.groupby("r20_band").apply(summ),
        "r20_above_-20pct": summ(d[d.r20 > -0.2]),
        "by_prior5d": d.groupby("r5_sign").apply(summ),
        "by_raw_abs_quartile": dr.groupby("raw_abs_q").apply(summ).join(dr.groupby("raw_abs_q").raw.agg(["min", "max"])),
        "spearman_r20_ex": pd.Series(dict(rho=stats.spearmanr(d.dropna(subset=["r20"]).r20, d.dropna(subset=["r20"]).ex).correlation)),
    }
