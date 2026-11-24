def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book decomposition
    drows = []
    for c, wd in data["days"].items():
        for w, d in wd.items():
            t = d[["day", "book_return", "coin_return"]].copy()
            t["coin"] = c; t["w"] = w
            drows.append(t)
    D = pd.concat(drows).dropna(subset=["book_return"])
    D["year"] = pd.to_datetime(D["day"]).dt.year
    D["wkday"] = pd.to_datetime(D["day"]).dt.weekday
    # position held: from bars
    brows = []
    for c, wb in data["bars"].items():
        for w, b in wb.items():
            b = b.copy()
            b["coin"] = c; b["w"] = w
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["ret"] = b["close"].pct_change()
            b["r1f"] = b["close"].shift(-1) / b["close"] - 1
            b["r2f"] = b["close"].shift(-2) / b["close"] - 1
            b["r14"] = b["close"] / b["close"].shift(14) - 1
            b["r3"] = b["close"] / b["close"].shift(3) - 1
            b["r7"] = b["close"] / b["close"].shift(7) - 1
            s20 = b["ret"].rolling(20).std(); s60 = b["ret"].rolling(60).std()
            b["vr"] = s20 / s60
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["r1f"]
            brows.append(b)
    B = pd.concat(brows)
    B["wd"] = B["ts"].dt.weekday
    B["year"] = B["ts"].dt.year
    coinmean = B.groupby("coin")["ret"].mean()
    B["mkt"] = B["pos"] * B["coin"].map(coinmean)
    out["bar gain total / market part / n bars in pos"] = pd.Series({
        "gain_sum": B["gain"].sum(), "mkt_sum": B["mkt"].sum(),
        "n_inpos": int((B["pos"].abs() > 1e-9).sum())})
    out["gain by coin"] = B.groupby("coin").agg(gain=("gain", "sum"), mkt=("mkt", "sum"),
                                              npos=("pos", lambda x: (x.abs() > 1e-9).sum()))
    out["gain by year"] = B.groupby("year").agg(gain=("gain", "sum"), mkt=("mkt", "sum"))
    out["gain by weekday held"] = B.groupby("wd").agg(gain=("gain", "sum"),
                                                     npos=("pos", lambda x: (x.abs() > 1e-9).sum()))
    # trades
    T = pd.concat([t.assign(coin=c) for c, wt in data["trades"].items() for w, t in wt.items()])
    tp = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": tp.mean(), "median": tp.median(),
                               "sum": tp.sum(), "top10_sum": tp.head(10).sum(),
                               "share_pos": (tp > 0).mean()})
    # ---- weekend effect: all Fridays, by vr regime and sign/quintile of r14
    drift2 = {}
    for c in B["coin"].unique():
        v = []
        for w, g in B[B.coin == c].groupby("w"):
            cl = g["close"].values
            v += list(cl[2::2] / cl[:-2:2] - 1)
        drift2[c] = np.mean(v)
    F = B[(B.wd == 4)].dropna(subset=["r2f", "r14", "vr"]).copy()
    F["u"] = F["r2f"] - F["coin"].map(drift2)
    F["hv"] = F["vr"] > 1
    F["up14"] = F["r14"] > 0
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["Fri weekend unusual by hv x up14"] = F.groupby(["hv", "up14"])["u"].apply(tt).unstack()
    F["q14"] = F.groupby("hv")["r14"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["Fri weekend unusual by hv x r14 quintile"] = F.groupby(["hv", "q14"])["u"].apply(tt).unstack()
    # any weekday, hv, r14>0: 2-day unusual (grid by window positions every 2)
    A = B.dropna(subset=["r2f", "r14", "vr"]).copy()
    A["u"] = A["r2f"] - A["coin"].map(drift2)
    out["all weekdays hv & up14, 2d unusual by weekday"] = A[(A.vr > 1) & (A.r14 > 0)].groupby("wd")["u"].apply(tt).unstack()
    out["all weekdays lowvol & up14 by weekday"] = A[(A.vr <= 1) & (A.r14 > 0)].groupby("wd")["u"].apply(tt).unstack()
    out["Fri all, by weekday-only: unusual"] = A.groupby("wd")["u"].apply(tt).unstack()
    out["Fri hv up14 by year"] = F[F.hv & F.up14].groupby("year")["u"].apply(tt).unstack()
    out["Fri hv up14 by coin"] = F[F.hv & F.up14].groupby("coin")["u"].apply(tt).unstack()
    return out
