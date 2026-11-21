def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    fdist = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        rr = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 18, 18)
            rr += list(c[idx + 18] / c[idx] - 1)
        drift[coin] = np.mean(rr); usual[coin] = np.std(rr)
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            f = b["forecast"].fillna(0).values
            rng = (h - l) / c
            rng_s = pd.Series(rng)
            q = (rng_s.rolling(42).mean() / rng_s.rolling(360, min_periods=90).mean()).values
            hi12 = pd.Series(h).shift(1).rolling(12).max().values
            lo12 = pd.Series(l).shift(1).rolling(12).min().values
            narrow = ((hi12 - lo12) / c) / (rng_s.rolling(180, min_periods=60).mean().values * 12)
            brk = (c - hi12) / c
            ret120 = pd.Series(c).pct_change(180).values  # 30-day trend
            fdist += list(f[f > 0])
            low = 0.0; n = len(c)
            taken = set()
            for t in range(1, n):
                if f[t] <= 0:
                    low = 0.0; continue
                if f[t] - low >= 2:
                    cell = t // 18
                    if cell not in taken:
                        taken.add(cell)
                        rec = dict(coin=coin, win=int(w[1:]), year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                                   f=f[t], q=q[t], narrow=narrow[t], brk=brk[t], tr=ret120[t])
                        for H in (6, 12, 18, 36):
                            rec[f"r{H}"] = (c[t + H] / c[t] - 1 - drift[coin] * H / 18) if t + H < n else np.nan
                        rows.append(rec)
                    low = f[t]
                else:
                    low = min(low, f[t])
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["r18"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out["all"] = summ(d)
    out["horizons"] = pd.DataFrame({H: [d[f"r{H}"].mean(), d[f"r{H}"].mean() / (d[f"r{H}"].std() / np.sqrt(d[f"r{H}"].count())), d[f"r{H}"].count()] for H in (6, 12, 18, 36)}, index=["mean", "t", "n"])
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_forecast_q"] = d.groupby(pd.qcut(d["f"].rank(method="first"), 4, labels=False)).apply(summ)
    out["share_f_at_20"] = float((d["f"] >= 19.99).mean())
    out["fdist_quantiles"] = pd.Series(np.quantile(fdist, [0.1, 0.25, 0.5, 0.75, 0.9]))
    out["by_quietweek_q"] = d.groupby(pd.qcut(d["q"], 4, labels=False)).apply(summ)
    out["by_narrow_q"] = d.groupby(pd.qcut(d["narrow"], 4, labels=False)).apply(summ)
    out["by_brk_q"] = d.groupby(pd.qcut(d["brk"], 4, labels=False)).apply(summ)
    out["by_trend30d_q"] = d.groupby(pd.qcut(d["tr"], 4, labels=False)).apply(summ)
    out["trend_bounds"] = pd.Series(np.nanquantile(d["tr"], [0.25, 0.5, 0.75]))
    return out
