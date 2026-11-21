def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            # recompute ichimoku cloud
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            mid = (sa + sb) / 2
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            cslope = mid / mid.shift(26) - 1
            thick = (top - bot) / c
            above = c / top - 1; below = c / bot - 1
            fwd = c.shift(-H) / c - 1
            for i in range(0, len(b), H):
                if i + H >= len(b): break
                rows.append(dict(coin=coin, w=w, yr=ts[i].year, fwd=fwd[i], reg=b["regime"].iloc[i],
                                 past26=c[i] / c[i - 26] - 1 if i >= 26 else np.nan,
                                 past52=c[i] / c[i - 52] - 1 if i >= 52 else np.nan,
                                 cslope=cslope[i], thick=thick[i], above=above[i], below=below[i],
                                 vol=r1.rolling(30).std()[i]))
            daily.append(pd.DataFrame(dict(coin=coin, ts=ts.dt.floor("D"), r=r1, wd=ts.dt.dayofweek, yr=ts.dt.year)))
    df = pd.DataFrame(rows)
    st = df.groupby("coin")["fwd"].agg(["mean", "std"])
    df["ex"] = df["fwd"] - df["coin"].map(st["mean"]); df["sx"] = df["ex"] / df["coin"].map(st["std"])
    df["vp26"] = df["past26"] / (df["vol"] * np.sqrt(26))
    out = {}
    def grp(col, q=4, sub=None):
        x = (df if sub is None else sub).dropna(subset=[col, "ex"]).copy()
        x["bin"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False) if len(s) >= q else np.nan)
        g = x.groupby("bin").agg(n=("ex", "size"), ex=("ex", "mean"), sx=("sx", "mean"), sd=("sx", "std"), med=(col, "median"))
        g["t_sx"] = g["sx"] / (g["sd"] / np.sqrt(g["n"]))
        g.loc["top-bottom t", "sx"] = stats.ttest_ind(x[x.bin == q - 1]["sx"], x[x.bin == 0]["sx"], equal_var=False).statistic
        g.loc["spearman", "sx"] = stats.spearmanr(x[col], x["sx"]).correlation
        return g.drop(columns="sd")
    for col in ["past26", "past52", "vp26", "cslope", "thick"]:
        out["all_" + col] = grp(col)
    mr = df[(df["below"] < 0) & (df["cslope"] < 0)]
    for col in ["cslope", "past26", "below", "thick"]:
        out["belowfalling_" + col] = grp(col, 3, mr)
    ab = df[(df["above"] > 0) & (df["cslope"] > 0)]
    out["abovering_past26"] = grp("past26", 3, ab)
    # momentum by year: spearman of past26 vs sx
    out["mom_by_year"] = df.dropna(subset=["past26"]).groupby("yr").apply(
        lambda x: pd.Series(dict(n=len(x), rho=stats.spearmanr(x["past26"], x["sx"]).correlation,
                                 topminusbot=x[x.vp26 > 0]["sx"].mean() - x[x.vp26 <= 0]["sx"].mean())))
    # weekday, collapsed per day across coins (avoid cross-coin correlation)
    dd = pd.concat(daily).dropna(subset=["r"])
    pd_ = dd.groupby(["ts"]).agg(r=("r", "mean"), wd=("wd", "first"), yr=("yr", "first"))
    g = pd_.groupby("wd").agg(n=("r", "size"), r=("r", "mean"), sd=("r", "std"))
    g["t"] = g["r"] / (g["sd"] / np.sqrt(g["n"])); out["weekday_collapsed"] = g.drop(columns="sd")
    pd_["wed_sat"] = pd_["wd"].isin([2, 5])
    out["wedsat_minus_rest_by_year"] = pd_.groupby("yr").apply(lambda x: x[x.wed_sat]["r"].mean() - x[~x.wed_sat]["r"].mean())
    return out
