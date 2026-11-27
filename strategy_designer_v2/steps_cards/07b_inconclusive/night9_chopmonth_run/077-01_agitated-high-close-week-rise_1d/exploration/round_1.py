import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 3, 7, 14]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            cl = np.where(rng > 0, (c - lo) / np.where(rng > 0, rng, 1), np.nan)
            agit = (df["regime"] != "chop").values
            n = len(df)
            r60 = pd.Series(c).pct_change(60).values
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, i=i, ts=df["timestamp"].iloc[i],
                                     cl=cl[i], agit=agit[i], r60=r60[i],
                                     ret=c[i + h] / c[i] - 1,
                                     fc=df["forecast"].iloc[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]
    R["day"] = pd.to_datetime(R["ts"]).dt.floor("D")
    R["year"] = pd.to_datetime(R["ts"]).dt.year
    R = R.dropna(subset=["cl"])
    R["q"] = pd.cut(R["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["q1low", "q2", "q3", "q4", "q5high"])

    def tclust(sub):
        g = sub.groupby("day")["ex"].sum()
        n = len(sub)
        m = sub["ex"].mean()
        se = np.sqrt((g - g.index.map(lambda d: 0).values * 0).pow(2).sum() - 0) if False else None
        dev = (sub["ex"] - m).groupby(sub["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return m, (m / se if se > 0 else np.nan), n

    out = {}
    t = []
    for h in H:
        for a in [True, False]:
            for q in ["q1low", "q2", "q3", "q4", "q5high"]:
                s = R[(R.h == h) & (R.agit == a) & (R.q == q)]
                m, tt, n = tclust(s)
                t.append(dict(h=h, agit=a, q=q, mean_ex=m, t=tt, n=n))
    out["by_h_agit_q"] = pd.DataFrame(t).pivot_table(index=["h", "agit"], columns="q", values=["mean_ex", "t"])
    # correlation cl vs ex in agitated, by h
    c2 = []
    for h in H:
        for a in [True, False]:
            s = R[(R.h == h) & (R.agit == a)]
            rho, p = stats.spearmanr(s["cl"], s["ex"])
            c2.append(dict(h=h, agit=a, spearman=rho, p=p, n=len(s)))
    out["rank_corr"] = pd.DataFrame(c2)
    # by trend in agitated, h=7, top vs bottom
    A = R[(R.agit) & (R.h == 7)].copy()
    A["trend"] = pd.cut(A["r60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    tr = []
    for tg in ["falling", "choppy", "rising"]:
        for q in ["q1low", "q3", "q5high"]:
            s = A[(A.trend == tg) & (A.q == q)]
            if len(s) > 5:
                m, tt, n = tclust(s); tr.append(dict(trend=tg, q=q, mean_ex=m, t=tt, n=n))
    out["agit_h7_trend"] = pd.DataFrame(tr)
    # by coin and by year: top minus bottom half, agit, h7
    A["upper"] = A["cl"] > 0.5
    out["agit_h7_coin"] = A.groupby(["coin", "upper"])["ex"].agg(["mean", "count"]).unstack()
    out["agit_h7_year"] = A.groupby(["year", "upper"])["ex"].agg(["mean", "count"]).unstack()
    # step-5-like weighted main measure check on recomputed
    s = A[A.fc > 0]
    out["fc_pos_weighted"] = pd.Series(dict(wmean=(s.ex * s.fc).sum() / s.fc.sum(), n=len(s),
                                            corr_fc_ex=stats.spearmanr(s.fc, s.ex)[0]))
    return out
