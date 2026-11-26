def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        r_all = []
        for w, df in wins.items():
            c = df["close"].values
            r_all.append(c[1:]/c[:-1]-1)
        drift[coin] = np.concatenate(r_all).mean()
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            rng = (h - l) / c
            mult = rng / rng.rolling(20).mean()
            r1 = c.pct_change()
            tr60 = (c / c.shift(60) - 1) * 100
            for H in (1, 2, 3, 5):
                fwd = c.shift(-H) / c - 1
                d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                                  "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                                  "year": pd.to_datetime(df["timestamp"]).dt.year,
                                  "mult": mult, "up": r1 > 0, "r1": r1, "tr60": tr60,
                                  "fc": df["forecast"], "H": H,
                                  "fwd_dev": -(fwd - drift[coin] * H)})
                rows.append(d)
    A = pd.concat(rows).dropna(subset=["mult", "tr60", "fwd_dev"])
    A["prof"] = np.where(A.tr60 < -10, "falling", np.where(A.tr60 > 10, "rising", "choppy"))

    def summ(g):
        days = g.groupby("day")["fwd_dev"].sum()
        n = len(g); D = len(days)
        m = g.fwd_dev.mean()
        se = np.sqrt((days - days.index.map(lambda x: 0)).pow(0).sum() * 0 + ((g.groupby("day")["fwd_dev"].apply(lambda s: (s - m).sum()))**2).sum()) / n * np.sqrt(D/(D-1)) if D > 1 else np.nan
        return pd.Series({"n": n, "days": D, "mean_short_dev_%": 100*m, "t_day": m/se if se else np.nan})

    out = {}
    # H=1 only, falling up days by width bucket (non-overlap trivially for H=1)
    A1 = A[A.H == 1]
    up = A1[A1.up]
    up = up.assign(wb=pd.cut(up.mult, [0, 0.8, 1.0, 1.3, 1.7, 2.2, 99]))
    out["H1 up days by profile x width"] = up.groupby(["prof", "wb"]).apply(summ)
    fw = up[(up.prof == "falling") & (up.mult > 1)]
    out["H1 falling wide-up by coin"] = fw.groupby("coin").apply(summ)
    out["H1 falling wide-up by window"] = fw.groupby("win").apply(summ)
    out["H1 falling wide-up by year"] = fw.groupby("year").apply(summ)
    # horizons, non-overlapping grid per window
    res = {}
    for H in (1, 2, 3, 5):
        g = A[(A.H == H) & (A.pos % H == 0) & A.up & (A.prof == "falling") & (A.mult > 1)]
        res[H] = summ(g)
    out["falling wide-up by horizon (grid)"] = pd.DataFrame(res).T
    # by size of the up day itself
    fw = fw.assign(rb=pd.qcut(fw.r1, 4))
    out["H1 falling wide-up by up-day return quartile"] = fw.groupby("rb").apply(summ)
    # agitation proxy: 30d std vs 365 median not available fully; use cases with forecast<=-2
    fc = A1[(A1.fc <= -2)]
    out["H1 forecast<=-2 cases"] = summ(fc)
    sl = stats.linregress(fw.mult, fw.fwd_dev)
    out["slope short_dev on mult (falling wide up)"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(fw)}"
    return out
