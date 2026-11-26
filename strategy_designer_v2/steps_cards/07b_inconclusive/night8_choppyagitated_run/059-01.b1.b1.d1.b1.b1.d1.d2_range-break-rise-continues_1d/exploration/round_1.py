def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [7, 14, 28]
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            inprof = (df["regime"] == "unknown").values
            fc = df["forecast"].values
            # raw components recomputed
            r7 = pd.Series(c).pct_change(7)
            ma = r7.abs().rolling(30).mean()
            scaled = (r7 / ma).values
            hi30 = pd.Series(c).rolling(30).max()
            dist = ((hi30 - pd.Series(c)) / hi30 * 100).values
            for h in H:
                for i in range(0, n - h, h):
                    recs.append(dict(coin=coin, w=w, h=h, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                     ret=c[i + h] / c[i] - 1, prof=inprof[i], fc=fc[i],
                                     scaled=scaled[i], dist=dist[i]))
    R = pd.DataFrame(recs)
    # drift per coin per h over all grid
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]

    def tday(sub, col="ex"):
        if len(sub) < 3: return np.nan
        g = sub.groupby("day")[col].apply(lambda x: (x - sub[col].mean()).sum())
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(sub)
        return sub[col].mean() / se

    out = {}
    rows = []
    for h in H:
        s = R[R.h == h]
        for name, sub in [("all", s), ("prof", s[s.prof]), ("prof_fc>0", s[s.prof & (s.fc > 0)]),
                          ("prof_fc=0", s[s.prof & (s.fc <= 0)]), ("prof_scaled>0", s[s.prof & (s.scaled > 0)]),
                          ("prof_scaled<=0", s[s.prof & (s.scaled <= 0)])]:
            rows.append(dict(h=h, grp=name, n=len(sub), mean_ex=sub.ex.mean(), t=tday(sub), mean_ret=sub.ret.mean()))
    out["by_horizon_group"] = pd.DataFrame(rows)
    s = R[(R.h == 14) & R.prof & (R.fc > 0)].copy()
    out["fc_quartiles_h14"] = s.groupby(pd.qcut(s.fc, 4, duplicates="drop"))["ex"].agg(["count", "mean"])
    s["ywin"] = s.w
    out["by_window_h14"] = s.groupby("w")["ex"].agg(["count", "mean"])
    out["by_coin_h14"] = s.groupby("coin")["ex"].agg(["count", "mean"])
    p = R[(R.h == 14) & R.prof].copy()
    p = p.dropna(subset=["scaled", "dist"])
    p["sq"] = pd.qcut(p.scaled, 5, duplicates="drop")
    out["prof_h14_by_scaled_quintile"] = p.groupby("sq")["ex"].agg(["count", "mean"])
    p["dq"] = pd.qcut(p.dist, 4, duplicates="drop")
    out["prof_h14_by_dist_quartile"] = p.groupby("dq")["ex"].agg(["count", "mean"])
    p28 = R[(R.h == 28) & R.prof].dropna(subset=["scaled"]).copy()
    p28["sq"] = pd.qcut(p28.scaled, 5, duplicates="drop")
    out["prof_h28_by_scaled_quintile"] = p28.groupby("sq")["ex"].agg(["count", "mean"])
    p7 = R[(R.h == 7) & R.prof].dropna(subset=["scaled"]).copy()
    p7["sq"] = pd.qcut(p7.scaled, 5, duplicates="drop")
    out["prof_h7_by_scaled_quintile"] = p7.groupby("sq")["ex"].agg(["count", "mean"])
    return out
