def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 7
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r1 = c.pct_change()
            b["ret1"] = r1
            b["ret3p"] = c / c.shift(3) - 1
            b["ret14p"] = c / c.shift(14) - 1
            b["ret60p"] = c / c.shift(60) - 1
            b["vol60"] = r1.rolling(60, min_periods=20).std()
            b["ret1z"] = r1 / b["vol60"]
            b["fwd7"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd3"] = c.shift(-3) / c - 1
            b["share"] = b["debug_info.components.rsi_share.last_history_value"]
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    g = df[df.pos % H == 0].copy()
    cm = g.groupby("coin")["fwd7"].mean()
    g["fwd7x"] = g["fwd7"] - g["coin"].map(cm)
    g = g.dropna(subset=["fwd7x"])
    # pooled OLS t for several predictors
    res = []
    for col in ["share", "ret1", "ret1z", "ret3p", "ret14p", "ret60p"]:
        s = g.dropna(subset=[col])
        x = s.groupby("coin")[col].transform(lambda v: (v - v.mean()) / v.std())
        lr = stats.linregress(x, s["fwd7x"])
        res.append((col, lr.slope, lr.slope / lr.stderr, len(s)))
    out["ols_fwd7x_on_z"] = pd.DataFrame(res, columns=["col", "slope", "t", "n"])
    # share effect within long-term trend regime (ret60p sign)
    s = g.dropna(subset=["share", "ret60p"]).copy()
    s["trend"] = np.where(s.ret60p > 0, "up60", "down60")
    rr = []
    for k, q in s.groupby("trend"):
        lr = stats.linregress(q["share"], q["fwd7x"])
        rr.append((k, lr.slope, lr.slope / lr.stderr, len(q), q.fwd7x.mean()))
    out["share_slope_by_60d_trend"] = pd.DataFrame(rr, columns=["trend", "slope", "t", "n", "mean_fwd7x"])
    # book decomposition by side, per coin, daily
    df["gain"] = df["alloc"] * df["fwd1"]
    mu = df.groupby("coin")["fwd1"].mean()
    df["mkt"] = df["alloc"] * df["coin"].map(mu)
    df["timing"] = df["gain"] - df["mkt"]
    df["side"] = np.sign(df["alloc"])
    out["timing_by_side"] = df.dropna(subset=["gain"]).groupby("side")[["gain", "mkt", "timing"]].agg(["mean"]).assign(
        n=df.dropna(subset=["gain"]).groupby("side").size())
    # short side: fwd1 when short by 60d trend
    df["trend"] = np.where(df.ret60p > 0, "up60", np.where(df.ret60p <= 0, "down60", "na"))
    t2 = df.dropna(subset=["gain"]).groupby(["trend", "side"])["gain"].agg(["mean", "count", "std"])
    t2["t"] = t2["mean"] / (t2["std"] / np.sqrt(t2["count"]))
    out["gain_by_trend_side"] = t2
    # volatility: abs fwd7 after large |ret1z|
    s = g.dropna(subset=["ret1z"]).copy()
    s["absz_q"] = s.groupby("coin")["ret1z"].transform(lambda v: pd.qcut(v.abs().rank(method="first"), 5, labels=False))
    s["absfwd"] = s["fwd7"].abs()
    out["absfwd7_by_absret1z_q"] = s.groupby("absz_q")[["absfwd", "fwd7x"]].mean().assign(n=s.groupby("absz_q").size())
    # book largest days: what preceded
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk.book_return.quantile([0.05, 0.95])
    out["book_tail_coin_ret"] = pd.DataFrame({
        "worst5pct_book": bk[bk.book_return <= q[0.05]].mean(),
        "best5pct_book": bk[bk.book_return >= q[0.95]].mean()})
    # weekday test split by year halves
    df["wd"] = pd.to_datetime(df["timestamp"]).dt.weekday
    df["yr"] = pd.to_datetime(df["timestamp"]).dt.year
    df["early"] = df["yr"] <= df["yr"].median()
    wt = df.dropna(subset=["fwd1"]).groupby(["early", "wd"])["fwd1"].agg(["mean", "count", "std"])
    wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["count"]))
    out["fwd1_weekday_by_half"] = wt[["mean", "count", "t"]]
    return out
