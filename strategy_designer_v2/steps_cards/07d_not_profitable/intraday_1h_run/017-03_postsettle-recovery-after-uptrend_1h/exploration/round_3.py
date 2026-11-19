def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["hour"] = b["ts"].dt.hour
            b["coin"] = c; b["w"] = w
            b["r72"] = b["close"] / b["close"].shift(72) - 1
            for h in [2, 8, 16, 24]:
                b[f"f{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["pos_idx"] = np.arange(len(b))
            rows.append(b[["coin","w","hour","r72","pos_idx","f2","f8","f16","f24"]])
    B = pd.concat(rows, ignore_index=True)
    means = {h: B[B["pos_idx"] % h == 0].groupby("coin")[f"f{h}"].mean() for h in [2, 8, 16, 24]}
    def tt(s):
        s = s.dropna(); return pd.Series({"bp": s.mean()*1e4, "n": len(s), "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    res = {}
    for hr in [7, 15, 23]:
        E = B[(B["hour"] == hr) & (B["r72"] > 0)].copy()
        for h in [2, 8, 16, 24]:
            x = E[f"f{h}"] - E["coin"].map(means[h])
            res[(hr, h)] = tt(x)
    out["excess_by_entryhour_horizon_up"] = pd.DataFrame(res).T
    # graded: 15:00 entries, x8 and x24 by r72 quintile (all signs of r72)
    E = B[B["hour"] == 15].dropna(subset=["r72"]).copy()
    E["q"] = E.groupby("coin")["r72"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    for h in [8, 24]:
        E[f"x{h}"] = E[f"f{h}"] - E["coin"].map(means[h])
    out["h15_x8_by_q"] = E.groupby("q")["x8"].apply(tt).unstack()
    out["h15_x24_by_q"] = E.groupby("q")["x24"].apply(tt).unstack()
    # slope t of x8 on r72 for up entries at 15
    U = E[E["r72"] > 0].dropna(subset=["x8"])
    from scipy import stats
    r = stats.linregress(U["r72"], U["x8"])
    out["h15_up_x8_slope_t"] = r.slope / r.stderr
    # placebo: non-settlement hour 11 entries
    P = B[(B["hour"] == 11) & (B["r72"] > 0)]
    out["h11_up_x8"] = tt(P["f8"] - P["coin"].map(means[8]))
    return out
