def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = pd.Timedelta(hours=1)
    recs = []; dayrecs = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df[["timestamp", "close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            ts = d["timestamp"]
            r1 = d["close"].pct_change().where((ts - ts.shift(1)) == H)
            d["ct"] = ts + H
            d["hr"] = d["ct"].dt.hour; d["wd"] = d["ct"].dt.weekday; d["yr"] = d["ct"].dt.year
            d["r1"] = r1
            # at close 22:00 (bar ending 22:00): past 8h return (14->22), next 3h (22->01)
            past8 = d["close"] / d["close"].shift(8) - 1
            past8 = past8.where((ts - ts.shift(8)) == 8 * H)
            fwd3 = d["close"].shift(-3) / d["close"] - 1
            fwd3 = fwd3.where((ts.shift(-3) - ts) == 3 * H)
            fwd2 = d["close"].shift(-2) / d["close"] - 1
            fwd2 = fwd2.where((ts.shift(-2) - ts) == 2 * H)
            vol = r1.rolling(168, min_periods=100).std()
            s = d[d["hr"] == 21].copy()
            s["past8"] = past8[s.index]; s["fwd2"] = fwd2[s.index]; s["fwd3"] = fwd3[s.index]
            s["vol"] = vol[s.index]; s["coin"] = coin; s["w"] = w
            recs.append(s[["coin", "w", "wd", "yr", "past8", "fwd2", "fwd3", "vol"]])
            # daily: Friday return (Fri00->Sat00) vs Saturday return
            dd = d[d["hr"] == 0].copy()
            dd["ret_next24"] = d["close"].shift(-24)[dd.index] / dd["close"] - 1
            dd["ok"] = ((ts.shift(-24) - ts) == 24 * H)[dd.index]
            dd["ret_past24"] = dd["close"] / d["close"].shift(24)[dd.index] - 1
            dd["okp"] = ((ts - ts.shift(24)) == 24 * H)[dd.index]
            dd = dd[dd["ok"] & dd["okp"]]
            dd["coin"] = coin
            dayrecs.append(dd[["coin", "wd", "yr", "ret_next24", "ret_past24"]])
    S = pd.concat(recs).dropna()
    # late-hours 2h move (close 21 -> close 23, i.e. bars of hours 22,23) stats
    S["z2"] = S["fwd2"] / S["vol"] / np.sqrt(2)
    out["late2h_overall"] = pd.Series({"n": len(S), "mean_fwd2_pct": S["fwd2"].mean() * 100,
                                       "t": S["fwd2"].mean() / S["fwd2"].std() * np.sqrt(len(S))})
    out["late2h_by_year"] = S.groupby("yr")["fwd2"].agg(mean_pct=lambda x: x.mean() * 100, n="size",
                                                       t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["late2h_by_coin"] = S.groupby("coin")["fwd2"].agg(mean_pct=lambda x: x.mean() * 100,
                                                         t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["late2h_by_weekday"] = S.groupby("wd")["fwd2"].agg(mean_pct=lambda x: x.mean() * 100,
                                                          t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    S["p8z"] = S["past8"] / S["vol"]
    S["q"] = pd.qcut(S["p8z"], 5, labels=False)
    out["late2h_by_past8_quintile"] = S.groupby("q").agg(p8z=("p8z", "mean"), fwd2_pct=("fwd2", lambda x: x.mean() * 100),
                                                         n=("fwd2", "size"))
    lr = stats.linregress(S["p8z"], S["fwd2"] / S["vol"])
    out["late2h_on_past8_slope"] = pd.Series({"slope": lr.slope, "t": lr.slope / lr.stderr})
    S["vq"] = S.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["late2h_by_vol_tercile"] = S.groupby("vq")["fwd2"].agg(mean_pct=lambda x: x.mean() * 100,
                                                              t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    Dd = pd.concat(dayrecs).dropna()
    res = []
    for wd, s in Dd.groupby("wd"):
        lr = stats.linregress(s["ret_past24"], s["ret_next24"])
        res.append({"wd_close": wd, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr,
                    "mean_next_pct": s["ret_next24"].mean() * 100})
    out["day_momentum_by_weekday"] = pd.DataFrame(res)
    return out
