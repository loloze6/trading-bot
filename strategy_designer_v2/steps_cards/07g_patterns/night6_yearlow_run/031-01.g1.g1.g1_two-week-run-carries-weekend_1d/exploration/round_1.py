import pandas as pd, numpy as np
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            ret14 = c / c.shift(14) - 1
            z14 = ret14 / (sd20 * np.sqrt(14))
            z1 = r1 / sd20
            lo = c.rolling(60, min_periods=40).min()
            hi = c.rolling(60, min_periods=40).max()
            dlow = np.log(c / lo) / (sd20 * np.sqrt(60))
            pos = (c - lo) / (hi - lo)
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            f3 = c.shift(-3) / c - 1
            f5 = c.shift(-5) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "wd": ts.dt.weekday, "year": ts.dt.year, "z14": z14, "z1": z1, "sd20": sd20,
                               "dlow": dlow, "pos": pos, "f1": f1, "f2": f2, "f3": f3, "f5": f5,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # coin drifts on grids
    for h in [1, 2, 3, 5]:
        g = d[d["i"] % h == 0]
        d["m%d" % h] = d["coin"].map(g.groupby("coin")["f%d" % h].mean())
        d["u%d" % h] = d["f%d" % h] - d["m%d" % h]
    out = {}
    # 1. next-day unusual return by weekday of signal bar
    wd = d.groupby("wd")["u1"].agg(["mean", "count"])
    wd["t_dayclust"] = [ _t(d[d.wd == k].groupby("day")["u1"].sum()) for k in wd.index]
    out["next-day unusual return by weekday of bar"] = wd
    # 2. momentum z14 (clipped) x unusual 2-day move, by weekday
    res = []
    for k in range(7):
        s = d[d.wd == k].dropna(subset=["z14", "u2"])
        prod = s["z14"].clip(-3, 3) * s["u2"]
        res.append({"wd": k, "mean_zxu2": prod.mean(), "t_day": _t(prod.groupby(s["day"]).sum()),
                    "corr": s["z14"].corr(s["u2"]), "n": len(s)})
    out["z14 x unusual 2-day move by weekday"] = pd.DataFrame(res).set_index("wd")
    # 3. z14 graded quintiles on Friday, f2 unusual
    fr = d[d.wd == 4].dropna(subset=["z14", "u2"]).copy()
    fr["q"] = pd.qcut(fr["z14"], 5, labels=False)
    out["friday z14 quintile -> unusual weekend move"] = fr.groupby("q").agg(z=("z14", "mean"), u2=("u2", "mean"), n=("u2", "size"))
    # 4. after large one-day moves (all days, grid h=1): z1 quintile -> next day
    s = d.dropna(subset=["z1", "u1"]).copy()
    s["q"] = pd.qcut(s["z1"], 5, labels=False)
    out["z1 quintile -> next-day unusual"] = s.groupby("q").agg(z=("z1", "mean"), u1=("u1", "mean"), n=("u1", "size"))
    # 5. distance from 60-day low (grid h=5) -> 5-day unusual
    s = d[(d.i % 5 == 0)].dropna(subset=["pos", "u5"]).copy()
    s["q"] = pd.qcut(s["pos"], 5, labels=False, duplicates="drop")
    g = s.groupby("q").agg(pos=("pos", "mean"), u5=("u5", "mean"), n=("u5", "size"))
    g["t"] = [_t(s[s.q == k].groupby("day")["u5"].sum()) for k in g.index]
    out["position in 60-day range quintile -> 5-day unusual"] = g
    # 6. volatility tercile x Friday momentum
    fr["vq"] = fr.groupby("coin")["sd20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    fr["prod"] = np.sign(fr["z14"]) * fr["u2"]
    out["friday signed weekend move by vol tercile"] = fr.groupby("vq")["prod"].agg(["mean", "count"])
    # 7. by year
    out["friday signed weekend move by year"] = fr.groupby("year")["prod"].agg(["mean", "count"])
    # 8. book daily returns by weekday, largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd, ignore_index=True)
    dd["wd"] = pd.to_datetime(dd["day"], utc=True).dt.weekday
    book = dd.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), wd=("wd", "first")).dropna()
    out["book mean daily return by weekday"] = book.groupby("wd")["br"].agg(["mean", "std", "count"])
    top = book.nlargest(30, "br"); bot = book.nsmallest(30, "br")
    out["weekday of 30 best / worst book days"] = pd.DataFrame({"best": top["wd"].value_counts(), "worst": bot["wd"].value_counts()}).fillna(0)
    out["book by window: mean, min"] = book.groupby("w")["br"].agg(["mean", "min", "sum"])
    return out
