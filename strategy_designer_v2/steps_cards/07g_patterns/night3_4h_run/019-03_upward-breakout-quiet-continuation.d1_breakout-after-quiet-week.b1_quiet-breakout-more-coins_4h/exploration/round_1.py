import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    hrows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo) / c
            f = pd.DataFrame({
                "fwd": c.shift(-H) / c - 1,
                "r1d": c / c.shift(6) - 1,
                "r3d": c / c.shift(18) - 1,
                "r7d": c / c.shift(42) - 1,
                "r30d": c / c.shift(180) - 1,
                "volratio": rng.rolling(42).mean() / rng.rolling(180).mean(),
                "brk_up": c / hi.shift(1).rolling(12).max() - 1,
                "brk_dn": lo.shift(1).rolling(12).min() / c - 1,
                "near_hi": c / hi.rolling(180).max() - 1,
                "lastbar": c / c.shift(1) - 1,
                "fc": b["forecast"].astype(float),
            })
            g = f.iloc[::H].copy(); g["window"] = w
            recs.append(g)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.shift(-1) / c - 1
            hrows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r1": r1}))
        d = pd.concat(recs)
        d = d.dropna(subset=["fwd"])
        mu, sd = d["fwd"].mean(), d["fwd"].std()
        d["s"] = (d["fwd"] - mu) / sd
        d["coin"] = coin
        rows.append(d)
    D = pd.concat(rows)
    out = {}
    feats = ["r1d", "r3d", "r7d", "r30d", "volratio", "brk_up", "brk_dn", "near_hi", "lastbar", "fc"]
    summ = []
    for ft in feats:
        x = D.dropna(subset=[ft, "s"])
        rho, p = stats.spearmanr(x[ft], x["s"])
        x = x.copy()
        x["q"] = x.groupby("coin")[ft].rank(pct=True)
        qs = pd.cut(x["q"], [0, .2, .4, .6, .8, 1.0], labels=False, include_lowest=True)
        m = x.groupby(qs)["s"].agg(["mean", "count"])
        top = x.loc[qs == 4, "s"]; bot = x.loc[qs == 0, "s"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        summ.append({"feat": ft, "n": len(x), "spearman": rho, "p": p,
                     "q1": m["mean"].get(0), "q2": m["mean"].get(1), "q3": m["mean"].get(2),
                     "q4": m["mean"].get(3), "q5": m["mean"].get(4), "t_q5_q1": t})
    out["feature_vs_fwd3d_strength"] = pd.DataFrame(summ)
    # vol level interaction with past 7d return
    x = D.dropna(subset=["r7d", "volratio", "s"]).copy()
    x["vq"] = pd.qcut(x.groupby("coin")["volratio"].rank(pct=True), 3, labels=["quiet", "mid", "loud"])
    x["mq"] = pd.qcut(x.groupby("coin")["r7d"].rank(pct=True), 3, labels=["down", "mid", "up"])
    out["vol_x_mom7d_mean_strength"] = x.pivot_table(index="vq", columns="mq", values="s", aggfunc="mean")
    out["vol_x_mom7d_count"] = x.pivot_table(index="vq", columns="mq", values="s", aggfunc="count")
    # usual move per coin and raw fwd
    out["fwd_raw_by_coin"] = D.groupby("coin")["fwd"].agg(["mean", "std", "count"])
    Hh = pd.concat(hrows).dropna()
    Hh["z"] = Hh.groupby("coin")["r1"].transform(lambda v: (v - v.mean()) / v.std())
    gh = Hh.groupby("hour")["z"].agg(["mean", "count", "std"]); gh["t"] = gh["mean"] / (gh["std"] / np.sqrt(gh["count"]))
    gw = Hh.groupby("wd")["z"].agg(["mean", "count", "std"]); gw["t"] = gw["mean"] / (gw["std"] / np.sqrt(gw["count"]))
    out["next4h_by_hour"] = gh; out["next4h_by_weekday"] = gw
    # book by year
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            br.append(pd.DataFrame({"year": pd.to_datetime(dd["day"]).dt.year, "w": w, "b": dd["book_return"], "c": dd["coin_return"]}))
    B = pd.concat(br).dropna()
    gy = B.groupby("year")[["b", "c"]].agg(["mean", "std", "count"])
    out["book_coin_daily_by_year"] = gy
    return out
