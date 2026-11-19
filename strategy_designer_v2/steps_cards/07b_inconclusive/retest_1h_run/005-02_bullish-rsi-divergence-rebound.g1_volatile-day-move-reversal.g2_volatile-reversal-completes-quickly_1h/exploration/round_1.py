def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for H in [24, 48, 72, 120, 168]:
        for coin, wins in bars.items():
            recs = []
            for w, df in wins.items():
                c = df["close"].values
                f = df["forecast"].values
                reg = df["regime"].values
                ts = pd.to_datetime(df["timestamp"])
                n = len(df)
                for p in range(0, n - H, H):
                    recs.append((w, ts.iloc[p].year, f[p], reg[p], c[p + H] / c[p] - 1))
            r = pd.DataFrame(recs, columns=["w", "year", "f", "reg", "ret"])
            m = r["ret"].mean()
            r["ex"] = np.sign(r["f"]) * (r["ret"] - m)
            r["coin"] = coin
            r["H"] = H
            rows.append(r)
    R = pd.concat(rows)
    sel = R[(R.reg == "mean_reversion") & (R.f.abs() >= 10)]
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["by_horizon"] = sel.groupby("H").apply(summ)
    s72 = sel[sel.H == 72].copy()
    out["72_by_coin"] = s72.groupby("coin").apply(summ)
    s72["side"] = np.where(s72.f > 0, "long_after_fall", "short_after_rise")
    out["72_by_side"] = s72.groupby("side").apply(summ)
    out["by_horizon_side"] = sel.assign(side=np.where(sel.f > 0, "long", "short")).groupby(["H", "side"]).apply(summ)
    out["72_by_year"] = s72.groupby("year").apply(summ)
    all72 = R[(R.H == 72) & (R.reg == "mean_reversion") & (R.f != 0)].copy()
    all72["bucket"] = pd.cut(all72.f.abs(), [0, 2.5, 5, 10, 19.99, 20])
    out["72_by_absf_bucket"] = all72.groupby("bucket").apply(summ)
    out["72_raw_ret_by_side"] = s72.groupby("side")["ret"].agg(["mean", "std", "count"])
    return out
