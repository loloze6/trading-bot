def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            r = c.pct_change()
            f = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D")})
            hi20 = h.shift(1).rolling(20).max()
            hi10 = h.shift(1).rolling(10).max()
            hi40 = h.shift(1).rolling(40, min_periods=30).max()
            vol20 = r.rolling(20).std()
            f["a10"] = c / hi10 - 1
            f["a20"] = c / hi20 - 1
            f["a40"] = c / hi40 - 1
            f["a20n"] = f["a20"] / vol20
            for H in (5, 10):
                f[f"fwd{H}"] = c.shift(-H) / c - 1
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    def clt(s, col="ex"):
        G = s.groupby("day")[col].sum() - s.groupby("day")[col].count() * s[col].mean()
        n = len(G)
        if n < 3: return np.nan
        se = np.sqrt((G**2).sum() * n / (n - 1)) / len(s)
        return s[col].mean() / se
    out = {}
    # robustness over grid offsets: above20 at H10 and H5
    res = []
    for H in (5, 10):
        for off in range(H):
            g = A[(A["pos"] - off) % H == 0].dropna(subset=[f"fwd{H}"]).copy()
            g["ex"] = g[f"fwd{H}"] - A[A["pos"] % H == 0].groupby("coin")[f"fwd{H}"].mean().reindex(g["coin"]).values
            s = g[g["a20"] > 0]
            res.append({"H": H, "off": off, "n": len(s), "days": s["day"].nunique(), "mean_ex%": s["ex"].mean()*100, "t_cl": clt(s)})
    out["above20 by grid offset"] = pd.DataFrame(res).round(3)
    # graded slope on all bars with a20>0 (grid 0), overshoot in vol units, and other lookbacks
    res = []
    for H in (5, 10):
        g = A[A["pos"] % H == 0].dropna(subset=[f"fwd{H}"]).copy()
        g["ex"] = g[f"fwd{H}"] - g.groupby("coin")[f"fwd{H}"].transform("mean")
        for col in ("a10", "a20", "a40"):
            s = g[g[col] > 0].dropna(subset=["ex"])
            res.append({"H": H, "cond": col, "n": len(s), "days": s["day"].nunique(), "mean_ex%": s["ex"].mean()*100, "t_cl": clt(s)})
        s = g[g["a20"] > 0].dropna(subset=["a20n", "ex"]).copy()
        x = s["a20n"] - s["a20n"].mean()
        beta = (x * s["ex"]).sum() / (x**2).sum()
        u = x * (s["ex"] - s["ex"].mean() - beta * x)
        G = u.groupby(s["day"]).sum(); n = len(G)
        se = np.sqrt((G**2).sum() * n / (n - 1)) / (x**2).sum()
        res.append({"H": H, "cond": "slope ex on a20n", "n": len(s), "days": n, "mean_ex%": beta*100, "t_cl": beta/se})
    out["lookbacks and slope"] = pd.DataFrame(res).round(3)
    # non-break bars for contrast at H10
    g = A[A["pos"] % 10 == 0].dropna(subset=["fwd10"]).copy()
    g["ex"] = g["fwd10"] - g.groupby("coin")["fwd10"].transform("mean")
    s = g[g["a20"] <= 0].dropna(subset=["a20"])
    out["not above20 H10"] = {"n": len(s), "mean_ex%": s["ex"].mean()*100, "t_cl": clt(s)}
    return out
