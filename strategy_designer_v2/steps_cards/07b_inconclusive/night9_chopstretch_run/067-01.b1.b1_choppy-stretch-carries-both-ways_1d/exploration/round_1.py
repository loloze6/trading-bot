def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [1, 3, 5, 10, 20]
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs) if rs else 0.0
            usual[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 2 else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            fc = df["forecast"].values
            raw = df.get("debug_info.components.stretch.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            ret = pd.Series(c).pct_change()
            vol20 = ret.rolling(20).std().values
            r20 = pd.Series(c).pct_change(20).values
            for h in H:
                for i in range(0, len(c) - h, h):
                    if fc[i] == 0 or np.isnan(fc[i]):
                        continue
                    fr = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ts=df["timestamp"].iloc[i],
                                     f=fc[i], raw=raw[i], fr=fr,
                                     ex=fr - drift[(coin, h)],
                                     strn=(fr - drift[(coin, h)]) * np.sign(fc[i]) / usual[(coin, h)],
                                     vol20=vol20[i], r20=r20[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows)
    out = {}
    def summ(g):
        s = g["ex"] * np.sign(g["f"])
        n = len(g)
        t = s.mean() / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        sl = stats.linregress(g["f"], g["ex"]) if n > 5 else None
        return pd.Series(dict(n=n, signed_ex_mean=s.mean(), t_signed=t,
                              strength=g["strn"].mean(),
                              long_ex=g.loc[g.f > 0, "ex"].mean(), short_ex=g.loc[g.f < 0, "ex"].mean(),
                              n_long=(g.f > 0).sum(), n_short=(g.f < 0).sum(),
                              slope_t=(sl.slope / sl.stderr) if sl is not None else np.nan))
    out["by_horizon"] = R.groupby("h").apply(summ)
    r5 = R[R.h == 5].copy()
    r10 = R[R.h == 10].copy()
    out["h5_by_coin"] = r5.groupby("coin").apply(summ)
    out["h5_by_year"] = r5.groupby("year").apply(summ)
    out["h5_by_window"] = r5.groupby("w").apply(summ)
    for name, rr in [("h5", r5), ("h10", r10)]:
        rr = rr.copy()
        rr["fq"] = pd.qcut(rr["f"].abs(), 4, labels=False, duplicates="drop")
        out[name + "_by_absforecast_q"] = rr.groupby("fq").apply(summ)
        rr["rq"] = pd.qcut(rr["raw"].abs(), 4, labels=False, duplicates="drop")
        out[name + "_by_absraw_q"] = rr.groupby("rq").apply(summ)
        rr["vq"] = rr.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
        out[name + "_by_vol_tercile"] = rr.groupby("vq").apply(summ)
        rr["side"] = np.where(rr.f > 0, "long", "short")
        out[name + "_by_side_absq"] = rr.groupby(["side", "fq"]).apply(summ)[["n", "signed_ex_mean", "t_signed"]]
    out["corr_f_raw"] = float(R[R.h == 5][["f", "raw"]].corr().iloc[0, 1])
    return out
