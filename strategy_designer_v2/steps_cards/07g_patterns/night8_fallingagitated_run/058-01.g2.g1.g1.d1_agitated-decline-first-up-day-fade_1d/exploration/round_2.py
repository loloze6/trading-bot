def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["pos"] = np.arange(len(b))
            d["r0"] = r
            d["rprev"] = r.shift(1)
            d["f1"] = c.shift(-1) / c - 1
            d["f2"] = c.shift(-2) / c - 1
            up = (r > 0).astype(int)
            st = up.groupby((up != up.shift()).cumsum()).cumsum()
            d["upstreak"] = np.where(up == 1, st, 0)
            sd = r.rolling(30, min_periods=20).std()
            d["sd"] = sd
            d["r0z"] = r / sd
            d["rpz"] = r.shift(1) / sd
            d["rng"] = (b["high"] - b["low"]).astype(float) / c / sd
            d["clv"] = ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)).astype(float)
            d["gapup"] = (b["open"].astype(float) / c.shift(1) - 1) / sd
            d["tr60"] = (c / c.shift(60) - 1) * 100
            d["inprof"] = (b["regime"] != "chop").astype(int)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["fc"] = b["forecast"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2):
        D[f"e{h}"] = D[f"f{h}"] - D["coin"].map(D.groupby("coin")[f"f{h}"].mean())
    D["day"] = D["ts"].dt.floor("D")

    def ct(sub, col, sign=1):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan})
        x = sign * s[col]
        m = x.mean()
        g = (x - m).groupby(s["day"]).sum()
        D_ = len(g)
        se = np.sqrt((g ** 2).sum() * D_ / max(D_ - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D_, "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    P = D[D.inprof == 1]
    F = P[P.upstreak == 1]
    res = {}
    for col in ("r0z", "rpz", "clv", "rng", "gapup"):
        s = F.dropna(subset=[col]).copy()
        s["q"] = pd.qcut(s[col], 3, labels=False, duplicates="drop")
        for q in sorted(s.q.unique()):
            res[(col, q)] = ct(s[s.q == q], "e1", -1)
    out["first_up_in_profile_short_next_by_tercile"] = pd.DataFrame(res).T
    # correlation of grading vars with short-signed next excess, first up days
    cor = {}
    for col in ("r0z", "rpz", "clv", "rng", "gapup"):
        s = F.dropna(subset=[col, "e1"])
        cor[col] = pd.Series({"spearman": s[col].corr(-s["e1"], method="spearman"), "n": len(s)})
    out["first_up_spearman_with_short_next"] = pd.DataFrame(cor).T
    # all up days in profile (any streak) by r0z tercile
    U = P[P.upstreak >= 1].dropna(subset=["r0z"]).copy()
    U["q"] = pd.qcut(U["r0z"], 3, labels=False)
    out["all_up_in_profile_short_next_by_r0z"] = U.groupby("q").apply(lambda s: ct(s, "e1", -1))
    # out of profile, first up day, by 60d trend computable within window
    O = D[(D.inprof == 0) & (D.upstreak == 1)].dropna(subset=["tr60"]).copy()
    O["tr"] = np.where(O.tr60 < -10, "falling", np.where(O.tr60 > 10, "rising", "choppy"))
    out["first_up_out_profile_short_next_by_trend60"] = O.groupby("tr").apply(lambda s: ct(s, "e1", -1))
    # down days in profile by prior size: compare
    Dn = P[P.r0 < 0].dropna(subset=["r0z"]).copy()
    Dn["q"] = pd.qcut(Dn["r0z"], 3, labels=False)
    out["down_days_in_profile_long_next_by_r0z"] = Dn.groupby("q").apply(lambda s: ct(s, "e1"))
    # book: largest days concentration
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            x = t.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    bs = bk.sort_values(ascending=False).values
    out["book_concentration"] = pd.Series({
        "total_sum": bk.sum(), "top5_sum": bs[:5].sum(), "top10_sum": bs[:10].sum(),
        "bottom5_sum": bs[-5:].sum(), "bottom10_sum": bs[-10:].sum(),
        "w14_sum": bk.loc["w14"].sum(), "nonzero_days": int((bk != 0).sum())})
    return out
