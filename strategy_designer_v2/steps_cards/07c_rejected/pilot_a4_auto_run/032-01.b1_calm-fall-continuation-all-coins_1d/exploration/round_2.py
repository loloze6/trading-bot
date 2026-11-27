import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].astype(float).values)
            n = len(c)
            feats = {
                "r3": c.pct_change(3), "r7": c.pct_change(7), "r14": c.pct_change(14),
                "r30": c.pct_change(30), "r60": c.pct_change(60),
                "off_low30": c / c.rolling(30).min() - 1,
                "off_high30": c / c.rolling(30).max() - 1,
            }
            for i in range(n):
                d = {"coin": coin, "win": w, "pos": i, "inprof": df["regime"].iloc[i] == "unknown",
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year}
                for k, v in feats.items():
                    d[k] = v.iloc[i]
                for h in (1, 3, 5, 10):
                    d[f"f{h}"] = c.iloc[i+h]/c.iloc[i]-1 if i+h < n else np.nan
                rows.append(d)
    X = pd.DataFrame(rows)
    out = {}
    P = X[X.inprof]
    res = []
    for h in (1, 3, 5, 10):
        dr = X[X.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        for f in ["r3", "r7", "r14", "r30", "r60", "off_low30", "off_high30"]:
            g = P[P.pos % h == 0].dropna(subset=[f"f{h}", f]).copy()
            g["ex"] = g[f"f{h}"] - g.coin.map(dr)
            sl = stats.linregress(g[f], g["ex"])
            # top vs bottom half
            med = g[f].median()
            hi = g[g[f] > med].ex; lo = g[g[f] <= med].ex
            res.append({"h": h, "feat": f, "n": len(g), "slope": sl.slope, "t": sl.slope/sl.stderr,
                        "ex_hi_minus_lo": hi.mean()-lo.mean(),
                        "t_welch": stats.ttest_ind(hi, lo, equal_var=False).statistic})
    out["slopes"] = pd.DataFrame(res)
    # off_low30 quintiles at h3 and h5, and per coin slope at h3
    for h in (3, 5):
        dr = X[X.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        g = P[P.pos % h == 0].dropna(subset=[f"f{h}", "off_low30", "r7"]).copy()
        g["ex"] = g[f"f{h}"] - g.coin.map(dr)
        g["q"] = pd.qcut(g["off_low30"], 4, labels=False)
        out[f"offlow_q_h{h}"] = g.groupby("q").agg(n=("ex", "size"), off=("off_low30", "mean"), ex=("ex", "mean"))
        g["q7"] = pd.qcut(g["r7"], 4, labels=False)
        out[f"r7_q_h{h}"] = g.groupby("q7").agg(n=("ex", "size"), r7=("r7", "mean"), ex=("ex", "mean"))
        out[f"r7_coin_h{h}"] = g.groupby("coin").apply(lambda s: pd.Series({"n": len(s),
            "corr_r7": np.corrcoef(s.r7, s.ex)[0, 1] if len(s) > 3 else np.nan,
            "corr_offlow": np.corrcoef(s.off_low30, s.ex)[0, 1] if len(s) > 3 else np.nan}))
        out[f"r7_year_h{h}"] = g.groupby("year").apply(lambda s: pd.Series({"n": len(s),
            "corr_r7": np.corrcoef(s.r7, s.ex)[0, 1] if len(s) > 3 else np.nan}))
    # out of profile same r7 slope h5 for contrast
    dr = X[X.pos % 5 == 0].groupby("coin")["f5"].mean()
    g = X[(~X.inprof) & (X.pos % 5 == 0)].dropna(subset=["f5", "r7"]).copy()
    g["ex"] = g.f5 - g.coin.map(dr)
    sl = stats.linregress(g.r7, g.ex)
    out["outprof_r7_h5"] = pd.Series({"n": len(g), "slope": sl.slope, "t": sl.slope/sl.stderr})
    return out
