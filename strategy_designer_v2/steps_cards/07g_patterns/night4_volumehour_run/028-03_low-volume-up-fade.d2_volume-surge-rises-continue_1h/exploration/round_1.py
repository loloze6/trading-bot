import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def _summ(df, by, col):
    g = df.groupby(by, observed=True)[col]
    out = pd.DataFrame({"n": g.size(), "mean_bp": g.mean() * 1e4, "t": g.apply(_t)})
    return out

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = v / v.rolling(720, min_periods=240).mean()
            r24 = c / c.shift(24) - 1
            vol24 = r1.rolling(24).std() / sd
            ts = pd.to_datetime(b["timestamp"])
            for h in (6, 24):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({
                    "coin": coin, "w": w, "h": h,
                    "z": (r1 / sd).values[idx], "vr": vr.values[idx],
                    "r24z": (r24 / (sd * np.sqrt(24))).values[idx],
                    "vol24": vol24.values[idx],
                    "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx],
                    "year": ts.dt.year.values[idx],
                    "fwd": fwd.values[idx],
                    "pos": b["postRebalance_current_allocation"].values[idx],
                })
                rows.append(d)
    D = pd.concat(rows).dropna(subset=["fwd"])
    D["drift"] = D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["ex"] = D["fwd"] - D["drift"]
    D6 = D[D.h == 6].dropna(subset=["z", "vr"]).copy()
    D24 = D[D.h == 24].dropna(subset=["r24z", "vol24"]).copy()
    D6["zbin"] = pd.cut(D6["z"], [-np.inf, -3, -1.5, 1.5, 3, np.inf])
    D6["vrbin"] = pd.cut(D6["vr"], [0, 1, 2, 3, np.inf])
    res = {}
    res["6h_ex_by_z_and_volratio"] = _summ(D6, ["zbin", "vrbin"], "ex")
    res["6h_ex_by_z"] = _summ(D6, ["zbin"], "ex")
    D24["mom"] = pd.qcut(D24["r24z"], 5)
    res["24h_ex_by_past24h_z_quintile"] = _summ(D24, ["mom"], "ex")
    D24["vq"] = pd.qcut(D24["vol24"], 4)
    D24["sgn"] = np.sign(D24["r24z"])
    res["24h_ex_by_volregime_and_past24sign"] = _summ(D24, ["vq", "sgn"], "ex")
    res["6h_ex_by_hour"] = _summ(D6, ["hour"], "ex")
    res["24h_ex_by_weekday"] = _summ(D24, ["wd"], "ex")
    res["6h_ex_by_coin_year_bigup_hivol"] = _summ(D6[(D6.z > 3) & (D6.vr > 2)], ["coin", "year"], "ex")
    # book: daily returns, largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    DD = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    DD["wd"] = pd.to_datetime(DD["day"]).dt.weekday
    res["book_daily_by_weekday"] = _summ(DD, ["wd"], "book_return")
    DD["cq"] = pd.qcut(DD["coin_return"], 5)
    res["book_daily_by_coin_day_quintile"] = _summ(DD, ["cq"], "book_return")
    return res
