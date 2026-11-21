import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for coin, wins in bars.items():
        vals = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            vals.append(c[idx + 24] / c[idx] - 1)
        drift = np.nanmean(np.concatenate(vals))
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"]); hr = ts.dt.hour.values
            r1 = pd.Series(np.r_[np.nan, c[1:] / c[:-1] - 1])
            vol = r1.rolling(20).std().values
            vol30 = r1.rolling(720, min_periods=240).std()
            volrel = (vol30 / vol30.rolling(4320, min_periods=1000).median()).values
            r2 = np.r_[np.nan, np.nan, c[2:] / c[:-2] - 1]
            z = r2 / (vol * np.sqrt(2))
            r7 = np.r_[[np.nan]*168, c[168:] / c[:-168] - 1]
            for p in np.where(np.isin(hr, [23, 17, 5, 11]))[0]:
                if p + 24 >= len(c) or not np.isfinite(z[p]) or z[p] == 0: continue
                s = -np.sign(z[p])
                rows.append({"coin": coin, "hour": hr[p], "az": abs(z[p]), "volrel": volrel[p],
                             "vol": vol[p], "trend7_vs": s * np.sign(r7[p]) if np.isfinite(r7[p]) else np.nan,
                             "year": ts.iloc[p].year,
                             "x24": s * (c[p + 24] / c[p] - 1 - drift)})
    R = pd.DataFrame(rows)
    R["vq"] = R.groupby(["coin"])["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    R["zq"] = pd.qcut(R["az"], 3, labels=False)
    def summ(g):
        v = g["x24"].dropna()
        return pd.Series({"n": len(v), "x24_bps": 1e4 * v.mean(), "t": stats.ttest_1samp(v, 0).statistic if len(v) > 2 else np.nan})
    S = R[R.hour == 23]
    out["settle_vol_x_z"] = S.groupby(["vq", "zq"]).apply(summ)
    out["allhours_vol_x_z_top"] = R[(R.vq == 2)].groupby(["hour", "zq"]).apply(summ)
    S2 = S.dropna(subset=["volrel"]).copy()
    S2["vrq"] = pd.qcut(S2["volrel"], 3, labels=False)
    out["settle_by_volrel_tercile"] = S2.groupby("vrq").apply(summ)
    out["settle_highvol_by_year"] = S[S.vq == 2].groupby("year").apply(summ)
    out["settle_by_trend7_sign"] = S.groupby("trend7_vs").apply(summ)
    # book falls
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            dd.append(pd.DataFrame({"win": w, "coin": coin, "day": df["day"].values, "b": df["book_return"].values, "c": df["coin_return"].values}))
    D = pd.concat(dd)
    P = D.groupby(["win", "day"]).agg(b=("b", "mean"), c=("c", "mean")).reset_index()
    P["wn"] = P["win"].str[1:].astype(int)
    P = P.sort_values(["wn", "day"]).dropna()
    eq = (1 + P["b"]).cumprod(); dd_ = eq / eq.cummax() - 1
    P["dd"] = dd_.values
    out["book_by_window"] = P.groupby("wn").agg(book_bps=("b", lambda v: 1e4*v.mean()), coin_bps=("c", lambda v: 1e4*v.mean()), min_dd=("dd", "min"))
    return out
