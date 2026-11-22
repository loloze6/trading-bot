import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    hourly = []
    rows = []
    for coin, wins in data["bars"].items():
        g48 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48.extend(list(c[idx + 48] / c[idx] - 1))
        drift = np.nanmean(g48); sd = np.nanstd(g48)
        for w, b in wins.items():
            st = pd.to_datetime(b["timestamp"])
            ts = st + pd.Timedelta(hours=1)
            s = pd.Series(b["close"].values, index=ts)
            s = s[~s.index.duplicated()]
            r1 = s.pct_change()
            r24 = s / s.shift(24) - 1
            vol24 = r1.rolling(24).std()
            vol720 = r1.rolling(720, min_periods=200).std()
            hb = s.index - pd.Timedelta(hours=1)
            hourly.append(pd.DataFrame({"coin": coin, "yr": hb.year, "wd": hb.weekday, "hr": hb.hour,
                "r": r1.values, "prev24": r24.shift(1).values, "vr": (vol24 / vol720).shift(1).values}))
            for t in s.index[(s.index.hour == 0) & (s.index.weekday == 4)]:
                tp = t - pd.Timedelta(hours=48); tf = t + pd.Timedelta(hours=48)
                if tp in s.index and tf in s.index:
                    past = s[t] / s[tp] - 1; fut = s[tf] / s[t] - 1
                    rows.append((coin, w, t.year, past, fut - drift, (fut - drift) / sd))
    h = pd.concat(hourly).dropna(subset=["r"])
    h["late"] = h.hr.isin([21, 22])
    def tt(x): return x.mean() / (x.std() / np.sqrt(len(x)))
    lt = h[h.late]
    out["hours 21-22: by year"] = lt.groupby("yr")["r"].agg(["mean", "count", tt])
    out["hours 21-22: by coin"] = lt.groupby("coin")["r"].agg(["mean", "count", tt])
    out["hours 21-22: by weekday"] = lt.groupby("wd")["r"].agg(["mean", "count", tt])
    l2 = lt.dropna(subset=["prev24"]).copy()
    l2["q"] = pd.qcut(l2.prev24, 5, labels=False)
    out["hours 21-22: by prior 24h return quintile"] = l2.groupby("q").agg(prev=("prev24", "mean"), r=("r", "mean"), n=("r", "size"), t=("r", tt))
    l3 = lt.dropna(subset=["vr"]).copy()
    l3["q"] = pd.qcut(l3.vr, 5, labels=False)
    out["hours 21-22: by vol ratio quintile"] = l3.groupby("q").agg(vr=("vr", "mean"), r=("r", "mean"), n=("r", "size"), t=("r", tt))
    out["other hours by year"] = h[~h.late].groupby("yr")["r"].agg(["mean", "count", tt])
    out["Saturday hourly by year"] = h[h.wd == 5].groupby("yr")["r"].agg(["mean", "count", tt])
    f = pd.DataFrame(rows, columns=["coin", "w", "yr", "past", "unus", "z"])
    def sl(g):
        l = stats.linregress(g.past, g.unus)
        return pd.Series({"n": len(g), "slope": l.slope, "t": l.slope / l.stderr})
    out["Fri 0h: Wed-Thu return -> Fri-Sat unusual, by coin"] = f.groupby("coin").apply(sl)
    out["Fri 0h: by year"] = f.groupby("yr").apply(sl)
    f["q"] = pd.qcut(f.past, 5, labels=False)
    out["Fri 0h: quintiles"] = f.groupby("q").agg(past=("past", "mean"), unus=("unus", "mean"), z=("z", "mean"), n=("unus", "size"), t=("unus", tt))
    # other days momentum test for comparison: same 48h->48h at 0h any day pooled, weekdays non-Fri
    return out
