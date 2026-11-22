import pandas as pd, numpy as np

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    stats_c = {}
    for c in bars:
        rr = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            hi = b["high"].rolling(30).max(); lo = b["low"].rolling(30).min()
            ratio = (b["close"] - b["close"].shift(29)).abs() / (hi - lo)
            mid = (b["close"] - (hi + lo) / 2) / b["close"] * 100
            r90 = b["close"] / b["close"].shift(89) - 1
            r30 = b["close"] / b["close"].shift(29) - 1
            vol = b["close"].pct_change().rolling(30).std()
            for i in range(0, n - H, H):
                r = cl[i + H] / cl[i] - 1; rr.append(r)
                rows.append(dict(coin=c, w=w, f=b["forecast"].iloc[i], r=r, ratio=ratio.iloc[i],
                                 mid=mid.iloc[i], r90=r90.iloc[i], r30=r30.iloc[i], vol=vol.iloc[i]))
        stats_c[c] = (np.mean(rr), np.std(rr))
    d = pd.DataFrame(rows)
    d["drift"] = d.coin.map(lambda c: stats_c[c][0]); d["sd"] = d.coin.map(lambda c: stats_c[c][1])
    d["ex"] = (d.r - d.drift) / d.sd
    d = d.dropna(subset=["ratio", "mid"])
    def agg(g):
        x = g.ex
        return pd.Series(dict(n=len(x), mean_ex=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              mean_r=g.r.mean()))
    d["flat"] = np.where(d.ratio <= 0.33, "flat", "trend")
    d["midq"] = d.groupby("flat").mid.transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["ex_by_regime_midq"] = d.groupby(["flat", "midq"]).apply(agg)
    out["mid_by_regime_midq"] = d.groupby(["flat", "midq"]).mid.mean()
    # trend: signed continuation, sign of r30
    t = d[d.flat == "trend"].copy()
    t["cont"] = np.sign(t.r30) * t.ex
    t["r30q"] = pd.qcut(t.r30.abs(), 4, labels=False)
    out["trend_continuation_by_absr30q"] = t.groupby("r30q").cont.agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["trend_cont_by_dir"] = t.groupby(np.sign(t.r30)).cont.agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # flat: reversion split by 90d trend sign
    f = d[d.flat == "flat"].dropna(subset=["r90"]).copy()
    f["rev"] = -np.sign(f.mid) * f.ex
    f["mside"] = np.where(f.mid > 0, "above", "below")
    f["t90"] = np.where(f.r90 > 0, "up90", "down90")
    out["flat_rev_by_t90_side"] = f.groupby(["t90", "mside"]).rev.agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    f["volq"] = pd.qcut(f.vol, 3, labels=False)
    out["flat_rev_by_volq"] = f.groupby("volq").rev.agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # book chain deepest fall
    bk = pd.concat([dd.assign(coin=c, w=w) for c in days for w, dd in days[c].items()])
    daily = bk.groupby(["w", "day"]).book_return.mean().dropna().reset_index()
    daily["wn"] = daily.w.str[1:].astype(int)
    daily = daily.sort_values(["wn", "day"])
    eq = (1 + daily.book_return).cumprod().values
    dd_ = eq / np.maximum.accumulate(eq) - 1
    yrs = len(eq) / 365
    out["book_chain"] = pd.Series(dict(yearly=eq[-1] ** (1 / yrs) - 1, maxdd=dd_.min(), days=len(eq)))
    daily["dd"] = dd_
    out["dd_by_window_min"] = daily.groupby("wn").dd.min()
    return out
