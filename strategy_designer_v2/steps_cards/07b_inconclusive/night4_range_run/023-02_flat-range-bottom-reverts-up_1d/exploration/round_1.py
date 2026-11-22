def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in [1, 3, 5, 10, 20]:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            hi = df["high"].rolling(30).max(); lo = df["low"].rolling(30).min()
            mid = (hi + lo) / 2
            dist = (df["close"] - mid) / df["close"]
            net = (df["close"] - df["close"].shift(29)).abs()
            nmr = net / (hi - lo)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [1, 3, 5, 10, 20]:
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, yr=yr[i], fc=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i], dist=dist.iloc[i], nmr=nmr.iloc[i],
                        ret=c[i + h] / c[i] - 1 - drift[(coin, h)][0], sd=drift[(coin, h)][1]))
    R = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.ret.mean(), t=g.ret.mean() / (g.ret.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    act = R[R.fc > 0]
    out = {}
    out["by_horizon_active"] = act.groupby("h").apply(summ)
    a5 = act[act.h == 5].copy()
    out["h5_by_coin"] = a5.groupby("coin").apply(summ)
    out["h5_by_year"] = a5.groupby("yr").apply(summ)
    a5["q"] = pd.qcut(a5.fc.rank(method="first"), 4, labels=False)
    out["h5_by_fc_quartile"] = a5.groupby("q").apply(summ)
    # below-mid outside flat regime
    b = R[(R.dist < 0) & (R.fc <= 0) & R.nmr.notna()].copy()
    out["below_mid_nonflat_by_h"] = b.groupby("h").apply(summ)
    # above-mid flat
    ab = R[(R.dist > 0) & (R.nmr <= 0.3)]
    out["above_mid_flat_by_h"] = ab.groupby("h").apply(summ)
    # graded on dist in flat below
    fb = R[(R.dist < 0) & (R.nmr <= 0.3)].copy()
    out["flat_below_corr_dist_ret_by_h"] = fb.groupby("h").apply(lambda g: pd.Series(dict(n=len(g), spearman=stats.spearmanr(-g.dist, g.ret)[0])))
    fb5 = fb[fb.h == 5].copy()
    fb5["nq"] = pd.qcut(fb5.nmr, 3, labels=False)
    out["flat_below_h5_by_nmr_tercile"] = fb5.groupby("nq").apply(summ)
    out["regimes"] = R[R.h == 5].reg.value_counts()
    return out
