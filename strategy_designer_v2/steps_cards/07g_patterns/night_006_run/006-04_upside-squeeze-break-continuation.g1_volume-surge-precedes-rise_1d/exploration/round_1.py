def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            vr = np.log(v.rolling(5).mean() / v.rolling(30).mean())
            rng5 = (h.rolling(5).max() / l.rolling(5).min() - 1)
            rng30 = (h.rolling(30).max() / l.rolling(30).min() - 1)
            comp = np.log(rng5 / rng30)
            vol20 = r1.rolling(20).std()
            ret3p = c / c.shift(3) - 1
            ret10p = c / c.shift(10) - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - 3, 3):
                rows.append(dict(coin=coin, win=w, fc=b["forecast"].iloc[i],
                                 fwd=c.iloc[i+3]/c.iloc[i]-1, vr=vr.iloc[i], comp=comp.iloc[i],
                                 vol=vol20.iloc[i], r3=ret3p.iloc[i], r10=ret10p.iloc[i],
                                 r1=r1.iloc[i], wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year,
                                 absfwd=abs(c.iloc[i+3]/c.iloc[i]-1)))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def binned(col, q=5, y="ex"):
        d = g.dropna(subset=[col, y]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("b")[y].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    out["fc_bins_ex"] = binned("fc", 5)
    out["vr_bins_ex"] = binned("vr", 5)
    out["vr_bins_absfwd"] = binned("vr", 5, "absfwd")
    out["comp_bins_absfwd"] = binned("comp", 5, "absfwd")
    out["comp_bins_ex"] = binned("comp", 5)
    out["r3_bins_ex"] = binned("r3", 5)
    out["r10_bins_ex"] = binned("r10", 5)
    out["vol_bins_ex"] = binned("vol", 5)
    out["vol_bins_absfwd"] = binned("vol", 5, "absfwd")
    wd = g.groupby("wd")["ex"].agg(["mean", "count"]); out["weekday_ex"] = wd.round(4)
    # per coin slope of ex on vr
    pc = {}
    for coin, d in g.dropna(subset=["vr"]).groupby("coin"):
        s = stats.linregress(d["vr"], d["ex"]); pc[coin] = [round(s.slope, 4), round(s.slope/s.stderr, 2), len(d)]
    out["per_coin_vr_slope_t_n"] = pd.DataFrame(pc, index=["slope", "t", "n"]).T
    # interaction: vr high with prior r3 sign
    d = g.dropna(subset=["vr", "r3"]).copy()
    d["vrhi"] = d["vr"] > d.groupby("coin")["vr"].transform("median")
    d["up"] = d["r3"] > 0
    out["vrhi_x_up_ex"] = d.groupby(["vrhi", "up"])["ex"].agg(["mean", "count"]).round(4)
    out["year_fc_pos_ex"] = g[g.fc > 0].groupby("yr")["ex"].agg(["mean", "count"]).round(4)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    D = pd.concat(dd)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book_extreme_days_coinret"] = pd.DataFrame({
        "worst2pct": bk[bk.book_return <= q.iloc[0]].mean(),
        "best2pct": bk[bk.book_return >= q.iloc[1]].mean()}).round(4)
    out["book_by_win"] = bk.groupby("win")["book_return"].agg(["mean", "std", "count"]).round(5)
    return out
