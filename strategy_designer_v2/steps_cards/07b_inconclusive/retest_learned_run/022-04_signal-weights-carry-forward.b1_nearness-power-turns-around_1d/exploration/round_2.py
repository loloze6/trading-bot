def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values
            for i in range(0, len(df) - 5, 5):
                rows.append((coin, w, f[i], c[i+5]/c[i]-1))
    d = pd.DataFrame(rows, columns=["coin","win","fc","ret"])
    d["ex"] = d["ret"] - d.groupby("coin")["ret"].transform("mean")
    d["prod"] = d["fc"]/10*d["ex"]
    out = {}
    x = d["prod"]
    lo, hi = x.quantile(0.01), x.quantile(0.99)
    xt = x.clip(lo, hi)
    out["robust"] = pd.Series({
        "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))),
        "wins_mean": xt.mean(), "wins_t": xt.mean()/(xt.std()/np.sqrt(len(xt))),
        "share_prod_pos_active": (x[d["fc"]!=0] > 0).mean(),
        "top10_share_of_sum": x.sort_values(ascending=False).head(10).sum()/x.sum(),
        "sign_hit_t": stats.ttest_1samp(np.sign(d.loc[d["fc"]!=0,"fc"])*d.loc[d["fc"]!=0,"ex"], 0)[1],
    })
    wm = d.groupby(["coin","win"])["prod"].mean()
    out["windows_positive_share"] = pd.Series({"n_coin_windows": len(wm), "share_pos": (wm > 0).mean(),
        "t_over_windows": wm.mean()/(wm.std()/np.sqrt(len(wm)))})
    d["absq"] = pd.qcut(d["fc"].abs().rank(method="first"), 5, labels=False)
    out["sign_ex_by_absq"] = d.groupby("absq").apply(lambda g: pd.Series({
        "n": len(g), "mean_signed_ex": (np.sign(g["fc"])*g["ex"]).mean(),
        "t": (np.sign(g["fc"])*g["ex"]).mean()/((np.sign(g["fc"])*g["ex"]).std()/np.sqrt(len(g)))}))
    return out
