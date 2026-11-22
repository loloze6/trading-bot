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
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48.extend(list(c[idx + 48] / c[idx] - 1))
        g48 = np.array(g48)
        usual[coin] = (np.nanmean(g48), np.nanstd(g48, ddof=1))
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"]).values
            c = df["close"].values.astype(float)
            n = len(c)
            close_t = pd.to_datetime(ts) + pd.Timedelta(hours=1)
            dow = close_t.dayofweek.values
            hr = close_t.hour.values
            yr = close_t.year.values
            for i in np.where(hr == 0)[0]:
                if i - 48 < 0 or i + 48 >= n:
                    continue
                past = c[i] / c[i - 48] - 1
                rec = dict(coin=coin, win=w, year=yr[i], dow=dow[i], past=past)
                for h in (12, 24, 48, 72):
                    rec[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    d["mu"] = d["coin"].map(lambda k: usual[k][0])
    d["sd"] = d["coin"].map(lambda k: usual[k][1])
    d["z"] = d["past"] / d["sd"]
    d["dirn"] = -np.sign(d["past"])
    d["unus48"] = d["dirn"] * (d["f48"] - d["mu"])
    d["score"] = -d["z"] * (d["f48"] - d["mu"]) / d["sd"]
    for h in (12, 24, 72):
        d[f"unus{h}"] = d["dirn"] * (d[f"f{h}"] - d["mu"] * h / 48)

    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))})

    out = {}
    # by end weekday (all days, not only Mon/Wed/Fri)
    out["by_dow_unus48"] = d.groupby("dow")["unus48"].apply(tt).unstack()
    out["by_dow_score"] = d.groupby("dow")["score"].apply(tt).unstack()
    wk = d[d.dow == 0]
    out["mon_by_horizon"] = pd.DataFrame({h: tt(wk[f"unus{h}"]) for h in (12, 24, 48, 72)}).T
    out["mon_by_coin"] = wk.groupby("coin")["unus48"].apply(tt).unstack()
    out["mon_by_year"] = wk.groupby("year")["unus48"].apply(tt).unstack()
    wk = wk.copy()
    wk["side"] = np.where(wk["past"] > 0, "after_rise", "after_fall")
    out["mon_by_side"] = wk.groupby("side")["unus48"].apply(tt).unstack()
    wk["q"] = pd.qcut(wk["z"].abs(), 5, labels=False)
    out["mon_by_absz_quintile"] = wk.groupby("q")["unus48"].apply(tt).unstack()
    out["mon_by_side_q"] = wk.groupby(["side", "q"])["unus48"].apply(tt).unstack()
    # regression of next 48h on past 48h (z units), monday vs others
    def slope(x):
        x = x.dropna(subset=["z", "f48"])
        y = (x["f48"] - x["mu"]) / x["sd"]
        r = stats.linregress(x["z"], y)
        return pd.Series({"n": len(x), "slope": r.slope, "t": r.slope / r.stderr})
    out["slope_by_dow"] = d.groupby("dow").apply(slope)
    return out
