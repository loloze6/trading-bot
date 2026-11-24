def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H_list = [5, 10, 20, 30]
    # coin mean h-return over all windows (non-overlapping grid)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            # trailing 20d raw return and 60d return
            r20 = pd.Series(c).pct_change(20).values
            r60 = pd.Series(c).pct_change(60).values
            vol = pd.Series(c).pct_change().rolling(60, min_periods=20).std().values
            for h in H_list:
                for i in range(0, n - h, 10 if h == 10 else h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=yr[i], f=f[i],
                                     ret=c[i + h] / c[i] - 1, r20=r20[i], r60=r60[i], vol=vol[i],
                                     day=str(pd.Timestamp(df["timestamp"].iloc[i]).date())))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["mu"]
    d = d[d["f"].notna() & (d["f"] != 0)]
    d["prod"] = d["f"] / 10 * d["ex"]
    d["dirx"] = np.sign(d["f"]) * d["ex"]

    def ct(g, col="prod"):
        x = g[col]
        m = x.mean()
        dev = (x - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return pd.Series(dict(n=len(x), days=g["day"].nunique(), mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    out["by_horizon"] = d.groupby("h").apply(ct)
    d10 = d[d["h"] == 10].copy()
    out["by_horizon_dir"] = d.groupby("h").apply(lambda g: ct(g, "dirx"))
    out["by_coin"] = d10.groupby("coin").apply(ct)
    out["by_year"] = d10.groupby("year").apply(ct)
    d10["side"] = np.where(d10["f"] > 0, "up", "down")
    out["by_side"] = d10.groupby("side").apply(lambda g: ct(g, "dirx"))
    d10["fbin"] = pd.cut(d10["f"], [-20.01, -15, -10, -5, 0, 5, 10, 15, 20.01])
    out["by_fbin_dirx"] = d10.groupby("fbin").apply(lambda g: ct(g, "dirx"))
    d10["r60side"] = np.where(d10["r60"] > 0, "60d up", "60d down")
    out["by_side_x_60d"] = d10.dropna(subset=["r60"]).groupby(["side", "r60side"]).apply(lambda g: ct(g, "dirx"))
    q = d10["vol"].quantile([1/3, 2/3]).values
    d10["volt"] = np.where(d10["vol"] <= q[0], "lowvol", np.where(d10["vol"] <= q[1], "midvol", "highvol"))
    out["by_vol"] = d10.dropna(subset=["vol"]).groupby("volt").apply(ct)
    return out
