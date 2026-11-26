def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 2, 3, 5]
    drift = {}
    for c in bars:
        drift[c] = {}
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[c][h] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(30).std()
            z = (r1 / sd).values
            f = b["forecast"].values
            reg = b["regime"].values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(b)
            for s in range(0, n, 3):
                for i in range(s, min(s + 3, n)):
                    if f[i] <= -2:
                        d = {"coin": c, "win": w, "year": yr[i], "f": -f[i], "z": z[i],
                             "day": str(b["timestamp"].iloc[i])[:10]}
                        for h in H:
                            d["u%d" % h] = -(cl[i + h] / cl[i] - 1 - drift[c][h]) if i + h < n else np.nan
                            d["t%d" % h] = -(cl[i + h] / cl[i] - 1) if i + h < n else np.nan
                        rows.append(d)
                        break
    df = pd.DataFrame(rows)
    def ct(x, days):
        m = pd.DataFrame({"x": x, "d": days}).dropna()
        dev = m["x"] - m["x"].mean()
        s = dev.groupby(m["d"]).sum()
        return m["x"].mean() / (np.sqrt((s ** 2).sum()) / len(m)) if len(m) > 2 else np.nan
    def summ(g):
        out = {"n": len(g), "days": g["day"].nunique()}
        for h in H:
            out["u%d" % h] = g["u%d" % h].mean()
            out["t_u%d" % h] = ct(g["u%d" % h].values, g["day"].values)
        out["tot3"] = g["t3"].mean()
        return pd.Series(out)
    res = {}
    res["all"] = summ(df).to_frame().T
    res["by_coin"] = df.groupby("coin").apply(summ)
    res["by_window"] = df.groupby("win").apply(summ)
    res["by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["f"], 4, labels=False, duplicates="drop")
    res["by_forecast_q"] = df.groupby("fq").apply(summ)
    df["zq"] = pd.qcut(df["z"], 4, labels=False, duplicates="drop")
    res["by_z_q"] = df.groupby("zq").apply(summ)
    from scipy import stats
    sl = {}
    for h in H:
        m = df[["z", "u%d" % h]].dropna()
        r = stats.linregress(m["z"], m["u%d" % h])
        sl["z_slope_u%d" % h] = r.slope; sl["z_slope_t%d" % h] = r.slope / r.stderr
    res["slopes"] = pd.Series(sl)
    return res
