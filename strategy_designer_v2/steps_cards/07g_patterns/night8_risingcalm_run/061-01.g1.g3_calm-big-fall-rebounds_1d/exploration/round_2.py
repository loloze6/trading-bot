import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r = c.pct_change()
            lr = np.log(c).diff()
            sd = r.rolling(30, min_periods=20).std()
            b["z"] = r / sd.shift(1)
            b["calm"] = (b["regime"] != "chop").astype(int)
            b["tr60"] = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday; b["yr"] = ts.dt.year; b["day"] = ts.dt.floor("D")
            for h in (1, 2, 3, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
                b[f"g{h}"] = (np.arange(len(b)) % h == 0)
            b["coin"] = coin; b["win"] = w
            rows.append(b[["coin","win","day","yr","wd","z","calm","tr60"] + [f"f{h}" for h in (1,2,3,5)] + [f"g{h}" for h in (1,2,3,5)]])
    d = pd.concat(rows, ignore_index=True)
    d["trb"] = pd.cut(d["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out = {}
    def slope(s, h, x="zp"):
        dd = s.groupby("day")[["ex", x]].sum()
        if len(dd) < 10: return [np.nan, np.nan, len(dd)]
        l = stats.linregress(dd[x], dd["ex"]); return [l.slope, l.slope / l.stderr, len(dd)]
    res = []; res2 = []; res3 = []
    for h in (1, 2, 3, 5):
        g = d[d[f"g{h}"]].dropna(subset=[f"f{h}", "z", "tr60"]).copy()
        g["ex"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
        g["zp"] = g["z"].clip(lower=0)   # up-day size
        g["zn"] = (-g["z"]).clip(lower=0) # down-day size
        for trb in ["fall", "chop", "rise", "notrise"]:
            s = g[g.trb != "rise"] if trb == "notrise" else g[g.trb == trb]
            su = s[s.z > 0]
            m = su["ex"]; dsum = su.groupby("day")["ex"].sum()
            res.append([h, trb] + slope(su, h, "zp") + [m.mean(), dsum.mean() / (dsum.std() / np.sqrt(len(dsum)))])
            sd_ = s[s.z < 0]
            res2.append([h, trb] + slope(sd_, h, "zn") + [sd_["ex"].mean()])
        # stability by year: non-rising, up-days
        if h == 3:
            s = g[(g.trb != "rise") & (g.z > 0)]
            for y, sy in s.groupby("yr"):
                res3.append([y] + slope(sy, h, "zp") + [sy["ex"].mean(), len(sy)])
            for cn, sy in s.groupby("coin"):
                res3.append([cn] + slope(sy, h, "zp") + [sy["ex"].mean(), len(sy)])
    out["up-day size -> excess (long ret), by trend"] = pd.DataFrame(res, columns=["h", "trend", "slope", "t", "days", "mean_ex", "t_mean"]).round(4)
    out["down-day size -> excess, by trend"] = pd.DataFrame(res2, columns=["h", "trend", "slope", "t", "days", "mean_ex"]).round(4)
    out["h3 notrise up-days by year/coin"] = pd.DataFrame(res3, columns=["grp", "slope", "t", "days", "mean_ex", "n"]).round(4)
    g = d[d["g1"]].dropna(subset=["f1"]).copy()
    g["ex"] = g["f1"] - g.groupby("coin")["f1"].transform("mean")
    gt = g[g.calm == 1]
    t = gt.groupby(["yr", "wd"])["ex"].mean().unstack().round(4)
    out["calm h1 excess yr x weekday"] = t
    return out
