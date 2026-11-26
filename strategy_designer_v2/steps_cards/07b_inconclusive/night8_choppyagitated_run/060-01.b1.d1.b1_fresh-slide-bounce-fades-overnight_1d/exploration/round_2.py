def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    coinmean = {}
    for coin, ws in bars.items():
        allr = [df["close"].astype(float).reset_index(drop=True).pct_change().dropna() for w, df in ws.items()]
        coinmean[coin] = pd.concat(allr).mean()
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "fc": df["forecast"].astype(float),
                "rise": r / sd, "p5": (c.shift(1) / c.shift(6) - 1) / (sd.shift(1) * np.sqrt(5)),
                "f1": c.shift(-1) / c - 1, "day": ts.dt.floor("D"), "year": ts.dt.year,
                "p1": r.shift(1) / sd.shift(1)}))
    D = pd.concat(rows, ignore_index=True)
    D["m"] = D["coin"].map(coinmean)
    A = D[D.fc < 0].dropna(subset=["f1", "rise", "p5"]).copy()
    A["x1"] = -(A.f1 - A.m)
    out = {}
    def slope_t(x, y, day):
        x = x - x.mean()
        b = (x * y).sum() / (x * x).sum()
        e = y - y.mean() - b * x
        g = (x * e).groupby(day).sum()
        se = np.sqrt((g ** 2).sum()) / (x * x).sum()
        return b, b / se
    res = {}
    for var in ["rise", "p5", "p1"]:
        s = A.dropna(subset=[var])
        b, t = slope_t(-s[var] if var != "rise" else s[var], s["x1"], s["day"])
        res[var] = {"slope_x1_on_size": b, "t_day": t, "n": len(s)}
    s = A[A.rise <= A.rise.quantile(0.75)]
    b, t = slope_t(s["rise"], s["x1"], s["day"]); res["rise_below_q75"] = {"slope_x1_on_size": b, "t_day": t, "n": len(s)}
    s = A[A.rise <= 1.0]
    b, t = slope_t(s["rise"], s["x1"], s["day"]); res["rise_le_1sd"] = {"slope_x1_on_size": b, "t_day": t, "n": len(s)}
    out["slopes"] = pd.DataFrame(res).T
    A["rq"] = pd.cut(A.rise, [0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 10])
    out["by_rise_bin"] = A.groupby("rq").agg(x1=("x1", "mean"), sd=("x1", "std"), n=("x1", "size"))
    A["pq"] = pd.cut(A.p5, [-10, -2, -1.5, -1.0, -0.6, -0.3, 0])
    out["by_p5_bin"] = A.groupby("pq").agg(x1=("x1", "mean"), sd=("x1", "std"), n=("x1", "size"))
    A["deepq"] = pd.qcut(A.p5, 2, labels=["deep", "shallow"])
    A["riseq"] = pd.qcut(A.rise, 2, labels=["small", "large"])
    out["deep_x_rise"] = A.pivot_table(index="deepq", columns="riseq", values="x1", aggfunc="mean")
    out["deep_x_rise_n"] = A.pivot_table(index="deepq", columns="riseq", values="x1", aggfunc="size")
    # t of mean, day-clustered, by p5 half
    tt = {}
    for k, s in A.groupby("deepq"):
        g = s.groupby("day")["x1"].sum(); n = len(s)
        tt[k] = {"mean": s.x1.mean(), "t_day": s.x1.mean() / (g.std() * np.sqrt(len(g)) / n), "n": n, "days": len(g)}
    out["mean_by_depth_half"] = pd.DataFrame(tt).T
    return out
