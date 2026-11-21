def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 26
    drift = {}
    for c in bars:
        fr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                fr.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(fr)
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            hi = b["high"].values
            sl = b.get("debug_info.components.slope_size.last_history_value", pd.Series([np.nan]*n)).values
            for i in range(0, n - H, H):
                f = b["forecast"].iloc[i]
                if not f < 0: continue
                r = cl[i + H] / cl[i] - 1
                p26 = cl[i] / cl[i - 26] - 1 if i >= 26 else np.nan
                p52 = cl[i] / cl[i - 52] - 1 if i >= 52 else np.nan
                p7 = cl[i] / cl[i - 7] - 1 if i >= 7 else np.nan
                dd = cl[i] / np.max(hi[max(0, i - 52):i + 1]) - 1 if i >= 26 else np.nan
                rows.append(dict(coin=c, win=w, f=f, r=r, ex=r - drift[c], p26=p26, p52=p52, p7=p7, dd=dd, slope=sl[i]))
    df = pd.DataFrame(rows)
    out = {}
    def tab(col, q=4):
        a = df.dropna(subset=[col]).copy()
        a["q"] = pd.qcut(a[col], q, labels=False, duplicates="drop")
        g = a.groupby("q").agg(n=("r", "size"), x=(col, "mean"), r=("r", "mean"), ex=("ex", "mean"))
        g["t_r"] = a.groupby("q").r.apply(lambda x: stats.ttest_1samp(x, 0).statistic)
        return g
    for col in ["p7", "p52", "dd", "slope"]:
        out["by " + col] = tab(col)
    a = df.dropna(subset=["slope", "p26"]).copy()
    a["steep"] = a.slope < a.slope.median()
    a["fell26"] = a.p26 < a.p26.median()
    out["steep slope x fell26 (r, n)"] = a.groupby(["steep", "fell26"]).agg(n=("r", "size"), r=("r", "mean"), ex=("ex", "mean"))
    rho = df.dropna(subset=["slope"])
    out["spearman r vs slope / vs p26 / vs dd"] = f"{stats.spearmanr(rho.slope, rho.r)[0]:.3f} / {stats.spearmanr(df.dropna(subset=['p26']).p26, df.dropna(subset=['p26']).r)[0]:.3f} / {stats.spearmanr(df.dropna(subset=['dd']).dd, df.dropna(subset=['dd']).r)[0]:.3f}"
    # book daily return by window, worst windows
    bw = []
    for c in days:
        for w, d in days[c].items():
            bw.append(dict(win=w, book=d.book_return.sum(), coin=d.coin_return.sum()))
    bw = pd.DataFrame(bw).groupby("win").mean()
    out["book vs coin summed daily return by window"] = bw
    return out
