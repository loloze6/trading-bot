def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 40: continue
            c, o, hi, lo = b["close"], b["open"], b["high"], b["low"]
            rng = hi - lo
            r = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            r["pos"] = np.arange(len(b))
            r["width"] = rng / rng.rolling(20).mean()
            r["body"] = (c - o) / rng.replace(0, np.nan)
            r["push"] = (c - o) / rng.rolling(20).mean()   # signed body in units of 20-day mean range
            r["ret5"] = c / c.shift(6) - 1
            r["fwd10"] = c.shift(-10) / c - 1
            r["fwd1"] = c.shift(-1) / c - 1
            r["cell"] = r["pos"] // 10
            rows.append(r)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D"); A["yr"] = A["ts"].dt.year; A["wd"] = A["ts"].dt.weekday
    A["wn"] = A["win"].str[1:].astype(int)
    g = A[(A["pos"] % 10 == 0) & A["fwd10"].notna()]
    dr = g.groupby("coin")["fwd10"].mean()
    A["ex10"] = A["fwd10"] - A["coin"].map(dr)

    def pooled(df, col):
        df = df.dropna(subset=[col]); n = len(df)
        if n < 8: return pd.Series({"n": n, "mean": df[col].mean() if n else np.nan, "t": np.nan, "days": n})
        m = df[col].mean(); d = (df[col] - m).groupby(df["day"]).sum(); D = len(d)
        se = np.sqrt(D / (D - 1) * (d ** 2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t": m / se, "days": D})

    def fpc(mask):
        s = A[mask & A["fwd10"].notna()]
        return s.groupby(["coin", "win", "cell"]).head(1)

    def slope(s, xcol):
        s = s.dropna(subset=["ex10", xcol])
        x = s[xcol] - s[xcol].mean(); y = s["ex10"]
        beta = (x * y).sum() / (x ** 2).sum(); res = y - y.mean() - beta * x
        dd = (x * res).groupby(s["day"]).sum(); D = len(dd)
        se = np.sqrt(D / (D - 1) * (dd ** 2).sum()) / (x ** 2).sum()
        return pd.Series({"beta": beta, "t": beta / se, "n": len(s), "days": D})

    out = {}
    wub = (A["width"] >= 1.5) & (A["ret5"] > 0) & (A["body"] > 0.5)
    s = fpc(wub)
    out["wide_up_body_by_year"] = s.groupby("yr").apply(lambda x: pooled(x, "ex10"))
    out["wide_up_body_by_coin"] = s.groupby("coin").apply(lambda x: pooled(x, "ex10"))
    out["wide_up_body_by_halfwindows"] = s.assign(h=(s["wn"] > 12).astype(int)).groupby("h").apply(lambda x: pooled(x, "ex10"))
    s = fpc(A["push"] > 0)
    out["slope_ex10_on_push_up"] = slope(s, "push")
    s = s.copy(); s["pb"] = pd.cut(s["push"], [0, 0.25, 0.5, 1, 1.5, 99])
    out["push_up_bins"] = s.groupby("pb").apply(lambda x: pooled(x, "ex10"))
    s = fpc(A["push"] < 0)
    out["slope_ex10_on_push_dn"] = slope(s, "push")
    d1 = A[A["wd"] == 4].dropna(subset=["fwd1"])
    out["friday_next_by_year"] = d1.groupby("yr").apply(lambda x: pooled(x, "fwd1"))
    return out
