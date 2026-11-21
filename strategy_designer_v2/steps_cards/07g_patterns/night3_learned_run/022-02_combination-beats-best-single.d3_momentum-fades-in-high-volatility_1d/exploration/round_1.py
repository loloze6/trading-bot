def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        # drifts per horizon over all windows
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            df["r1"] = r1
            for L in [1, 3, 7, 14, 28]:
                df[f"p{L}"] = c / c.shift(L) - 1
            df["vol30"] = r1.rolling(30, min_periods=20).std()
            df["vol7"] = r1.rolling(7, min_periods=5).std()
            df["near28"] = c / c.rolling(28, min_periods=20).max() - 1
            df["fc"] = b["forecast"].astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            df["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            for h in [1, 3, 5, 10, 20]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # drifts & usual moves per coin per horizon on grid
    for h in [1, 3, 5, 10, 20]:
        g = D[D.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        sd = g.groupby("coin")[f"f{h}"].std()
        D[f"x{h}"] = (D[f"f{h}"] - D.coin.map(dr)) / D.coin.map(sd)
        D[f"e{h}"] = D[f"f{h}"] - D.coin.map(dr)
    # z of past returns by vol30
    for L in [1, 3, 7, 14, 28]:
        D[f"z{L}"] = D[f"p{L}"] / (D["vol30"] * np.sqrt(L))
    D["volrel"] = np.log(D["vol7"] / D["vol30"])
    # vol30 rank within coin (expanding not available; use coin-wide pct rank)
    D["volrank"] = D.groupby("coin")["vol30"].rank(pct=True)
    res = []
    sigs = [f"z{L}" for L in [1, 3, 7, 14, 28]] + ["near28", "volrel", "volrank", "fc"]
    for s in sigs:
        for h in [1, 3, 5, 10, 20]:
            g = D[(D.pos % h == 0)].dropna(subset=[s, f"x{h}"])
            sv = (g[s] - g.groupby("coin")[s].transform("mean")) / g.groupby("coin")[s].transform("std")
            prod = sv * g[f"x{h}"]
            t = prod.mean() / (prod.std() / np.sqrt(len(prod)))
            rho = stats.spearmanr(g[s], g[f"x{h}"])[0]
            ncoin_pos = int((g.assign(p=prod).groupby("coin").p.mean() > 0).sum())
            res.append([s, h, len(g), round(prod.mean(), 4), round(t, 2), round(rho, 3), ncoin_pos])
    out["signal_vs_fwd"] = pd.DataFrame(res, columns=["sig", "h_days", "n", "mean_prod", "t", "spearman", "coins_pos"])
    # large days: quintile of z1 -> next 1,3,5 excess (bps)
    g = D.dropna(subset=["z1"]).copy()
    g["q"] = pd.qcut(g["z1"], [0, .05, .2, .5, .8, .95, 1], labels=False)
    tab = {}
    for h in [1, 3, 5]:
        gg = g[g.pos % h == 0]
        tab[f"e{h}_bps"] = gg.groupby("q")[f"e{h}"].mean() * 1e4
        tab[f"n{h}"] = gg.groupby("q")[f"e{h}"].count()
    out["after_day_move"] = pd.DataFrame(tab)
    # weekday daily excess
    wdg = D.dropna(subset=["e1"]).groupby("wd")["e1"]
    out["weekday"] = pd.DataFrame({"bps": wdg.mean() * 1e4, "t": wdg.mean() / (wdg.std() / np.sqrt(wdg.count())), "n": wdg.count()})
    # vol rank quintile -> 20d excess and raw
    g = D[D.pos % 20 == 0].dropna(subset=["volrank", "e20"]).copy()
    g["q"] = pd.qcut(g["volrank"], 5, labels=False)
    out["volrank_f20"] = g.groupby("q").agg(e20=("e20", "mean"), f20=("f20", "mean"), n=("e20", "count"))
    # momentum by vol tercile, h=20, z28
    g["vq"] = pd.qcut(g["volrank"], 3, labels=False)
    r = []
    for vq, gg in g.dropna(subset=["z28"]).groupby("vq"):
        p = gg["z28"] * gg["x20"]
        r.append([vq, len(gg), p.mean(), p.mean() / (p.std() / np.sqrt(len(p)))])
    out["mom_by_vol"] = pd.DataFrame(r, columns=["vq", "n", "mean", "t"])
    # book by year
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["book_return", "coin_return"]].copy(); x["yr"] = pd.to_datetime(d["day"]).dt.year; dd.append(x)
    DD = pd.concat(dd)
    out["book_by_year"] = DD.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    return out
