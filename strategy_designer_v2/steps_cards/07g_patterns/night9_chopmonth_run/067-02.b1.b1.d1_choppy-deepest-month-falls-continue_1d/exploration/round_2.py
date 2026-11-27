def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            v30 = r1.rolling(30).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r30": c / c.shift(30) - 1, "r60": c / c.shift(60) - 1,
                "r14": c / c.shift(14) - 1,
                "f7": c.shift(-7) / c - 1, "f3": c.shift(-3) / c - 1, "f14": c.shift(-14) / c - 1,
                "vol30": v30,
                "vmed": v30.expanding(min_periods=20).median(),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for h in ["f3", "f7", "f14"]:
        hn = int(h[1:])
        dr = d[d.pos % hn == 0].groupby("coin")[h].mean()
        d["u" + h[1:]] = d[h] - d.coin.map(dr)
    d["year"] = d.ts.dt.year
    d["day"] = d.ts.dt.floor("D")
    d["agit"] = d.vol30 > d.vmed
    d["trend"] = np.where(d.r60 > 0.10, "rising", np.where(d.r60 < -0.10, "falling", "choppy"))
    d["prof"] = d.trend + "_" + np.where(d.agit, "agit", "calm")
    g = d[d.pos % 7 == 0].dropna(subset=["u7", "r30", "r60", "vol30", "vmed"]).copy()
    g["sr30"] = g.r30 / (g.vol30 * np.sqrt(30))
    def clus_t(x, col):
        x = x.dropna(subset=[col])
        s = x.groupby("day")[col].sum()
        G = len(s); n = len(x)
        if G < 3: return np.nan
        m = x[col].mean()
        dev = x.groupby("day")[col].apply(lambda v: (v - m).sum())
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return m / se
    # signed signal: return in direction of the month (continuation) = sign(r30)*u7 weighted by |sr30|
    res = []
    for p, x in g.groupby("prof"):
        x = x.copy()
        x["cont"] = np.sign(x.r30) * x.u7
        rho, pv = stats.spearmanr(x.r30, x.u7)
        q = pd.qcut(x.r30.rank(method="first"), 3, labels=False)
        lo = x[q == 0]; hi = x[q == 2]
        res.append({"prof": p, "n": len(x), "days": x.day.nunique(), "rho": rho, "p": pv,
                    "low3_u7": lo.u7.mean(), "low3_t": clus_t(lo, "u7"),
                    "high3_u7": hi.u7.mean(), "high3_t": clus_t(hi, "u7"),
                    "cont_mean": x.cont.mean(), "cont_t": clus_t(x, "cont")})
    out["by_profile_r30"] = pd.DataFrame(res).set_index("prof")
    # falling agitated: graded quintiles of r30, and by year
    fa = g[g.prof == "falling_agit"].copy()
    fa["q"] = pd.qcut(fa.r30.rank(method="first"), 5, labels=False)
    out["falling_agit_q30"] = fa.groupby("q").agg(n=("u7", "size"), r30=("r30", "mean"), u7=("u7", "mean"))
    fa["rev"] = -np.sign(fa.r30) * fa.u7
    out["falling_agit_rev_by_year"] = fa.groupby("year").agg(n=("rev", "size"), rev=("rev", "mean"))
    out["falling_agit_rho_year"] = fa.groupby("year").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x.r30, x.u7)[0]}))
    # falling agitated, only months up (r30>0): a bear rally
    up = fa[fa.r30 > 0]
    out["falling_agit_r30pos"] = pd.Series({"n": len(up), "u7": up.u7.mean(), "t": clus_t(up, "u7"),
                                            "rho": stats.spearmanr(up.r30, up.u7)[0] if len(up) > 5 else np.nan})
    dn = fa[fa.r30 <= 0]
    out["falling_agit_r30neg"] = pd.Series({"n": len(dn), "u7": dn.u7.mean(), "t": clus_t(dn, "u7"),
                                            "rho": stats.spearmanr(dn.r30, dn.u7)[0] if len(dn) > 5 else np.nan})
    # choppy calm by year and by side
    cc = g[g.prof == "choppy_calm"].copy()
    cc["cont"] = np.sign(cc.r30) * cc.u7
    out["choppy_calm_cont_year"] = cc.groupby("year").agg(n=("cont", "size"), cont=("cont", "mean"))
    out["choppy_calm_side"] = cc.groupby(cc.r30 > 0).apply(lambda x: pd.Series({"n": len(x), "u7": x.u7.mean(), "t": clus_t(x, "u7"), "rho": stats.spearmanr(x.r30, x.u7)[0]}))
    # falling calm by year
    fc = g[g.prof == "falling_calm"].copy()
    fc["cont"] = np.sign(fc.r30) * fc.u7
    out["falling_calm_cont_year"] = fc.groupby("year").agg(n=("cont", "size"), cont=("cont", "mean"))
    # other horizons for falling agit reversal
    for h in [3, 14]:
        gh = d[(d.pos % h == 0) & (d.prof == "falling_agit")].dropna(subset=["u" + str(h), "r30"])
        out[f"falling_agit_rho_h{h}"] = pd.Series({"n": len(gh), "rho": stats.spearmanr(gh.r30, gh["u" + str(h)])[0], "p": stats.spearmanr(gh.r30, gh["u" + str(h)])[1]})
    return out
