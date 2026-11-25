def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [3, 5, 7, 10]
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
            r1 = pd.Series(c).pct_change().values
            for i in np.where(trg)[0]:
                for h in H:
                    if i + h >= len(c):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, i=i, cell=i // h, day=ts[i].normalize(),
                                     year=ts[i].year, depth=depth[i], r1=r1[i],
                                     ret=c[i + h] / c[i] - 1, un=c[i + h] / c[i] - 1 - drift[h][0],
                                     sd=drift[h][1], drift=drift[h][0]))
    r = pd.DataFrame(rows)
    r = r.sort_values("i").groupby(["coin", "w", "h", "cell"], as_index=False).first()

    def summ(g):
        d = g.groupby("day")["un"].sum()
        m = g["un"].mean()
        cnt = g.groupby("day").size()
        se = np.sqrt(((d - cnt * m) ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=len(d), mean_un_long=m, t=m / se if se > 0 else np.nan,
                              mean_total=g["ret"].mean(), drift=g["drift"].mean(), usual=g["sd"].mean()))
    res = []
    for h in H:
        g = r[(r.h == h) & r.depth.notna()]
        sl = stats.linregress(-g["depth"], g["un"])
        sl2 = stats.linregress(-g["r1"].fillna(0), g["un"])
        res.append(dict(h=h, n=len(g), slope_depth=sl.slope, t_depth=sl.slope / sl.stderr,
                        slope_r1=sl2.slope, t_r1=sl2.slope / sl2.stderr,
                        rho_depth=stats.spearmanr(-g["depth"], g["un"]).correlation))
    out["grading"] = pd.DataFrame(res).set_index("h")
    for h in [7, 10]:
        rr = r[r.h == h].copy()
        out[f"h{h}_by_year"] = rr.groupby("year").apply(summ)
        out[f"h{h}_by_coin"] = rr.groupby("coin").apply(summ)
        rr["dq"] = pd.qcut(rr["depth"], 3, labels=["deep", "mid", "shallow"])
        out[f"h{h}_by_depth"] = rr.groupby("dq").apply(summ)
    out["h3_overall"] = summ(r[r.h == 3])
    out["h10_overall"] = summ(r[r.h == 10])
    return out
