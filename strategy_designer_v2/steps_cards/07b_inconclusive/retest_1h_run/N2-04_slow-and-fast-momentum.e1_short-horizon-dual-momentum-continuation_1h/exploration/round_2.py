def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    h = 72
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            fs = df.get("debug_info.components.slow.last_history_value")
            ff = df.get("debug_info.components.fast.last_history_value")
            fs = fs.values if fs is not None else np.full(len(c), np.nan)
            ff = ff.values if ff is not None else np.full(len(c), np.nan)
            n = len(c)
            for i in range(0, n - h, h):
                r20 = c[i]/c[i-480]-1 if i >= 480 else np.nan
                r3 = c[i]/c[i-72]-1 if i >= 72 else np.nan
                rows.append((coin, w, f[i], fs[i], ff[i], r20, r3, c[i+h]/c[i]-1))
    d = pd.DataFrame(rows, columns=["coin","w","f","slow","fast","r20","r3","r"])
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    on = d[d.f > 0].copy()
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    sp = stats.spearmanr(on.f, on.ex)
    out["spearman_f_ex_on"] = pd.Series({"rho": sp[0], "p": sp[1], "n": len(on)})
    on["half"] = np.where(on.f >= on.f.median(), "top", "bottom")
    out["by_half"] = on.groupby("half")["ex"].apply(tt).unstack()
    out["by_half_coin"] = on.groupby(["coin","half"])["ex"].apply(tt).unstack()
    for col in ["slow","fast","r3"]:
        s = on.dropna(subset=[col]).copy()
        s["q"] = pd.qcut(s[col].rank(method="first"), 3, labels=False)
        out["by_"+col+"_tercile"] = s.groupby("q")["ex"].apply(tt).unstack()
    out["top_half_minus_bottom_welch"] = pd.Series(stats.ttest_ind(on[on.half=="top"].ex, on[on.half=="bottom"].ex, equal_var=False))
    return out
