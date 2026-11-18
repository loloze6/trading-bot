def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5]
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
            flush_rec = ((df["regime"] == "mean_reversion") & (df["forecast"] > 0)).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            last = -99
            for t in range(len(df)):
                v = vsr.iloc[t]
                if np.isnan(v) or v > -2:
                    continue
                if t - last <= 3:
                    continue
                last = t
                d = dict(coin=c, w=w, yr=yr[t], flush=bool(flush_rec[t]), vsr=v, wick=wick[t], vr=vr.iloc[t],
                         drop=drop[t], dropz=drop[t] / sd.iloc[t], ret=r1.iloc[t], fc=df["forecast"].iloc[t])
                for h in H:
                    d[f"x{h}"] = cl[t + h] / cl[t] - 1 - cm[(c, h)] if t + h < len(cl) else np.nan
                rows.append(d)
    R = pd.DataFrame(rows)
    out = {}
    def sl(df, x, y):
        d = df[[x, y]].replace([np.inf, -np.inf], np.nan).dropna()
        if len(d) < 8: return (len(d), np.nan, np.nan)
        s = stats.linregress(d[x], d[y]); return (len(d), s.slope, s.slope / s.stderr)
    tab = []
    for grp, D in [("all_sharp", R), ("flush", R[R.flush]), ("nonflush", R[~R.flush])]:
        for x in ["drop", "dropz", "wick", "vr", "vsr"]:
            for h in H:
                n, b, t = sl(D, x, f"x{h}")
                tab.append(dict(grp=grp, x=x, h=h, n=n, slope=b, t=t))
    out["slopes"] = pd.DataFrame(tab)
    out["fc_share_capped"] = float((R[R.flush].fc >= 19.99).mean())
    R["hivol"] = R.vr >= 2
    R["hiwick"] = R.wick >= 0.3
    out["cells"] = R.groupby(["hivol", "hiwick"]).agg(n=("x1", "count"), m1=("x1", "mean"), m3=("x3", "mean"), m5=("x5", "mean"))
    A = R.copy(); A["vq"] = pd.qcut(A.vsr.rank(method="first"), 4, labels=["q1deep", "q2", "q3", "q4shallow"])
    out["all_by_vsr_q"] = A.groupby("vq").agg(n=("x1", "count"), vsr=("vsr", "mean"), m1=("x1", "mean"), m3=("x3", "mean"))
    A["wq"] = pd.qcut(A.wick.rank(method="first"), 4, labels=["w1lo", "w2", "w3", "w4hi"])
    out["all_by_wick_q"] = A.groupby("wq").agg(n=("x1", "count"), wick=("wick", "mean"), m1=("x1", "mean"), m3=("x3", "mean"))
    out["all_by_year_x1"] = R.groupby("yr").agg(n=("x1", "count"), m1=("x1", "mean"), m3=("x3", "mean"))
    return out
