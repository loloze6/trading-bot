def explore(data):
    import numpy as np, pandas as pd
    res = {}
    # 1) book decomposition: drift vs timing
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; days.append(x)
    D = pd.concat(days)
    pos = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp")
            x = pd.DataFrame({"day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "alloc": b["postRebalance_current_allocation"].astype(float).shift(1)})
            x["coin"] = coin; x["w"] = w; pos.append(x)
    P = pd.concat(pos)
    D["day"] = pd.to_datetime(D["day"]).dt.floor("D")
    M = D.merge(P, on=["coin", "w", "day"], how="left")
    cm = M.groupby("coin")["coin_return"].transform("mean")
    M["from_drift"] = M["alloc"] * cm
    M["timing"] = M["alloc"] * (M["coin_return"] - cm)
    daily = M.groupby("day")[["book_return", "from_drift", "timing", "alloc"]].mean()
    t = lambda s: s.mean() / (s.std() / np.sqrt(s.notna().sum()))
    res["book_decomp"] = pd.DataFrame({"mean": daily.mean(), "t": [t(daily[c]) for c in daily.columns]}).round(6)
    res["alloc_share_short"] = float((M["alloc"] < 0).mean())
    # 2) graded move-size: 1-day return in vol units, next H days, H in 1,3,5
    out = []
    for H in [1, 3, 5]:
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.sort_values("timestamp").reset_index(drop=True)
                c = b["close"].astype(float).values
                ts = pd.to_datetime(b["timestamp"]).dt.floor("D").values
                r = pd.Series(c).pct_change()
                z = (r / r.rolling(30).std().shift(1)).values
                # streak-depth: cumulative return of current same-sign run, in vol units
                n = len(c)
                runret = np.full(n, np.nan)
                start = 0
                for i in range(1, n):
                    if i > 1 and np.sign(r[i]) != np.sign(r[i-1]):
                        start = i - 1
                    runret[i] = c[i] / c[start] - 1 if i > 0 else np.nan
                vs = r.rolling(30).std().shift(1).values
                rz = runret / (vs * np.sqrt(5))
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, day=ts[i], fwd=c[i+H]/c[i]-1, z=z[i], rz=rz[i]))
        d = pd.DataFrame(rows)
        d["u"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        d["s"] = d["u"] / d.groupby("coin")["fwd"].transform("std")
        for key in ["z", "rz"]:
            dd = d.dropna(subset=[key])
            dd = dd.assign(q=pd.qcut(dd[key].rank(method="first"), 5, labels=False))
            for q, sub in dd.groupby("q"):
                m = sub["u"].mean()
                dev = (sub["u"] - m).groupby(sub["day"]).sum()
                se = np.sqrt((dev**2).sum()) / len(sub)
                out.append(dict(H=H, key=key, q=q, n=len(sub), days=sub["day"].nunique(),
                                strength=round(sub["s"].mean(), 4), t=round(m/se, 2)))
            # slope of s on key, day-clustered-ish via spearman
            from scipy.stats import spearmanr
            rho, p = spearmanr(dd[key], dd["u"])
            out.append(dict(H=H, key=key, q="rho", n=len(dd), days=dd["day"].nunique(),
                            strength=round(rho, 4), t=round(p, 4)))
    res["graded_moves"] = pd.DataFrame(out)
    return res
