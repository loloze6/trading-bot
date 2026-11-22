import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        # drift over 48h on grid
        g48 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48.extend(list(c[idx + 48] / c[idx] - 1))
        drift = np.nanmean(g48); sd = np.nanstd(g48)
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"]) + pd.Timedelta(hours=1)
            s = pd.Series(b["close"].values, index=ts)
            s = s[~s.index.duplicated()]
            # hourly returns (bar's own)
            r1 = s.pct_change()
            hourly.append(pd.DataFrame({"coin": coin, "wd": (s.index - pd.Timedelta(hours=1)).weekday,
                                        "hr": (s.index - pd.Timedelta(hours=1)).hour, "r": r1.values}))
            mids = s.index[(s.index.hour == 0)]
            for t in mids:
                tp = t - pd.Timedelta(hours=48); tf = t + pd.Timedelta(hours=48)
                tp24 = t - pd.Timedelta(hours=24)
                if tp in s.index and tf in s.index and tp24 in s.index:
                    past = s[t] / s[tp] - 1
                    fut = s[tf] / s[t] - 1
                    rows.append((coin, w, t.weekday(), past, s[t]/s[tp24]-1, fut, (fut - drift) / sd, fut - drift))
    df = pd.DataFrame(rows, columns=["coin", "w", "dow", "past", "past24", "fut", "z", "unus"])
    res = []
    for d, g in df.groupby("dow"):
        sl = stats.linregress(g["past"], g["unus"])
        neg = g[g.past < 0]; pos = g[g.past > 0]
        res.append({"dow_at_0h": d, "n": len(g), "corr": g[["past","unus"]].corr().iloc[0,1],
                    "slope": sl.slope, "t_slope": sl.slope / sl.stderr,
                    "unus_after_fall": neg.unus.mean(), "t_fall": stats.ttest_1samp(neg.unus, 0).statistic,
                    "unus_after_rise": pos.unus.mean(), "t_rise": stats.ttest_1samp(pos.unus, 0).statistic})
    out["48h past vs next 48h unusual, by day (Mon=0)"] = pd.DataFrame(res)
    mon = df[df.dow == 0].copy()
    mon["q"] = pd.qcut(mon["past"], 5, labels=False)
    out["Monday: weekend return quintile"] = mon.groupby("q").agg(n=("unus","size"), past=("past","mean"),
        unus=("unus","mean"), z=("z","mean"), tstat=("unus", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["Monday by coin"] = mon.groupby("coin").apply(lambda g: pd.Series({
        "n": len(g), "slope": stats.linregress(g.past, g.unus).slope,
        "t": (lambda l: l.slope/l.stderr)(stats.linregress(g.past, g.unus)),
        "mean_unus": g.unus.mean()}))
    # all days pooled: weekdays-only vs weekend
    h = pd.concat(hourly).dropna()
    hw = h.groupby("wd")["r"].agg(["mean", "std", "count"])
    hw["t"] = hw["mean"] / (hw["std"] / np.sqrt(hw["count"]))
    out["hourly return by weekday"] = hw
    hh = h.groupby("hr")["r"].agg(["mean", "std", "count"])
    hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["hourly return by hour"] = hh
    # Sunday 24h vs Monday next
    return out
