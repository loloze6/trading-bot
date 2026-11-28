import numpy as np, pandas as pd

def explore(data):
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            f3 = c.shift(-3) / c - 1
            allf.append(f3.iloc[::3].dropna())
        drift[coin] = pd.concat(allf).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l, o, v = b["close"], b["high"], b["low"], b["open"], b["volume"]
            rr = (h - l) / c
            mr = rr.rolling(30, min_periods=10).mean()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "fc": (b["regime"] == "unknown"),
                "f3": c.shift(-3) / c - 1,
                "f1": c.shift(-1) / c - 1,
                "s7": (c / c.shift(7) - 1) / mr,
                "s1": (c / c.shift(1) - 1) / mr,
                "s3": (c / c.shift(3) - 1) / mr,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "rng": rr / mr,
                "volr": v / v.rolling(20, min_periods=10).mean(),
                "dhi": (c / h.rolling(20, min_periods=10).max() - 1) / mr,
                "dlo": (c / l.rolling(20, min_periods=10).min() - 1) / mr,
                "pos": b["postRebalance_current_allocation"],
            })
            d = d.iloc[::3]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["u3"] = D["f3"] - D["coin"].map(drift)
    D["day"] = D["ts"].dt.floor("D")
    F = D[D["fc"]].dropna(subset=["u3"])
    out = {}
    out["counts"] = pd.Series({"grid_all": len(D.dropna(subset=["u3"])), "grid_fallcalm": len(F),
                               "fallcalm_mean_u3": F["u3"].mean(), "fallcalm_mean_f3": F["f3"].mean()})
    def tc(x, days):
        s = x.groupby(days).sum()
        n = len(x)
        if n < 3: return np.nan
        m = x.mean()
        se = np.sqrt((s - s.index.map(days.value_counts()).values * m).pow(2).sum()) / n
        return m / se if se > 0 else np.nan
    def tab(col, q=5):
        G = F.dropna(subset=[col]).copy()
        G["bin"] = pd.qcut(G[col], q, labels=False, duplicates="drop")
        r = G.groupby("bin").apply(lambda g: pd.Series({
            "lo": g[col].min(), "hi": g[col].max(), "n": len(g), "days": g["day"].nunique(),
            "mean_u3": g["u3"].mean(), "t_day": tc(g["u3"], g["day"])}))
        sl = np.polyfit(G[col], G["u3"], 1)[0]
        r.loc["slope"] = [np.nan, np.nan, len(G), np.nan, sl, np.corrcoef(G[col], G["u3"])[0, 1] * np.sqrt(len(G))]
        return r
    for col in ["s7", "s1", "s3", "clv", "rng", "volr", "dhi", "dlo"]:
        out["fc_" + col] = tab(col)
    F2 = F.copy(); F2["wd"] = F2["ts"].dt.dayofweek
    out["fc_weekday"] = F2.groupby("wd")["u3"].agg(["count", "mean"])
    out["fc_by_coin"] = F.groupby("coin")["u3"].agg(["count", "mean"])
    out["fc_by_year"] = F.groupby(F["ts"].dt.year)["u3"].agg(["count", "mean"])
    out["fc_by_window"] = F.groupby("win")["u3"].agg(["count", "mean"])
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            y = x.copy(); y["coin"] = coin; y["win"] = w; dd.append(y)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    out["book_days"] = pd.Series({"n": len(DD), "mean": DD["book_return"].mean(),
                                  "share_nonzero": (DD["book_return"].abs() > 1e-9).mean(),
                                  "top10_sum": DD["book_return"].nlargest(10).sum(),
                                  "bot10_sum": DD["book_return"].nsmallest(10).sum(),
                                  "total_sum": DD["book_return"].sum()})
    return out
