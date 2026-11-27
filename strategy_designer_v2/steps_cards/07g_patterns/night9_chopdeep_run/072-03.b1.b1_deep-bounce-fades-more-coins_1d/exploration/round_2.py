import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            hi20 = c.rolling(20).max()
            depth = ((c - hi20) / hi20) / sd20
            r60 = c / c.shift(60) - 1
            reg = b["regime"].astype(str)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)), "r1": r1,
                              "depth": depth, "r60": r60, "reg": reg,
                              "day": ts.dt.floor("D"), "year": ts.dt.year,
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "sdrel": sd20 / sd20.rolling(60, min_periods=30).median()})
            for h in (1, 3, 10):
                d[f"f{h}"] = c.shift(-h) / c - 1
                d[f"g{h}"] = (d["i"] % h == 0) & d[f"f{h}"].notna()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 10):
        drift = D[D[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(drift)
    D["choppy"] = D["reg"] != "chop"
    D["tr"] = np.where(D["choppy"], "choppy",
               np.where(D["r60"] > 0.10, "rising", np.where(D["r60"] < -0.10, "falling", "trend_unk")))
    D["up"] = np.where(D["r1"] > 0, "up", "down")
    ok = D["depth"].notna()
    D.loc[ok, "dq"] = pd.qcut(D.loc[ok, "depth"].rank(method="first"), 5, labels=False)
    D["agit"] = np.where(D["sdrel"] > 1, "agit", "calm")
    def ct(sub, col):
        x = sub[[col, "day"]].dropna()
        n = len(x)
        if n < 5: return pd.Series({"n": n, "days": np.nan, "mean": np.nan, "t_day": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"n": n, "days": x["day"].nunique(), "mean": m, "t_day": m / se})
    out = {}
    up = D[(D["up"] == "up") & ok]
    for h in (1, 3, 10):
        g = up[up[f"g{h}"]]
        out[f"up days u{h} by trend x depth q"] = g.groupby(["tr", "dq"]).apply(lambda s: ct(s, f"u{h}"))
    g = up[up["g1"]]
    out["up days u1 deep q0 by trend x agit"] = g[g["dq"] == 0].groupby(["tr", "agit"]).apply(lambda s: ct(s, "u1"))
    out["up days u1 deep q0 by year"] = g[g["dq"] == 0].groupby("year").apply(lambda s: ct(s, "u1"))
    out["up days u1 q0 minus q4 by year"] = g.groupby("year").apply(
        lambda s: s.loc[s["dq"] == 0, "u1"].mean() - s.loc[s["dq"] == 4, "u1"].mean())
    # next-day continuous: deep up-day slope, all profiles
    gg = g.copy()
    out["up days u1 spearman depth vs u1 by trend"] = gg.groupby("tr").apply(
        lambda s: pd.Series({"rho": s["depth"].corr(s["u1"], method="spearman"), "n": len(s)}))
    # down days, all bars, by trend x depth (next day)
    dn = D[(D["up"] == "down") & ok & D["g1"]]
    out["down days u1 by trend x depth q"] = dn.groupby(["tr", "dq"]).apply(lambda s: ct(s, "u1"))
    # book: gain by entry depth and by holding age
    D["gain"] = D["alloc"] * D["f1"]
    held = D[D["alloc"].abs() > 0].copy()
    out["book gain by trend of bar"] = held.groupby(["tr", "up"]).apply(lambda s: ct(s, "gain"))
    return out
