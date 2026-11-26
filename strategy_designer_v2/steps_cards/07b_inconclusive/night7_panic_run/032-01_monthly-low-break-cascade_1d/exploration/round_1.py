def explore(data):
    import numpy as np, pandas as pd, json, ast
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [1, 2, 3, 5, 7, 10]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[h] = (np.mean(rs), np.std(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            trg = (df["regime"] == "trending").values
            prior_min = pd.Series(c).shift(1).rolling(30, min_periods=30).min().values
            depth = c / prior_min - 1
            last = -999
            for i in np.where(trg)[0]:
                gap = i - last
                last = i
                for h in H:
                    if i + h >= len(c):
                        continue
                    if i // h != (i - 1) // h and False:
                        pass
                    rows.append(dict(coin=coin, w=w, h=h, i=i, cell=i // h, day=ts[i].normalize(),
                                     year=ts[i].year, depth=depth[i], gap=gap,
                                     ret=c[i + h] / c[i] - 1, un=c[i + h] / c[i] - 1 - drift[h][0],
                                     sd=drift[h][1]))
    r = pd.DataFrame(rows)
    # first signal per grid cell
    r = r.sort_values("i").groupby(["coin", "w", "h", "cell"], as_index=False).first()

    def summ(g):
        d = g.groupby("day")["un"].sum()
        ndays = len(d)
        # day-pooled t: mean of cases via day sums
        m = g["un"].mean()
        se = np.sqrt(((d - d.index.map(g.groupby("day").size()) * m) ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=ndays, mean_un_long=m, t=m / se if se > 0 else np.nan,
                              strength=(g["un"] / g["sd"]).mean(), hit_up=(g["ret"] > 0).mean()))
    out["by_horizon"] = r.groupby("h").apply(summ)
    r3 = r[r.h == 3].copy()
    r5 = r[r.h == 5].copy()
    for name, rr in [("h3", r3), ("h5", r5)]:
        rr["dq"] = pd.qcut(rr["depth"], 3, labels=["deep", "mid", "shallow"])
        out[name + "_by_depth"] = rr.groupby("dq").apply(summ)
        out[name + "_by_coin"] = rr.groupby("coin").apply(summ)
        out[name + "_by_year"] = rr.groupby("year").apply(summ)
        rr["fresh"] = np.where(rr["gap"] > 5, "first_break", "repeat")
        out[name + "_fresh"] = rr.groupby("fresh").apply(summ)
        sl = stats.linregress(-rr["depth"].dropna(), rr.loc[rr["depth"].notna(), "un"])
        out[name + "_slope_un_on_depthbelow"] = f"slope {sl.slope:.3f} t {sl.slope/sl.stderr:.2f} n {rr['depth'].notna().sum()}"
    return out
