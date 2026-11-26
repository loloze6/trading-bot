def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame(index=b.index)
            df["coin"] = coin
            df["win"] = w
            df["r"] = r.values
            df["nxt1"] = (c.shift(-1) / c - 1).values
            df["nxt3"] = (c.shift(-3) / c - 1).values
            sd = r.rolling(30, min_periods=20).std()
            df["sd"] = sd.values
            df["z1"] = (r / sd).values
            df["z3"] = ((c / c.shift(3) - 1) / (sd * np.sqrt(3))).values
            df["rng"] = ((b["high"] - b["low"]) / c / sd).values
            df["clpos"] = ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)).values
            up = (r > 0).astype(int)
            df["upstreak"] = (up.groupby((up != up.shift()).cumsum()).cumsum() * up).values
            dn = (r < 0).astype(int)
            df["dnstreak"] = (dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn).values
            df["inprof"] = (b["regime"].astype(str) != "chop").values
            ts = pd.to_datetime(b["timestamp"])
            df["wd"] = ts.dt.weekday.values
            df["year"] = ts.dt.year.values
            df["idx"] = np.arange(len(df))
            df["pos3"] = (df["idx"] % 3 == 0)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["r", "sd"])
    drift1 = D.groupby("coin")["nxt1"].mean()
    drift3 = D[D.pos3].groupby("coin")["nxt3"].mean()
    D["u1"] = D["nxt1"] - D["coin"].map(drift1)
    D["u3"] = D["nxt3"] - D["coin"].map(drift3)

    def summ(g, col="u1"):
        x = g[col].dropna()
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(n))})

    def grp(X, key, col="u1"):
        try:
            res = {}
            for k, g in X.groupby(key):
                res[k] = summ(g, col)
            return pd.DataFrame(res).T
        except Exception as e:
            return "err " + str(e)[:80]

    def q(s, n=5):
        return pd.qcut(s, n, labels=False, duplicates="drop")

    out = {}
    P = D[D.inprof]; O = D[~D.inprof]
    out["share_in_profile"] = float(D.inprof.mean())
    out["prof_upstreak_next1"] = grp(P, P.upstreak.clip(0, 4))
    out["prof_dnstreak_next1"] = grp(P, P.dnstreak.clip(0, 4))
    out["outprof_upstreak_next1"] = grp(O, O.upstreak.clip(0, 4))
    out["prof_z1_quint_next1"] = grp(P, q(P.z1))
    out["outprof_z1_quint_next1"] = grp(O, q(O.z1))
    P3 = P[P.pos3]; O3 = O[O.pos3]
    out["prof_z3_quint_next3_nonov"] = grp(P3, q(P3.z3), "u3")
    out["outprof_z3_quint_next3_nonov"] = grp(O3, q(O3.z3), "u3")
    out["prof_rng_quint_next1"] = grp(P, q(P.rng))
    out["outprof_rng_quint_next1"] = grp(O, q(O.rng))
    F = P[P.upstreak == 1]
    out["prof_firstup_rng_tercile"] = grp(F, q(F.rng, 3))
    out["prof_firstup_clpos_tercile"] = grp(F, q(F.clpos, 3))
    out["prof_firstup_by_year"] = grp(F, "year")
    out["prof_firstup_by_coin"] = grp(F, "coin")
    Dn = P[P.dnstreak >= 1]
    out["prof_downday_rng_tercile"] = grp(Dn, q(Dn.rng, 3))
    out["prof_weekday_next1"] = grp(P, "wd")
    out["all_weekday_next1"] = grp(D, "wd")
    out["prof_clpos_quint_next1"] = grp(P, q(P.clpos))
    out["outprof_clpos_quint_next1"] = grp(O, q(O.clpos))
    try:
        dd = []
        for coin, wins in data["days"].items():
            for w, d in wins.items():
                x = d[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
                dd.append(x)
        Dd = pd.concat(dd, ignore_index=True).dropna()
        big = Dd.loc[Dd.book_return.abs().sort_values(ascending=False).index[:30]]
        out["book_top30_by_coin_sign"] = big.groupby(["coin", np.sign(big.book_return)]).size()
        out["book_by_coin_sum%"] = Dd.groupby("coin").book_return.sum() * 100
        out["book_by_window_sum%"] = Dd.groupby("win").book_return.sum() * 100
    except Exception as e:
        out["book_err"] = str(e)[:100]
    return out
