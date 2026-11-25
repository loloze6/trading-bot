def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    out = {}
    rows = []
    allrows = []
    drift = {}
    for coin, wins in bars.items():
        for H in (1, 3, 5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; lo = df["low"]; hi = df["high"]
            plow = lo.rolling(20).min().shift(1)
            phigh = hi.rolling(20).max().shift(1)
            depth = (c - plow) / plow * 100
            rngpos = (c - plow) / (phigh - plow)
            r60 = c / c.shift(60) - 1
            sd30 = c.pct_change().rolling(30).std()
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(0, n - 5, 5):
                d = {"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "depth": depth.iloc[i], "rpos": rngpos.iloc[i], "r60": r60.iloc[i], "sd30": sd30.iloc[i],
                     "fc": df["forecast"].iloc[i]}
                for H in (1, 3, 5, 10, 20):
                    if i + H < n:
                        d[f"ex{H}"] = -(c.iloc[i + H] / c.iloc[i] - 1 - drift[(coin, H)][0])
                        d[f"st{H}"] = d[f"ex{H}"] / drift[(coin, H)][1]
                allrows.append(d)
    A = pd.DataFrame(allrows)
    C = A[A["depth"] < 0].copy()

    def tday(s, days):
        x = pd.DataFrame({"v": s - s.mean(), "d": days}).dropna()
        g = x.groupby("d")["v"].sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return s.mean() / se if se > 0 else np.nan

    def summ(df, col="ex5"):
        d = df.dropna(subset=[col])
        return pd.Series({"n": len(d), "days": d["day"].nunique(), "mean": d[col].mean(),
                          "t_day": tday(d[col], d["day"]) if len(d) > 3 else np.nan, "hit": (d[col] > 0).mean()})

    out["cases by horizon"] = pd.DataFrame({H: summ(C, f"ex{H}") for H in (1, 3, 5, 10, 20)}).T
    out["by coin"] = C.groupby("coin").apply(summ)
    out["by year"] = C.groupby("year").apply(summ)
    C["dq"] = pd.qcut(C["depth"], 4, labels=["deepest", "q2", "q3", "shallow"])
    out["by depth quartile"] = C.groupby("dq").apply(summ)
    C["trend"] = np.where(C["r60"] > 0.1, "rising", np.where(C["r60"] < -0.1, "falling", "choppy"))
    out["by trend"] = C.groupby("trend").apply(summ)
    # all grid bars: range position quintile, excess rise (sign flip) at 5 days
    A["rq"] = pd.qcut(A["rpos"], 5, labels=False, duplicates="drop")
    out["all bars by range pos quintile (excess fall 5d)"] = A.groupby("rq").apply(summ)
    out["corr depth vs ex5"] = float(C[["depth", "ex5"]].dropna().corr().iloc[0, 1])
    return out
