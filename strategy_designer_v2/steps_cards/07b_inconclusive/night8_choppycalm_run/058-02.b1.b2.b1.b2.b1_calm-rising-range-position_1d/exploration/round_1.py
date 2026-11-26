def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for h in [5, 10, 20]:
            # coin mean over all windows on grid h
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
                    per.append((w, i, r, f[i], rp[i], yr[i], str(df["timestamp"].iloc[i])[:10]))
            m = np.mean(allr) if allr else np.nan
            for (w, i, r, fc, rpv, y, d) in per:
                if fc != 0:
                    rows.append(dict(coin=coin, h=h, win=w, year=y, day=d, f=fc, rp=rpv,
                                     ex=r - m, tot=r, meas=fc / 10 * (r - m)))
    R = pd.DataFrame(rows)

    def tday(sub, col="meas"):
        s = sub.groupby("day")[col].sum()
        n = len(s)
        if n < 3:
            return pd.Series(dict(n_cases=len(sub), n_days=n, mean=np.nan, t=np.nan))
        return pd.Series(dict(n_cases=len(sub), n_days=n, mean=s.mean(),
                              t=s.mean() / (s.std(ddof=1) / np.sqrt(n))))

    out = {}
    out["by_horizon"] = R.groupby("h").apply(tday)
    R10 = R[R.h == 10].copy()
    R10["side"] = np.where(R10.f > 0, "long", "short")
    out["h10_by_side"] = R10.groupby("side").apply(tday)
    out["h10_by_side_signed_excess"] = R10.groupby("side").apply(lambda s: tday(s.assign(x=np.sign(s.f) * s.ex), "x"))
    R10["fbin"] = pd.cut(R10.f, [-21, -10, -5, 0, 5, 10, 21])
    out["h10_by_fbin_excess"] = R10.groupby("fbin").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_tot=("tot", "mean"))
    R10["rpbin"] = pd.cut(R10.rp, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["h10_by_rangepos_excess"] = R10.groupby("rpbin").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_tot=("tot", "mean"))
    out["h10_by_coin"] = R10.groupby("coin").apply(tday)
    out["h10_by_window"] = R10.groupby("win").apply(tday)
    out["h10_by_year"] = R10.groupby("year").apply(tday)
    for h in [5, 20]:
        Rh = R[R.h == h].copy()
        Rh["side"] = np.where(Rh.f > 0, "long", "short")
        out[f"h{h}_by_side"] = Rh.groupby("side").apply(tday)
    return out
