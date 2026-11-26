def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    out = {}
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
            up = (c - phigh) / phigh * 100
            dn = (c - plow) / plow * 100
            rpos = (c - plow) / (phigh - plow)
            r60 = c / c.shift(60) - 1
            ret = c.pct_change()
            sd30 = ret.rolling(30).std()
            sdpct = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(0, n - 5, 5):
                d = {"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "up": up.iloc[i], "dn": dn.iloc[i], "rpos": rpos.iloc[i], "r60": r60.iloc[i],
                     "ag": sdpct.iloc[i]}
                for H in (1, 3, 5, 10, 20):
                    if i + H < n:
                        d[f"ex{H}"] = (c.iloc[i + H] / c.iloc[i] - 1 - drift[(coin, H)][0])
                        d[f"st{H}"] = d[f"ex{H}"] / drift[(coin, H)][1]
                allrows.append(d)
    A = pd.DataFrame(allrows)

    def tday(s, days):
        x = pd.DataFrame({"v": s - s.mean(), "d": days}).dropna()
        g = x.groupby("d")["v"].sum(); G = len(g)
        if G < 3: return np.nan
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return s.mean() / se if se > 0 else np.nan

    def summ(df, col="ex5"):
        d = df.dropna(subset=[col])
        return pd.Series({"n": len(d), "days": d["day"].nunique(), "mean_excess_rise": d[col].mean(),
                          "t_day": tday(d[col], d["day"]) if len(d) > 3 else np.nan,
                          "strength": d[col.replace("ex", "st")].mean()})

    U = A[A["up"] > 0].copy()
    out["upside breaks by horizon (excess rise)"] = pd.DataFrame({H: summ(U, f"ex{H}") for H in (1, 3, 5, 10, 20)}).T
    out["upside by year"] = U.groupby("year").apply(summ)
    out["upside by coin"] = U.groupby("coin").apply(summ)
    if len(U) >= 8:
        U["uq"] = pd.qcut(U["up"], 2, labels=["shallow", "deep"])
        out["upside by depth half"] = U.groupby("uq").apply(summ)
    A["trend"] = np.where(A["r60"] > 0.1, "rising", np.where(A["r60"] < -0.1, "falling", "choppy"))
    A["agit"] = np.where(A["ag"] > 0.5, "agitated", np.where(A["ag"].notna(), "calm", "na"))
    T = A[A["rpos"] >= A["rpos"].quantile(0.8)]
    out["top quintile rpos by trend"] = T.groupby("trend").apply(summ)
    out["top quintile rpos by agit"] = T.groupby("agit").apply(summ)
    out["top quintile rpos by year"] = T.groupby("year").apply(summ)
    out["top quintile rpos by horizon"] = pd.DataFrame({H: summ(T, f"ex{H}") for H in (1, 3, 5, 10, 20)}).T
    out["all bars rpos decile (excess rise 5d)"] = A.groupby(pd.qcut(A["rpos"], 10, labels=False, duplicates="drop")).apply(summ)
    B = A[A["dn"] < 0]
    out["downside breaks by agit (excess rise)"] = B.groupby("agit").apply(summ)
    out["corr rpos vs ex5 all"] = float(A[["rpos", "ex5"]].dropna().corr().iloc[0, 1])
    return out
