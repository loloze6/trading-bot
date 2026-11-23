def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # daily returns by weekday of the return day, all bars, per coin and per year
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            ts = pd.to_datetime(b["timestamp"])
            b["r1"] = b["close"].pct_change()
            b["wd"] = ts.dt.weekday
            b["yr"] = ts.dt.year
            b["coin"] = coin; b["win"] = w
            b["r20"] = b["close"].pct_change(20)
            b["hi30"] = b["close"] / b["high"].rolling(30, min_periods=10).max() - 1
            b["absr1"] = b["r1"].abs()
            b["vol20"] = b["r1"].rolling(20).std()
            b["z1"] = b["r1"] / b["vol20"].shift(1)
            b["nx1"] = b["close"].shift(-1) / b["close"] - 1
            b["nx5"] = b["close"].shift(-5) / b["close"] - 1
            b["pos"] = np.arange(len(b))
            rows.append(b[["coin","win","r1","wd","yr","r20","hi30","z1","nx1","nx5","pos","vol20"]])
    df = pd.concat(rows)
    d = df.dropna(subset=["r1"])
    mu = d.groupby("coin")["r1"].transform("mean")
    d = d.assign(ex1=d["r1"] - mu)
    def tt(s): return s.mean() / (s.std() / np.sqrt(len(s)))
    out["r1_by_weekday"] = d.groupby("wd")["ex1"].agg(["mean","count",tt])
    wk = d.assign(weekend=d["wd"].isin([5,6]).astype(int))
    out["weekend_minus_weekday_by_coin"] = wk.groupby("coin").apply(lambda x: pd.Series({
        "diff": x[x.weekend==1].ex1.mean() - x[x.weekend==0].ex1.mean(),
        "t": stats.ttest_ind(x[x.weekend==1].ex1, x[x.weekend==0].ex1, equal_var=False).statistic}))
    out["weekend_minus_weekday_by_year"] = wk.groupby("yr").apply(lambda x: pd.Series({
        "diff": x[x.weekend==1].ex1.mean() - x[x.weekend==0].ex1.mean(),
        "t": stats.ttest_ind(x[x.weekend==1].ex1, x[x.weekend==0].ex1, equal_var=False).statistic}))
    # r20 momentum on 5-day grid, by coin and year
    g = df[(df["pos"] % 5 == 0)].dropna(subset=["nx5","r20"]).copy()
    g["ex5"] = g["nx5"] - g.groupby("coin")["nx5"].transform("mean")
    out["r20_slope_by_coin"] = g.groupby("coin").apply(lambda x: pd.Series({
        "t": (lambda s: s.slope/s.stderr)(stats.linregress(x["r20"], x["ex5"])), "n": len(x)}))
    out["r20_slope_by_year"] = g.groupby("yr").apply(lambda x: pd.Series({
        "t": (lambda s: s.slope/s.stderr)(stats.linregress(x["r20"], x["ex5"])), "n": len(x)}))
    g2 = g.dropna(subset=["hi30"])
    out["hi30_slope_by_year"] = g2.groupby("yr").apply(lambda x: pd.Series({
        "t": (lambda s: s.slope/s.stderr)(stats.linregress(x["hi30"], x["ex5"])), "n": len(x)}))
    # next-day reversal after large standardized days (z1), all bars (overlap-free at 1 day)
    z = d.dropna(subset=["z1","nx1"]).copy()
    z["exn"] = z["nx1"] - z.groupby("coin")["r1"].transform("mean")
    z["zq"] = pd.qcut(z["z1"].rank(method="first"), 7, labels=False)
    out["next_day_by_z1_septile"] = z.groupby("zq")["exn"].agg(["mean","count",tt])
    # book: largest gain/loss days vs coin
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"] = coin; bd.append(dd)
    bd = pd.concat(bd).dropna(subset=["book_return"])
    bd["wd"] = pd.to_datetime(bd["day"]).dt.weekday
    out["book_by_weekday"] = bd.groupby("wd")[["book_return","coin_return"]].mean()
    return out
