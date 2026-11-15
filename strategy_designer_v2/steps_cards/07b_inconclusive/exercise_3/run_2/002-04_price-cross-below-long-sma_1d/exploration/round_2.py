def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    cmean = {}
    for c in bars:
        cmean[c] = pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            al = df["postRebalance_current_allocation"].values
            dist = df["debug_info.components.below_ma.last_history_value"].values if "debug_info.components.below_ma.last_history_value" in df else np.full(len(df), np.nan)
            sma = cl / (1 + dist)
            below = (dist < 0).astype(float)
            run = np.zeros(len(df))
            for i in range(len(df)):
                run[i] = run[i-1] + 1 if (below[i] and i > 0) else (1 if below[i] else 0)
            n = len(df); h = 10
            for i in range(0, n - h, h):
                r = cl[i + h] / cl[i] - 1
                sl = sma[i] / sma[i-20] - 1 if i >= 20 else np.nan
                ddist = dist[i] - dist[i-10] if i >= 10 else np.nan
                rows.append(dict(coin=c, w=w, alloc=al[i], dist=dist[i], ex=r - h*cmean[c], r=r,
                                 slope=sl, ddist=ddist, run=run[i]))
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    a = d[d.alloc < 0].copy()
    a["slope_sign"] = np.where(a.slope < 0, "sma_falling", np.where(a.slope >= 0, "sma_rising", np.nan))
    out["slope_negex"] = a.groupby("slope_sign").apply(lambda g: tt(-g.ex))
    a2 = a.dropna(subset=["slope"]).copy()
    a2["sq"] = pd.qcut(a2.slope.rank(method="first"), 3, labels=["steep_fall", "mid", "rising"])
    out["slope_tercile_negex"] = a2.groupby("sq").apply(lambda g: tt(-g.ex))
    a3 = a.dropna(subset=["ddist"]).copy()
    a3["dq"] = pd.qcut(a3.ddist.rank(method="first"), 3, labels=["deepening", "mid", "recovering"])
    out["ddist_negex"] = a3.groupby("dq").apply(lambda g: tt(-g.ex))
    a["rq"] = pd.cut(a.run, [0, 10, 30, 80, 10000], labels=["fresh<=10", "11-30", "31-80", ">80"])
    out["run_negex"] = a.groupby("rq").apply(lambda g: tt(-g.ex))
    # all bars with dist known: below vs above, raw excess
    k = d.dropna(subset=["dist"])
    out["below_vs_above_ex"] = k.groupby(k.dist < 0).apply(lambda g: tt(g.ex))
    # book decomposition
    rows2 = []
    for c in bars:
        for w, df in bars[c].items():
            b = df.copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dy = days[c][w].copy(); dy["day"] = pd.to_datetime(dy["day"]).dt.floor("D")
            dy = dy.set_index("day")
            dy["pos"] = pos.reindex(dy.index).values
            dy["coin"] = c; dy["w"] = w
            rows2.append(dy)
    dd = pd.concat(rows2)
    dd["mkt"] = dd.pos * dd.coin.map(cmean)
    bk = dd.groupby(["w", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean")).dropna()
    out["book_mean"] = bk.book.mean(); out["market_part"] = bk.mkt.mean(); out["timing_part"] = bk.book.mean() - bk.mkt.mean()
    return out
