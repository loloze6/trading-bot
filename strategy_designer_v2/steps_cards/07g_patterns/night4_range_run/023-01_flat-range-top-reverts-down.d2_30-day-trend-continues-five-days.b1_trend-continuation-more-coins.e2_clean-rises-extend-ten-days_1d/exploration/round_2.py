def explore(data):
    import numpy as np, pandas as pd
    H = 10
    out = {}
    # ---- daily panel with dates for day-level aggregation (dates never returned)
    drows = []
    grows = []
    for coin, wins in data["bars"].items():
        fw_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            fw_all += list(c[idx + H] / c[idx] - 1)
        drift = np.nanmean(fw_all)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change(); vol = r1.rolling(30).std()
            rhi = hi.rolling(31).max(); rlo = lo.rolling(31).min(); rng = rhi - rlo
            nmr = (c - c.shift(30)) / rng
            pos = (c - (rhi + rlo) / 2) / rng
            r5 = c / c.shift(5) - 1
            r30 = c / c.shift(30) - 1
            fwd = c.shift(-H) / c - 1
            for t in range(1, len(b)):
                drows.append((coin, ts[t].normalize(), ts[t].year, ts[t].weekday(), r1[t],
                              r1[t-1] / vol[t-1] if vol[t-1] and vol[t-1] > 0 else np.nan))
            for t in range(0, len(b) - H, H):
                grows.append(dict(coin=coin, yr=ts[t].year, nmr=nmr[t], pos=pos[t], r5=r5[t],
                                  r30=r30[t], vol=vol[t], ex=fwd[t] - drift))
    d = pd.DataFrame(drows, columns=["coin", "day", "yr", "wd", "r", "zprev"]).dropna(subset=["r"])
    def tt(s):
        s = s.dropna(); return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s)))))
    # weekday, cross-coin mean per day, then t across days
    dm = d.groupby(["day"]).agg(r=("r", "mean"), yr=("yr", "first"), wd=("wd", "first"))
    out["weekday: day-level cross-coin mean return"] = dm.groupby("wd")["r"].apply(tt).unstack().round(5)
    out["Wed minus Thu, day-level, by year"] = dm.groupby("yr").apply(
        lambda x: x[x.wd == 2].r.mean() - x[x.wd == 3].r.mean()).round(5)
    out["Saturday day-level mean by year"] = dm[dm.wd == 5].groupby("yr")["r"].apply(tt).unstack().round(5)
    # weekday per coin: share of coins with Sat > mean
    pc = d.groupby(["coin", "wd"])["r"].mean().unstack()
    out["per coin: share with weekday mean > 0"] = (pc > 0).mean().round(3)
    # after big drops: next-day return per coin, by year
    d["zq"] = d.groupby("coin")["zprev"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    big = d[d.zq == 0]
    out["day after bottom-decile vol-scaled drop, by year"] = big.groupby("yr")["r"].apply(tt).unstack().round(5)
    bd = big.groupby("day")["r"].mean()
    out["day after bottom-decile drop, day-level"] = tt(bd).round(5)
    # flat range position (momentum inside flat ranges) by year
    g = pd.DataFrame(grows).dropna(subset=["nmr", "ex", "pos"])
    flat = g[g.nmr.abs() < 0.5].copy()
    flat["hi"] = flat.pos > flat.pos.median()
    out["flat: upper-half minus lower-half 10d excess, by year"] = flat.groupby("yr").apply(
        lambda x: pd.Series(dict(n=len(x), diff=x[x.hi].ex.mean() - x[~x.hi].ex.mean()))).round(4)
    # graded: correlation pos vs ex in flat
    out["flat: rank corr pos vs 10d excess"] = round(flat[["pos", "ex"]].corr("spearman").iloc[0, 1], 4)
    out["all bars: rank corr nmr vs 10d excess"] = round(g[["nmr", "ex"]].corr("spearman").iloc[0, 1], 4)
    # clean up with strong 5d: by year and per coin
    up = g[g.nmr >= 0.5].copy()
    up["r5t"] = pd.qcut(up.r5, 3, labels=False)
    out["clean up, top 5d tercile, by year"] = up[up.r5t == 2].groupby("yr")["ex"].apply(tt).unstack().round(4)
    out["clean up: rank corr r5 vs excess"] = round(up[["r5", "ex"]].corr("spearman").iloc[0, 1], 4)
    out["clean up top r5 tercile: share of coins mean>0"] = round(
        (up[up.r5t == 2].groupby("coin").ex.mean() > 0).mean(), 3)
    # all bars: 5d return grading
    g["r5q"] = pd.qcut(g.r5, 5, labels=False)
    out["all: 10d excess by 5d return quintile"] = g.groupby("r5q")["ex"].apply(tt).unstack().round(4)
    return out
