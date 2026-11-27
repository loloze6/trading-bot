def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    H = [1, 2, 3, 5, 7]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            rng = ((df["high"] - df["low"]) / df["close"]).rolling(30).mean().values
            sr = (df["close"] / df["close"].shift(3) - 1).values / rng
            fc = df["forecast"].fillna(0).values
            n = len(df)
            low = 0.0
            cases = []
            for i in range(n):
                if fc[i] - low >= 2:
                    cases.append(i); low = fc[i]
                else:
                    low = min(low, fc[i])
            seen = set()
            for i in cases:
                cell = i // 3
                if cell in seen: continue
                seen.add(cell)
                r = dict(coin=c, win=w, i=i, sr=sr[i], fc=fc[i], year=pd.Timestamp(df["timestamp"][i]).year)
                for h in H:
                    r[f"um{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)] if i + h < n else np.nan
                rows.append(r)
    C = pd.DataFrame(rows)
    def summ(g, col="um3"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(), share_pos=(x > 0).mean(),
                              t=stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan))
    out["cases by horizon"] = pd.DataFrame({h: summ(C, f"um{h}") for h in H}).T
    out["cases by coin h3"] = C.groupby("coin").apply(summ)
    out["cases by window h3"] = C.groupby("win").apply(summ)
    out["cases by year h3"] = C.groupby("year").apply(summ)
    C["srq"] = pd.qcut(C.sr, 3, labels=["low", "mid", "high"])
    out["cases by sr tercile h3"] = C.groupby("srq").apply(summ)
    out["cases by sr tercile h1"] = C.groupby("srq").apply(lambda g: summ(g, "um1"))
    out["cases by sr tercile h5"] = C.groupby("srq").apply(lambda g: summ(g, "um5"))
    out["sr tercile edges"] = C.groupby("srq").sr.agg(["min", "max"])
    x = C.dropna(subset=["um3"])
    lr = stats.linregress(x.fc, x.um3)
    out["slope um3 on fc"] = pd.Series(dict(slope=lr.slope, t=lr.slope / lr.stderr, n=len(x)))
    out["um3 dispersion"] = pd.Series(dict(std=x.um3.std(), p10=x.um3.quantile(.1), p90=x.um3.quantile(.9),
                                           mean_without_top5=x.um3.sort_values().iloc[:-5].mean()))
    return out
