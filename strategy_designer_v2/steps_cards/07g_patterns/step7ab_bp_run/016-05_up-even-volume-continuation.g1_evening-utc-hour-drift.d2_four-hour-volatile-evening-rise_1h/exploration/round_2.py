import numpy as np, pandas as pd
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    bars = data["bars"]; out = {}
    day_rows = []; grind = []; book_rows = []
    for coin, wins in bars.items():
        g24 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            g24.extend(list(c[idx + 24] / c[idx] - 1))
        m24, s24 = np.mean(g24), np.std(g24)
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]); c = df["close"].values.astype(float)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            vol7 = pd.Series(lr).rolling(168, min_periods=120).std().values
            # 24h from the close of the bar starting 23:00 (i.e. midnight close) -> one full UTC day
            end_hours = (ts.dt.hour.values == 23)
            for t in np.where(end_hours)[0]:
                if t + 24 >= len(c): continue
                nxt = ts.iloc[t] + pd.Timedelta(hours=1)
                F = c[t + 24] / c[t] - 1
                p7 = c[t] / c[t - 168] - 1 if t >= 168 else np.nan
                day_rows.append((coin, w, nxt.weekday(), nxt.year, F - m24, F, vol7[t], p7, (F - m24) / s24))
            # turnover and book
            a = df["postRebalance_current_allocation"].astype(float).values
            pa = df["previous_allocation"].astype(float).values
            tv = df["total_portfolio_value"].astype(float).values
            ptv = df["postRebalance_total_value"].astype(float).values
            nd = ts.dt.floor("D").nunique()
            book_rows.append((coin, w, np.nansum(np.abs(a - pa)) / nd, np.nansum(tv - ptv) / np.nanmean(tv) / nd,
                              (df["forecast"] != 0).mean(), np.nanmean(np.abs(a))))
    D = pd.DataFrame(day_rows, columns=["coin", "w", "wd", "yr", "Fu", "F", "vol7", "p7", "Fz"])
    g = D.groupby("wd").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), F_bps=("F", lambda x: x.mean() * 1e4), t=("Fu", tstat))
    out["next UTC day unusual move by weekday (all coins)"] = g.round(2)
    sat = D[D["wd"] == 5]
    out["Saturday unusual move by coin"] = sat.groupby("coin").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), t=("Fu", tstat)).round(2)
    out["Saturday unusual move by year"] = sat.groupby("yr").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), t=("Fu", tstat)).round(2)
    out["Saturday by window count positive"] = pd.Series({"windows": sat["w"].nunique(),
        "share of window means > 0": sat.groupby("w")["Fu"].mean().gt(0).mean()})
    sat = sat.copy()
    sat["vt"] = sat.groupby("coin")["vol7"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    sat["pt"] = sat.groupby("coin")["p7"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["Saturday by 7d vol third"] = sat.groupby("vt").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), Fz=("Fz", "mean"), t=("Fu", tstat)).round(3)
    out["Saturday by 7d return third"] = sat.groupby("pt").agg(n=("Fu", "size"), Fu_bps=("Fu", lambda x: x.mean() * 1e4), Fz=("Fz", "mean"), t=("Fu", tstat)).round(3)
    # weekend 48h (Sat+Sun) vs weekday
    B = pd.DataFrame(book_rows, columns=["coin", "w", "turnover_per_day", "fee_share_per_day", "active_share", "mean_abs_alloc"])
    out["book turnover and fees by coin"] = B.groupby("coin")[["turnover_per_day", "fee_share_per_day", "active_share", "mean_abs_alloc"]].mean().round(5)
    return out
