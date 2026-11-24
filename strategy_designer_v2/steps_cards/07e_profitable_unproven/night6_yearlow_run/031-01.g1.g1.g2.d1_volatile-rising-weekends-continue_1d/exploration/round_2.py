def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    brows = []
    for c, wb in data["bars"].items():
        for w, b in wb.items():
            b = b.copy(); b["coin"] = c; b["w"] = w
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["ret"] = b["close"].pct_change()
            b["r2f"] = b["close"].shift(-2) / b["close"] - 1
            for L in (3, 7, 14, 28):
                b[f"r{L}"] = b["close"] / b["close"].shift(L) - 1
            b["vr"] = b["ret"].rolling(20).std() / b["ret"].rolling(60).std()
            b["s60"] = b["ret"].rolling(60).std()
            b["pos"] = b["postRebalance_current_allocation"]
            brows.append(b)
    B = pd.concat(brows)
    B["wd"] = B["ts"].dt.weekday
    B["day"] = B["ts"].dt.floor("D")
    drift2 = {}
    for c in B["coin"].unique():
        v = []
        for w, g in B[B.coin == c].groupby("w"):
            cl = g["close"].values
            v += list(cl[2::2] / cl[:-2:2] - 1)
        drift2[c] = np.mean(v)
    sd2 = {}
    for c in B["coin"].unique():
        v = []
        for w, g in B[B.coin == c].groupby("w"):
            cl = g["close"].values
            v += list(cl[2::2] / cl[:-2:2] - 1)
        sd2[c] = np.std(v, ddof=1)
    B["u"] = B["r2f"] - B["coin"].map(drift2)
    def ct(df, col="u"):
        df = df.dropna(subset=[col])
        g = df.groupby("day")[col].sum()
        n = len(df); m = df[col].mean()
        dev = df[col] - m
        gd = dev.groupby(df["day"]).sum()
        se = np.sqrt((gd ** 2).sum()) / n
        return pd.Series({"n": n, "days": df["day"].nunique(), "mean": m, "t_cl": m / se if se > 0 else np.nan})
    F = B[B.wd == 4].dropna(subset=["r2f", "r14", "vr", "s60"]).copy()
    # standardised lookback returns (per coin, by 60d vol * sqrt(L))
    for L in (3, 7, 14, 28):
        F[f"z{L}"] = F[f"r{L}"] / (F["s60"] * np.sqrt(L))
    # rank-correlation and regression of u on z for all Fridays
    rows = {}
    for L in (3, 7, 14, 28):
        x = F[f"z{L}"]; y = F["u"] / F["coin"].map(sd2)
        ok = x.notna() & y.notna()
        sl = stats.linregress(x[ok], y[ok])
        rows[f"z{L}"] = {"spearman": stats.spearmanr(x[ok], y[ok])[0], "slope": sl.slope, "t_slope": sl.slope / sl.stderr, "n": ok.sum()}
    out["Fri: u/usual vs standardised L-day return"] = pd.DataFrame(rows).T
    # quintiles of z14 across all Fridays, clustered t
    F["q"] = pd.qcut(F["z14"], 5, labels=False)
    out["Fri z14 quintile, clustered"] = F.groupby("q").apply(ct)
    # long/short sides clustered
    out["Fri r14>0 clustered"] = ct(F[F.r14 > 0])
    out["Fri r14<0 clustered (signed in short dir)"] = ct(F[F.r14 < 0].assign(u=-F.loc[F.r14 < 0, "u"]))
    # vol ratio grading among r14>0
    P = F[F.r14 > 0].copy()
    P["vq"] = pd.qcut(P["vr"], 4, labels=False)
    out["Fri r14>0 by vr quartile"] = P.groupby("vq").apply(ct)
    # same for other weekdays: slope of u on z14 per weekday
    A = B.dropna(subset=["r2f", "r14", "s60"]).copy()
    A["z14"] = A["r14"] / (A["s60"] * np.sqrt(14))
    A["un"] = A["u"] / A["coin"].map(sd2)
    wr = {}
    for d, g in A.groupby("wd"):
        sl = stats.linregress(g["z14"], g["un"])
        wr[d] = {"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(g)}
    out["slope u on z14 by weekday (overlapping, indicative)"] = pd.DataFrame(wr).T
    # book daily: mean, market part
    rows = []
    for c, wd_ in data["days"].items():
        for w, d in wd_.items():
            t = d[["day", "book_return", "coin_return"]].copy(); t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows).dropna(subset=["book_return"])
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bd = D.groupby("day")["book_return"].mean()
    out["book daily mean / std / t / n"] = pd.Series({"mean": bd.mean(), "std": bd.std(), "t": bd.mean() / (bd.std() / np.sqrt(len(bd))), "n": len(bd)})
    # market part: pos at end of day * coin mean daily ret
    cm = D.groupby("coin")["coin_return"].mean()
    B["dday"] = B["day"].dt.strftime("%Y-%m-%d")
    pe = B.groupby(["coin", "w", "dday"])["pos"].last().reset_index()
    pe["mk"] = pe["pos"] * pe["coin"].map(cm)
    mk = pe.groupby("dday")["mk"].mean()
    out["book market part daily mean"] = mk.mean()
    out["book by year mean daily"] = D.groupby("year")["book_return"].mean()
    return out
