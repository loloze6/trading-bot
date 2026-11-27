def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [2, 5, 10]
    drift = {}; usual = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            rs = np.array(rs)
            drift[(c, h)] = rs.mean() if len(rs) else np.nan
            usual[(c, h)] = rs.std() if len(rs) else np.nan
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            f = b["forecast"].fillna(0).values
            s = pd.Series(cl)
            sma = s.rolling(20).mean().values
            rets = s.pct_change()
            sd = rets.rolling(20).std().values
            raw = (cl / sma - 1) / sd
            sd5 = rets.rolling(5).std().values
            ret20 = (s / s.shift(20) - 1).values
            ret60 = (s / s.shift(60) - 1).values
            low20 = s.rolling(20).min().values
            fprev = np.r_[0, f[:-1]]
            n = len(b)
            for start in range(0, n, 5):
                for i in range(start, min(start + 5, n)):
                    if f[i] < 0 and (fprev[i] - f[i]) >= 2 and raw[i] < 0:
                        d = {"coin": c, "win": w, "absf": -f[i], "raw": raw[i],
                             "dayts": str(pd.Timestamp(b["timestamp"].iloc[i]).date()),
                             "ret20": ret20[i], "ret60": ret60[i],
                             "vol_ratio": sd5[i] / sd[i] if sd[i] > 0 else np.nan,
                             "at_low": cl[i] / low20[i] - 1,
                             "ret1": rets.values[i]}
                        for h in H:
                            if i + h < n:
                                tot = -(cl[i + h] / cl[i] - 1)
                                d[f"un{h}"] = tot + drift[(c, h)]
                            else:
                                d[f"un{h}"] = np.nan
                        rows.append(d)
                        break
    df = pd.DataFrame(rows)
    def tclust(s, days):
        x = pd.DataFrame({"v": s - s.mean(), "d": days}).dropna()
        g = x.groupby("d")["v"].sum()
        D = len(g)
        if D < 3: return np.nan
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(x)
        return s.mean() / se
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            s = g[f"un{h}"].dropna()
            out[f"un{h}"] = s.mean()
            out[f"t{h}"] = tclust(s, g.loc[s.index, "dayts"])
        out["med5"] = g["un5"].median()
        out["pos5"] = (g["un5"] > 0).mean()
        return pd.Series(out)
    res = {}
    for col, lab in [("ret60", "by_ret60"), ("ret20", "by_ret20"), ("vol_ratio", "by_vol_ratio"),
                     ("at_low", "by_dist_from_20d_low"), ("ret1", "by_last_day_ret"), ("absf", "by_absf_terc")]:
        q = pd.qcut(df[col].rank(method="first"), 3, labels=["low", "mid", "high"])
        res[lab] = df.groupby(q).apply(summ)
    res["corr"] = df[["raw", "absf", "ret20", "ret60", "vol_ratio", "at_low", "ret1", "un5"]].corr()["un5"].to_frame()
    res["by_win"] = df.groupby("win").apply(summ)
    return res
