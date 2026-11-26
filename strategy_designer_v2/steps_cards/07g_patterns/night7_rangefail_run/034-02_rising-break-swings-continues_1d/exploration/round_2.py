def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi20 = c.shift(1).rolling(20).max()
            sd20 = r1.rolling(20).std()
            dist = (c - hi20) / hi20 / sd20
            tr60 = c / c.shift(60) - 1
            ret20 = c / c.shift(20) - 1
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "dist": dist, "tr60": tr60, "ret20": ret20,
                               "r1z": r1 / sd20, "fwd": fwd, "usual": np.nan,
                               "day": ts.dt.floor("D"), "wd": ts.dt.weekday, "year": ts.dt.year})
            rows.append(df.iloc[::H])
    d = pd.concat(rows).dropna(subset=["fwd"])
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["usual"] = d.groupby("coin")["fwd"].transform("std")
    d["prof"] = np.where(d["tr60"] > .10, "rising", np.where(d["tr60"] < -.10, "falling", "choppy"))
    d.loc[d["tr60"].isna(), "prof"] = np.nan

    def ct(g, col="ex"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": g[col].mean(), "t_day": np.nan})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": m, "t_day": m / se})

    out = {}
    dd = d.dropna(subset=["dist", "prof"]).copy()
    # breakouts outside rising: graded?
    bk = dd[dd["dist"] > 0]
    out["breakout_by_prof_dayt"] = bk.groupby("prof").apply(ct)
    out["breakout_spearman_by_prof"] = bk.groupby("prof").apply(lambda g: pd.Series(stats.spearmanr(g["dist"], g["ex"])[:2], index=["rho", "p"]))
    nr = bk[bk["prof"] != "rising"].copy()
    nr["half"] = np.where(nr["dist"] > nr["dist"].median(), "far_above", "near_above")
    out["breakout_nonrising_halves"] = nr.groupby("half").apply(ct)
    # below-high depth in choppy: continuation down?
    ch = dd[dd["prof"] == "choppy"].copy()
    ch["b"] = pd.cut(ch["dist"], [-100, -4, -2, 0, 100])
    out["choppy_depth_dayt"] = ch.groupby("b").apply(ct)
    out["choppy_dist_spearman_below0"] = pd.Series(stats.spearmanr(ch.loc[ch.dist < 0, "dist"], ch.loc[ch.dist < 0, "ex"])[:2], index=["rho", "p"])
    out["choppy_depth_by_year"] = ch[ch["dist"] < -2].groupby("year").apply(ct)
    # strength scaled by usual move, all profiles graded on dist
    dd["s"] = dd["ex"] / dd["usual"]
    dd["q"] = pd.qcut(dd["dist"], 5)
    out["all_dist_quintiles_strength"] = dd.groupby("q").apply(lambda g: ct(g, "s"))
    out["all_dist_quintiles_by_year_top_minus_bottom"] = dd.groupby("year").apply(
        lambda g: g.loc[g["dist"] > dd["dist"].quantile(.8), "ex"].mean() - g.loc[g["dist"] < dd["dist"].quantile(.2), "ex"].mean())
    out["weekday_dayt"] = d.groupby("wd").apply(ct)
    d2 = d.dropna(subset=["r1z"]).copy()
    d2["b"] = pd.qcut(d2["r1z"], 6)
    out["r1z_dayt"] = d2.groupby("b").apply(ct)
    d4 = d.dropna(subset=["ret20", "prof"]).copy()
    d4["b"] = pd.qcut(d4["ret20"], 4)
    out["ret20_by_prof_dayt"] = d4.groupby(["prof", "b"]).apply(ct)
    return out
