def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    # A. reversal after large 24h falls: by coin, by year, graded slope, other horizons
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"]).values
            for lb, h in [(24, 24), (24, 72), (72, 72), (168, 168)]:
                st = max(lb, 0)
                idx = np.arange(0, len(cl) - h, h)
                idx = idx[idx >= lb]
                if len(idx) == 0: continue
                rows.append(pd.DataFrame({"coin": c, "w": w, "lb": lb, "h": h,
                                          "yr": pd.DatetimeIndex(ts[idx]).year,
                                          "past": cl[idx] / cl[idx - lb] - 1,
                                          "fut": cl[idx + h] / cl[idx] - 1}))
    d = pd.concat(rows)
    d["ex"] = d["fut"] - d.groupby(["coin", "lb", "h"])["fut"].transform("mean")
    d["pz"] = d.groupby(["coin", "lb", "h"])["past"].transform(lambda x: (x - x.mean()) / x.std())
    res = []
    for (lb, h), s in d.groupby(["lb", "h"]):
        for nm, ss in [("all", s), ("pz<0", s[s["pz"] < 0]), ("pz>0", s[s["pz"] > 0])]:
            sl = stats.linregress(ss["pz"], ss["ex"])
            res.append({"lb": lb, "h": h, "set": nm, "n": len(ss), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["slope_ex_on_pastz"] = pd.DataFrame(res)
    s = d[(d.lb == 24) & (d.h == 24)].copy()
    s["q"] = s.groupby("coin")["pz"].transform(lambda x: pd.qcut(x, 5, labels=False))
    lo = s[s.q == 0]
    f = lambda x: pd.Series({"n": len(x), "mean_ex": x["ex"].mean(), "t": x["ex"].mean() / x["ex"].std() * np.sqrt(len(x))})
    out["bottomq24_by_coin"] = lo.groupby("coin").apply(f)
    out["bottomq24_by_year"] = lo.groupby("yr").apply(f)
    out["bottomq24_decile_by_strength"] = s[s.pz < 0].assign(b=lambda x: pd.qcut(x["pz"], 4, labels=False)).groupby("b").apply(f)
    # B. hours 21-22 UTC effect by coin and year, plus weekday
    hr = []
    for c in bars:
        for w, b in bars[c].items():
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            hr.append(pd.DataFrame({"coin": c, "h": ts.dt.hour.values, "wd": ts.dt.weekday.values, "yr": ts.dt.year.values, "r": r.values}))
    hr = pd.concat(hr).dropna()
    hr["ex"] = hr["r"] - hr.groupby("coin")["r"].transform("mean")
    g = lambda x: pd.Series({"n": len(x), "mean": x["ex"].mean(), "t": x["ex"].mean() / x["ex"].std() * np.sqrt(len(x))})
    e = hr[hr.h.isin([21, 22])]
    out["h2122_by_coin"] = e.groupby("coin").apply(g)
    out["h2122_by_year"] = e.groupby("yr").apply(g)
    out["h2122_by_weekday"] = e.groupby("wd").apply(g)
    out["weekday_all"] = hr.groupby("wd").apply(g)
    # is h21-22 move bigger after a down day? graded
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            pos = np.where(ts.dt.hour.values == 20)[0]
            pos = pos[(pos >= 21) & (pos + 2 < len(cl))]
            rows.append(pd.DataFrame({"coin": c, "past": cl[pos] / cl[pos - 20] - 1, "fut": cl[pos + 2] / cl[pos] - 1}))
    q = pd.concat(rows)
    q["pz"] = q.groupby("coin")["past"].transform(lambda x: (x - x.mean()) / x.std())
    sl = stats.linregress(q["pz"], q["fut"])
    out["h2122_on_past20h"] = pd.Series({"n": len(q), "slope": sl.slope, "t": sl.slope / sl.stderr, "mean": q["fut"].mean()})
    return out
