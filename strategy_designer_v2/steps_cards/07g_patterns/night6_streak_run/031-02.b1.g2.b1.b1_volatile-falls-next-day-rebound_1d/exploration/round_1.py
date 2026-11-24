def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        sd = pd.concat(allr).std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w,
                               "ts": pd.to_datetime(b["timestamp"]),
                               "r0": r, "f": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            df["y1"] = c.shift(-1) / c - 1 - mu
            df["vol60"] = r.rolling(60, min_periods=20).std()
            df["z0"] = df["r0"] / df["vol60"]
            df["ret5"] = c / c.shift(5) - 1
            df["z5"] = df["ret5"] / (df["vol60"] * np.sqrt(5))
            df["ret20"] = c / c.shift(20) - 1
            df["z20"] = df["ret20"] / (df["vol60"] * np.sqrt(20))
            df["y5"] = c.shift(-5) / c - 1 - 5 * mu
            df["grid5"] = (np.arange(len(df)) % 5 == 0)
            df["volrank"] = df["vol60"] / df["vol60"].rolling(365, min_periods=60).median()
            # streak
            s = np.sign(r.fillna(0)).values
            st = np.zeros(len(s))
            for i in range(len(s)):
                if s[i] == 0: st[i] = 0
                elif i > 0 and np.sign(st[i-1]) == s[i]: st[i] = st[i-1] + s[i]
                else: st[i] = s[i]
            df["streak"] = st
            df["usd"] = sd
            df["day"] = df["ts"].dt.floor("D")
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    def ct(g, y):
        g = g.dropna(subset=[y])
        n = len(g)
        if n < 10: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        m = g[y].mean()
        s = (g[y] - m).groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum()) / n
        return pd.Series({"n": n, "mean%": 100*m, "t": m/se})

    out = {}
    d = D.dropna(subset=["z0", "y1"])
    d = d.assign(q=pd.qcut(d["z0"], 10, labels=False))
    out["next1 by today z-return decile"] = d.groupby("q").apply(lambda g: ct(g, "y1"))
    st = D.dropna(subset=["y1"]).copy()
    st["sb"] = st["streak"].clip(-5, 5)
    out["next1 by streak"] = st.groupby("sb").apply(lambda g: ct(g, "y1"))
    g5 = D[D["grid5"]].dropna(subset=["z5", "y5"])
    g5 = g5.assign(q=pd.qcut(g5["z5"], 5, labels=False))
    out["next5 by past5 z quintile (grid)"] = g5.groupby("q").apply(lambda g: ct(g, "y5"))
    g20 = D[D["grid5"]].dropna(subset=["z20", "y5"])
    g20 = g20.assign(q=pd.qcut(g20["z20"], 5, labels=False))
    out["next5 by past20 z quintile (grid)"] = g20.groupby("q").apply(lambda g: ct(g, "y5"))
    wd = D.dropna(subset=["y1"]).copy()
    wd["nextwd"] = (wd["ts"] + pd.Timedelta(days=1)).dt.weekday
    out["next1 by weekday of next day"] = wd.groupby("nextwd").apply(lambda g: ct(g, "y1"))
    v = D.dropna(subset=["volrank", "y1", "z0"]).copy()
    v["vq"] = pd.qcut(v["volrank"], 3, labels=False)
    v["dn"] = (v["r0"] < 0).astype(int)
    out["next1 by vol-rank tercile x down day"] = v.groupby(["vq", "dn"]).apply(lambda g: ct(g, "y1"))
    v["yr"] = v["ts"].dt.year
    out["next1 down-day z<-1 by year"] = v[v["z0"] < -1].groupby("yr").apply(lambda g: ct(g, "y1"))
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin, win=w))
    B = pd.concat(bk).dropna(subset=["book_return"])
    bd = B.groupby("day")[["book_return", "coin_return"]].mean()
    bd = bd.sort_values("book_return")
    out["book worst 20 days mean / coin"] = pd.Series({"book%": 100*bd["book_return"].head(20).mean(), "coin%": 100*bd["coin_return"].head(20).mean(), "book best20%": 100*bd["book_return"].tail(20).mean(), "coin best20%": 100*bd["coin_return"].tail(20).mean(), "corr book coin": bd["book_return"].corr(bd["coin_return"])})
    return out
