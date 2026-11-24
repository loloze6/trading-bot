def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ret1": c / c.shift(1) - 1,
                "ret5": c / c.shift(5) - 1,
                "ret60": c / c.shift(60) - 1,
                "rm": rng / rng.rolling(20).mean().shift(1),
                "body": (c - o) / rng.replace(0, np.nan),
                "bodypct": (c - o) / o,
                "vol20": c.pct_change().rolling(20).std(),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "fc": b["forecast"].astype(float),
                "day": ts.dt.floor("D"),
                "yr": ts.dt.year,
                "wd": ts.dt.weekday,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    dr1 = D.groupby("coin")["f1"].mean()
    dr3 = D[D["pos"] % 3 == 0].groupby("coin")["f3"].mean()
    D["u1"] = D["f1"] - D["coin"].map(dr1)
    D["u3"] = D["f3"] - D["coin"].map(dr3)
    D["z1"] = D["ret1"] / D["vol20"]  # 1-day return in units of own vol
    D["zb"] = D["bodypct"] / D["vol20"]
    out = {}

    def daypooled_t(df, col):
        s = df.groupby("day")[col].sum()
        n = len(df); Dn = len(s)
        m = df[col].mean()
        dev = df.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev ** 2).sum() * Dn / (Dn - 1)) / n
        return m, m / se, n, Dn

    def tab(df, col, key, q=5):
        df = df.dropna(subset=[col, key]).copy()
        df["b"] = pd.qcut(df[key].rank(method="first"), q, labels=False)
        r = []
        for k, g in df.groupby("b"):
            m, t, n, Dn = daypooled_t(g, col)
            r.append({"b": k, "keymean": g[key].mean(), "mean": m, "t_daypool": t, "n": n, "days": Dn})
        return pd.DataFrame(r).set_index("b").round(5)

    # 1-day reversal graded by vol-scaled 1-day return
    out["u1 by z1 decile"] = tab(D, "u1", "z1", 10)
    # by year: bottom decile z1
    lo = D[D["z1"] < D["z1"].quantile(0.1)]
    out["u1 after bottom-decile z1, by year"] = lo.groupby("yr")["u1"].agg(["mean", "count"]).round(4)
    out["u1 after bottom-decile z1, by coin"] = lo.groupby("coin")["u1"].agg(["mean", "count"]).round(4)
    # 3-day after down days on grid
    G = D[D["pos"] % 3 == 0].copy()
    out["u3 by z1 quintile (grid)"] = tab(G, "u3", "z1", 5)
    # wide red day graded: rm * negative body
    G["widered"] = G["rm"] * (-G["body"]).clip(lower=0)
    Gr = G[G["body"] < 0]
    out["u3 red days by rm quintile"] = tab(Gr, "u3", "rm", 5)
    Gg = G[G["body"] > 0]
    out["u3 green days by rm quintile"] = tab(Gg, "u3", "rm", 5)
    # red wide days by trend
    Gr2 = Gr[Gr["rm"] > Gr["rm"].quantile(0.6)].copy()
    Gr2["up60"] = Gr2["ret60"] > 0
    out["u3 wide red, by 60d trend"] = Gr2.groupby("up60")["u3"].agg(["mean", "count"]).round(4)
    out["u3 wide red, by year"] = Gr2.groupby("yr")["u3"].agg(["mean", "count"]).round(4)
    # weekday stability by year: Thu+Fri minus Mon+Wed
    D["wdg"] = D["wd"].map({0: "MonWed", 2: "MonWed", 3: "ThuFri", 4: "ThuFri"})
    out["u1 weekday groups by year"] = D.dropna(subset=["wdg"]).pivot_table(index="yr", columns="wdg", values="u1", aggfunc="mean").round(4)
    # top-forecast effect by year
    H = G[G["fc"] > 15]
    out["u3 forecast>15 by year"] = H.groupby("yr")["u3"].agg(["mean", "count"]).round(4)
    m, t, n, Dn = daypooled_t(H.dropna(subset=["u3"]), "u3")
    out["u3 forecast>15 pooled"] = pd.Series({"mean": m, "t": t, "n": n, "days": Dn}).round(4)
    return out
