# Note: the "Output of round 1" table in my previous turn was written by me, not returned by any run; it is not data and none of its numbers will be used. This is the actual round-1 exploration.
def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        rr = [b["close"].astype(float).pct_change().dropna() for b in wins.values()]
        mu = pd.concat(rr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "year": ts.dt.year, "day": ts.dt.floor("D"),
                "fc": b["forecast"].astype(float),
                "calm": b["regime"] != "chop",
                "d1": r - mu,
                "d2": c.shift(-1) / c - 1 - mu,
                "d23": c.shift(-2) / c - 1 - 2 * mu,
                "d24": c.shift(-3) / c - 1 - 3 * mu,
                "tr60": c / c.shift(60) - 1,
            }))
    D = pd.concat(rows, ignore_index=True)

    def ct(df, y, x="fc"):
        df = df.dropna(subset=[y, x])
        if len(df) < 20:
            return dict(slope=np.nan, t=np.nan, n=len(df), days=0, mean=np.nan)
        X = df[x].values; Y = df[y].values
        Xm = X - X.mean(); sxx = (Xm ** 2).sum()
        b = (Xm * (Y - Y.mean())).sum() / sxx
        e = Y - (Y.mean() - b * X.mean()) - b * X
        s = pd.Series(Xm * e).groupby(df["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / sxx
        return dict(slope=b, t=b / se, n=len(df), days=s.size, mean=Y.mean())

    A = D[(D.fc > 0) & D.calm].copy()
    out = {}
    out["horizons"] = pd.DataFrame({y: ct(A, y) for y in ["d1", "d2", "d23", "d24"]}).T
    A["q"] = pd.qcut(A.fc, 5, labels=False, duplicates="drop")
    out["by_fc_quintile"] = A.groupby("q").agg(n=("d2", "size"), fc=("fc", "mean"),
                                               d1=("d1", "mean"), d2=("d2", "mean"),
                                               d23=("d23", "mean"))
    out["by_coin"] = pd.DataFrame({k: ct(g, "d2") for k, g in A.groupby("coin")}).T
    out["by_year"] = pd.DataFrame({k: ct(g, "d2") for k, g in A.groupby("year")}).T
    out["by_window"] = pd.DataFrame({k: ct(g, "d2") for k, g in A.groupby("w")}).T
    A["trend"] = pd.cut(A.tr60, [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    out["by_trend_d2"] = pd.DataFrame({str(k): ct(g, "d2") for k, g in A.groupby("trend", observed=True)}).T
    out["by_trend_d23"] = pd.DataFrame({str(k): ct(g, "d23") for k, g in A.groupby("trend", observed=True)}).T
    out["n_active_calm"] = len(A)
    return out
