def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 84
    bars = data["bars"]
    rows = []
    allgrid = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                g.append(c[i + H] / c[i] - 1)
        allgrid[coin] = (np.mean(g), np.std(g))
    col = "debug_info.components.bounce.last_history_value"
    for coin, wins in bars.items():
        mu, sd = allgrid[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(c)
            act = (df["regime"] == "mean_reversion").values
            bcol = df[col].values if col in df.columns else np.full(n, np.nan)
            seen = set()
            for t in np.where(act)[0]:
                cell = t // H
                if cell in seen: continue
                seen.add(cell)
                b = bcol[t]
                if not np.isfinite(b) and t >= 6: b = (c[t] / c[t - 6] - 1) * 100
                r84 = c[t + H] / c[t] - 1 if t + H < n else np.nan
                fall = c[t - 6] / c[t - 12] - 1 if t >= 12 else np.nan
                rng = (hi[t-11:t-5].max() - lo[t-11:t-5].min()) / c[t-12] if t >= 12 else np.nan
                yr = pd.Timestamp(df["timestamp"].iloc[t]).year
                rows.append(dict(coin=coin, win=w, year=yr, bounce=b, fall=fall, rng=rng,
                                 ex84=r84 - mu, sd=sd))
    d = pd.DataFrame(rows).dropna(subset=["bounce", "ex84"])
    def sl(g, y="ex84"):
        m = g[["bounce", y]].dropna()
        if len(m) < 8: return pd.Series(dict(n=len(m), slope=np.nan, t=np.nan, rho=np.nan, wins_t=np.nan))
        r = stats.linregress(m.bounce, m[y])
        ql, qh = m[y].quantile([0.02, 0.98])
        rw = stats.linregress(m.bounce, m[y].clip(ql, qh))
        return pd.Series(dict(n=len(m), slope=r.slope, t=r.slope / r.stderr,
                              rho=stats.spearmanr(m.bounce, m[y])[0], wins_t=rw.slope / rw.stderr))
    out = {}
    out["bounce units"] = d.bounce.describe()
    noz = d[d.coin != "ZECUSD"]
    out["all"] = sl(d)
    out["without ZEC"] = sl(noz)
    out["ZEC only"] = sl(d[d.coin == "ZECUSD"])
    out["without ZEC, by year"] = noz.groupby("year").apply(sl)
    out["ZEC by year"] = d[d.coin == "ZECUSD"].groupby("year").apply(sl)
    d["fq"] = pd.qcut(d.fall, 3, labels=False)
    out["by fall tercile (all)"] = d.groupby("fq").apply(sl)
    noz = d[d.coin != "ZECUSD"]
    out["by fall tercile, without ZEC"] = noz.groupby("fq").apply(sl)
    out["ZEC share by fall tercile"] = d.groupby("fq").apply(lambda g: (g.coin == "ZECUSD").mean())
    d["yrgrp"] = np.where(d.year >= 2024, "2024-25", "2018-23")
    out["by year group, without ZEC"] = d[d.coin != "ZECUSD"].groupby("yrgrp").apply(sl)
    d["rq"] = pd.qcut(d.rng, 3, labels=False)
    out["by stretch range tercile"] = d.groupby("rq").apply(sl)
    # top 10 ex84 contribution
    m = d.copy(); m["lev"] = (m.bounce - m.bounce.mean()) * (m.ex84 - m.ex84.mean())
    top = m.nlargest(10, "lev")
    out["top 10 leverage cases by coin"] = top.groupby("coin").size()
    out["slope without top 10 leverage"] = sl(m.drop(top.index))
    return out
