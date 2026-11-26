def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for h in [3, 5, 7, 10]:
            allr = []
            per = []
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                f = df["forecast"].fillna(0).values
                hi = df["high"].rolling(20).max().values
                lo = df["low"].rolling(20).min().values
                rp = (c - lo) / (hi - lo)
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                for i in range(0, len(df) - h, h):
                    r = c[i + h] / c[i] - 1
                    allr.append(r)
                    per.append((w, r, f[i], rp[i], yr[i], str(df["timestamp"].iloc[i])[:10]))
            m = np.mean(allr) if allr else np.nan
            for (w, r, fc, rpv, y, d) in per:
                if fc != 0:
                    rows.append(dict(coin=coin, h=h, win=w, year=y, day=d, f=fc, rp=rpv,
                                     ex=r - m, sx=np.sign(fc) * (r - m), meas=fc / 10 * (r - m)))
    R = pd.DataFrame(rows)

    def tday(sub, col="meas"):
        s = sub.groupby("day")[col].sum()
        n = len(s)
        if n < 3:
            return pd.Series(dict(n_cases=len(sub), n_days=n, mean=np.nan, t=np.nan))
        return pd.Series(dict(n_cases=len(sub), n_days=n, mean=s.mean(),
                              t=s.mean() / (s.std(ddof=1) / np.sqrt(n))))

    out = {}
    out["by_horizon_meas"] = R.groupby("h").apply(tday)
    out["by_horizon_signed_excess"] = R.groupby("h").apply(lambda s: tday(s, "sx"))
    R["side"] = np.where(R.f > 0, "long", "short")
    out["by_horizon_side"] = R.groupby(["h", "side"]).apply(tday)
    R["absf"] = pd.cut(R.f.abs(), [0, 10, 21])
    out["by_horizon_absf_signed_excess"] = R.groupby(["h", "absf"]).apply(lambda s: tday(s, "sx"))
    R5 = R[R.h == 5].copy()
    R5["rpbin"] = pd.cut(R5.rp, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["h5_by_rangepos_excess"] = R5.groupby("rpbin").agg(n=("ex", "size"), mean_ex=("ex", "mean"))
    out["h5_by_year"] = R5.groupby("year").apply(tday)
    out["h5_by_coin"] = R5.groupby("coin").apply(tday)
    return out
