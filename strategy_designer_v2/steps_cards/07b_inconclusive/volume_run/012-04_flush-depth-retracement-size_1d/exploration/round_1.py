def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    # coin mean h-return on non-overlapping grid pooled
    cm = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            cm[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; op = df["open"].values; lo = df["low"].values; hi = df["high"].values
            vol = df["volume"].values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(20).std()
            vsr = r1 / sd
            vr = pd.Series(vol) / pd.Series(vol).shift(1).rolling(20).mean()
            rng = hi - lo
            wick = (np.minimum(op, cl) - lo) / np.where(rng > 0, rng, np.nan)
            drop = (op - lo) / op
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            flush_rec = ((df["regime"] == "mean_reversion") & (df["forecast"] > 0)).values
            last = -99
            for t in range(len(df)):
                sharp = vsr.iloc[t] <= -2 if not np.isnan(vsr.iloc[t]) else False
                if not (flush_rec[t] or sharp):
                    continue
                d = dict(coin=c, w=w, yr=yr[t], flush=bool(flush_rec[t]), fc=df["forecast"].iloc[t],
                         drop=drop[t], dropz=drop[t] / sd.iloc[t] if sd.iloc[t] > 0 else np.nan,
                         wick=wick[t], vr=vr.iloc[t], r1d=r1.iloc[t], vsr=vsr.iloc[t])
                for h in H:
                    d[f"x{h}"] = cl[t + h] / cl[t] - 1 - cm[(c, h)] if t + h < len(cl) else np.nan
                rows.append(d)
    R = pd.DataFrame(rows)
    # declustering for flush
    F = R[R.flush].copy()
    out = {}
    def slope(df, x, y):
        d = df[[x, y]].dropna()
        if len(d) < 5: return (len(d), np.nan, np.nan)
        s = stats.linregress(d[x], d[y]); return (len(d), s.slope, s.slope / s.stderr)
    tab = []
    for h in H:
        n, b, t = slope(F, "fc", f"x{h}")
        n2, b2, t2 = slope(F, "dropz", f"x{h}")
        m = F[f"x{h}"].dropna()
        tab.append(dict(h=h, n=n, slope_fc=b, t_fc=t, t_dropz=t2, mean=m.mean(), t_mean=m.mean() / (m.std() / np.sqrt(len(m)))))
    out["flush_by_h"] = pd.DataFrame(tab)
    # sharp falls non-flush
    S = R[(~R.flush) & (R.vsr <= -2)]
    tab = []
    for h in H:
        m = S[f"x{h}"].dropna(); mf = F[f"x{h}"].dropna()
        tab.append(dict(h=h, n_other=len(m), mean_other=m.mean(), t_other=m.mean() / (m.std() / np.sqrt(len(m))),
                        welch_t_flush_minus_other=stats.ttest_ind(mf, m, equal_var=False).statistic))
    out["other_sharp_falls"] = pd.DataFrame(tab)
    g = F.groupby("coin").agg(n=("x3", "count"), mean3=("x3", "mean"), mean5=("x5", "mean"), mean10=("x10", "mean"))
    g["t_fc3"] = [slope(F[F.coin == c], "fc", "x3")[2] for c in g.index]
    out["by_coin"] = g
    g = F.groupby("yr").agg(n=("x3", "count"), mean3=("x3", "mean"), mean5=("x5", "mean"), mean10=("x10", "mean"))
    out["by_year"] = g
    F["q"] = pd.qcut(F["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_fc_tercile"] = F.groupby("q").agg(n=("x3", "count"), fc=("fc", "mean"), drop=("drop", "mean"), dropz=("dropz", "mean"),
                                             mean1=("x1", "mean"), mean3=("x3", "mean"), mean5=("x5", "mean"), mean10=("x10", "mean"))
    F["wq"] = pd.qcut(F["wick"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_wick_tercile"] = F.groupby("wq").agg(n=("x3", "count"), wick=("wick", "mean"), mean3=("x3", "mean"), mean5=("x5", "mean"), mean10=("x10", "mean"))
    F["vq"] = pd.qcut(F["vsr"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["by_ret_tercile"] = F.groupby("vq").agg(n=("x3", "count"), vsr=("vsr", "mean"), mean3=("x3", "mean"), mean5=("x5", "mean"), mean10=("x10", "mean"))
    out["corr_fc_drop_dropz_vsr"] = F[["fc", "drop", "dropz", "vsr", "wick", "vr"]].corr().round(2)
    return out
