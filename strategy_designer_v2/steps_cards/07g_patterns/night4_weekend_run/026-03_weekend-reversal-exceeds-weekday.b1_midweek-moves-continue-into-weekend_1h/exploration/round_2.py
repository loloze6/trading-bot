def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = []
    C = []
    for coin, wins in bars.items():
        r48 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            r48.extend(c[idx + 48] / c[idx] - 1)
        usual = np.std(r48); drift = np.mean(r48)
        for w, df in wins.items():
            d = df[["timestamp", "close"]].copy().reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"])
            c = d["close"].values; n = len(c)
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values; yr = ts.dt.year.values
            lr = pd.Series(np.log(c)).diff()
            vol = lr.rolling(720, min_periods=240).std().values
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            # hours 20+21 combined: 2h return from close of 19:00 bar to close of 21:00 bar
            for i in np.where(hr == 19)[0]:
                if i - 24 < 0 or i + 2 >= n:
                    continue
                f2 = c[i + 2] / c[i] - 1
                b24 = c[i] / c[i - 24] - 1
                b20 = c[i] / c[i - 20] - 1  # since 23:00 previous day
                C.append((coin, w, yr[i], wd[i], f2, b24, b20, vol[i]))
            for i in np.where(hr == 23)[0]:
                if i - 48 < 0 or i + 48 >= n or wd[i] != 3:
                    continue
                back = c[i] / c[i - 48] - 1
                fwd = c[i + 48] / c[i] - 1
                H.append((coin, w, yr[i], back / usual, (fwd - drift) / usual, fwd - drift, fwd))
    X = pd.DataFrame(C, columns=["coin", "w", "yr", "wd", "f2", "b24", "b20", "vol"]).dropna()
    def tt(s):
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)})
    out["h20_21_by_coin"] = X.groupby("coin")["f2"].apply(tt).unstack()
    out["h20_21_by_year"] = X.groupby("yr")["f2"].apply(tt).unstack()
    out["h20_21_by_weekday"] = X.groupby("wd")["f2"].apply(tt).unstack()
    X["vq"] = X.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["h20_21_by_vol_tercile"] = X.groupby("vq")["f2"].apply(tt).unstack()
    X["bq"] = X.groupby("coin")["b20"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["h20_21_by_prior20h_quintile"] = X.groupby("bq")["f2"].apply(tt).unstack()
    X["zb"] = X.groupby("coin")["b20"].transform(lambda x: x / x.std())
    sl = stats.linregress(X["zb"], X["f2"])
    out["h20_21_on_prior20h_slope"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(X)})
    Y = pd.DataFrame(H, columns=["coin", "w", "yr", "zb", "zf", "uf", "fwd"])
    out["frisat_by_year"] = Y.groupby("yr").apply(lambda g: pd.Series({
        "n": len(g), "slope_t": (lambda s: s.slope / s.stderr)(stats.linregress(g["zb"], g["zf"])),
        "mean_fwd_unusual": g["uf"].mean(), "t_unusual": g["uf"].mean() / (g["uf"].std() / np.sqrt(len(g)))}))
    Y["side"] = np.where(Y["zb"] > 0, "up", "down")
    out["frisat_by_midweek_side"] = Y.groupby("side").apply(lambda g: pd.Series({
        "n": len(g), "mean_unusual": g["uf"].mean(), "t": g["uf"].mean() / (g["uf"].std() / np.sqrt(len(g))),
        "slope_t": (lambda s: s.slope / s.stderr)(stats.linregress(g["zb"], g["zf"]))}))
    Y["q"] = Y.groupby("coin")["zb"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["frisat_by_midweek_quintile"] = Y.groupby("q")["uf"].apply(tt).unstack()
    return out
