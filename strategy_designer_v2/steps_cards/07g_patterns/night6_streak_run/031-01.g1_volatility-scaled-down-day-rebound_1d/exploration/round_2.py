def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol60 = r.rolling(60, min_periods=20).std()
            s = np.sign(r.fillna(0)).values
            st = np.zeros(len(s))
            for i in range(len(s)):
                if s[i] == 0: st[i] = 0
                elif i > 0 and np.sign(st[i-1]) == s[i]: st[i] = st[i-1] + s[i]
                else: st[i] = s[i]
            d = pd.DataFrame({"coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "streak": st, "vol": vol60, "close": c})
            for L in [7, 14, 30]:
                d[f"r{L}z"] = (c / c.shift(L) - 1) / (vol60 * np.sqrt(L))
            for H in [3, 7, 10]:
                d[f"f{H}"] = c.shift(-H) / c - 1
            # streak relative to coin's usual |streak| inside window history
            d["upst"] = d["streak"].clip(lower=0)
            d["dnst"] = (-d["streak"]).clip(lower=0)
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    res = {}

    def prep(H):
        G = A[(A["pos"] % H == 0) & A[f"f{H}"].notna()].copy()
        st = G.groupby("coin")[f"f{H}"].agg(["mean", "std"])
        G["y"] = (G[f"f{H}"] - G["coin"].map(st["mean"])) / G["coin"].map(st["std"])
        return G

    def slope_t(g, col):
        g = g.dropna(subset=[col, "y"])
        x = (g[col] - g[col].mean()) / g[col].std()
        bb = (x * g["y"]).sum() / (x ** 2).sum()
        e = g["y"] - g["y"].mean() - bb * x
        dd = (x * e).groupby(g["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / (x ** 2).sum()
        return pd.Series({"slope": bb, "t": bb / se, "n": len(g)})

    out = {}
    for H in [3, 7, 10]:
        G = prep(H)
        for col in ["r7z", "r14z", "r30z", "upst", "dnst"]:
            out[(H, col)] = slope_t(G, col)
    res["slopes_by_horizon"] = pd.DataFrame(out).T

    # stability: r7z and upst at H=3 and 7, by half of windows and by coin
    st = {}
    for H in [3, 7]:
        G = prep(H)
        G["half"] = np.where(G["wn"] <= 12, "w1-12", "w13-24")
        for col in ["r7z", "r14z", "upst"]:
            for k, x in G.groupby("half"):
                st[(H, col, k)] = slope_t(x, col)["t"]
            for k, x in G.groupby("coin"):
                st[(H, col, k)] = slope_t(x, col)["t"]
    res["stability_t"] = pd.Series(st).unstack()

    # up-streak length table at H=7
    G = prep(7)
    G["ub"] = G["streak"].clip(-5, 5)
    t = []
    for k, x in G.groupby("ub"):
        dd = x.groupby("day")["y"].sum()
        m = x["y"].mean(); se = dd.std(ddof=1) * np.sqrt(len(dd)) / len(x)
        t.append({"streak": k, "n": len(x), "mean_y": m, "t": m / se, "raw%": 100 * x["f7"].mean()})
    res["streak_H7"] = pd.DataFrame(t)

    # book: largest gain/loss days and what preceded
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    bd = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    q = bd["book_return"].quantile([0.02, 0.98])
    res["book_tails"] = pd.DataFrame({
        "worst2%": bd[bd["book_return"] <= q.iloc[0]].mean() * 100,
        "best2%": bd[bd["book_return"] >= q.iloc[1]].mean() * 100,
        "all": bd.mean() * 100})
    res["book_coin_corr"] = float(bd.corr().iloc[0, 1])
    return res
