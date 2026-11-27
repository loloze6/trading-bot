def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [2, 5, 10]
    # coin drift and usual move per horizon, non-overlapping, all visible windows
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
            sma = pd.Series(cl).rolling(20).mean().values
            sd = pd.Series(cl).pct_change().rolling(20).std().values
            raw = (cl / sma - 1) / sd
            fprev = np.r_[0, f[:-1]]
            n = len(b)
            for start in range(0, n, 5):
                for i in range(start, min(start + 5, n)):
                    if f[i] < 0 and (fprev[i] - f[i]) >= 2 and raw[i] < 0:
                        d = {"coin": c, "win": w, "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                             "absf": -f[i], "raw": raw[i], "day": i,
                             "dayts": str(pd.Timestamp(b["timestamp"].iloc[i]).date())}
                        r5 = cl[i+5:i+6]
                        # past returns
                        d["ret5past"] = cl[i] / cl[i-5] - 1 if i >= 5 else np.nan
                        for h in H:
                            if i + h < n:
                                tot = -(cl[i + h] / cl[i] - 1)
                                d[f"tot{h}"] = tot
                                d[f"un{h}"] = tot + drift[(c, h)]
                                d[f"st{h}"] = d[f"un{h}"] / usual[(c, h)]
                            else:
                                d[f"tot{h}"] = d[f"un{h}"] = d[f"st{h}"] = np.nan
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
            out[f"t{h}"] = tclust(g[f"un{h}"].dropna(), g.loc[s.index, "dayts"])
        out["tot5"] = g["tot5"].mean()
        return pd.Series(out)
    res = {}
    res["all"] = summ(df).to_frame().T
    res["by_coin"] = df.groupby("coin").apply(summ)
    res["by_year"] = df.groupby("year").apply(summ)
    df["rawq"] = pd.qcut(df["raw"], 4, labels=["deepest", "q2", "q3", "shallow"])
    res["by_raw_quartile"] = df.groupby("rawq").apply(summ)
    df["fq"] = pd.qcut(df["absf"].rank(method="first"), 4, labels=["f_low", "f2", "f3", "f_high"])
    res["by_forecast_quartile"] = df.groupby("fq").apply(summ)
    df["pastq"] = pd.qcut(df["ret5past"], 3, labels=["fell_most", "mid", "fell_least"])
    res["by_past5"] = df.groupby("pastq").apply(summ)
    res["corr_raw_un5"] = float(df[["raw", "un5"]].corr().iloc[0, 1])
    return res
