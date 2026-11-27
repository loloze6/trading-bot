def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        # coin drift over all its windows (1-day returns, non-overlapping grid of 1)
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(c[1:] / c[:-1] - 1)
        drift1 = np.concatenate(allr).mean()
        sd1 = np.concatenate(allr).std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = h - l
            mr = rng.rolling(20, min_periods=20).mean()
            width = rng / mr
            loc = (c - l) / rng.replace(0, np.nan)
            raw = (c - (h + l) / 2) / mr
            tr60 = c / c.shift(60) - 1
            for k in (1, 2, 3):
                b[f"r{k}"] = c.shift(-k) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "year": ts.dt.year, "wd": ts.dt.weekday, "day": ts.dt.floor("D"),
                "regime": b["regime"], "fc": b["forecast"], "width": width, "loc": loc, "raw": raw,
                "tr60": tr60, "r1": b["r1"], "r2": b["r2"], "r3": b["r3"], "drift": drift1, "sd": sd1,
                "dayret": c / o - 1})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["u1"] = -(D["r1"] - D["drift"])
    D["u2"] = -(D["r2"] - 2 * D["drift"])
    D["u3"] = -(D["r3"] - 3 * D["drift"])

    def ct(s, days):
        s = s.dropna(); dd = days.loc[s.index]
        m = s.mean()
        g = (s - m).groupby(dd).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return m, (m / se if se > 0 else np.nan), len(s), dd.nunique()

    def summ(sub, col="u1"):
        m, t, n, nd = ct(sub[col], sub["day"])
        return pd.Series({"mean": m, "t": t, "n": n, "days": nd})

    cases = D[(D["regime"] == "mean_reversion") & (D["fc"] < 0)].copy()
    out = {}
    out["cases_h1_h2_h3"] = pd.DataFrame({k: summ(cases, k) for k in ["u1", "u2", "u3"]}).T
    out["by_coin"] = cases.groupby("coin").apply(summ)
    out["by_window"] = cases.groupby("win").apply(summ)
    out["by_year"] = cases.groupby("year").apply(summ)
    cases["fq"] = pd.qcut(cases["fc"].rank(method="first"), 4, labels=["q1_strongest", "q2", "q3", "q4_weakest"])
    out["by_forecast_quartile"] = cases.groupby("fq").apply(summ)
    cases["wq"] = pd.qcut(cases["width"], 3, labels=["w_low", "w_mid", "w_high"])
    cases["lq"] = pd.qcut(cases["loc"], 3, labels=["l_low", "l_mid", "l_high"])
    out["by_width_tercile"] = cases.groupby("wq").apply(summ)
    out["by_loc_tercile"] = cases.groupby("lq").apply(summ)
    cases["upday"] = np.where(cases["dayret"] > 0, "up_day", "down_day")
    out["by_up_down_day"] = cases.groupby("upday").apply(summ)
    # same pattern outside the falling agitated profile (chop = profile vetoed)
    pat = (D["width"] > 1) & (D["loc"] > 0.5)
    other = D[pat & (D["regime"] == "chop")].copy()
    other["trend"] = np.where(other["tr60"] > 0.10, "rising", np.where(other["tr60"] < -0.10, "falling", np.where(other["tr60"].notna(), "choppy", "na")))
    out["pattern_outside_profile_by_trend"] = other.groupby("trend").apply(summ)
    inprof_nopat = D[(D["regime"] == "unknown")]
    out["in_profile_no_pattern"] = summ(inprof_nopat).to_frame().T
    out["regime_counts"] = D["regime"].value_counts()
    return out
