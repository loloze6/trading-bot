import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    H = [1, 3, 6, 12, 24, 48, 72]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon from non-overlapping grids
        drift = {}
        for h in H:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.append(c[idx + h] / c[idx] - 1)
            drift[h] = np.nanmean(np.concatenate(vals))
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            hr = ts.dt.hour.values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(r1).rolling(20).std().values
            r2 = np.r_[np.nan, np.nan, c[2:] / c[:-2] - 1]
            z = r2 / (vol * np.sqrt(2))
            fee = (df["total_portfolio_value"] - df["postRebalance_total_value"]).values / df["total_portfolio_value"].values
            for hh in [23, 11, 5, 17]:
                pos = np.where(hr == hh)[0]
                for p in pos:
                    if not np.isfinite(z[p]) or z[p] == 0: continue
                    d = {"coin": coin, "win": w, "hour": hh, "z": z[p], "vol": vol[p],
                         "year": ts.iloc[p].year}
                    s = -np.sign(z[p])
                    for h in H:
                        if p + h < len(c):
                            d[f"x{h}"] = s * (c[p + h] / c[p] - 1 - drift[h])
                            d[f"t{h}"] = s * (c[p + h] / c[p] - 1)
                    rows.append(d)
    R = pd.DataFrame(rows)
    S = R[R.hour == 23].copy()
    def summ(g):
        o = {"n": len(g)}
        for h in H:
            v = g[f"x{h}"].dropna()
            o[f"x{h}_bps"] = 1e4 * v.mean()
        o["t24"] = stats.ttest_1samp(g["x24"].dropna(), 0).statistic
        o["tot24_bps"] = 1e4 * g["t24"].dropna().mean()
        return pd.Series(o)
    out["by_hour_placebo"] = R.groupby("hour").apply(summ)
    S["az"] = S["z"].abs()
    S["zq"] = pd.qcut(S["az"], 5, labels=False)
    out["settle_by_absz_quintile"] = S.groupby("zq").apply(summ)
    S["vq"] = S.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    out["settle_by_vol_tercile"] = S.groupby("vq").apply(summ)
    out["settle_by_coin"] = S.groupby("coin").apply(summ)
    out["settle_by_year"] = S.groupby("year").apply(summ)
    S["dir"] = np.where(S["z"] < 0, "after_fall_long", "after_rise_short")
    out["settle_by_dir"] = S.groupby("dir").apply(summ)
    # book
    brows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            a = df["postRebalance_current_allocation"].values
            fee = ((df["total_portfolio_value"] - df["postRebalance_total_value"]) / df["total_portfolio_value"]).values
            brows.append({"coin": coin, "mean_abs_alloc": np.nanmean(np.abs(a)),
                          "turnover_per_day": 24 * np.nanmean(np.abs(np.diff(a))),
                          "fee_bps_per_day": 1e4 * 24 * np.nanmean(fee)})
    B = pd.DataFrame(brows)
    out["book_by_coin"] = B.groupby("coin").mean()
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            dd.append(pd.DataFrame({"win": w, "coin": coin, "b": df["book_return"].values, "c": df["coin_return"].values}))
    D = pd.concat(dd)
    out["days_by_coin"] = D.groupby("coin").agg(book_mean_bps=("b", lambda v: 1e4*v.mean()), coin_mean_bps=("c", lambda v: 1e4*v.mean()))
    return out
