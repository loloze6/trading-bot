def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 20
    hs = (5, 10, 20)
    drift = {h: {} for h in hs}; usual = {}
    for coin, wins in bars.items():
        for h in hs:
            g = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    g.append(c[i + h] / c[i] - 1)
            drift[h][coin] = np.mean(g) if g else np.nan
            if h == H:
                usual[coin] = np.std(g, ddof=1)
    rows = []; base = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"]); n = len(c)
            ret60 = pd.Series(c).pct_change(60).values
            ret30 = pd.Series(c).pct_change(30).values
            ret10 = pd.Series(c).pct_change(10).values
            lr = np.log(pd.Series(c)).diff()
            vol20 = lr.rolling(20).std().values
            low = 0.0; taken = set()
            for i in range(n):
                if f[i] <= 0:
                    low = 0.0; continue
                if f[i] - low >= 2:
                    cell = i // H; low = f[i]
                    if cell in taken or i + H >= n: continue
                    taken.add(cell)
                    rec = dict(coin=coin, day=ts[i].normalize(), year=ts[i].year, f=f[i],
                               ret60=ret60[i], ret30=ret30[i], ret10=ret10[i], vol20=vol20[i])
                    for h in hs:
                        rec["u%d" % h] = c[i + h] / c[i] - 1 - drift[h][coin]
                    rows.append(rec)
                else:
                    low = min(low, f[i])
            for i in range(0, n - H, H):
                if ret30[i] > 0:
                    base.append(dict(coin=coin, day=ts[i].normalize(), ret60=ret60[i],
                                     u20=c[i+H]/c[i]-1-drift[H][coin]))
    d = pd.DataFrame(rows); b = pd.DataFrame(base)
    def tday(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3: return np.nan
        s = (x[col] - x[col].mean()).groupby(x["day"]).sum()
        se = np.sqrt((s**2).sum()) / len(x)
        return x[col].mean() / se
    def summ(x, col="u20"):
        x = x.dropna(subset=[col])
        return pd.Series({"n": len(x), "days": x["day"].nunique(), "mean": x[col].mean(),
                          "t_day": tday(x, col), "median": x[col].median()})
    out = {}
    out["unusual_by_horizon"] = pd.DataFrame({h: summ(d, "u%d" % h) for h in hs}).T
    lo, hi = d["u20"].quantile([0.025, 0.975])
    dw = d.assign(u20=d["u20"].clip(lo, hi))
    out["winsorised_2.5pct"] = summ(dw)
    d["r60s"] = np.where(d["ret60"].isna(), "na", np.where(d["ret60"] > 0, "ret60>0", "ret60<=0"))
    out["by_ret60_sign"] = d.groupby("r60s").apply(summ)
    b["r60s"] = np.where(b["ret60"].isna(), "na", np.where(b["ret60"] > 0, "ret60>0", "ret60<=0"))
    out["baseline_by_ret60_sign"] = b.groupby("r60s").apply(summ)
    x = d.dropna(subset=["ret10"]).copy()
    x["r10q"] = pd.qcut(x["ret10"], 3, labels=["lo", "mid", "hi"])
    out["by_ret10_third"] = x.groupby("r10q").apply(summ)
    x = d.dropna(subset=["vol20"]).copy()
    x["vq"] = pd.qcut(x["vol20"], 3, labels=["lo", "mid", "hi"])
    out["by_vol20_third"] = x.groupby("vq").apply(summ)
    out["corr_f_u20_spearman"] = d[["f", "u20"]].corr(method="spearman").iloc[0, 1]
    return out
