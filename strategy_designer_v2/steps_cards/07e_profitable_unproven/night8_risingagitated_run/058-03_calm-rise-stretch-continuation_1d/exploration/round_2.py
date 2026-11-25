def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]
    def build(h):
        recs = []
        for c in bars:
            frs = []
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                frs.append((b["close"].shift(-h) / b["close"] - 1).iloc[::h])
            mu = pd.concat(frs).dropna().mean()
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                sma = b["close"].rolling(20).mean()
                g = pd.DataFrame({"dist": b["close"] / sma - 1,
                                  "fr": b["close"].shift(-h) / b["close"] - 1 - mu,
                                  "r60": b["close"] / b["close"].shift(60) - 1,
                                  "regime": b["regime"],
                                  "day": pd.to_datetime(b["timestamp"]).dt.floor("D")}).iloc[::h].dropna()
                g["coin"] = c; g["window"] = w
                recs.append(g)
        R = pd.concat(recs)
        R["prof"] = np.where(R["regime"] == "unknown", "rising calm",
                     np.where(R["r60"] > 0.10, "rising agit",
                     np.where(R["r60"] < -0.10, "falling", "choppy")))
        return R
    def slope_t(R):
        if len(R) < 20: return (len(R), np.nan, np.nan, np.nan)
        x = R["dist"] - R["dist"].mean(); y = R["fr"]
        b = (x * y).sum() / (x * x).sum()
        e = y - y.mean() - b * x
        s = (x * e).groupby(R["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (x * x).sum()
        return (len(R), R["day"].nunique(), b, b / se)
    for h in [5, 10]:
        R = build(h)
        rows = {}
        for p, G in R.groupby("prof"):
            rows[p + " all"] = slope_t(G)
            rows[p + " dist>0"] = slope_t(G[G["dist"] > 0])
        rows["ALL all"] = slope_t(R); rows["ALL dist>0"] = slope_t(R[R["dist"] > 0])
        rows["not rc, all"] = slope_t(R[R["prof"] != "rising calm"])
        out[f"slope h{h} n,days,slope,t"] = pd.DataFrame(rows, index=["n", "days", "slope", "t"]).T
        R["dq"] = pd.qcut(R["dist"], 5, labels=False)
        out[f"h{h} mean unusual by dist quintile x prof"] = R.pivot_table(index="dq", columns="prof", values="fr", aggfunc="mean")
        if h == 5:
            out["h5 count dq x prof"] = R.pivot_table(index="dq", columns="prof", values="fr", aggfunc="count")
            rc = R[R["prof"] == "rising calm"]
            out["h5 rising calm: dist>0 vs <=0"] = rc.groupby(rc["dist"] > 0)["fr"].agg(["mean", "count"])
            out["h5 slope by year, all profiles"] = pd.DataFrame({y: slope_t(G) for y, G in R.groupby(R["day"].dt.year)}, index=["n","days","slope","t"]).T
            out["h5 slope by coin, all profiles"] = pd.DataFrame({c: slope_t(G) for c, G in R.groupby("coin")}, index=["n","days","slope","t"]).T
    T = pd.concat([trades[c][w].assign(coin=c, window=w) for c in trades for w in trades[c] if len(trades[c][w])])
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    top = T.sort_values("net_profit_loss_percent", ascending=False).head(20)
    out["top20 trades by coin"] = top.groupby("coin")["net_profit_loss_percent"].agg(["count", "sum"])
    out["top20 trades by year"] = top.groupby("year")["net_profit_loss_percent"].agg(["count", "sum"])
    out["trades by year"] = T.groupby("year")["net_profit_loss_percent"].agg(["count", "sum", "median"])
    T["efq"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
    out["trades by entry forecast third"] = T.groupby("efq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
