import pandas as pd, numpy as np

def explore(data):
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        g_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            g_all.append(c[idx + H] / c[idx] - 1)
        g_all = np.concatenate(g_all)
        if len(g_all) < 10:
            continue
        drift, usual = g_all.mean(), g_all.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(60, min_periods=20).std()
            rng = (b["high"] - b["low"]) / c
            rng_s = rng / rng.rolling(60, min_periods=20).mean()
            rng3 = rng.rolling(3).mean() / rng.rolling(60, min_periods=20).mean()
            volu = b["volume"].astype(float)
            volu_s = volu / volu.rolling(60, min_periods=20).mean()
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in np.arange(0, len(c) - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 sr=r.iloc[i] / vol.iloc[i] if vol.iloc[i] > 0 else np.nan,
                                 rng_s=rng_s.iloc[i], rng3=rng3.iloc[i], volu_s=volu_s.iloc[i],
                                 u=fwd.iloc[i] - drift, z=(fwd.iloc[i] - drift) / usual))
    d = pd.DataFrame(rows).dropna(subset=["u", "rng_s", "sr"])
    d["up"] = np.where(d["sr"] > 0, "up", "down")

    def slope(x, col):
        X = x[col].values; Y = x["z"].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = Y - Y.mean() - b * Xc
        sc = pd.Series(Xc * e).groupby(x["day"].values).sum()
        se = np.sqrt((sc ** 2).sum()) / (Xc ** 2).sum()
        return pd.Series(dict(n=len(x), days=x["day"].nunique(), slope=b, t=b / se))

    def tab(x, col, q):
        x = x.copy(); x["b"] = pd.qcut(x[col], q, duplicates="drop")
        out = []
        for k, g in x.groupby("b", observed=True):
            dd = g.groupby("day")["u"].sum(); nd = len(dd)
            out.append(dict(bin=str(k), n=len(g), days=nd, mean_u_pct=100 * g["u"].mean(),
                            strength=g["z"].mean(),
                            t_day=g["u"].mean() / (dd.std() * np.sqrt(nd) / len(g))))
        return pd.DataFrame(out)

    d["lrng"] = np.log(d["rng_s"].clip(lower=0.05))
    d["lvol"] = np.log(d["volu_s"].clip(lower=0.05))
    res = {}
    res["slope_lrng_by_side"] = pd.DataFrame({s: slope(g, "lrng") for s, g in d.groupby("up")}).T
    res["slope_lvol_by_side"] = pd.DataFrame({s: slope(g.dropna(subset=["lvol"]), "lvol") for s, g in d.groupby("up")}).T
    res["slope_lrng_all"] = slope(d, "lrng").to_frame().T
    res["slope_rng3"] = slope(d.dropna(subset=["rng3"]).assign(l3=lambda x: np.log(x["rng3"])), "l3").to_frame().T
    res["rng_tab_up"] = tab(d[d.up == "up"], "rng_s", 5)
    res["rng_tab_down"] = tab(d[d.up == "down"], "rng_s", 5)
    res["slope_lrng_by_year"] = pd.DataFrame({y: slope(g, "lrng") for y, g in d.groupby("year")}).T
    bc = pd.DataFrame({c: slope(g, "lrng") for c, g in d.groupby("coin") if len(g) > 100}).T
    res["slope_lrng_by_coin"] = bc
    res["coins_positive_share"] = float((bc["slope"] > 0).mean())
    return res
