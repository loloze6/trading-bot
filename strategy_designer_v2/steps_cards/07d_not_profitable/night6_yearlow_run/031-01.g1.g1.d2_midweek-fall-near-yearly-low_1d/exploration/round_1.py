def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            x = d[["day", "book_return", "coin_return"]].copy()
            x["w"] = w; x["coin"] = c
            rows.append(x)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    eq = (1 + B["book_return"]).cumprod()
    dd = eq / eq.cummax() - 1
    B["dd"] = dd.values
    out["maxdd"] = float(dd.min())
    byw = B.groupby("wn").agg(book=("book_return", lambda r: (1 + r).prod() - 1),
                              coin=("coin_return", lambda r: (1 + r).prod() - 1),
                              ddmin=("dd", "min"), n=("book_return", "size"))
    out["by_window"] = byw
    # worst days
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["worst_book_days_share"] = pd.Series({
        "sum_all": B.book_return.sum(),
        "sum_worst20": B.book_return.nsmallest(20).sum(),
        "sum_best20": B.book_return.nlargest(20).sum()})
    # cases
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["ret3"] = b["close"].shift(1) / b["close"].shift(4) - 1  # Thu/Mon at Fri bar
            lr = np.log(b["close"]).diff()
            b["vol20"] = lr.rolling(20).std()
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["fri_ret"] = b["close"] / b["close"].shift(1) - 1
            b["coin"] = c; b["w"] = w
            cs.append(b)
    A = pd.concat(cs)
    A["ts"] = pd.to_datetime(A["timestamp"])
    A["wd"] = A["ts"].dt.weekday
    mu = A.groupby("coin")["ret1"].mean()
    A["mu"] = A["coin"].map(mu)
    F = A[(A["wd"] == 4) & (A["postRebalance_current_allocation"].abs() > 1e-6)].dropna(subset=["ret1"]).copy()
    F["al"] = F["postRebalance_current_allocation"]
    F["pnl"] = F["al"] * F["ret1"]
    F["side"] = np.where(F["al"] > 0, "long", "short")
    F["grp"] = F["regime"] + "_" + F["side"]
    def summ(g):
        return pd.Series({"n": len(g), "mean_pnl": g.pnl.mean(), "t": g.pnl.mean() / g.pnl.std() * np.sqrt(len(g)),
                          "worst5pct": g.pnl.quantile(0.05), "min": g.pnl.min(), "mean_abs_al": g.al.abs().mean(),
                          "hit": (g.pnl > 0).mean()})
    out["by_regime_side"] = F.groupby("grp").apply(summ)
    F["fq"] = pd.qcut(F["forecast"], 6, duplicates="drop")
    out["by_forecast"] = F.groupby("fq").apply(summ)
    F["volq"] = F.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_vol_side"] = F.groupby(["volq", "side"]).apply(summ)
    F["r20s"] = np.sign(F["ret20"])
    out["by_ret20_side"] = F.groupby(["r20s", "side"]).apply(summ)
    F["year"] = F["ts"].dt.year
    out["by_year_side"] = F.groupby(["year", "side"])["pnl"].agg(["count", "mean", "sum"])
    out["by_coin_side"] = F.groupby(["coin", "side"])["pnl"].agg(["count", "mean", "sum"])
    return out
