def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    # drift per coin per horizon over all windows (non-overlapping)
    H = [1, 3, 5, 7]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]; rng = ((df["high"] - df["low"]) / cl).rolling(30).mean()
            sr = (cl / cl.shift(3) - 1) / rng
            reg = df["regime"].astype(str)
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=c, win=w, h=h, i=i, reg=reg[i], sr=sr[i],
                                     fc=df["forecast"][i],
                                     um=cl[i + h] / cl[i] - 1 - drift[(c, h)],
                                     tm=cl[i + h] / cl[i] - 1))
    R = pd.DataFrame(rows)
    R["inprof"] = R["reg"].isin(["trending", "unknown"])
    out["regime counts h1"] = R[R.h == 1]["reg"].value_counts()
    def summ(g):
        return pd.Series(dict(n=len(g), mean_um=g.um.mean(), t=stats.ttest_1samp(g.um, 0).statistic if len(g) > 2 else np.nan))
    P = R[R.inprof & R.sr.notna()].copy()
    P["srbin"] = pd.cut(P.sr, [-np.inf, -1, 0, 1, 2, 3, np.inf])
    out["in profile, by scaled rise bin and horizon"] = P.groupby(["h", "srbin"]).apply(summ)
    T = R[(R.reg == "trending")]
    out["trending bars by coin and h"] = T.groupby(["h", "coin"]).apply(summ)
    out["trending bars by window h3"] = T[T.h == 3].groupby("win").apply(summ)
    out["slope um on sr in profile by h"] = P.groupby("h").apply(lambda g: pd.Series(dict(slope=stats.linregress(g.sr, g.um).slope, t=stats.linregress(g.sr, g.um).slope / stats.linregress(g.sr, g.um).stderr, n=len(g))))
    out["usual move"] = pd.Series({f"{k[0]}_{k[1]}": v for k, v in usual.items()})
    return out
