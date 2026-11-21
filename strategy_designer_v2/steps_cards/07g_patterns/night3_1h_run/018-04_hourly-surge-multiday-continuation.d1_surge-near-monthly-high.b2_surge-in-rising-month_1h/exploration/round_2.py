def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    allrows = []
    for off in (0, 120):
        for coin, ws in bars.items():
            for w, df in ws.items():
                c = df["close"].astype(float).reset_index(drop=True)
                n = len(c)
                ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
                r168 = c / c.shift(168) - 1
                r720 = c / c.shift(720) - 1
                hi720 = c.rolling(720, min_periods=360).max()
                hi1440 = c.rolling(1440, min_periods=720).max()
                near = c / hi720 - 1
                near60 = c / hi1440 - 1
                vol = c.pct_change().rolling(720, min_periods=360).std() * np.sqrt(24)
                f240 = c.shift(-240) / c - 1
                f120 = c.shift(-120) / c - 1
                for i in range(off, n, 240):
                    allrows.append(dict(off=off, coin=coin, w=w, near=near[i], near60=near60[i],
                                        nearv=near[i] / vol[i] if vol[i] > 0 else np.nan,
                                        r168=r168[i], r720=r720[i], f240=f240[i], f120=f120[i],
                                        year=ts[i].year))
    g = pd.DataFrame(allrows)
    g0 = g[g.off == 0]
    drift = g0.groupby("coin")["f240"].mean(); drift120 = g0.groupby("coin")["f120"].mean()
    g["ex"] = g["f240"] - g["coin"].map(drift)
    g["ex120"] = g["f120"] - g["coin"].map(drift120)
    def summ(gr, col="ex"):
        def f(s):
            s = s.dropna()
            return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
        return gr[col].apply(f).unstack()
    h = g.dropna(subset=["near", "ex", "r168"]).copy()
    for col in ["near", "nearv", "near60", "r168"]:
        h[col + "_q"] = h.groupby(["off", "coin"])[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["near_q_by_offset"] = summ(h.groupby(["off", "near_q"]))
    out["nearv_q_by_offset"] = summ(h.groupby(["off", "nearv_q"]))
    out["near60_q_off0"] = summ(h[h.off == 0].groupby("near60_q"))
    out["r168_q_by_offset"] = summ(h.groupby(["off", "r168_q"]))
    out["near_q_ex120_off0"] = summ(h[h.off == 0].groupby("near_q"), "ex120")
    h0 = h[h.off == 0]
    top = h0[h0.near_q == 4]
    out["near_top_by_coin"] = summ(top.groupby("coin"))
    top["half"] = (top.year >= 2022).astype(int)
    out["near_top_by_half"] = summ(top.groupby("half"))
    out["near_top_by_30dsign"] = summ(top.assign(up=(top.r720 > 0).astype(int)).groupby("up"))
    # grading: correlation near (rank within coin) with ex
    rows = []
    for coin, x in h0.groupby("coin"):
        x = x.dropna(subset=["near", "ex"])
        rho, p = stats.spearmanr(x["near"], x["ex"])
        rows.append(dict(coin=coin, rho=rho, p=p, n=len(x)))
    out["spearman_near_ex_by_coin"] = pd.DataFrame(rows)
    # partial: near top vs r168 top cross
    out["near_x_r168_top"] = summ(h0.assign(nt=(h0.near_q == 4).astype(int), rt=(h0.r168_q == 4).astype(int)).groupby(["nt", "rt"]))
    return out
