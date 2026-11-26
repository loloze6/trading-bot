def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "day": ts.dt.floor("D"), "year": ts.dt.year,
                               "r30": c / c.shift(30) - 1, "r60": c / c.shift(60) - 1,
                               "r7": c / c.shift(7) - 1,
                               "vol30": r1.rolling(30).std()})
            for h in (5, 10, 20):
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (5, 10, 20):
        g = D[D["pos"] % h == 0]
        dr = g.groupby("coin")["f%d" % h].mean()
        D["u%d" % h] = D["f%d" % h] - D["coin"].map(dr)
    D["z30"] = D["r30"] / (D["vol30"] * np.sqrt(30))
    D["vrank"] = D.groupby("coin")["vol30"].rank(pct=True)
    D["agit"] = np.where(D["vrank"] > 0.5, "agitated", "calm")
    D["trend"] = np.where(D["r60"] > 0.10, "rising", np.where(D["r60"] < -0.10, "falling", "choppy"))
    D.loc[D["r60"].isna(), "trend"] = np.nan
    out = {}

    def pooled_t(g, col, sign):
        x = g[col] * sign
        m = x.mean()
        dev = (x - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return m, m / se if se > 0 else np.nan, g["day"].nunique()

    res = []
    for h in (5, 10, 20):
        C = D[(D["trend"] == "choppy") & (D["pos"] % h == 0)].dropna(subset=["z30", "u%d" % h])
        for side, sub, s in [("rise", C[C["z30"] > 0], 1), ("fall", C[C["z30"] < 0], -1)]:
            m, t, nd = pooled_t(sub, "u%d" % h, s)
            rho, p = stats.spearmanr(sub["z30"].abs(), sub["u%d" % h] * s)
            big = sub[sub["z30"].abs() > 1]; small = sub[sub["z30"].abs() <= 1]
            res.append({"h": h, "side": side, "n": len(sub), "days": nd, "mean_signed_u": m, "t_pooled": t,
                        "median_signed_u": (sub["u%d" % h] * s).median(),
                        "rho_abs": rho, "big_minus_small": (big["u%d" % h] * s).mean() - (small["u%d" % h] * s).mean(),
                        "n_big": len(big)})
    out["choppy_by_side"] = pd.DataFrame(res)

    # signed continuation (sign(z30) * u) in choppy, by agitation, by year, by window, h=5 and 10
    for h in (5, 10):
        C = D[(D["trend"] == "choppy") & (D["pos"] % h == 0)].dropna(subset=["z30", "u%d" % h]).copy()
        C["sc"] = np.sign(C["z30"]) * C["u%d" % h]
        C["wz"] = C["z30"] * C["u%d" % h]
        for key in ("agit", "year", "win", "coin"):
            t = C.groupby(key).agg(n=("sc", "size"), mean_sc=("sc", "mean"), med_sc=("sc", "median"),
                                   share_pos=("sc", lambda s: (s > 0).mean()))
            out["choppy_h%d_by_%s" % (h, key)] = t
    # choppy using r7 alone vs r30 controlling: partial
    C = D[(D["trend"] == "choppy") & (D["pos"] % 5 == 0)].dropna(subset=["z30", "u5", "r7"]).copy()
    C["z7"] = C["r7"] / (C["vol30"] * np.sqrt(7))
    out["choppy_spearman_z30_z7"] = pd.DataFrame({"z30_u5": [stats.spearmanr(C["z30"], C["u5"])[0]],
                                                 "z7_u5": [stats.spearmanr(C["z7"], C["u5"])[0]],
                                                 "z30_z7": [stats.spearmanr(C["z30"], C["z7"])[0]], "n": [len(C)]})
    # all bars non-choppy: same signed metric to compare
    res = []
    for tr in ("rising", "falling", "choppy"):
        for ag in ("calm", "agitated"):
            G = D[(D["trend"] == tr) & (D["agit"] == ag) & (D["pos"] % 10 == 0)].dropna(subset=["z30", "u10"])
            if len(G) < 15: continue
            sc = np.sign(G["z30"]) * G["u10"]
            res.append({"profile": tr + " " + ag, "n": len(G), "mean_sc10": sc.mean(),
                        "t": sc.mean() / (sc.std() / np.sqrt(len(sc))), "rho": stats.spearmanr(G["z30"], G["u10"])[0]})
    out["profile_continuation_h10"] = pd.DataFrame(res)
    return out
