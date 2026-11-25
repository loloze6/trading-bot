import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5]
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            f = df["forecast"].fillna(0).values
            prior_low = pd.Series(lo).shift(1).rolling(30).min().values
            ret30 = pd.Series(c).pct_change(30).values
            rng = (hi - lo) / c
            rr = pd.Series(rng).rolling(30).mean().values / pd.Series(rng).rolling(365, min_periods=91).mean().values
            depth = c / prior_low - 1
            for h in H:
                for start in range(0, n, h):
                    cell = range(start, min(start + h, n))
                    # broad situation: any close below prior 30-day low (no regime filter)
                    pick = [i for i in cell if not np.isnan(depth[i]) and depth[i] < 0]
                    if not pick:
                        continue
                    i = pick[0]
                    if i + h >= n:
                        continue
                    r = c[i + h] / c[i] - 1
                    d, s = drift[(coin, h)]
                    rows.append(dict(coin=coin, h=h, r=r, u=r - d, st=(r - d) / s, year=ts[i].year,
                                     day=ts[i].normalize(), depth=depth[i], fc=f[i],
                                     inreg=(ret30[i] < 0) and (rr[i] > 1) if not np.isnan(rr[i]) else False,
                                     rr=rr[i]))
    R = pd.DataFrame(rows)
    def tday(g):
        n = len(g); m = g["u"].mean()
        dev = g.groupby("day")["u"].apply(lambda x: (x - m).sum()); D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / n if D > 1 else np.nan
        return pd.Series(dict(n=n, days=D, mean_u=m, t=m / se if se else np.nan, strength=g["st"].mean()))
    out = {}
    S = R[R.fc >= 2]
    out["signal_by_h_excl2020"] = S[S.year != 2020].groupby("h").apply(tday)
    out["signal_by_h_only2020"] = S[S.year == 2020].groupby("h").apply(tday)
    out["signal_h1_by_coin"] = S[S.h == 1].groupby("coin").apply(tday)
    out["broad_by_h"] = R.groupby("h").apply(tday)
    out["broad_inreg_by_h"] = R[R.inreg].groupby("h").apply(tday)
    out["broad_outreg_by_h"] = R[~R.inreg].groupby("h").apply(tday)
    B = R[R.inreg].copy()
    B["dq"] = B.groupby("h")["depth"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["inreg_by_h_depthtercile(0=deepest)"] = B.groupby(["h", "dq"]).apply(tday)
    B2 = R[R.inreg & (R.year != 2020)].copy()
    out["inreg_excl2020_by_h"] = B2.groupby("h").apply(tday)
    C = R[~R.inreg].copy()
    C["dq"] = C.groupby("h")["depth"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["outreg_by_h_depthtercile"] = C.groupby(["h", "dq"]).apply(tday)
    return out
