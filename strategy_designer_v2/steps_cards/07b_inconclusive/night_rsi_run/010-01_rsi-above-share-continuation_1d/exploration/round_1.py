def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    res = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for h in [3, 7, 14, 28]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], r=c[i+h]/c[i]-1, year=yr[i],
                                     past=(c[i]/c[max(0,i-30)]-1)))
    d = pd.DataFrame(rows).dropna(subset=["f","r"])
    d["ex"] = d["r"] - d.groupby(["coin","h"])["r"].transform("mean")
    def slope_t(g):
        if len(g) < 10 or g["f"].std() == 0: return pd.Series({"n": len(g), "t": np.nan, "slope": np.nan})
        s = stats.linregress(g["f"], g["ex"])
        return pd.Series({"n": len(g), "t": s.slope/s.stderr, "slope": s.slope})
    res["by_horizon"] = d.groupby("h").apply(slope_t)
    d14 = d[d.h == 14].copy()
    res["by_coin_14"] = d14.groupby("coin").apply(slope_t)
    res["by_year_14"] = d14.groupby("year").apply(slope_t)
    d14["side"] = np.sign(d14["f"])
    res["side_mean_ex_14"] = d14.groupby("side")["ex"].agg(["count","mean","std"])
    d14["q"] = pd.qcut(d14["f"], 5, labels=False, duplicates="drop")
    res["quintile_14"] = d14.groupby("q").agg(n=("ex","count"), f=("f","mean"), ex=("ex","mean"))
    d14["vol_reg"] = d14.groupby("coin")["past"].transform(lambda x: pd.qcut(x.abs(), 2, labels=False))
    res["by_absmove_14"] = d14.groupby("vol_reg").apply(slope_t)
    res["pos_vs_neg_slope_14"] = pd.concat({"long": slope_t(d14[d14.f > 0]), "short": slope_t(d14[d14.f < 0])}, axis=1)
    return res
