def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    H = 26
    for coin, ws in bars.items():
        allr = []
        cases = []
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            hi = df["high"]; lo = df["low"]
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb).values
            bot = np.minimum(sa, sb).values
            mid = ((sa + sb) / 2).values
            f = df["forecast"].fillna(0).values
            n = len(df)
            for i in range(0, n - H, H):
                r = c[i + H] / c[i] - 1
                allr.append(r)
                past = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                dist = c[i] / top[i] - 1 if not np.isnan(top[i]) else np.nan
                thick = (top[i] - bot[i]) / c[i] if not np.isnan(top[i]) else np.nan
                cases.append((w, r, f[i], past, dist, thick))
        drift = np.mean(allr)
        for (w, r, fc, past, dist, thick) in cases:
            rows.append(dict(coin=coin, w=w, ex=r - drift, fc=fc, past=past, dist=dist, thick=thick))
    d = pd.DataFrame(rows)
    a = d[d.fc > 0].copy()
    ina = d[d.fc <= 0]
    out["welch_active_minus_inactive"] = pd.Series(dict(diff=a.ex.mean() - ina.ex.mean(), t=stats.ttest_ind(a.ex, ina.ex, equal_var=False).statistic))
    q = a.ex.quantile([0.05, 0.95]).values
    w_ = a.ex.clip(q[0], q[1])
    out["winsor5_mean_t"] = pd.Series(dict(mean=w_.mean(), t=w_.mean() / (w_.std() / np.sqrt(len(w_)))))
    s = a.ex.sort_values(ascending=False)
    out["mean_without_top5"] = pd.Series(dict(mean=s.iloc[5:].mean(), t=s.iloc[5:].mean() / (s.iloc[5:].std() / np.sqrt(len(s) - 5))))
    out["skew_ex"] = float(stats.skew(a.ex))
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.ex.mean(), t=g.ex.mean() / (g.ex.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    for col in ["past", "dist", "thick"]:
        b = a.dropna(subset=[col]).copy()
        if len(b) > 20:
            b["q"] = pd.qcut(b[col].rank(method="first"), 3, labels=["lo", "mid", "hi"])
            out[f"by_{col}_tercile"] = b.groupby("q").apply(summ)
            lr = stats.linregress(b[col], b.ex)
            out[f"reg_{col}"] = pd.Series(dict(n=len(b), slope=lr.slope, t=lr.slope / lr.stderr))
    a["wn"] = a.w.str[1:].astype(int)
    a["half"] = np.where(a.wn <= 12, "w1-w12", "w13-w24")
    out["by_half"] = a.groupby("half").apply(summ)
    return out
