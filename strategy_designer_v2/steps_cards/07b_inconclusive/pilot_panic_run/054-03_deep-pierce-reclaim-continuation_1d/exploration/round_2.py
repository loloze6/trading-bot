import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [5, 10]
    rows = []; drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            lo, cl = b["low"].values, b["close"].values
            L = pd.Series(lo).rolling(30).min().shift(1).values
            cs = pd.Series(cl)
            tr = (cs / cs.shift(60) - 1).values * 100
            vol = cs.pct_change().rolling(30).std()
            pct = vol.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True).values
            ts = pd.to_datetime(b["timestamp"]); n = len(b)
            for t in range(30, n):
                if not (lo[t] < L[t] and cl[t] >= L[t]):
                    continue
                r = {"coin": coin, "w": w, "t": t, "depth": (L[t] - lo[t]) / L[t] * 100,
                     "trend": "rising" if tr[t] > 10 else ("falling" if tr[t] < -10 else ("choppy" if not np.isnan(tr[t]) else "na")),
                     "agit": "agitated" if pct[t] > 0.5 else ("calm" if not np.isnan(pct[t]) else "na"),
                     "inprof": b["regime"].iloc[t] != "chop", "year": ts.iloc[t].year, "day": ts.iloc[t].normalize()}
                for h in H:
                    r[f"u{h}"] = cl[t + h] / cl[t] - 1 - drift[(coin, h)] if t + h < n else np.nan
                rows.append(r)
    df = pd.DataFrame(rows)

    def summ(g, h):
        x = g.dropna(subset=[f"u{h}"])
        x = x.assign(cell=x["t"] // h).drop_duplicates(["coin", "w", "cell"])
        if len(x) < 3:
            return pd.Series({"n": len(x), "days": np.nan, "mean_long": np.nan, "t": np.nan})
        m = x[f"u{h}"].mean()
        gs = x.groupby("day")[f"u{h}"].agg(["sum", "count"])
        G = len(gs)
        if G < 2:
            return pd.Series({"n": len(x), "days": G, "mean_long": m, "t": np.nan})
        se = np.sqrt(((gs["sum"] - gs["count"] * m) ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean_long": m, "t": m / se})

    out = {}
    df["prof"] = df["trend"] + "_" + df["agit"]
    out["by_profile_h5"] = df.groupby("prof").apply(lambda g: summ(g, 5))
    out["by_profile_h10"] = df.groupby("prof").apply(lambda g: summ(g, 10))
    out["by_trend_h10"] = df.groupby("trend").apply(lambda g: summ(g, 10))
    out["by_agit_h10"] = df.groupby("agit").apply(lambda g: summ(g, 10))
    df["dq"] = pd.qcut(df["depth"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["all_by_depth_h10"] = df.groupby("dq").apply(lambda g: summ(g, 10))
    nf = df[df.trend != "falling"]
    out["notfalling_all_h5_h10"] = pd.DataFrame({h: summ(nf, h) for h in H}).T
    out["notfalling_by_depth_h10"] = nf.groupby("dq").apply(lambda g: summ(g, 10))
    out["notfalling_by_year_h10"] = nf.groupby("year").apply(lambda g: summ(g, 10))
    out["notfalling_by_coin_h10"] = nf.groupby("coin").apply(lambda g: summ(g, 10))
    out["all_by_year_h10"] = df.groupby("year").apply(lambda g: summ(g, 10))
    return out
