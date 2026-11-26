import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 10
    allret = []
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; lo = df["low"].values
            n = len(df)
            for i in range(0, n - H, H):
                allret.append(c[i + H] / c[i] - 1)
            f = df["forecast"].fillna(0).values
            prior_low = pd.Series(lo).shift(1).rolling(30, min_periods=30).min().values
            tr60 = pd.Series(c).pct_change(60).values * 100
            tr30 = pd.Series(c).pct_change(30).values * 100
            seen = set()
            fprev = np.r_[0, f[:-1]]
            for i in range(n - H):
                if (fprev[i] - f[i]) >= 2:
                    cell = i // H
                    if cell in seen: continue
                    seen.add(cell)
                    depth = (prior_low[i] - lo[i]) / prior_low[i] * 100 if not np.isnan(prior_low[i]) else np.nan
                    rows.append(dict(coin=coin, w=w, day=str(df["timestamp"].iloc[i])[:10],
                                     year=str(df["timestamp"].iloc[i])[:4], absf=abs(f[i]),
                                     depth=depth, tr60=tr60[i], tr30=tr30[i],
                                     ret=c[i + H] / c[i] - 1))
    ev = pd.DataFrame(rows)
    drift = np.mean(allret); sd = np.std(allret, ddof=1)
    ev["u"] = -(ev["ret"] - drift)
    ev["strength"] = ev["u"] / sd

    def summ(g):
        m = g["u"].mean()
        dd = g.groupby("day")["u"].apply(lambda x: (x - m).sum())
        G = len(dd)
        se = np.sqrt((dd ** 2).sum() * G / max(G - 1, 1)) / len(g)
        return pd.Series(dict(n=len(g), days=G, mean_short=m, t=m / se if se > 0 else np.nan,
                              share_pos=(g["u"] > 0).mean(), median=g["u"].median()))
    out = {}
    out["drift_sd"] = pd.Series(dict(drift=drift, sd=sd))
    out["recorded_cases_BC"] = summ(ev)
    out["by_year"] = ev.groupby("year").apply(summ)
    out["by_coin"] = ev.groupby("coin").apply(summ)
    out["by_window"] = ev.groupby("w").apply(summ)
    ev["trq"] = pd.qcut(ev["tr60"].rank(method="first"), 3, labels=["weak_up", "mid_up", "strong_up"]) if ev["tr60"].notna().sum() >= 6 else "na"
    out["by_tr60_tercile"] = ev.groupby("trq").apply(summ)
    out["tr60_range"] = ev["tr60"].describe()
    out["corr_u_tr60"] = float(ev[["u", "tr60"]].dropna().corr().iloc[0, 1]) if ev["tr60"].notna().sum() > 3 else np.nan
    out["corr_u_absf"] = float(ev[["u", "absf"]].corr().iloc[0, 1])
    out["corr_u_depth"] = float(ev[["u", "depth"]].dropna().corr().iloc[0, 1])
    out["mean_strength"] = float(ev["strength"].mean())
    return out
