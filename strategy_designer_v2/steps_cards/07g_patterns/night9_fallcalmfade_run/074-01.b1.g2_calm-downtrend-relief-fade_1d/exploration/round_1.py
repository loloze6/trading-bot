def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            df["r0"] = r
            df["r1"] = c.shift(-1)/c - 1
            df["r2"] = c.shift(-2)/c - 1
            df["r3"] = c.shift(-3)/c - 1
            df["sd30"] = r.shift(1).rolling(30, min_periods=20).std()
            df["tr60"] = c/c.shift(60) - 1
            down = (r < 0).astype(int).values
            run = np.zeros(len(c), int); loss = np.zeros(len(c))
            for i in range(1, len(c)):
                k = 0; j = i-1
                while j >= 1 and down[j] == 1 and k < 30:
                    k += 1; j -= 1
                run[i] = k
                loss[i] = (c.iloc[i-1]/c.iloc[i-1-k] - 1) if k > 0 else 0.0
            up = (r > 0).astype(int).values
            urun = np.zeros(len(c), int)
            for i in range(1, len(c)):
                k = 0; j = i-1
                while j >= 1 and up[j] == 1 and k < 30:
                    k += 1; j -= 1
                urun[i] = k
            df["run"] = run; df["loss"] = loss; df["urun"] = urun
            df["depth"] = -df["loss"]/df["sd30"]
            df["fc"] = b["forecast"].values
            df["alloc"] = b["postRebalance_current_allocation"].values
            df["wd"] = df["ts"].dt.weekday
            df["yr"] = df["ts"].dt.year
            df["day"] = df["ts"].dt.floor("D")
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].mean()
    D["mu"] = D["coin"].map(mu)
    D["x1"] = D["r1"] - D["mu"]
    D["x2"] = D["r2"] - 2*D["mu"]
    D["x3"] = D["r3"] - 3*D["mu"]
    D["trend"] = np.where(D["tr60"] > 0.10, "rising", np.where(D["tr60"] < -0.10, "falling", np.where(D["tr60"].notna(), "choppy", "na")))
    D["z0"] = D["r0"]/D["sd30"]
    def ct(v, d):
        m = pd.DataFrame({"v": v, "d": d}).dropna()
        if len(m) < 5: return pd.Series({"n": len(m), "days": m["d"].nunique() if len(m) else 0, "mean": np.nan, "t": np.nan})
        mean = m["v"].mean()
        S = (m["v"]-mean).groupby(m["d"]).sum()
        se = np.sqrt((S**2).sum())/len(m)
        return pd.Series({"n": len(m), "days": m["d"].nunique(), "mean": mean, "t": mean/se if se > 0 else np.nan})
    out = {}
    rb = D[(D["r0"] > 0) & (D["run"] >= 1)].copy()
    rb["rb"] = rb["run"].clip(upper=4)
    out["runbreak_short_x1_by_trend_run"] = rb.groupby(["trend", "rb"]).apply(lambda g: ct(-g["x1"], g["day"])).round(4)
    out["runbreak_run2_short_x2_x3_by_trend"] = pd.concat({
        "x2": rb[rb.run >= 2].groupby("trend").apply(lambda g: ct(-g["x2"], g["day"])),
        "x3": rb[rb.run >= 2].groupby("trend").apply(lambda g: ct(-g["x3"], g["day"]))}, axis=1).round(4)
    rb2 = rb[rb.run >= 2].copy()
    rb2["dq"] = pd.qcut(rb2["depth"], 4, labels=False, duplicates="drop")
    out["runbreak_run2_short_x1_by_depthq"] = rb2.groupby("dq").apply(lambda g: ct(-g["x1"], g["day"])).round(4)
    # mirror: first down day after up run
    md = D[(D["r0"] < 0) & (D["urun"] >= 1)].copy()
    md["ub"] = md["urun"].clip(upper=4)
    out["mirror_downbreak_long_x1_by_trend_run"] = md.groupby(["trend", "ub"]).apply(lambda g: ct(g["x1"], g["day"])).round(4)
    # all bars: next day by today's scaled move decile
    a = D.dropna(subset=["z0", "x1"]).copy()
    a["zq"] = pd.qcut(a["z0"], 10, labels=False, duplicates="drop")
    out["all_x1_by_z0_decile"] = a.groupby("zq").apply(lambda g: ct(g["x1"], g["day"])).round(4)
    out["all_x1_by_z0_decile_falling"] = a[a.trend == "falling"].groupby(pd.qcut(a[a.trend == "falling"]["z0"], 5, labels=False)).apply(lambda g: ct(g["x1"], g["day"])).round(4)
    out["all_x1_by_weekday"] = a.groupby("wd").apply(lambda g: ct(g["x1"], g["day"])).round(4)
    out["all_x1_by_trend"] = a.groupby("trend").apply(lambda g: ct(g["x1"], g["day"])).round(4)
    act = D[D["fc"] < 0]
    out["book_cases_short_x1_by_year"] = act.groupby("yr").apply(lambda g: ct(-g["x1"], g["day"])).round(4)
    out["book_cases_short_x1_by_coin"] = act.groupby("coin").apply(lambda g: ct(-g["x1"], g["day"])).round(4)
    out["book_cases_trend_share"] = act["trend"].value_counts()
    return out
