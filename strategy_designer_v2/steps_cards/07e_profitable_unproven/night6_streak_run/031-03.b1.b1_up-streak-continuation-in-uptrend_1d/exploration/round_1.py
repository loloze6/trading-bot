def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    H = [1, 5, 10, 20]
    recs = []
    drift = {}
    mu1 = {}
    for coin in bars:
        # coin mean daily return over all windows
        dr = pd.concat([d["coin_return"] for d in days[coin].values()]).dropna()
        mu1[coin] = dr.mean()
        drift[coin] = {}
        for h in H:
            vals = []
            for w, df in bars[coin].items():
                c = df.sort_values("timestamp")["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            drift[coin][h] = np.mean(vals) if vals else np.nan
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            up = np.r_[False, c[1:] > c[:-1]]
            streak = np.zeros(n, int)
            for i in range(n):
                streak[i] = streak[i-1] + 1 if (up[i] and i > 0) else 0
            d = pd.DataFrame({
                "coin": coin, "w": w, "ts": df["timestamp"],
                "year": pd.to_datetime(df["timestamp"]).dt.year,
                "alloc": df["postRebalance_current_allocation"].fillna(0).values,
                "fc": df["forecast"].fillna(0).values,
                "regime": df["regime"].values, "streak": streak, "pos": np.arange(n),
                "ret30": pd.Series(c).pct_change(30).values,
            })
            d["r1"] = np.r_[c[1:] / c[:-1] - 1, np.nan]
            for h in H:
                f = np.full(n, np.nan); f[:n-h] = c[h:] / c[:n-h] - 1
                d[f"f{h}"] = f
                d[f"u{h}"] = f - drift[coin][h]
            d["gain"] = d["alloc"] * d["r1"]
            d["mkt"] = d["alloc"] * mu1[coin]
            recs.append(d)
    A = pd.concat(recs, ignore_index=True)
    A["day"] = pd.to_datetime(A["ts"]).dt.floor("D")
    out = {}
    # book-level: mean over coins per day of gain and market part
    g = A.dropna(subset=["r1"]).groupby("day")[["gain", "mkt"]].mean()
    out["book mean daily gain pre-cost vs market part"] = pd.Series({
        "gain": g["gain"].mean(), "market_part": g["mkt"].mean(),
        "timing": g["gain"].mean() - g["mkt"].mean(), "days": len(g)})
    # actual book daily from days table
    D = pd.concat([d.assign(coin=c_) for c_ in days for d in days[c_].values()])
    bd = D.dropna(subset=["book_return"]).groupby("day")[["book_return", "coin_return"]].mean()
    out["book actual daily mean"] = pd.Series({"book": bd["book_return"].mean(), "hold": bd["coin_return"].mean()})
    # contributions by coin and year (pre-cost gain sum, share)
    tot = A["gain"].sum()
    bc = A.groupby("coin").agg(gain=("gain", "sum"), mkt=("mkt", "sum"), inpos=("alloc", lambda x: (x > 0).mean()))
    bc["share"] = bc["gain"] / tot
    out["by coin"] = bc.sort_values("gain", ascending=False)
    by = A.groupby("year").agg(gain=("gain", "sum"), mkt=("mkt", "sum"), n=("gain", "size"))
    by["share"] = by["gain"] / tot
    out["by year"] = by
    # gain by streak count while held, and by ret30 bucket while held
    held = A[A["alloc"] > 0].copy()
    held["sb"] = held["streak"].clip(upper=5)
    out["held: gain by streak at bar"] = held.groupby("sb").agg(n=("gain", "size"), mean_gain=("gain", "mean"), sum=("gain", "sum"))
    held["rb"] = pd.qcut(held["ret30"], 5, duplicates="drop")
    out["held: gain by ret30 quintile"] = held.groupby("rb", observed=True).agg(n=("gain", "size"), mean_gain=("gain", "mean"), mkt=("mkt", "mean"))

    def clt(x, dayk):
        x = np.asarray(x, float); m = x.mean(); n = len(x)
        s = pd.Series(x - m).groupby(np.asarray(dayk)).sum()
        G = len(s)
        se = np.sqrt(G / (G - 1) * (s ** 2).sum()) / n
        return m, m / se, n, G
    # grid unusual moves: ret30 sign, and ret30 quintile, horizons
    rows = []
    for h in [5, 10, 20]:
        G_ = A[(A["pos"] % h == 0)].dropna(subset=[f"u{h}", "ret30"])
        G_ = G_.copy()
        G_["rq"] = pd.qcut(G_["ret30"], 5, labels=False)
        for q, s in G_.groupby("rq"):
            m, t, n, nd = clt(s[f"u{h}"], s["day"])
            rows.append({"h": h, "ret30_q": q, "unusual": m, "t": t, "n": n, "days": nd, "ret30_mean": s["ret30"].mean()})
    out["unusual by ret30 quintile (all bars, grid)"] = pd.DataFrame(rows)
    rows = []
    for h in [5, 10, 20]:
        G_ = A[(A["pos"] % h == 0) & (A["ret30"] > 0)].dropna(subset=[f"u{h}"])
        G_ = G_.copy(); G_["sb"] = G_["streak"].clip(upper=4)
        for q, s in G_.groupby("sb"):
            m, t, n, nd = clt(s[f"u{h}"], s["day"])
            rows.append({"h": h, "streak": q, "unusual": m, "t": t, "n": n})
    out["ret30>0: unusual by streak (grid)"] = pd.DataFrame(rows)
    return out
