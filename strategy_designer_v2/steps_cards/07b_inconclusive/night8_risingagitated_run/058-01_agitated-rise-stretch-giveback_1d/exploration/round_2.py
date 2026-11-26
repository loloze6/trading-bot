def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    hs = [3, 5, 10, 20]
    drift = {}
    for c in bars:
        for h in hs:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            sma = cl.rolling(20).mean()
            dist = cl / sma - 1
            dr = cl.pct_change()
            vol20 = dr.rolling(20).std()
            zdist = dist / (vol20 * np.sqrt(20))
            ret60 = cl / cl.shift(60) - 1
            inprof = (df["regime"] == "unknown").values
            fc = df["forecast"].values
            for h in hs:
                for i in range(0, len(cl) - h, h):
                    if np.isnan(dist.iloc[i]):
                        continue
                    r = cl.iloc[i + h] / cl.iloc[i] - 1
                    rows.append(dict(coin=c, win=w, h=h, dist=dist.iloc[i], zd=zdist.iloc[i],
                                     prof=inprof[i], fc=fc[i], ex=r - drift[(c, h)],
                                     rising=ret60.iloc[i] > 0.10))
    R = pd.DataFrame(rows)
    out = {}
    def summ(d):
        m = d["ex"].mean(); s = d["ex"].std()
        return pd.Series(dict(n=len(d), mean_ex=m, t=m / (s / np.sqrt(len(d))) if len(d) > 2 else np.nan))
    # test's own forecast cases
    S = R[R.prof & (R.fc < 0)].copy()
    S["afc"] = -S["fc"]
    res = []
    for h in hs:
        d = S[S.h == h]
        if len(d) < 10: continue
        s = stats.linregress(d["afc"], d["ex"])
        res.append(dict(h=h, n=len(d), slope=s.slope, t_slope=s.slope / s.stderr, mean_ex=d.ex.mean()))
    out["test_forecast_by_h"] = pd.DataFrame(res).set_index("h")
    S5 = S[S.h == 5].copy()
    S5["q"] = pd.qcut(S5["afc"], 4, labels=False, duplicates="drop")
    out["test_fc_quartile_h5"] = S5.groupby("q").apply(summ)
    # top quintile of raw distance vs rest, in profile, by h
    res = []
    for h in hs:
        d = R[R.prof & (R.dist > 0) & (R.h == h)]
        if len(d) < 15: continue
        thr = d["dist"].quantile(0.8)
        top = d[d.dist >= thr].ex; rest = d[d.dist < thr].ex
        tt = stats.ttest_ind(top, rest, equal_var=False)
        res.append(dict(h=h, n_top=len(top), top=top.mean(), rest=rest.mean(), welch_t=tt.statistic))
    out["top20_vs_rest_inprof"] = pd.DataFrame(res).set_index("h")
    # vol-scaled distance quintiles, in profile h5 and h10
    for h in [5, 10]:
        d = R[R.prof & (R.dist > 0) & (R.h == h)].copy()
        d["q"] = pd.qcut(d["zd"], 5, labels=False)
        out[f"zdist_quint_h{h}_in"] = d.groupby("q").apply(lambda x: pd.concat([summ(x), pd.Series(dict(zd=x.zd.mean()))]))
    # rising calm (rising, not in profile) comparison
    d = R[(~R.prof) & R.rising & (R.dist > 0) & (R.h == 5)].copy()
    d["q"] = pd.qcut(d["dist"], 5, labels=False)
    out["rising_calm_h5_quint"] = d.groupby("q").apply(summ)
    return out
