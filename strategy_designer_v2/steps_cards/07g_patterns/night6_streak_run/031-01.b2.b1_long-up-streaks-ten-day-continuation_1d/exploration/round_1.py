import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sgn = np.sign(r1.fillna(0)).values
            streak = np.zeros(len(c))
            for i in range(1, len(c)):
                if sgn[i] == 0: streak[i] = 0
                elif sgn[i] == np.sign(streak[i-1]) : streak[i] = streak[i-1] + sgn[i]
                else: streak[i] = sgn[i]
            past10 = c / c.shift(10) - 1
            past30 = c / c.shift(30) - 1
            vol20 = r1.rolling(20).std()
            hi30 = c / c.rolling(30).max() - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(c)), "streak": streak,
                               "r1": r1, "past10": past10, "past30": past30, "vol20": vol20, "hi30": hi30,
                               "fwd": fwd, "fwd1": fwd1, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"], "ts": ts})
            daily.append(df)
    d = pd.concat(daily, ignore_index=True)
    g = d[(d.pos % H == 0) & d.fwd.notna()].copy()
    drift = g.groupby("coin").fwd.mean(); usual = g.groupby("coin").fwd.std()
    g["ex"] = (g.fwd - g.coin.map(drift)) / g.coin.map(usual)
    d["ex1"] = (d.fwd1 - d.groupby("coin").fwd1.transform("mean")) / d.groupby("coin").fwd1.transform("std")
    def summ(df, key, col="ex"):
        out = df.groupby(key)[col].agg(["mean", "std", "count"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.round(4)
    g["sbin"] = g.streak.clip(-4, 4)
    for col in ["past10", "past30", "vol20", "hi30", "r1"]:
        g[col + "_q"] = g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        d[col + "_q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    res = {}
    res["10d excess (usual-move units) by signed streak"] = summ(g, "sbin")
    res["10d excess by past10 quintile"] = summ(g, "past10_q")
    res["10d excess by past30 quintile"] = summ(g, "past30_q")
    res["10d excess by vol20 quintile"] = summ(g, "vol20_q")
    res["10d excess by dist from 30d high quintile"] = summ(g, "hi30_q")
    res["10d excess by 1d return quintile"] = summ(g, "r1_q")
    res["next-day excess by 1d return quintile (all bars)"] = summ(d.dropna(subset=["ex1"]), "r1_q", "ex1")
    res["next-day excess by weekday (all bars)"] = summ(d.dropna(subset=["ex1"]), "wd", "ex1")
    res["10d excess by year"] = summ(g, "year")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd, ignore_index=True)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    res["book vs hold daily mean,std"] = pd.DataFrame({"mean": bk.mean(), "std": bk.std()}).round(5)
    res["book beta to hold"] = float(np.polyfit(bk.coin_return, bk.book_return, 1)[0])
    a = d.dropna(subset=["alloc"]).copy()
    a["abin"] = pd.cut(a.alloc, [-0.01, 0.01, 0.5, 1, 1.5, 2.01])
    res["alloc distribution and next-day ret"] = a.groupby("abin").fwd1.agg(["mean", "count"]).round(5)
    res["share of bars with forecast>0"] = float((d.fc > 0).mean())
    return res
