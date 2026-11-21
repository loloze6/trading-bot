def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drifts = {}
    H = 40
    for coin, ws in bars.items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drifts[coin] = (np.mean(rets), np.std(rets))
    rows = []
    wlen = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            wlen.append(len(b))
            c = b["close"]; hi = b["high"]; lo = b["low"]
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            thick = (top - bot) / c
            sa_up = sa - sa.shift(5)
            ma = c.rolling(40).mean()
            r60 = c.pct_change(60); r20 = c.pct_change(20)
            vol = c.pct_change().rolling(30).std()
            cv = c.values; n = len(cv)
            tr = (b["regime"] == "trending").values
            fc = b["forecast"].fillna(0).values
            seen = set()
            for i in np.where(tr)[0]:
                if i + H >= n: continue
                cell = i // H
                if cell in seen: continue
                seen.add(cell)
                d, s = drifts[coin]
                rows.append(dict(coin=coin, w=w, i=i, fc=fc[i], r60=r60[i], r20=r20[i],
                                 thick=thick[i], saup=sa_up[i] / cv[i] if not np.isnan(sa_up[i]) else np.nan,
                                 dist_ma=cv[i] / ma[i] - 1, vol=vol[i],
                                 year=pd.to_datetime(b["timestamp"].iloc[i]).year,
                                 unus=cv[i + H] / cv[i] - 1 - d, strength=(cv[i + H] / cv[i] - 1 - d) / s,
                                 lunus=np.log(cv[i + H] / cv[i]) - np.log(1 + d)))
    df = pd.DataFrame(rows)
    out = {"window_len": pd.Series(wlen).describe()}
    top = df.sort_values("unus", ascending=False).head(8)
    out["top8_cases"] = top[["coin", "w", "year", "fc", "r60", "unus"]].reset_index(drop=True)
    def tests(g, x):
        m = g[x].notna()
        gg = g[m]
        if len(gg) < 8: return dict(var=x, n=len(gg))
        r = stats.linregress(gg[x], gg.unus)
        rl = stats.linregress(gg[x], gg.lunus)
        sp = stats.spearmanr(gg[x], gg.unus)
        return dict(var=x, n=len(gg), t_ols=r.slope / r.stderr, t_ols_log=rl.slope / rl.stderr, spearman=sp.correlation, sp_p=sp.pvalue)
    res = []
    for sub, g in [("all", df), ("fc>0", df[df.fc > 0])]:
        for x in ["fc", "r60", "r20", "thick", "saup", "dist_ma", "vol"]:
            d = tests(g, x); d["sub"] = sub; res.append(d)
    out["graded_tests"] = pd.DataFrame(res)
    out["log_mean_all"] = float(df.lunus.mean())
    out["log_t_all"] = float(stats.ttest_1samp(df.lunus, 0).statistic)
    p = df[df.fc > 0]
    out["log_mean_pos"] = float(p.lunus.mean()); out["log_t_pos"] = float(stats.ttest_1samp(p.lunus, 0).statistic)
    out["n_thick_avail"] = int(df.thick.notna().sum())
    t = df[df.thick.notna()].copy()
    if len(t) >= 12:
        t["tq"] = pd.qcut(t.thick, 3, labels=False, duplicates="drop")
        out["by_thick_tercile"] = t.groupby("tq").agg(n=("unus", "size"), thick=("thick", "mean"), mean=("unus", "mean"), med=("unus", "median"), lmean=("lunus", "mean"), frac_pos=("unus", lambda x: (x > 0).mean()))
    df["side_r60"] = np.where(df.r60 > 0, "r60>0", "r60<=0")
    out["by_r60_sign"] = df.groupby("side_r60").agg(n=("unus", "size"), mean=("unus", "mean"), med=("unus", "median"), lmean=("lunus", "mean"), frac_pos=("unus", lambda x: (x > 0).mean()))
    df["era"] = np.where(df.year <= 2021, "<=2021", ">=2022")
    out["by_era_pos"] = df[df.fc > 0].groupby("era").agg(n=("unus", "size"), mean=("unus", "mean"), med=("unus", "median"), lmean=("lunus", "mean"))
    return out
