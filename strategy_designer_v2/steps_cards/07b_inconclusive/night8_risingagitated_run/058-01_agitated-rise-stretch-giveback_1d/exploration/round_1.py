def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    hs = [1, 2, 3, 5, 10, 20]
    out = {}
    # drift per coin per h
    drift = {}
    for c in bars:
        for h in hs:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            sma = cl.rolling(20).mean()
            dist = cl / sma - 1
            ret60 = cl / cl.shift(60) - 1
            inprof = (df["regime"] == "unknown").values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in hs:
                for i in range(0, len(cl) - h, h):
                    if np.isnan(dist.iloc[i]):
                        continue
                    r = cl.iloc[i + h] / cl.iloc[i] - 1
                    rows.append(dict(coin=c, win=w, year=yr[i], h=h, dist=dist.iloc[i],
                                     prof=inprof[i], fc=df["forecast"].iloc[i],
                                     ex=r - drift[(c, h)], r=r, ret60=ret60.iloc[i]))
    R = pd.DataFrame(rows)
    def reg(d):
        if len(d) < 10:
            return pd.Series(dict(n=len(d)))
        s = stats.linregress(d["dist"], d["ex"])
        t = s.slope / s.stderr if s.stderr > 0 else np.nan
        m = d["ex"].mean(); tm = m / (d["ex"].std() / np.sqrt(len(d)))
        return pd.Series(dict(n=len(d), slope=s.slope, t_slope=t, mean_ex=m, t_mean=tm))
    pos = R[R["dist"] > 0]
    out["by_h_inprofile_above"] = pos[pos.prof].groupby("h").apply(reg)
    out["by_h_outprofile_above"] = pos[~pos.prof].groupby("h").apply(reg)
    out["by_h_inprofile_below"] = R[(R.dist <= 0) & R.prof].groupby("h").apply(reg)
    p5 = pos[pos.prof & (pos.h == 5)].copy()
    p5["q"] = pd.qcut(p5["dist"], 5, labels=False)
    out["h5_in_quintile"] = p5.groupby("q").agg(n=("ex", "size"), dist=("dist", "mean"), mean_ex=("ex", "mean"))
    out["h5_in_by_coin"] = p5.groupby("coin").apply(reg)
    out["h5_in_by_year"] = p5.groupby("year").apply(reg)
    p5["r60q"] = pd.qcut(p5["ret60"], 3, labels=False)
    out["h5_in_by_ret60tercile"] = p5.groupby("r60q").apply(reg)
    q5 = pos[~pos.prof & (pos.h == 5)].copy()
    q5["q"] = pd.qcut(q5["dist"], 5, labels=False)
    out["h5_out_quintile"] = q5.groupby("q").agg(n=("ex", "size"), dist=("dist", "mean"), mean_ex=("ex", "mean"))
    p10 = pos[pos.prof & (pos.h == 10)].copy()
    p10["q"] = pd.qcut(p10["dist"], 5, labels=False)
    out["h10_in_quintile"] = p10.groupby("q").agg(n=("ex", "size"), dist=("dist", "mean"), mean_ex=("ex", "mean"))
    out["share_inprof"] = float(R[R.h == 1].prof.mean())
    return out
