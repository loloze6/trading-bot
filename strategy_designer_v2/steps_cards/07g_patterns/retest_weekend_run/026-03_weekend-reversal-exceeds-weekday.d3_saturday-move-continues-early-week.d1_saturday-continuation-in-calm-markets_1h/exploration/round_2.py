def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = pd.Timedelta(hours=1)
    rows = []; hrs = []
    for coin in bars:
        g48 = []; g24 = []
        for w, df in bars[coin].items():
            c = df["close"].values
            i = np.arange(0, len(c) - 48, 48); g48 += list(c[i + 48] / c[i] - 1)
            i = np.arange(0, len(c) - 24, 24); g24 += list(c[i + 24] / c[i] - 1)
        d48 = np.mean(g48); d24 = np.mean(g24); u48 = np.std(g48, ddof=1)
        vols = []; prep = {}
        for w, df in bars[coin].items():
            d = df[["timestamp", "close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            r = d["close"].pct_change()
            d["vol"] = r.rolling(720, min_periods=500).std()
            d["t_end"] = d["timestamp"] + H
            hrs.append(pd.DataFrame({"coin": coin, "w": w, "year": d["timestamp"].dt.year,
                                     "hr": d["timestamp"].dt.hour, "r": r}))
            vols.append(d["vol"]); prep[w] = d.set_index("t_end")
        vq = pd.concat(vols).dropna().quantile([1/3, 2/3]).values
        for w, d in prep.items():
            px = d["close"]; vol = d["vol"]
            for T in px.index[(px.index.hour == 0) & (px.index.weekday == 0)]:
                ts = T - pd.Timedelta(days=1); tsa = T - pd.Timedelta(days=2)
                t1 = T + pd.Timedelta(hours=24); t2 = T + pd.Timedelta(hours=48)
                if not all(x in px.index for x in (ts, tsa, t2, t1)): continue
                v = vol.get(T, np.nan)
                if not np.isfinite(v) or v <= 0: continue
                sun = px[T] / px[ts] - 1; sat = px[ts] / px[tsa] - 1
                rows.append({"coin": coin, "w": w, "year": T.year,
                             "zsun": sun / (v * np.sqrt(24)), "zsat": sat / (v * np.sqrt(24)),
                             "vt": int(np.searchsorted(vq, v)),
                             "f48": (px[t2] / px[T] - 1 - d48) / u48,
                             "f48raw": px[t2] / px[T] - 1 - d48,
                             "f24": px[t1] / px[T] - 1 - d24})
    D = pd.DataFrame(rows)
    def summ(s, col="f48raw", z="zsun"):
        if len(s) < 30: return pd.Series({"n": len(s)})
        dr = -np.sign(s[z]) * s[col]
        sl = stats.linregress(s[z], s[col])
        return pd.Series({"n": len(s), "rev_mean%": 100 * dr.mean(),
                          "rev_t": dr.mean() / (dr.std(ddof=1) / np.sqrt(len(s))),
                          "slope_t": sl.slope / sl.stderr,
                          "strength": (-np.sign(s[z]) * s["f48"]).mean()})
    out = {}
    out["sun_all"] = summ(D).to_frame().T
    out["sun_by_coin"] = D.groupby("coin").apply(summ)
    out["sun_by_year"] = D.groupby("year").apply(summ)
    out["sun_by_voltercile"] = D.groupby("vt").apply(summ)
    D["q"] = pd.qcut(D["zsun"].abs(), 4, labels=False)
    out["sun_by_absz_quartile"] = D.groupby("q").apply(summ)
    out["sun_by_absz_quartile_f24"] = D.groupby("q").apply(lambda s: summ(s, "f24"))
    X = np.column_stack([np.ones(len(D)), D["zsun"], D["zsat"]])
    b, *_ = np.linalg.lstsq(X, D["f48raw"].values, rcond=None)
    res = D["f48raw"].values - X @ b
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=3)
    out["joint_reg_f48"] = pd.DataFrame({"coef": b, "t": b / np.sqrt(np.diag(cov))},
                                        index=["const", "zsun", "zsat"])
    out["corr_sun_sat"] = float(np.corrcoef(D.zsun, D.zsat)[0, 1])
    Hh = pd.concat(hrs).dropna()
    Hh["eve"] = Hh["hr"].isin([21, 22])
    def ht(s):
        a = s[s.eve]["r"]; b2 = s[~s.eve]["r"]
        return pd.Series({"eve_bp": 1e4 * a.mean(), "rest_bp": 1e4 * b2.mean(),
                          "t": stats.ttest_ind(a, b2, equal_var=False).statistic, "n": len(a)})
    out["hr21_22_by_coin"] = Hh.groupby("coin").apply(ht)
    out["hr21_22_by_year"] = Hh.groupby("year").apply(ht)
    return out
