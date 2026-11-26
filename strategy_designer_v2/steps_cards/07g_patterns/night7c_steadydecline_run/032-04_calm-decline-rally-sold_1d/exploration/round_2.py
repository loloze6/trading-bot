def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            rng = (b["high"] - b["low"]) / c
            r28 = c / c.shift(28) - 1
            r1 = c / c.shift(1) - 1
            r3 = c / c.shift(3) - 1
            rr = rng.rolling(28).mean() / rng.rolling(120, min_periods=40).mean()
            sd1 = r1.rolling(60, min_periods=20).std()
            fwd = c.shift(-H) / c - 1
            for i in np.arange(0, n - H, H):
                allf.append(fwd.iloc[i])
                rows.append(dict(coin=coin, w=w, ts=pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                                 fwd=fwd.iloc[i], r28=r28.iloc[i], r1=r1.iloc[i], r3=r3.iloc[i],
                                 rr=rr.iloc[i], sd1=sd1.iloc[i],
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
        drift[coin] = np.nanmean(allf)
    df = pd.DataFrame(rows)
    df["un"] = df["fwd"] - df["coin"].map(drift)
    df["z1"] = df["r1"] / df["sd1"]
    df["z3"] = df["r3"] / (df["sd1"] * np.sqrt(3))
    df = df.dropna(subset=["un", "r28", "rr", "z1"])
    def dayt(g):
        s = g.groupby("ts")["un"].sum()
        nd = len(s); m = g["un"].mean()
        se = np.sqrt((s - g.groupby("ts")["un"].count() * m).pow(2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=nd, mean=m, t_day=m / se if se > 0 else np.nan))
    out = {}
    cu = df[(df.r28 > 0) & (df.rr <= 1)].copy()
    cu["q1"] = pd.qcut(cu["z1"].rank(method="first"), 5, labels=False)
    out["calmup_by_z1_quintile"] = cu.groupby("q1").apply(dayt)
    sl = stats.linregress(cu["z1"].clip(-3, 3), cu["un"])
    out["calmup_slope_un_on_z1"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(cu)))
    cu["q3"] = pd.qcut(cu["z3"].rank(method="first"), 5, labels=False)
    out["calmup_by_z3_quintile"] = cu.groupby("q3").apply(dayt)
    # compare to wide-range uptrend
    wu = df[(df.r28 > 0) & (df.rr > 1)].copy()
    sl2 = stats.linregress(wu["z1"].clip(-3, 3), wu["un"])
    out["wideup_slope_un_on_z1"] = pd.Series(dict(slope=sl2.slope, t=sl2.slope / sl2.stderr, n=len(wu)))
    alls = stats.linregress(df["z1"].clip(-3, 3), df["un"])
    out["all_slope_un_on_z1"] = pd.Series(dict(slope=alls.slope, t=alls.slope / alls.stderr, n=len(df)))
    # signed product: un * sign(r1) in calm up
    cu["dirun"] = cu["un"] * np.sign(cu["r1"])
    out["calmup_dir_by_coin"] = cu.groupby("coin")["dirun"].agg(["count", "mean"])
    out["calmup_dir_by_year"] = cu.groupby("yr")["dirun"].agg(["count", "mean"])
    out["calmup_dir_by_window"] = cu.groupby("w")["dirun"].agg(["count", "mean"])
    # calm decline graded by r28 depth (all days)
    cd = df[(df.r28 < 0) & (df.rr <= 1)]
    sl3 = stats.linregress(cd["r28"], cd["un"])
    out["calmdown_slope_un_on_r28"] = pd.Series(dict(slope=sl3.slope, t=sl3.slope / sl3.stderr, n=len(cd)))
    # book days: largest gains/losses by regime of coin trend
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin))
    B = pd.concat(bk).dropna(subset=["book_return"])
    act = B[B.book_return != 0]
    out["book_days_active"] = pd.Series(dict(n=len(act), mean=act.book_return.mean(),
                                             corr_coin=act.book_return.corr(act.coin_return)))
    return out
