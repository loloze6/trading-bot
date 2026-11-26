import numpy as np, pandas as pd
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    out = {}
    dd = []
    for c, ws in data["days"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; t["win"] = w
            t["day"] = pd.to_datetime(t["day"])
            t["prev"] = t["coin_return"].shift(1)
            t["prev5"] = (1 + t["coin_return"]).rolling(5).apply(np.prod, raw=True).shift(1) - 1
            dd.append(t)
    dd = pd.concat(dd)
    dd["wd"] = dd["day"].dt.weekday
    sat = dd[dd.wd == 5].dropna(subset=["coin_return", "prev"]).copy()
    sat["q"] = pd.qcut(sat["prev"].rank(method="first"), 5, labels=False)
    g = sat.groupby("q")
    out["Saturday return by Friday return quintile"] = pd.DataFrame({
        "lo": g["prev"].min(), "hi": g["prev"].max(), "n": g.size(),
        "mean_sat": g["coin_return"].mean(),
        "t_day": g.apply(lambda x: tstat(x.groupby("day")["coin_return"].mean()))})
    sat2 = dd[dd.wd == 5].dropna(subset=["coin_return", "prev5"]).copy()
    sat2["q"] = pd.qcut(sat2["prev5"].rank(method="first"), 5, labels=False)
    g = sat2.groupby("q")
    out["Saturday return by prior 5d return quintile"] = pd.DataFrame({
        "n": g.size(), "mean_sat": g["coin_return"].mean(),
        "t_day": g.apply(lambda x: tstat(x.groupby("day")["coin_return"].mean()))})
    # Saturday excess vs coin's own all-window mean, by window halves
    dd["ex"] = dd["coin_return"] - dd.groupby("coin")["coin_return"].transform("mean")
    dd["wn"] = dd["win"].str[1:].astype(int)
    dd["half"] = np.where(dd["wn"] <= 12, "w1-w12", "w13-w24")
    s = dd[dd.wd == 5]
    out["Saturday excess by window half"] = s.groupby("half").apply(
        lambda x: pd.Series({"n_days": x["day"].nunique(), "mean_ex": x["ex"].mean(),
                             "t_day": tstat(x.groupby("day")["ex"].mean())}))
    # Saturday vs volatility: graded by prior 20d vol
    dd["vol20"] = dd.groupby(["coin", "win"])["coin_return"].transform(lambda x: x.rolling(20).std().shift(1))
    s = dd[(dd.wd == 5)].dropna(subset=["vol20", "ex"]).copy()
    s["q"] = pd.qcut(s["vol20"].rank(method="first"), 3, labels=["lowvol", "mid", "highvol"])
    out["Saturday excess by prior vol tercile"] = s.groupby("q").apply(
        lambda x: pd.Series({"n": len(x), "mean_ex": x["ex"].mean(),
                             "t_day": tstat(x.groupby("day")["ex"].mean())}))
    # book: what it earns on Saturday vs other days
    pdays = dd.groupby("day")[["book_return", "coin_return"]].mean().reset_index()
    pdays["wd"] = pdays["day"].dt.weekday
    out["book per-day by weekday"] = pdays.groupby("wd")["book_return"].agg(["count", "mean", tstat])
    return out
