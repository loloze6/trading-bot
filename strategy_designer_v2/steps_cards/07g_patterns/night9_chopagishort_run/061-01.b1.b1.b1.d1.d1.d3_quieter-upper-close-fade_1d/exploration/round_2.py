def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "r5p": c / c.shift(5) - 1,
                "r10p": c / c.shift(10) - 1,
                "tr60": c / c.shift(60) - 1,
                "vol20": r1.rolling(20).std(),
                "vol60": r1.rolling(60).std(),
                "vol5": r1.rolling(5).std(),
                "f5": c.shift(-5) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "alloc": b["postRebalance_current_allocation"].values,
            })
            df["vr"] = df["vol20"] / df["vol60"]
            df["vr5"] = df["vol5"] / df["vol60"]
            df["s5"] = df["r5p"] / (df["vol20"] * np.sqrt(5))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift5 = D[D.pos % 5 == 0].groupby("coin")["f5"].mean()
    D["u5"] = D["f5"] - D["coin"].map(drift5)
    G = D[(D.pos % 5 == 0)].dropna(subset=["u5", "tr60", "vr", "s5"]).copy()
    G["trend"] = pd.cut(G["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])

    def summ(g):
        # day-clustered t
        x = g.groupby("day")["u5"].sum()
        nd = len(x); m = g["u5"].mean()
        se = np.sqrt(((g.groupby("day")["u5"].apply(lambda s: (s - m).sum())) ** 2).sum()) / len(g) if len(g) > 2 else np.nan
        return pd.Series({"n": len(g), "days": nd, "mean": m, "t_day": m / se if se else np.nan})

    out = {}
    G["s5q"] = G.groupby("trend", observed=True)["s5"].transform(lambda s: pd.qcut(s, 4, labels=False))
    out["u5 by trend x 5d scaled return quartile"] = G.groupby(["trend", "s5q"], observed=True).apply(summ).round(4)
    G["vrq"] = G.groupby("trend", observed=True)["vr"].transform(lambda s: pd.qcut(s, 4, labels=False))
    out["u5 by trend x vol20/vol60 quartile"] = G.groupby(["trend", "vrq"], observed=True).apply(summ).round(4)
    C = G[G.trend == "chop"].copy()
    C["r5s"] = np.where(C.r5p < 0, "neg", "pos")
    C["vrh"] = np.where(C.vr > C.vr.median(), "vr_high", "vr_low")
    out["chop: r5 sign x vr half"] = C.groupby(["r5s", "vrh"]).apply(summ).round(4)
    out["chop by year"] = C.groupby("year").apply(summ).round(4)
    C["vr5q"] = pd.qcut(C["vr5"], 4, labels=False)
    out["chop by vol5/vol60 quartile"] = C.groupby("vr5q").apply(summ).round(4)
    out["chop corr u5 with vr, s5, r10"] = pd.Series({
        "vr": C["u5"].corr(C["vr"]), "s5": C["u5"].corr(C["s5"]), "r10": C["u5"].corr(C["r10p"]), "n": len(C)}).round(4)
    F = G[G.trend == "fall"].copy()
    F["vrq2"] = pd.qcut(F["vr"], 4, labels=False)
    out["fall: r5neg by vr quartile"] = F[F.r5p < 0].groupby("vrq2").apply(summ).round(4)
    # book largest days
    dd = []
    for coin, wins in days.items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book: share of total from top/bottom 10 days"] = pd.Series({
        "sum_all": bk.sum(), "top10": bk.nlargest(10).sum(), "bottom10": bk.nsmallest(10).sum(), "ndays": len(bk)}).round(4)
    out["book by window sum"] = bk.groupby(level=0).sum().round(4)
    return out
