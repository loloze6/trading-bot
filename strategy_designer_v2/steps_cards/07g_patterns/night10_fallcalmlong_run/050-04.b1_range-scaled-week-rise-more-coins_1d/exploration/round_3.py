import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allf = {H: [] for H in [3, 5, 7]}
        for w, b in wins.items():
            c = b.reset_index(drop=True)["close"]
            for H in allf:
                allf[H].append((c.shift(-H) / c - 1).iloc[::H].dropna())
        drift = {H: pd.concat(allf[H]).mean() for H in allf}
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l = b["close"], b["high"], b["low"]
            mr = ((h - l) / c).rolling(30, min_periods=10).mean()
            base = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "fc": (b["regime"] == "unknown"),
                "s7": (c / c.shift(7) - 1) / mr,
                "s14": (c / c.shift(14) - 1) / mr,
                "dhi": (c / h.rolling(20, min_periods=10).max() - 1) / mr,
                "fcst": b["forecast"],
            })
            for H in [3, 5, 7]:
                d = base.copy(); d["H"] = H
                d["u"] = (c.shift(-H) / c - 1) - drift[H]
                rows.append(d.iloc[::H])
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D"); D["year"] = D["ts"].dt.year
    F = D[D["fc"]].dropna(subset=["u"])
    def slope_t(G, x):
        G = G.dropna(subset=[x, "u"])
        if len(G) < 10: return (np.nan, np.nan, len(G))
        X = G[x] - G[x].mean()
        b = (X * G["u"]).sum() / (X ** 2).sum()
        e = G["u"] - G["u"].mean() - b * X
        s = (X * e).groupby(G["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return (b, b / se, len(G))
    def mean_t(G):
        x = G["u"]; n = len(x)
        if n < 3: return (np.nan, np.nan, n, 0)
        m = x.mean(); s = (x - m).groupby(G["day"]).sum()
        D_ = len(s); se = np.sqrt((s ** 2).sum() * D_ / max(D_ - 1, 1)) / n
        return (m, m / se, n, D_)
    out = {}
    r = {}
    for H in [3, 5, 7]:
        G = F[F["H"] == H]
        for x in ["s7", "s14", "dhi"]:
            b, t, n = slope_t(G[G["s7"] > 0], x); r[(H, x, "s7>0")] = {"slope": b, "t": t, "n": n}
        m, t, n, dd = mean_t(G[G["s7"] > 0]); r[(H, "mean", "s7>0")] = {"slope": m, "t": t, "n": n}
    out["rise_side_only"] = pd.DataFrame(r).T
    by = {}
    G5 = F[F["H"] == 5]
    for k, g in G5.groupby("coin"):
        b, t, n = slope_t(g, "s7"); by[(k, "s7")] = {"slope": b, "t": t, "n": n}
    for k, g in G5.groupby("year"):
        b, t, n = slope_t(g, "s7"); by[(str(k), "s7")] = {"slope": b, "t": t, "n": n}
    out["h5_s7_by_coin_year"] = pd.DataFrame(by).T
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr, ignore_index=True)
    T["q"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc"] = T.groupby("q").agg(n=("net_profit_loss_percent", "count"),
        fc_lo=("entry_forecast", "min"), fc_hi=("entry_forecast", "max"),
        net_mean=("net_profit_loss_percent", "mean"), gross_mean=("profit_loss_percent", "mean"))
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
