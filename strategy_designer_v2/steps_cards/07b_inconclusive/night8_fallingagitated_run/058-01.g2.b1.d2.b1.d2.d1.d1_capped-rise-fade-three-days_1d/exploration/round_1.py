def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 2, 3, 5, 7, 10]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            usual[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 2 else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ret = pd.Series(c).pct_change()
            sd = ret.rolling(30, min_periods=20).std()
            sr = (ret / sd).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for start in range(0, n, 3):
                for i in range(start, min(start + 3, n)):
                    if f[i] <= -2:
                        r = {"coin": coin, "win": w, "year": yr[i], "fc": -f[i], "sr": sr[i],
                             "day": str(df["timestamp"].iloc[i])[:10]}
                        for h in H:
                            if i + h < n:
                                r[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[(coin, h)])
                                r[f"t{h}"] = -(c[i + h] / c[i] - 1)
                            else:
                                r[f"u{h}"] = np.nan; r[f"t{h}"] = np.nan
                        rows.append(r)
                        break
    d = pd.DataFrame(rows)
    out = {}
    def tclust(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna()
        m = x["v"].mean()
        g = (x["v"] - m).groupby(x["d"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return m, m / se, G, len(x)
    hz = []
    for h in H:
        m, t, G, n = tclust(d[f"u{h}"], d["day"])
        mt = d[f"t{h}"].mean()
        hz.append({"h": h, "unusual": m, "t": t, "days": G, "n": n, "total": mt})
    out["by_horizon"] = pd.DataFrame(hz)
    def grp(key):
        res = []
        for k, g in d.groupby(key):
            m, t, G, n = tclust(g["u3"], g["day"])
            res.append({key: k, "n": n, "days": G, "u3": m, "t": t, "u1": g["u1"].mean(), "u5": g["u5"].mean(), "total3": g["t3"].mean()})
        return pd.DataFrame(res)
    out["by_coin"] = grp("coin")
    out["by_win"] = grp("win")
    out["by_year"] = grp("year")
    d["srbin"] = pd.cut(d["sr"], [-10, 0, 0.25, 0.5, 0.75, 1.0, 10])
    out["by_sr"] = grp("srbin").astype(str)
    d["fcq"] = pd.qcut(d["fc"], 4, labels=False)
    out["by_fc_quart"] = grp("fcq")
    return out
