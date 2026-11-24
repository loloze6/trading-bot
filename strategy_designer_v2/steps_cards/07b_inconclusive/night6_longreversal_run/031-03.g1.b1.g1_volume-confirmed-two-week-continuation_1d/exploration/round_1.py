def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def tday(df, col):
        g = df.groupby("timestamp")[col].sum()
        if len(g) < 3: return np.nan
        return g.mean() / (g.std(ddof=1) / np.sqrt(len(g)))
    rows = []
    for H in (7, 14, 28, 42):
        for coin, wins in bars.items():
            # coin mean H return over all windows
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr += list(c[idx + H] / c[idx] - 1)
            mu = np.mean(allr) if allr else np.nan
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values; v = b["volume"].values
                idx = np.arange(0, len(c) - H, H)
                for i in idx:
                    f = b["forecast"].iat[i]
                    if f == 0 or pd.isna(f): continue
                    r = c[i + H] / c[i] - 1
                    r14 = c[i] / c[i - 14] - 1 if i >= 14 else np.nan
                    vr = (v[i-13:i+1].mean() / v[i-29:i+1].mean()) if i >= 29 else np.nan
                    rows.append(dict(H=H, coin=coin, win=w, ts=b["timestamp"].iat[i],
                                     year=pd.Timestamp(b["timestamp"].iat[i]).year,
                                     regime=b["regime"].iat[i], f=f, r=r, mu=mu,
                                     dev=np.sign(f) * (r - mu), r14=r14, vr=vr,
                                     # continuation measure: signed by own 14d return
                                     cont=np.sign(r14) * (r - mu) if not pd.isna(r14) else np.nan))
    df = pd.DataFrame(rows).rename(columns={"ts": "timestamp"})
    def summ(d, col="dev"):
        d = d.dropna(subset=[col])
        return pd.Series({"n": len(d), "mean": d[col].mean(), "t_day": tday(d, col)})
    out["by_horizon"] = df.groupby("H").apply(summ)
    d14 = df[df.H == 14].copy()
    out["by_regime"] = d14.groupby("regime").apply(summ)
    d14["side"] = np.where(d14.f > 0, "long", "short")
    out["by_regime_side"] = d14.groupby(["regime", "side"]).apply(summ)
    d14["fq"] = pd.qcut(d14.f.abs(), 5, labels=False)
    out["by_abs_forecast_q"] = d14.groupby(["regime", "fq"]).apply(summ)
    out["by_year"] = d14.groupby("year").apply(summ)
    out["by_coin"] = d14.groupby("coin").apply(summ)
    # continuation of 14d return regardless of volume, by regime, horizons
    out["cont_by_H_regime"] = df.groupby(["H", "regime"]).apply(lambda d: summ(d, "cont"))
    d14["vrq"] = pd.qcut(d14.vr, 5, labels=False)
    out["cont_by_volratio_q"] = d14.groupby("vrq").apply(lambda d: pd.concat([summ(d, "cont"), pd.Series({"vr_mean": d.vr.mean()})]))
    d14["r14q"] = pd.qcut(d14.r14.abs(), 5, labels=False)
    out["cont_by_absr14_q"] = d14.groupby("r14q").apply(lambda d: summ(d, "cont"))
    return out
