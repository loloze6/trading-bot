import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30:
                continue
            rng = b["high"] - b["low"]
            ratio = rng / rng.rolling(20).mean()
            c = b["close"]
            r1 = c / c.shift(1) - 1
            r5 = c / c.shift(5) - 1
            fwd3 = c.shift(-3) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                               "pos": np.arange(len(b)), "ratio": ratio, "r1": r1, "r5": r5,
                               "fwd3": fwd3, "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 3 == 0].copy()
    drift = g.groupby("coin")["fwd3"].mean()
    usual = g.groupby("coin")["fwd3"].std()
    g["unus"] = g["fwd3"] - g["coin"].map(drift)
    g["str"] = g["unus"] / g["coin"].map(usual)
    g = g.dropna(subset=["unus", "ratio", "r1"])

    def summ(sub):
        s = sub.groupby(sub["ts"].dt.floor("D"))["unus"].sum()
        D = len(s); n = len(sub); m = sub["unus"].mean()
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / n if D > 2 else np.nan
        return pd.Series({"n": n, "days": D, "mean_unus%": m * 100,
                          "strength": sub["str"].mean(), "t_day": m / se})

    def slope(sub, x):
        sub = sub.dropna(subset=[x])
        r = stats.linregress(sub[x], sub["str"])
        return pd.Series({"n": len(sub), "slope": r.slope, "t": r.slope / r.stderr})

    out = {}
    # graded: day's range ratio on down days vs up days (signed move in strength units)
    g["dn"] = np.where(g["r1"] < 0, "down_day", "up_day")
    g["lr"] = np.log(g["ratio"])
    out["slope_str_on_logratio"] = g.groupby("dn").apply(lambda s: slope(s, "lr"))
    g["rb"] = pd.cut(g["ratio"], [0, 0.8, 1.2, 1.6, 2.2, 99])
    dd = g[g["dn"] == "down_day"]
    out["down_day_by_ratio"] = dd.groupby("rb").apply(summ)
    dw = dd[dd["ratio"] >= 1.6]
    out["down_wide_by_coin"] = dw.groupby("coin").apply(summ)
    out["down_wide_by_year"] = dw.groupby(dw["ts"].dt.year).apply(summ)
    # size of the down day itself, graded
    dw2 = dd[dd["ratio"] >= 1.3].copy()
    dw2["r1q"] = pd.qcut(dw2["r1"], 3, labels=["big_drop", "mid", "small_drop"])
    out["down_widish_by_drop_size"] = dw2.groupby("r1q").apply(summ)
    # all days: graded by ratio overall
    out["all_by_ratio"] = g.groupby("rb").apply(summ)
    # book: positions by weekday share and book daily returns by weekday
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin))
    bd = pd.concat(bd)
    bd["day"] = pd.to_datetime(bd["day"])
    book = bd.groupby("day")["book_return"].mean().dropna()
    out["book_by_weekday"] = book.groupby(book.index.dayofweek).agg(["count", "mean", "std"])
    return out
