def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    h = 10
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values)
            f = df["forecast"].values
            n = len(df)
            r20 = c.pct_change(20).values
            r60 = c.pct_change(60).values
            dvol = c.pct_change().rolling(60, min_periods=20).std().values
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, i=i, f=f[i], ret=c[i + h] / c[i] - 1,
                                 r20=r20[i], r60=r60[i], dvol=dvol[i],
                                 day=str(pd.Timestamp(df["timestamp"].iloc[i]).date())))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby("coin")["ret"].transform("mean")
    d["ex"] = d["ret"] - d["mu"]
    d["sd"] = d.groupby("coin")["ret"].transform("std")

    def ct(g, col):
        g = g.dropna(subset=[col])
        x = g[col]; m = x.mean()
        dev = (x - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return pd.Series(dict(n=len(x), days=g["day"].nunique(), mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    # raw 20d return scaled by its usual size (vol*sqrt(20)), capped
    d["z20"] = (d["r20"] / (d["dvol"] * np.sqrt(20))).clip(-3, 3)
    d["z60"] = (d["r60"] / (d["dvol"] * np.sqrt(60))).clip(-3, 3)
    d["p_z20"] = d["z20"] * d["ex"]
    d["p_z60"] = d["z60"] * d["ex"]
    d["dir20"] = np.sign(d["r20"]) * d["ex"]
    d["dir60"] = np.sign(d["r60"]) * d["ex"]
    out["alt_signals"] = pd.DataFrame({k: ct(d, k) for k in ["p_z20", "p_z60", "dir20", "dir60"]}).T
    dd = d[d["f"].notna() & (d["f"] != 0)].copy()
    dd["dirx"] = np.sign(dd["f"]) * dd["ex"]
    dd["prod"] = dd["f"] / 10 * dd["ex"]
    dflt = ["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]
    dd["grp"] = np.where(dd["coin"].isin(dflt), "default6", "others13")
    out["by_group"] = dd.groupby("grp").apply(lambda g: ct(g, "prod"))
    dd["agree"] = np.where(np.sign(dd["r20"]) == np.sign(dd["r60"]), "20d&60d agree", "disagree")
    out["by_agree"] = dd.dropna(subset=["r60"]).groupby("agree").apply(lambda g: ct(g, "dirx"))
    # graded inside agreement: |z60| terciles
    a = dd[(dd["agree"] == "20d&60d agree")].dropna(subset=["z60"]).copy()
    a["az"] = pd.qcut(a["z60"].abs(), 3, labels=["low", "mid", "high"])
    out["agree_by_z60_tercile"] = a.groupby("az").apply(lambda g: ct(g, "dirx"))
    dd["az20"] = pd.qcut(dd["z20"].abs(), 3, labels=["low", "mid", "high"])
    out["all_by_rawz20_tercile"] = dd.dropna(subset=["z20"]).groupby("az20").apply(lambda g: ct(g, "dirx"))
    dd["normex"] = dd["ex"] / dd["sd"]
    out["corr_f_ex"] = float(dd[["f", "ex"]].corr().iloc[0, 1])
    out["corr_z20_ex"] = float(d[["z20", "ex"]].dropna().corr().iloc[0, 1])
    return out
