def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            r1 = s.pct_change()
            mom = s / s.shift(28) - 1
            rev = -r1
            near = s / s.rolling(90).max()
            vol = -r1.rolling(30).std()
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], ret=c[i + h] / c[i] - 1,
                                     mom=mom.iloc[i], rev=rev.iloc[i], near=near.iloc[i], vol=vol.iloc[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    d["m"] = d["f"] / 10 * d["ex"]
    act = d[d["f"] != 0]

    def tstat(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))

    out = {}
    out["by_horizon"] = act.groupby("h")["m"].apply(tstat).unstack()
    a5 = act[act.h == 5].copy()
    out["by_coin"] = a5.groupby("coin")["m"].apply(tstat).unstack()
    out["by_year"] = a5.groupby("year")["m"].apply(tstat).unstack()
    a5["side"] = np.where(a5.f > 0, "long", "short")
    a5["sex"] = np.sign(a5.f) * a5.ex
    out["by_side_signedex"] = a5.groupby("side")["sex"].apply(tstat).unstack()
    a5["fq"] = pd.qcut(a5.f.abs(), 4, labels=False)
    out["by_absf_quartile_signedex"] = a5.groupby("fq")["sex"].apply(tstat).unstack()

    # single signals, rank IC vs ex per horizon (spearman, pooled), and per coin for 5d
    res = []
    for h in H:
        dh = d[d.h == h]
        for sig in ["mom", "rev", "near", "vol", "f"]:
            x = dh[[sig, "ex"]].dropna()
            rho, p = stats.spearmanr(x[sig], x["ex"])
            res.append(dict(h=h, sig=sig, n=len(x), rho=rho, t=rho * np.sqrt(len(x) - 2) / np.sqrt(1 - rho ** 2)))
    out["single_signal_ic"] = pd.DataFrame(res).set_index(["h", "sig"])
    d5 = d[d.h == 5]
    res = []
    for coin, g in d5.groupby("coin"):
        row = {"coin": coin}
        for sig in ["mom", "rev", "near", "vol"]:
            x = g[[sig, "ex"]].dropna()
            row[sig] = stats.spearmanr(x[sig], x["ex"])[0]
        res.append(row)
    out["ic5_by_coin"] = pd.DataFrame(res).set_index("coin")
    res = []
    for y, g in d5.groupby("year"):
        row = {"year": y}
        for sig in ["mom", "rev", "near", "vol"]:
            x = g[[sig, "ex"]].dropna()
            row[sig] = stats.spearmanr(x[sig], x["ex"])[0] if len(x) > 10 else np.nan
        res.append(row)
    out["ic5_by_year"] = pd.DataFrame(res).set_index("year")
    return out
