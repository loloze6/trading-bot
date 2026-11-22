import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    usual = {}
    for coin, wins in bars.items():
        g48 = []
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            idx = np.arange(0, len(c) - 48, 48)
            g48.extend(list(c[idx + 48] / c[idx] - 1))
        g48 = np.array(g48)
        usual[coin] = (np.nanmean(g48), np.nanstd(g48, ddof=1))
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values.astype(float)
            n = len(c)
            close_t = ts + pd.Timedelta(hours=1)
            dow = close_t.dt.dayofweek.values
            hr = close_t.dt.hour.values
            yr = close_t.dt.year.values
            for i in np.where(hr == 0)[0]:
                if i - 48 < 0 or i + 48 >= n:
                    continue
                rows.append(dict(coin=coin, win=w, year=yr[i], dow=dow[i],
                                 past=c[i] / c[i - 48] - 1, f48=c[i + 48] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["mu"] = d["coin"].map(lambda k: usual[k][0])
    d["sd"] = d["coin"].map(lambda k: usual[k][1])
    d["ex"] = d["f48"] - d["mu"]
    d["exz"] = d["ex"] / d["sd"]
    d["z"] = d["past"] / d["sd"]

    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))})

    out = {}
    # raw excess next-48h return by end weekday (no direction)
    out["excess_next48_by_dow"] = d.groupby("dow")["ex"].apply(tt).unstack()
    mon = d[d.dow == 0].copy()
    out["mon_excess_by_year"] = mon.groupby("year")["ex"].apply(tt).unstack()
    out["mon_excess_by_coin"] = mon.groupby("coin")["ex"].apply(tt).unstack()
    # after-fall continuation net of the Monday mean
    mon_mean = mon["ex"].mean()
    mon["side"] = np.where(mon["past"] > 0, "rise", "fall")
    mon["ex_net"] = mon["ex"] - mon_mean
    out["mon_excess_by_side"] = mon.groupby("side")["ex"].apply(tt).unstack()
    out["mon_netofmonday_by_side"] = mon.groupby("side")["ex_net"].apply(tt).unstack()
    # graded: slope of next on past by side (Monday)
    def slope(x):
        r = stats.linregress(x["z"], x["exz"])
        return pd.Series({"n": len(x), "slope": r.slope, "t": r.slope / r.stderr, "intercept": r.intercept})
    out["mon_slope_by_side"] = mon.groupby("side").apply(slope)
    # Friday-ending (Wed-Thu move) continuation, by year and coin
    fri = d[d.dow == 4]
    out["fri_slope_by_year"] = fri.groupby("year").apply(slope)
    out["fri_slope_by_coin"] = fri.groupby("coin").apply(slope)
    # weekend-minus-weekday welch, all weekdays 1..4 as comparison
    wkd = d[d.dow.isin([1, 2, 3, 4])]
    mon["score"] = -mon["z"] * mon["exz"]
    wkd = wkd.assign(score=-wkd["z"] * wkd["exz"])
    t, p = stats.ttest_ind(mon["score"], wkd["score"], equal_var=False)
    out["mon_vs_tue_fri_score"] = pd.Series({"diff": mon["score"].mean() - wkd["score"].mean(), "welch_t": t})
    return out
