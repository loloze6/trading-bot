def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(df); h = 72
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, regime=df["regime"].iat[i], fc=df["forecast"].iat[i],
                                 fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    mr = d[d.regime == "mean_reversion"].dropna(subset=["fc", "ex"]).copy()
    med = mr["fc"].median()
    mr["top"] = mr["fc"] > med
    pw = []
    for w, g in mr.groupby("w"):
        a = g[g.top]["ex"]; b = g[~g.top]["ex"]
        if len(a) > 3 and len(b) > 3:
            pw.append(dict(w=w, diff=a.mean() - b.mean(), n=len(g)))
    pw = pd.DataFrame(pw)
    out = {}
    out["per_window_diff_summary"] = pd.Series(dict(windows=len(pw), share_pos=(pw["diff"] > 0).mean(),
        mean=pw["diff"].mean(), t=pw["diff"].mean() / pw["diff"].std() * np.sqrt(len(pw))))
    a = mr[mr.top]["ex"]; b = mr[~mr.top]["ex"]
    diff = a.mean() - b.mean(); se = np.sqrt(a.var() / len(a) + b.var() / len(b))
    out["power"] = pd.Series(dict(diff=diff, se=se, t=diff / se, cases_now=len(mr),
                                  cases_needed_t2=len(mr) * (2 / (diff / se)) ** 2))
    # Spearman rank correlation of forecast with excess return
    rho, p = stats.spearmanr(mr["fc"], mr["ex"])
    out["spearman"] = pd.Series(dict(rho=rho, p=p, n=len(mr)))
    # book decomposition
    br = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.copy()
            df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            r = df["close"].pct_change().shift(-1)
            pos = df["postRebalance_current_allocation"]
            br.append(pd.DataFrame(dict(coin=coin, pos=pos, r=r)))
    b2 = pd.concat(br).dropna()
    cm = b2.groupby("coin")["r"].transform("mean")
    out["bar_gain_decomp"] = pd.Series(dict(mean_gain=(b2.pos * b2.r).mean(), market_part=(b2.pos * cm).mean(),
                                            timing=(b2.pos * (b2.r - cm)).mean(), mean_pos=b2.pos.mean()))
    dd = pd.concat([days[c][w].assign(coin=c) for c in days for w in days[c]])
    out["daily"] = pd.Series(dict(book_mean=dd["book_return"].mean(), coin_mean=dd["coin_return"].mean()))
    return out
