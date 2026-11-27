def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = [1, 2, 3, 5, 10]
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 15: continue
            c = b["close"].values; hi = b["high"].values; lo = b["low"].values
            rng = hi - lo
            cl = np.where(rng > 0, (hi - c) / np.where(rng > 0, rng, 1), np.nan)
            reg = b["regime"].astype(str).values
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            for h in H:
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     h=h, i=i, cl=cl[i], reg=reg[i], r=c[i + h] / c[i] - 1, r1=ret1[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "h"])["r"].mean().rename("drift")
    df = df.join(drift, on=["coin", "h"])
    df["u_short"] = -(df["r"] - df["drift"])
    df["inprof"] = df["reg"].isin(["mean_reversion", "unknown"])
    df["clq"] = pd.cut(df["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["top", "q2", "mid", "q4", "low"])
    def summ(g):
        x = g["u_short"].dropna()
        n = len(x)
        return pd.Series(dict(n=n, mean_short=x.mean(), t=(x.mean() / (x.std() / np.sqrt(n))) if n > 2 else np.nan,
                              total_short=(-g["r"]).mean()))
    out["regime counts h1"] = df[df.h == 1]["reg"].value_counts()
    out["in-profile by h and close location (short-signed unusual)"] = df[df.inprof].groupby(["h", "clq"]).apply(summ).round(4)
    out["out-of-profile by h and close location"] = df[~df.inprof].groupby(["h", "clq"]).apply(summ).round(4)
    low = df[df.inprof & (df.clq == "low")]
    out["in-profile low close by coin, h"] = low.groupby(["coin", "h"]).apply(summ).round(4)
    out["in-profile low close by year, h3"] = low[low.h == 3].groupby("year").apply(summ).round(4)
    ip = df[df.inprof & (df.h == 3)].dropna(subset=["cl"])
    out["in-profile h3 corr cl vs u_short"] = pd.Series(stats.spearmanr(ip["cl"], ip["u_short"])).round(4)
    # low close after big down day vs small
    low3 = low[low.h == 3].copy()
    low3["r1q"] = pd.qcut(low3["r1"], 3, labels=["deep fall", "mid", "small/up"])
    out["in-profile low close h3 by own day return"] = low3.groupby("r1q").apply(summ).round(4)
    return out
