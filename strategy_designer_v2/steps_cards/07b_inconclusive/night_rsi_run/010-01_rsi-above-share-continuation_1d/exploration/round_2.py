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
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], r=c[i+h]/c[i]-1, year=yr[i]))
    d = pd.DataFrame(rows).dropna(subset=["f","r"])
    d["ex"] = d["r"] - d.groupby(["coin","h"])["r"].transform("mean")
    def st(x, y):
        s = stats.linregress(x, y); return s.slope/s.stderr, len(x)
    out = {}
    for h, g in d.groupby("h"):
        g = g.copy()
        g["f_w"] = g["f"] - g.groupby(["coin","w"])["f"].transform("mean")
        g["r_w"] = g["ex"] - g.groupby(["coin","w"])["ex"].transform("mean")
        g["f_y"] = g["f"] - g.groupby(["coin","year"])["f"].transform("mean")
        g["r_y"] = g["ex"] - g.groupby(["coin","year"])["ex"].transform("mean")
        wm = g.groupby(["coin","w"]).agg(f=("f","mean"), ex=("ex","mean"))
        out[h] = {"pooled_t": st(g["f"], g["ex"])[0],
                  "within_window_t": st(g["f_w"], g["r_w"])[0],
                  "within_year_t": st(g["f_y"], g["r_y"])[0],
                  "between_window_t": st(wm["f"], wm["ex"])[0],
                  "n": len(g), "n_win": len(wm)}
    res["decomp"] = pd.DataFrame(out).T
    # window-level: share of windows with positive within-window slope at 14
    g = d[d.h == 14]
    sl = g.groupby(["coin","w"]).apply(lambda x: np.polyfit(x["f"], x["ex"], 1)[0] if x["f"].std() > 0 else np.nan)
    res["win_slope_14"] = pd.Series({"share_pos": (sl > 0).mean(), "mean": sl.mean(), "t": sl.mean()/(sl.std()/np.sqrt(sl.notna().sum())), "n": sl.notna().sum()})
    # book: gain from market rise vs timing
    dd = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            r = df["close"].shift(-1)/df["close"] - 1
            dd.append(pd.DataFrame({"coin": coin, "pos": df["postRebalance_current_allocation"], "r": r}))
    dd = pd.concat(dd).dropna()
    dd["mu"] = dd.groupby("coin")["r"].transform("mean")
    res["book_decomp"] = pd.Series({"mean_gain": (dd.pos*dd.r).mean(), "market_part": (dd.pos*dd.mu).mean(),
                                    "timing_part": (dd.pos*(dd.r-dd.mu)).mean(), "mean_pos": dd.pos.mean()})
    return res
