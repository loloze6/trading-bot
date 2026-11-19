def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    out = {}
    rows = []
    for H in [24, 72]:
        for coin, wins in bars.items():
            recs = []
            for w, df in wins.items():
                c = df["close"].values; f = df["forecast"].values; reg = df["regime"].values
                ts = pd.to_datetime(df["timestamp"]); n = len(df)
                lr = np.abs(df["close"].pct_change().values)
                for p in range(0, n - H, H):
                    recs.append((w, ts.iloc[p].year, f[p], reg[p], c[p + H] / c[p] - 1))
            r = pd.DataFrame(recs, columns=["w", "year", "f", "reg", "ret"])
            m = r["ret"].mean()
            r["ex"] = np.sign(r["f"]) * (r["ret"] - m)
            r["coin"] = coin; r["H"] = H
            rows.append(r)
    R = pd.concat(rows)
    sel = R[(R.reg == "mean_reversion") & (R.f.abs() >= 10)].copy()
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "sd": x.std(ddof=1),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    s24 = sel[sel.H == 24]
    out["24_by_coin"] = s24.groupby("coin").apply(summ)
    out["24_by_year"] = s24.groupby("year").apply(summ)
    s72 = sel[sel.H == 72]
    # share of positive cases and median
    out["72_pos_share_median"] = pd.Series({"pos_share": (s72.ex > 0).mean(), "median": s72.ex.median(),
                                            "mean": s72.ex.mean(), "sd": s72.ex.std()})
    # required n for t=2 at the observed mean/sd
    out["72_n_needed_t2"] = float((2 * s72.ex.std() / s72.ex.mean()) ** 2)
    # 72h excluding 2018
    out["72_excl_2018"] = summ(s72[s72.year != 2018])
    out["regime_share_bars"] = pd.Series({k: np.mean([ (df.regime == "mean_reversion").mean() for df in v.values()]) for k, v in bars.items()})
    return out
