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
            for h in (1, 2, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
            up = (r > 0).astype(int)
            st = up.groupby((up != up.shift()).cumsum()).cumsum()
            d["upstreak"] = np.where(up == 1, st, 0)
            dn = (r < 0).astype(int)
            st2 = dn.groupby((dn != dn.shift()).cumsum()).cumsum()
            d["dnstreak"] = np.where(dn == 1, st2, 0)
            sd = r.rolling(30, min_periods=20).std()
            d["sd"] = sd
            d["rng"] = (b["high"] - b["low"]).astype(float) / c / sd
            d["r0z"] = r / sd
            d["r3z"] = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            d["clv"] = ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)).astype(float)
            d["inprof"] = (b["regime"] != "chop").astype(int)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["wd"] = d["ts"].dt.weekday
            d["year"] = d["ts"].dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    for h in (1, 2, 3, 5):
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
    O = D[D.inprof == 0]
    # 1. next-day excess by up streak, in and out of profile (long sign)
    res = {}
    for name, S in (("in", P), ("out", O)):
        for k in (1, 2, 3):
            sub = S[(S.upstreak == k) if k < 3 else (S.upstreak >= 3)]
            res[(name, f"up{k}")] = ct(sub, "e1")
        for k in (1, 2, 3):
            sub = S[(S.dnstreak == k) if k < 3 else (S.dnstreak >= 3)]
            res[(name, f"dn{k}")] = ct(sub, "e1")
    out["next_day_excess_long_by_streak"] = pd.DataFrame(res).T
    # 2. first up day in profile: by range quintile, horizons, grid h
    res = {}
    for name, S in (("in", P), ("out", O)):
        s = S[S.upstreak == 1].dropna(subset=["rng"]).copy()
        s["q"] = pd.qcut(s["rng"], 4, labels=False)
        for q in range(4):
            res[(name, q)] = ct(s[s.q == q], "e1")
    out["first_up_day_next_excess_by_range_quartile"] = pd.DataFrame(res).T
    # horizons on grid
    res = {}
    for h in (1, 2, 3, 5):
        for name, S in (("in", P), ("out", O)):
            s = S[(S.upstreak == 1) & (S.pos % h == 0)]
            res[(name, f"h{h}")] = ct(s, f"e{h}")
            s = S[(S.upstreak >= 2) & (S.pos % h == 0)]
            res[(name + "_up2+", f"h{h}")] = ct(s, f"e{h}")
    out["up_days_excess_long_by_horizon"] = pd.DataFrame(res).T
    # 3. all days in profile by return z quintile, and by 3-day z
    res = {}
    for col in ("r0z", "r3z", "rng", "clv"):
        s = P.dropna(subset=[col]).copy()
        s["q"] = pd.qcut(s[col], 5, labels=False, duplicates="drop")
        for q in sorted(s.q.unique()):
            res[(col, q)] = ct(s[s.q == q], "e1")
    out["in_profile_next_excess_by_quintile"] = pd.DataFrame(res).T
    res = {}
    for col in ("r0z", "r3z"):
        s = O.dropna(subset=[col]).copy()
        s["q"] = pd.qcut(s[col], 5, labels=False, duplicates="drop")
        for q in sorted(s.q.unique()):
            res[(col, q)] = ct(s[s.q == q], "e1")
    out["out_profile_next_excess_by_quintile"] = pd.DataFrame(res).T
    # 4. weekday in profile
    out["in_profile_weekday"] = P.groupby("wd").apply(lambda s: ct(s, "e1"))
    out["first_up_in_profile_by_year"] = P[P.upstreak == 1].groupby("year").apply(lambda s: ct(s, "e1", -1))
    out["first_up_in_profile_by_coin"] = P[P.upstreak == 1].groupby("coin").apply(lambda s: ct(s, "e1", -1))
    out["profile_share"] = float(D.inprof.mean())
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            x = t.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "sum", "min", "max"])
    return out
