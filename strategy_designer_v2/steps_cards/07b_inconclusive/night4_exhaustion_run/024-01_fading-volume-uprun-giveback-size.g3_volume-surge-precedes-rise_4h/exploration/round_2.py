import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 18
    rows = []
    for coin, ws in bars.items():
        allr = []
        wdrift = {}
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rr = list(c[idx + H] / c[idx] - 1)
            allr += rr
            wdrift[w] = np.mean(rr) if len(rr) else np.nan
        drift = np.mean(allr)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            prior6 = np.r_[[np.nan] * 6, c[6:] / c[:-6] - 1]
            # trend of the prior 30 days
            prior180 = np.r_[[np.nan] * 180, c[180:] / c[:-180] - 1]
            # base rate: all grid cells regardless of signal
            for start in range(0, n - H, H):
                cell = np.arange(start, start + H)
                hit = cell[f[cell] >= 2]
                sig = len(hit) > 0
                t = hit[0] if sig else start
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1
                rows.append(dict(coin=coin, window=w, year=ts.iloc[t].year, sig=sig, f=f[t],
                                 ex=r - drift, exw=r - wdrift[w], prior6=prior6[t], prior180=prior180[t]))
    d = pd.DataFrame(rows)
    s = d[d.sig]
    ns = d[~d.sig]

    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})

    out = {}
    out["signal_ex_vs_window_drift"] = summ(s.exw)
    out["nonsignal_ex_global"] = summ(ns.ex)
    out["sig_minus_nonsig_welch"] = pd.Series({"diff": s.ex.mean() - ns.ex.mean(),
                                               "t": stats.ttest_ind(s.ex.dropna(), ns.ex.dropna(), equal_var=False)[0]})
    out["by_year_window_drift"] = s.groupby("year").exw.apply(summ).unstack()
    out["by_year_sig_minus_nonsig"] = d.groupby("year").apply(lambda g: g[g.sig].ex.mean() - g[~g.sig].ex.mean())
    s = s.copy()
    s["trend"] = np.where(s.prior180 > 0, "up30d", "down30d")
    out["by_30d_trend"] = s.groupby("trend").ex.apply(summ).unstack()
    s["p6sign"] = np.where(s.prior6 > 0, "prior1d_up", "prior1d_down")
    out["by_prior1d_sign"] = s.groupby("p6sign").ex.apply(summ).unstack()
    s["absp6q"] = pd.qcut(s.prior6.abs(), 4, labels=False)
    out["by_abs_prior1d_quartile"] = s.groupby("absp6q").ex.apply(summ).unstack()
    up = s[s.prior6 > 0].dropna(subset=["prior6", "ex"])
    out["spearman_prior1d_vs_ex_upside"] = pd.Series({"rho": stats.spearmanr(up.prior6, up.ex)[0], "n": len(up)})
    return out
