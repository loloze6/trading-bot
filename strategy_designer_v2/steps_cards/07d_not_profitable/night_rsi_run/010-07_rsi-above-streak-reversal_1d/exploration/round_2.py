def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    col = "debug_info.components.rsi_above_age.last_history_value"
    allb = []
    for coin, wins in data["bars"].items():
        dd = pd.concat([d.assign(window=w) for w, d in data["days"][coin].items()])
        mu = dd["coin_return"].mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            df["ret1"] = df["close"].shift(-1) / df["close"] - 1
            df["fwd14"] = df["close"].shift(-14) / df["close"] - 1
            df["fwd7"] = df["close"].shift(-7) / df["close"] - 1
            df["past14"] = df["close"] / df["close"].shift(14) - 1
            df["past60"] = df["close"] / df["close"].shift(60) - 1
            df["pos"] = np.arange(len(df)); df["coin"] = coin; df["window"] = w
            df["mu"] = mu
            df["year"] = pd.to_datetime(df["timestamp"]).dt.year
            allb.append(df)
    A = pd.concat(allb)
    A["age"] = A[col]
    A["ex1"] = A["ret1"] - A["mu"]
    bins = [-61, -20, -5, 0, 5, 10, 20, 40, 61]
    A["agebin"] = pd.cut(A["age"], bins)
    def tt(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    out["daily excess ret by age bin (t, overlapping-free 1d)"] = A.groupby("agebin").agg(n=("ex1", "count"), ex1=("ex1", "mean"), t=("ex1", tt))
    g7 = A[(A["pos"] % 7 == 0) & A["fwd7"].notna()].copy()
    m7 = g7.groupby("coin")["fwd7"].transform("mean")
    g7["ex7"] = g7["fwd7"] - m7
    out["7d grid excess by age bin"] = g7.groupby("agebin").agg(n=("ex7", "count"), ex7=("ex7", "mean"), t=("ex7", tt))
    pos = A[A["age"] > 0]
    out["slope ex1 on age, age>0"] = pd.Series(dict(zip(["slope", "t"], [stats.linregress(pos["age"], pos["ex1"].fillna(0)).slope, stats.linregress(pos["age"], pos["ex1"].fillna(0)).slope / stats.linregress(pos["age"], pos["ex1"].fillna(0)).stderr])))
    # age>0 bars split by past60 trend
    p = pos.dropna(subset=["past60", "ex1"]).copy()
    p["p60q"] = pd.qcut(p["past60"], 4)
    p["gain"] = p["postRebalance_current_allocation"] * p["ret1"]
    out["age>0: ex1 and gain by past60 quartile"] = p.groupby("p60q").agg(n=("ex1", "count"), ex1=("ex1", "mean"), t=("ex1", tt), gain=("gain", "mean"))
    p["agelong"] = p["age"] > 20
    out["age>0: ex1 by past60 quartile x long run"] = p.groupby(["p60q", "agelong"]).agg(n=("ex1", "count"), ex1=("ex1", "mean"))
    out["age>0 ex1 by year"] = pos.groupby("year").agg(n=("ex1", "count"), ex1=("ex1", "mean"), t=("ex1", tt))
    # book drawdown on days
    D = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            D.append(d.assign(coin=coin, window=w))
    D = pd.concat(D)
    bd = D.groupby(["window", "day"])["book_return"].mean().dropna()
    eq = (1 + bd).cumprod(); dd_ = eq / eq.cummax() - 1
    out["book max fall"] = float(dd_.min())
    out["book daily sharpe"] = float(bd.mean() / bd.std() * np.sqrt(365))
    return out
