def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb)
            width = (sa - sb).abs() / c * 100
            dist = (c - top) / c * 100
            above = (c > top).astype(float).where(top.notna())
            since = np.full(n, np.nan); cnt = np.nan
            for i in range(n):
                a = above.iloc[i]
                if np.isnan(a): cnt = np.nan
                elif a == 1: cnt = 1 if (np.isnan(cnt) or cnt == 0) else cnt + 1
                else: cnt = 0
                since[i] = cnt
            ret20 = c / c.shift(20) - 1
            fwd = c.shift(-H) / c - 1
            fwd10 = c.shift(-10) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            half = "h1" if int(w[1:]) <= 12 else "h2"
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, half=half, fwd=fwd.iloc[i], fwd10=fwd10.iloc[i], fc=b["forecast"].iloc[i],
                    since=since[i], width=width.iloc[i], dist=dist.iloc[i], ret20=ret20.iloc[i], above=above.iloc[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    out = {}
    ab = d[(d["above"] == 1)].dropna(subset=["since", "width", "dist", "ret20", "ex"]).copy()
    ab["lsince"] = np.log(ab["since"]); ab["lwidth"] = np.log1p(ab["width"])
    X = np.column_stack([np.ones(len(ab)), ab["lsince"], ab["lwidth"], ab["dist"], ab["ret20"]])
    y = ab["ex"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["multi_reg_above"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "lsince", "lwidth", "dist", "ret20"]).round(4)
    out["n_above"] = len(ab)
    out["corr_lsince_lwidth"] = round(float(np.corrcoef(ab["lsince"], ab["lwidth"])[0, 1]), 3)
    # 10-day horizon, own grid
    ab["ex10"] = ab["fwd10"] - d.groupby("coin")["fwd10"].transform("mean").loc[ab.index]
    x10 = ab.dropna(subset=["ex10"])
    s = stats.linregress(x10["lsince"], x10["ex10"])
    out["since_10d_overlapping_5grid"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(x10)}).round(4)
    # size: fresh third vs all-above total move
    q = pd.qcut(ab["since"].rank(method="first"), 3, labels=False)
    g = ab.groupby(q).agg(ex=("ex", "mean"), fwd=("fwd", "mean"), n=("ex", "count"), smin=("since", "min"), smax=("since", "max"))
    out["since_terciles"] = g.round(4)
    return out
