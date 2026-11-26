def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 2, 3]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ret = pd.Series(c).pct_change()
            sd = ret.rolling(30, min_periods=20).std()
            sr = (ret / sd).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            # grid of 1 bar for the 1-day horizon: every bar is its own cell
            for i in range(n - 1):
                if f[i] <= -2:
                    r = {"coin": coin, "win": w, "year": yr[i], "fc": -f[i], "sr": sr[i],
                         "day": str(df["timestamp"].iloc[i])[:10], "grid": "h1"}
                    r["u1"] = -(c[i + 1] / c[i] - 1 - drift[(coin, 1)])
                    r["t1"] = -(c[i + 1] / c[i] - 1)
                    r["u2"] = -(c[i + 2] / c[i + 1] - 1 - drift[(coin, 1)]) if i + 2 < n else np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    def tclust(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna()
        m = x["v"].mean()
        g = (x["v"] - m).groupby(x["d"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return m, m / se, G, len(x)
    out = {}
    m, t, G, n = tclust(d["u1"], d["day"])
    m2, t2, G2, n2 = tclust(d["u2"], d["day"])
    out["h1_all"] = pd.DataFrame([{"u1": m, "t": t, "days": G, "n": n, "total1": d["t1"].mean(),
                                    "u_day2_only": m2, "t_day2": t2}])
    def grp(key):
        res = []
        for k, g in d.groupby(key):
            m, t, G, n = tclust(g["u1"], g["day"])
            res.append({key: str(k), "n": n, "days": G, "u1": m, "t": t, "total1": g["t1"].mean()})
        return pd.DataFrame(res)
    med = d["fc"].median()
    d["fc_half"] = np.where(d["fc"] > med, "large", "small")
    out["h1_fc_half"] = grp("fc_half")
    meds = d["sr"].median()
    d["sr_half"] = np.where(d["sr"] > meds, "large", "small")
    out["h1_sr_half"] = grp("sr_half")
    d["srbin"] = pd.cut(d["sr"], [0, 0.25, 0.5, 0.75, 1.0])
    out["h1_sr_bin"] = grp("srbin")
    out["h1_year"] = grp("year")
    out["h1_coin"] = grp("coin")
    out["corr_sr_u1"] = float(d[["sr", "u1"]].dropna().corr().iloc[0, 1])
    out["corr_fc_u1"] = float(d[["fc", "u1"]].dropna().corr().iloc[0, 1])
    return out
