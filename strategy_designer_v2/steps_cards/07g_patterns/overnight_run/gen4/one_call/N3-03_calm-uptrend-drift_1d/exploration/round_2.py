def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = np.log(c).diff()
            vol20 = r1.rolling(20).std()
            vrank = vol20.rolling(100, min_periods=50).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ma100 = c.rolling(100, min_periods=60).mean()
            ret60 = np.log(c / c.shift(60))
            fwd5 = np.log(c.shift(-5) / c)
            fwd1 = r1.shift(-1)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "fwd5": fwd5, "fwd1": fwd1,
                "r1": r1, "vol20": vol20, "vrank": vrank, "above100": (c > ma100).where(ma100.notna()),
                "ret60": ret60, "fc": b["forecast"].astype(float), "wd": ts.dt.weekday, "yr": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float)}))
    D = pd.concat(rows, ignore_index=True)
    D["fwd5x"] = D["fwd5"] - D.groupby("coin")["fwd5"].transform("mean")
    D["fwd1x"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    def summ(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan, "hit": (x > 0).mean()})
    out = {}
    G = D[D["i"] % 5 == 0].dropna(subset=["fwd5x"])
    A = G[G["fc"] > 0]
    out["active_by_above_ma100"] = A.groupby("above100")["fwd5x"].apply(summ).unstack()
    out["active_by_ret60_sign"] = A.groupby(A["ret60"] > 0)["fwd5x"].apply(summ).unstack()
    Gl = G[G["vrank"] <= 0.5]
    out["calm_by_above100_ret60"] = Gl.groupby(["above100", Gl["ret60"] > 0])["fwd5x"].apply(summ).unstack()
    out["all_by_above100"] = G.groupby("above100")["fwd5x"].apply(summ).unstack()
    # weekday stability
    E = D.dropna(subset=["fwd1x"]).copy()
    E["tf"] = E["wd"].map({3: "thu_fri", 4: "thu_fri", 0: "mon_wed", 2: "mon_wed"}).fillna("other")
    tf = E[E["tf"] != "other"]
    piv = tf.groupby(["yr", "tf"])["fwd1x"].mean().unstack()
    piv["diff"] = piv["thu_fri"] - piv["mon_wed"]
    out["weekday_diff_by_year"] = piv
    pc = tf.groupby(["coin", "tf"])["fwd1x"].mean().unstack()
    pc["diff"] = pc["thu_fri"] - pc["mon_wed"]
    out["weekday_diff_by_coin"] = pc
    out["fwd1x_by_weekday_calm_vs_not"] = E.groupby([E["vrank"] <= 0.5, "wd"])["fwd1x"].mean().unstack()
    # down-day rebound
    E["z"] = E["r1"] / E["vol20"].shift(1)
    big = E[E["z"] <= -1.5]
    out["rebound_after_z_le_-1.5_by_coin"] = big.groupby("coin")["fwd1x"].apply(summ).unstack()
    out["rebound_by_year"] = big.groupby("yr")["fwd1x"].apply(summ).unstack()
    out["rebound_by_calm"] = big.groupby([big["vrank"] <= 0.5, big["above100"]])["fwd1x"].apply(summ).unstack()
    out["after_up_z_ge_1.5_by_above100"] = E[E["z"] >= 1.5].groupby("above100")["fwd1x"].apply(summ).unstack()
    # 2-day after down shock non-overlap not needed (1 day)
    return out
