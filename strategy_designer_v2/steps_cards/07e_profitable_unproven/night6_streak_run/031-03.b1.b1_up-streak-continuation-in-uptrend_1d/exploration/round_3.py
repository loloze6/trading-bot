def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    recs = []
    for coin in bars:
        drift = {}
        for h in [5, 10]:
            vals = []
            for w, df in bars[coin].items():
                c = df.sort_values("timestamp")["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(vals)
        allr = []
        for w, df in bars[coin].items():
            c = df.sort_values("timestamp")["close"].values
            for h in [5, 10]:
                idx = np.arange(0, len(c) - h, h)
                allr += []
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values; n = len(c); s = pd.Series(c)
            vol = s.pct_change().rolling(60, min_periods=30).std()
            d = pd.DataFrame({"coin": coin, "pos": np.arange(n),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "year": pd.to_datetime(df["timestamp"]).dt.year})
            d["m10"] = (s.pct_change(10) / (vol * np.sqrt(10))).values
            d["m30"] = (s.pct_change(30) / (vol * np.sqrt(30))).values
            for h in [5, 10]:
                f = np.full(n, np.nan); f[:n-h] = c[h:] / c[:n-h] - 1
                d[f"t{h}"] = f
                d[f"u{h}"] = f - drift[h]
                d[f"str{h}"] = d[f"u{h}"] / (vol.values * np.sqrt(h))
            recs.append(d)
    A = pd.concat(recs, ignore_index=True)

    def clt(x, k):
        x = np.asarray(x, float); m = x.mean(); n = len(x)
        s = pd.Series(x - m).groupby(np.asarray(k)).sum(); G = len(s)
        return m, m / (np.sqrt(G / (G - 1) * (s ** 2).sum()) / n), n, G
    out = {}
    for h in [5, 10]:
        for L in ["m10", "m30"]:
            P = A[(A["pos"] % h == 0) & (A[L] > 0)].dropna(subset=[L, f"u{h}"]).copy()
            P["q"] = pd.qcut(P[L], 4, labels=False)
            rows = []
            for q, s in P.groupby("q"):
                m, t, n, nd = clt(s[f"u{h}"], s["day"])
                rows.append({"q": q, "mom": s[L].mean(), "unusual": m, "t": t, "total": s[f"t{h}"].mean(),
                             "strength": s[f"str{h}"].mean(), "n": n, "days": nd})
            out[f"{L}>0 quartiles -> {h}d"] = pd.DataFrame(rows)
    P = A[(A["pos"] % 5 == 0) & (A["m10"] > 0)].dropna(subset=["m10", "u5"]).copy()
    P["top"] = P["m10"] > P["m10"].median()
    rows = []
    for y, s in P.groupby("year"):
        hi = s[s["top"]]["u5"]; lo = s[~s["top"]]["u5"]
        rows.append({"year": y, "top_minus_bottom_u5": hi.mean() - lo.mean(), "n": len(s)})
    out["m10>0 top-half minus bottom-half unusual 5d by year"] = pd.DataFrame(rows)
    return out
