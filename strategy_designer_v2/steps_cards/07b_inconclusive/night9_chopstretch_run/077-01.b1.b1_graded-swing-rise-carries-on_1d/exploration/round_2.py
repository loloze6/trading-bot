def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30).std()
            raw = (c / c.shift(14) - 1) / (sd * np.sqrt(14))
            yr = pd.to_datetime(df["timestamp"]).dt.year
            h = 7
            fwd = c.shift(-h) / c - 1
            for i in range(0, len(df), h):
                rows.append(dict(coin=coin, w=w, i=i, year=yr[i], regime=df["regime"].iloc[i],
                                 fc=df["forecast"].iloc[i], raw=raw.iloc[i], fwd=fwd.iloc[i],
                                 usual=np.nan, day=str(df["timestamp"].iloc[i])[:10]))
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    stat = g.groupby("coin")["fwd"].agg(["mean", "std"])
    g = g.join(stat, on="coin")
    g["u"] = g["fwd"] - g["mean"]
    ip = g[(g.regime == "unknown")].dropna(subset=["raw"]).copy()
    out = {}
    def slope_t(d, x):
        d = d.dropna(subset=[x, "u"])
        if len(d) < 10: return (np.nan, np.nan, len(d))
        X = d[x].values; y = d["u"].values
        xm = X - X.mean(); b = (xm * (y - y.mean())).sum() / (xm ** 2).sum()
        res = y - y.mean() - b * xm
        s = pd.Series(res * xm).groupby(d["day"].values).sum()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (xm ** 2).sum()
        return (b, b / se, len(d))
    out["corr_fc_raw"] = float(ip[["fc", "raw"]].corr().iloc[0, 1])
    out["share_raw_pos_fc_zero"] = float(((ip.raw > 0) & (ip.fc <= 0)).sum() / max((ip.raw > 0).sum(), 1))
    out["share_raw_neg_fc_pos"] = float(((ip.raw < 0) & (ip.fc > 0)).sum() / max((ip.raw < 0).sum(), 1))
    def case_stats(d, sign):
        v = d["u"] * sign
        s = v.groupby(d["day"]).sum()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if len(s) > 2 else np.nan
        return pd.Series(dict(n=len(d), days=len(s), unusual=v.mean(), total=(d["fwd"] * sign).mean(),
                              strength=(v / d["std"]).mean(), t_days=t))
    out["cases"] = pd.DataFrame({
        "raw_pos_long": case_stats(ip[ip.raw > 0], 1),
        "raw_neg_short": case_stats(ip[ip.raw < 0], -1),
        "both_signed": case_stats(ip[ip.raw != 0], np.sign(ip.loc[ip.raw != 0, "raw"])),
        "raw_top_half_abs": case_stats(ip[ip.raw.abs() > ip.raw.abs().median()],
                                       np.sign(ip.loc[ip.raw.abs() > ip.raw.abs().median(), "raw"])),
        "fc_pos_long": case_stats(ip[ip.fc > 0], 1),
    }).T
    ip["fq"] = pd.qcut(ip["fc"].rank(method="first"), 4, labels=False)
    out["fc_quartiles"] = ip.groupby("fq").agg(fc=("fc", "mean"), raw=("raw", "mean"), u=("u", "mean"), n=("u", "size"))
    out["by_window_raw"] = ip.groupby("w").apply(lambda x: pd.Series(dict(zip(["slope", "t", "n"], slope_t(x, "raw")))))
    out["by_year_signed_u"] = ip.groupby("year").apply(lambda x: pd.Series(dict(
        n=len(x), signed_u=(x.u * np.sign(x.raw)).mean(), corr=x[["raw", "u"]].corr().iloc[0, 1])))
    return out
