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
                "p10": (c.shift(1) / c.shift(11) - 1) / (sd.shift(1) * np.sqrt(10)),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "day": ts.dt.floor("D"), "year": ts.dt.year}))
    D = pd.concat(rows, ignore_index=True)
    D["m"] = D["coin"].map(coinmean)
    A = D[D.fc < 0].dropna(subset=["f1", "rise", "p5"]).copy()
    A["x1"] = -(A.f1 - A.m)
    A["x2"] = -(A.f2 - 2 * A.m)
    lo, hi = A.x1.quantile([0.01, 0.99])
    A["x1w"] = A.x1.clip(lo, hi)
    def slope_t(x, y, day):
        x = x - x.mean()
        b = (x * y).sum() / (x * x).sum()
        e = y - y.mean() - b * x
        g = (x * e).groupby(day).sum()
        se = np.sqrt((g ** 2).sum()) / (x * x).sum()
        return b, b / se
    res = {}
    for name, s, xv, yv in [
        ("depth_all_raw", A, -A.p5, "x1"),
        ("depth_all_wins", A, -A.p5, "x1w"),
        ("depth_rank_wins", A, -A.p5.rank(pct=True), "x1w"),
        ("rise_rank_wins", A, A.rise.rank(pct=True), "x1w"),
        ("fc_rank_wins", A, (-A.fc).rank(pct=True), "x1w"),
        ("depth10_wins", A.dropna(subset=["p10"]), -A.dropna(subset=["p10"]).p10, "x1w"),
    ]:
        b, t = slope_t(xv.loc[s.index], s[yv], s["day"])
        res[name] = {"slope": b, "t_day": t, "n": len(s)}
    small = A[A.rise <= A.rise.quantile(0.75)]
    b, t = slope_t(-small.p5, small.x1w, small.day); res["depth_rise_le_q75_wins"] = {"slope": b, "t_day": t, "n": len(small)}
    out = {"slopes": pd.DataFrame(res).T}
    A["dq"] = pd.qcut(A.p5, 3, labels=["deep", "mid", "shallow"])
    tt = {}
    for k, s in A.groupby("dq"):
        g = s.groupby("day")["x1w"].sum(); n = len(s)
        tt[k] = {"x1w": s.x1w.mean(), "t_day": s.x1w.mean() / (g.std() * np.sqrt(len(g)) / n), "x2": s.x2.mean(), "n": n}
    out["by_depth_tercile"] = pd.DataFrame(tt).T
    out["deep_half_by_year"] = A[A.p5 <= A.p5.median()].groupby("year").agg(x1=("x1", "mean"), n=("x1", "size"))
    g = A.groupby("day")["x1w"].sum(); n = len(A)
    out["all_wins_mean_t"] = pd.Series({"mean": A.x1w.mean(), "t": A.x1w.mean() / (g.std() * np.sqrt(len(g)) / n)})
    return out
