import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 120
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin drift per horizon, non-overlapping
        drift = {}
        sds = {}
        for h in (24, 48, 120, 240):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rs) if rs else np.nan
            sds[h] = np.std(rs) if rs else np.nan
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            prevf = np.r_[0, f[:-1]]
            sig = (prevf - f) >= 2
            # 30-day trend before signal (720 bars)
            seen = set()
            for i in np.where(sig)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                     "f": f[i], "hour": ts.iloc[i].hour}
                for h in (24, 48, 120, 240):
                    if i + h < n:
                        r[f"m{h}"] = -(c[i + h] / c[i] - 1 - drift[h])
                        r[f"s{h}"] = r[f"m{h}"] / sds[h]
                    else:
                        r[f"m{h}"] = np.nan
                r["tr30"] = c[i] / c[i - 720] - 1 if i >= 720 else np.nan
                r["tr90"] = c[i] / c[i - 2160] - 1 if i >= 2160 else np.nan
                r["d24"] = c[i] / c[i - 24] - 1 if i >= 24 else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    d["big"] = d["coin"].isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])
    def agg(g):
        x = g["m120"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "m24": g["m24"].mean(), "m48": g["m48"].mean(), "m240": g["m240"].mean()})
    out = {}
    out["overall"] = agg(d)
    hz = {}
    for h in (24, 48, 120, 240):
        x = d[f"m{h}"].dropna()
        hz[h] = [len(x), x.mean(), x.mean() / (x.std() / np.sqrt(len(x))), d[f"s{h}"].mean()]
    out["by_horizon"] = pd.DataFrame(hz, index=["n", "mean", "t", "strength"]).T
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 5, labels=False)  # 0 = most negative
    out["by_depth_quintile"] = d.groupby("fq").apply(agg)
    d["trq"] = pd.qcut(d["tr30"], 4, labels=False)
    out["by_30d_trend_q"] = d.groupby("trq").apply(agg)
    d["t90s"] = np.sign(d["tr90"])
    out["by_90d_trend_sign"] = d.groupby("t90s").apply(agg)
    d["sq"] = pd.qcut(d["d24"], 4, labels=False)
    out["by_surge_size_q"] = d.groupby("sq").apply(agg)
    out["default_vs_new"] = d.groupby("big").apply(agg)
    return out
