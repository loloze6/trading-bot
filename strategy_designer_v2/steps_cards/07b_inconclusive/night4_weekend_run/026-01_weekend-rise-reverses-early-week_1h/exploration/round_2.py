def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; drift = {}; usual = {}
    for coin, wins in bars.items():
        g48 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48 += list(c[idx + 48] / c[idx] - 1)
        drift[coin] = np.mean(g48); usual[coin] = np.std(g48)
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"]); c = df["close"].values; n = len(c)
            lr = np.diff(np.log(c), prepend=np.nan)
            pos = np.where((ts.dt.weekday.values == 6) & (ts.dt.hour.values == 23))[0]
            for p in pos:
                if p - 720 < 0 or p + 48 >= n:
                    continue
                past = c[p] / c[p - 48] - 1
                rows.append({"coin": coin, "year": ts.iloc[p].year, "past": past,
                             "past_z": past / usual[coin],
                             "tr30": c[p - 48] / c[p - 720] - 1,
                             "vol_wkend": np.nanstd(lr[p - 47:p + 1]),
                             "vol_prior": np.nanstd(lr[p - 215:p - 47]),
                             "u48": c[p + 48] / c[p] - 1 - drift[coin]})
    d = pd.DataFrame(rows)
    d["side"] = np.where(d["past"] > 0, "rise", "fall")
    d["rev"] = -np.sign(d["past"]) * d["u48"]
    d["trend"] = np.where(d["tr30"] > 0, "up30", "down30")
    d["volratio"] = d["vol_wkend"] / d["vol_prior"]
    d["vq"] = pd.qcut(d["volratio"], 3, labels=["thin_quiet", "mid", "wkend_active"])
    def summ(g):
        x = g["rev"].dropna(); n = len(x)
        sl = stats.linregress(g["past_z"].abs(), g["rev"]) if n > 10 else None
        return pd.Series({"n": n, "mean_rev": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)),
                          "slope_abs": sl.slope if sl else np.nan,
                          "slope_t": sl.slope / sl.stderr if sl else np.nan})
    out = {}
    out["all_monday_u48"] = pd.Series({"n": len(d), "mean_u48": d.u48.mean(),
                                       "t": d.u48.mean() / (d.u48.std() / np.sqrt(len(d)))})
    out["by_trend_side"] = d.groupby(["trend", "side"]).apply(summ)
    out["by_volratio_side"] = d.groupby(["vq", "side"]).apply(summ)
    d["aq"] = d.groupby("side")["past_z"].transform(lambda s: pd.qcut(s.abs(), 3, labels=False))
    out["by_side_absTercile"] = d.groupby(["side", "aq"]).apply(lambda g: pd.Series({
        "n": len(g), "abs_z": g.past_z.abs().mean(), "mean_rev": g.rev.mean(),
        "t": g.rev.mean() / (g.rev.std() / np.sqrt(len(g)))}))
    out["fall_by_year"] = d[d.side == "fall"].groupby("year").apply(summ)
    out["fall_by_coin"] = d[d.side == "fall"].groupby("coin").apply(summ)
    return out
