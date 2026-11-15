def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    # pooled mean daily return per coin
    mu = {}
    for c, ws in bars.items():
        rs = []
        for w, df in ws.items():
            r = df["close"].pct_change().dropna()
            rs.append(r)
        mu[c] = pd.concat(rs).mean()
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].values
            a = df["postRebalance_current_allocation"].values
            n = len(df)
            for h in [5, 10, 20, 40, 60]:
                for i in range(0, n - h, h):
                    ret = cl[i + h] / cl[i] - 1
                    rows.append((c, w, h, f[i], a[i], ret, ret - h * mu[c]))
    R = pd.DataFrame(rows, columns=["coin", "win", "h", "f", "a", "ret", "ex"])
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g.ex.mean(), "med_ex": g.ex.median(),
                          "share_pos": (g.ex > 0).mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    R["on"] = R.f > 0
    out["by_h_on"] = R.groupby(["h", "on"]).apply(summ)
    R20 = R[R.h == 20].copy()
    on = R20[R20.on].copy()
    on["fq"] = pd.qcut(on.f.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["h20_fquart"] = on.groupby("fq").apply(summ)
    out["h20_coin_on"] = on.groupby("coin").apply(summ)
    out["h20_coin_off"] = R20[~R20.on].groupby("coin").apply(summ)
    R20["yr"] = R20.win  # placeholder
    out["h20_win_on"] = on.groupby("win").apply(summ)
    R60 = R[(R.h == 60) & R.on].copy()
    R60["fq"] = pd.qcut(R60.f.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["h60_fquart"] = R60.groupby("fq").apply(summ)
    out["corr_f_ex_on_h20"] = float(stats.spearmanr(on.f, on.ex).correlation)
    out["welch_on_off_h20"] = float(stats.ttest_ind(on.ex, R20[~R20.on].ex, equal_var=False).statistic)
    return out
