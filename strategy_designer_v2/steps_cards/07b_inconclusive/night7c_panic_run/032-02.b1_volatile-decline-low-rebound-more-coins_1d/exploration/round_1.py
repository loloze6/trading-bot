import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5, 10, 20]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lo = df["low"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            f = df["forecast"].fillna(0).values
            reg = df["regime"].values
            prior_low = pd.Series(lo).shift(1).rolling(30).min().values
            ret30 = pd.Series(c).pct_change(30).values
            for h in H:
                for start in range(0, n, h):
                    cell = range(start, min(start + h, n))
                    # case: first bar in cell with forecast >= 2
                    pick = [i for i in cell if f[i] >= 2]
                    if not pick:
                        continue
                    i = pick[0]
                    if i + h >= n:
                        continue
                    r = c[i + h] / c[i] - 1
                    d, s = drift[(coin, h)]
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], r=r, u=r - d, st=(r - d) / s,
                                     year=ts[i].year, day=ts[i].normalize(),
                                     depth=c[i] / prior_low[i] - 1 if not np.isnan(prior_low[i]) else np.nan,
                                     ret30=ret30[i]))
    R = pd.DataFrame(rows)
    out = {}
    def tday(g):
        s = g.groupby("day")["u"].sum()
        D = len(s); n = len(g)
        m = g["u"].mean()
        dev = g.groupby("day")["u"].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / n if D > 1 else np.nan
        return pd.Series(dict(n=n, days=D, mean_u=m, t=m / se if se else np.nan, mean_r=g["r"].mean(), strength=g["st"].mean()))
    out["by_horizon"] = R.groupby("h").apply(tday)
    R5 = R[R.h == 5]
    out["h5_by_coin"] = R5.groupby("coin").apply(tday)
    out["h5_by_year"] = R5.groupby("year").apply(tday)
    R5 = R5.copy()
    R5["fq"] = pd.qcut(R5["f"], 3, labels=False, duplicates="drop")
    out["h5_by_forecast_tercile"] = R5.groupby("fq").apply(lambda g: pd.concat([tday(g), pd.Series(dict(fmean=g.f.mean(), depth=g.depth.mean()))]))
    R5["r30q"] = pd.qcut(R5["ret30"], 3, labels=False, duplicates="drop")
    out["h5_by_ret30_tercile"] = R5.groupby("r30q").apply(lambda g: pd.concat([tday(g), pd.Series(dict(r30=g.ret30.mean()))]))
    R1 = R[R.h == 1].copy()
    R1["fq"] = pd.qcut(R1["f"], 3, labels=False, duplicates="drop")
    out["h1_by_forecast_tercile"] = R1.groupby("fq").apply(tday)
    R10 = R[R.h == 10].copy()
    out["h10_by_year"] = R10.groupby("year").apply(tday)
    return out
