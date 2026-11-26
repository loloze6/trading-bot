def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w})
            df["r"] = r
            df["nxt1"] = c.shift(-1) / c - 1
            df["nxt3"] = c.shift(-3) / c - 1
            sd = r.rolling(30, min_periods=20).std()
            df["sd"] = sd
            df["z1"] = r / sd
            df["z3"] = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            df["rng"] = (b["high"] - b["low"]) / c / sd
            df["clpos"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            up = (r > 0).astype(int)
            st = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            dn = (r < 0).astype(int)
            sdn = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            df["upstreak"] = st
            df["dnstreak"] = sdn
            df["inprof"] = (b["regime"] != "chop").values
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            df["year"] = pd.to_datetime(b["timestamp"]).dt.year
            df["pos"] = b["postRebalance_current_allocation"].astype(float)
            df["idx"] = np.arange(len(df))
            df["pos3"] = (df["idx"] % 3 == 0)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["r", "sd"])
    # drift per coin over all windows
    drift1 = D.groupby("coin")["nxt1"].mean()
    drift3 = D[D.pos3].groupby("coin")["nxt3"].mean()
    D["u1"] = D["nxt1"] - D["coin"].map(drift1)
    D["u3"] = D["nxt3"] - D["coin"].map(drift3)

    def summ(g, col="u1"):
        x = g[col].dropna()
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})

    out = {}
    P = D[D.inprof]
    O = D[~D.inprof]
    out["share_in_profile"] = float(D.inprof.mean())
    out["prof_upstreak_next1"] = P.groupby(P.upstreak.clip(0, 4)).apply(summ)
    out["prof_dnstreak_next1"] = P.groupby(P.dnstreak.clip(0, 4)).apply(summ)
    out["outprof_upstreak_next1"] = O.groupby(O.upstreak.clip(0, 4)).apply(summ)
    out["prof_z1_quint_next1"] = P.groupby(pd.qcut(P.z1, 5, labels=False)).apply(summ)
    out["outprof_z1_quint_next1"] = O.groupby(pd.qcut(O.z1, 5, labels=False)).apply(summ)
    P3 = P[P.pos3]
    out["prof_z3_quint_next3_nonoverlap"] = P3.groupby(pd.qcut(P3.z3, 5, labels=False)).apply(lambda g: summ(g, "u3"))
    O3 = O[O.pos3]
    out["outprof_z3_quint_next3_nonoverlap"] = O3.groupby(pd.qcut(O3.z3, 5, labels=False)).apply(lambda g: summ(g, "u3"))
    out["prof_rng_quint_next1"] = P.groupby(pd.qcut(P.rng, 5, labels=False)).apply(summ)
    F = P[P.upstreak == 1]
    out["prof_firstup_closepos_tercile"] = F.groupby(pd.qcut(F.clpos, 3, labels=False)).apply(summ)
    out["prof_firstup_by_year"] = F.groupby("year").apply(summ)
    out["prof_firstup_by_coin"] = F.groupby("coin").apply(summ)
    out["prof_weekday_next1"] = P.groupby("wd").apply(summ)
    out["all_weekday_next1"] = D.groupby("wd").apply(summ)
    # close position overall in profile
    out["prof_closepos_quint_next1"] = P.groupby(pd.qcut(P.clpos, 5, labels=False)).apply(summ)
    # book daily: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            dd.append(x)
    Dd = pd.concat(dd).dropna()
    big = Dd.reindex(Dd.book_return.abs().sort_values(ascending=False).index).head(30)
    out["book_top30_abs_days_by_coin_sign"] = big.groupby(["coin", np.sign(big.book_return)]).size()
    out["book_by_coin_sum%"] = Dd.groupby("coin").book_return.sum() * 100
    out["book_by_window_sum%"] = Dd.groupby("win").book_return.sum() * 100
    return out
