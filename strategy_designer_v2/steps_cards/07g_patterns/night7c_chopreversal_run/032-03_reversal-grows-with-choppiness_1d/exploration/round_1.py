import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    daily = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            std30 = r.rolling(30, min_periods=20).std()
            ret7 = c / c.shift(7) - 1
            ret30 = c / c.shift(30) - 1
            ret3 = c / c.shift(3) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            volratio = std30 / r.rolling(90, min_periods=60).std()
            hl = ((df["high"] - df["low"]) / c).rolling(7).mean() / ((df["high"] - df["low"]) / c).rolling(60, min_periods=30).mean()
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df), 7):
                if i + 7 >= len(df): break
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), fwd7=fwd7.iloc[i],
                                 s7=ret7.iloc[i] / (std30.iloc[i] * np.sqrt(7)) if std30.iloc[i] > 0 else np.nan,
                                 s30=ret30.iloc[i] / (std30.iloc[i] * np.sqrt(30)) if std30.iloc[i] > 0 else np.nan,
                                 s3=ret3.iloc[i] / (std30.iloc[i] * np.sqrt(3)) if std30.iloc[i] > 0 else np.nan,
                                 er=er.iloc[i], vr=volratio.iloc[i], hl=hl.iloc[i], std30=std30.iloc[i],
                                 fc=df["forecast"].iloc[i]))
            for i in range(len(df) - 1):
                daily.append(dict(coin=coin, w=w, wd=ts.iloc[i].dayofweek, r1=r.iloc[i], fwd1=fwd1.iloc[i],
                                  z1=r.iloc[i] / std30.iloc[i] if std30.iloc[i] > 0 else np.nan,
                                  bk=df["postRebalance_total_value"].iloc[i+1] / df["postRebalance_total_value"].iloc[i] - 1,
                                  alloc=df["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd7"] - g.groupby("coin")["fwd7"].transform("mean")
    g["exs"] = g["ex"] / (g["std30"] * np.sqrt(7))
    d = pd.DataFrame(daily)

    def slope(sub, x, y="exs"):
        sub = sub.dropna(subset=[x, y])
        if len(sub) < 30: return (np.nan, np.nan, len(sub))
        X = sub[x] - sub[x].mean(); b = (X * sub[y]).sum() / (X**2).sum()
        e = sub[y] - sub[y].mean() - b * X
        sc = (X * e).groupby(sub["day"]).sum()
        G = len(sc); se = np.sqrt((sc**2).sum() * G / (G - 1)) / (X**2).sum()
        return (b, b / se, len(sub))

    out = {}
    res = {}
    for x in ["s3", "s7", "s30", "fc"]:
        res[x] = slope(g, x)
    out["slope scaled fwd7 on x (b,t,n)"] = pd.DataFrame(res, index=["b", "t", "n"]).T
    tab = {}
    for nm, col in [("er", "er"), ("vr", "vr"), ("hl", "hl")]:
        q = pd.qcut(g[col], 3, labels=["lo", "mid", "hi"])
        for lv in ["lo", "mid", "hi"]:
            tab[f"s7|{nm}_{lv}"] = slope(g[q == lv], "s7")
            tab[f"s30|{nm}_{lv}"] = slope(g[q == lv], "s30")
    out["slopes by regime tercile"] = pd.DataFrame(tab, index=["b", "t", "n"]).T
    g["s7b"] = pd.qcut(g["s7"], 5, labels=False)
    out["fwd7 excess by s7 quintile"] = g.groupby("s7b").agg(n=("ex", "size"), mean=("ex", "mean"), s7=("s7", "mean"))
    g["s30b"] = pd.qcut(g["s30"], 5, labels=False)
    out["fwd7 excess by s30 quintile"] = g.groupby("s30b").agg(n=("ex", "size"), mean=("ex", "mean"))
    out["slope by window s7"] = pd.DataFrame({w: slope(s, "s7") for w, s in g.groupby("w")}, index=["b", "t", "n"]).T
    out["slope by window s30"] = pd.DataFrame({w: slope(s, "s30") for w, s in g.groupby("w")}, index=["b", "t", "n"]).T
    d["exr"] = d["fwd1"] - d.groupby("coin")["fwd1"].transform("mean")
    out["weekday next-day return"] = d.groupby("wd")["fwd1"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    d["zb"] = pd.qcut(d["z1"], 5, labels=False)
    out["next day by z1 quintile"] = d.groupby("zb")["exr"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["book by coin"] = d.groupby("coin")["bk"].agg(["mean", "std"])
    out["book mean by abs alloc tercile"] = d.groupby(pd.qcut(d["alloc"].abs(), 3, labels=False))["bk"].mean()
    return out
