import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            cl = np.where(rng > 0, (c - lo) / np.where(rng > 0, rng, 1), np.nan)
            agit = (df["regime"] != "chop").values
            r60 = pd.Series(c).pct_change(60).values
            n = len(df)
            for i in range(0, n - 7):
                rows.append(dict(coin=coin, win=w, i=i, off=i % 7, ts=df["timestamp"].iloc[i],
                                 cl=cl[i], agit=agit[i], r60=r60[i],
                                 r7=c[i + 7] / c[i] - 1, r1=c[i + 1] / c[i] - 1,
                                 r17=c[i + 7] / c[i + 1] - 1, fc=df["forecast"].iloc[i]))
    R = pd.DataFrame(rows).dropna(subset=["cl"])
    g0 = R[R.off == 0]
    for col in ["r7", "r1", "r17"]:
        R["d_" + col] = R.groupby("coin")[col].transform(lambda s: s[R.loc[s.index, "off"] == 0].mean())
        R["x_" + col] = R[col] - R["d_" + col]
    R["day"] = pd.to_datetime(R["ts"]).dt.floor("D")
    R["trend"] = pd.cut(R["r60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    R["upper"] = R["cl"] > 0.5

    def tcl(s, col):
        m = s[col].mean(); dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return m, m / se if se > 0 else np.nan
    out = {}
    # grid offset robustness: agitated, spearman cl vs x_r7, and top-minus-bottom half
    o = []
    for off in range(7):
        s = R[(R.off == off) & R.agit]
        rho, p = stats.spearmanr(s.cl, s.x_r7)
        d = s[s.upper].x_r7.mean() - s[~s.upper].x_r7.mean()
        o.append(dict(off=off, rho=rho, p=p, up_minus_low=d, n=len(s)))
    out["offset_robust"] = pd.DataFrame(o)
    # all offsets pooled (overlapping, descriptive), by trend: spearman and upper/lower means
    A = R[R.agit]
    tr = []
    for tg in ["falling", "choppy", "rising"]:
        s = A[A.trend == tg]
        if len(s) > 20:
            rho = stats.spearmanr(s.cl, s.x_r7)[0]
            s0 = s[s.off == 0]
            mu, tu = tcl(s0[s0.upper], "x_r7"); ml, tl = tcl(s0[~s0.upper], "x_r7")
            tr.append(dict(trend=tg, rho_all_off=rho, n_all=len(s), up_mean=mu, up_t=tu, low_mean=ml, low_t=tl, n_grid=len(s0)))
    out["trend_split"] = pd.DataFrame(tr)
    # day 1 vs days 2-7, agitated grid off0, by quintile
    A0 = A[A.off == 0].copy()
    A0["q"] = pd.cut(A0.cl, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["q1", "q2", "q3", "q4", "q5"])
    out["agit_split_days"] = A0.groupby("q")[["x_r1", "x_r17", "x_r7"]].mean()
    out["agit_spearman_r17"] = pd.Series(dict(rho_r17=stats.spearmanr(A0.cl, A0.x_r17)[0],
                                              p=stats.spearmanr(A0.cl, A0.x_r17)[1]))
    # raw cl vs forecast: share of upper-half closes with fc>0, corr
    out["fc_vs_cl"] = pd.Series(dict(share_upper_fc_pos=(A[A.upper].fc > 0).mean(),
                                     share_lower_fc_pos=(A[~A.upper].fc > 0).mean(),
                                     spearman_fc_cl=stats.spearmanr(A.fc, A.cl)[0]))
    # by window: top minus bottom half, agit, all offsets
    out["by_window"] = A.groupby(["win", "upper"])["x_r7"].mean().unstack().assign(diff=lambda d: d[True] - d[False])
    return out
