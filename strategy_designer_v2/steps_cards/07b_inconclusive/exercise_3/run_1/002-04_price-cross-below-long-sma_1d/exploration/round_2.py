def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        mu = pd.concat([df["close"].pct_change().dropna() for df in ws.values()]).mean()
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; a = df["postRebalance_current_allocation"].values
            d = df["debug_info.components.below_ma.last_history_value"].values.astype(float)
            sma = c / (1 + d / 100.0) if np.nanmax(np.abs(d)) > 2 else c / (1 + d)
            n = len(df); h = 10
            for i in range(0, n - h, h):
                sl = sma[i] / sma[i-20] - 1 if i >= 20 else np.nan
                p60 = c[i] / c[i-60] - 1 if i >= 60 else np.nan
                rows.append(dict(coin=coin, a=a[i], d=d[i], ex=c[i+h]/c[i]-1-h*mu, sl=sl, p60=p60))
    R = pd.DataFrame(rows); A = R[R.a != 0].copy()
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    out = {}
    out["d_scale"] = pd.Series({"d_median_active": A.d.median(), "d_min": A.d.min()})
    A["slope_sign"] = np.where(A.sl < 0, "sma_falling", "sma_rising")
    out["by_sma_slope_sign"] = A.dropna(subset=["sl"]).groupby("slope_sign")["ex"].apply(tt).unstack()
    B = A.dropna(subset=["sl"]).copy()
    B["slq"] = pd.qcut(B.sl, 4, labels=["falling_most", "q2", "q3", "rising_most"])
    out["by_sma_slope_q"] = B.groupby("slq")["ex"].apply(tt).unstack()
    out["by_slope_q_coin_mean"] = B.groupby(["slq", "coin"])["ex"].mean().unstack()
    C = A.dropna(subset=["p60"]).copy()
    C["pq"] = pd.qcut(C.p60, 3, labels=["fell_most", "mid", "rose"])
    out["by_past60"] = C.groupby("pq")["ex"].apply(tt).unstack()
    # book decomposition on days
    br, mk, tm = [], [], []
    for coin, ws in days.items():
        allc = pd.concat([x["coin_return"] for x in ws.values()]).mean()
        for w, dd in ws.items():
            b = bars[coin][w].copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = dd.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.merge(pos.rename("pos").reset_index(), on="day", how="left")
            br.append(dd["book_return"]); mk.append(dd["pos"] * allc)
    out["book_mean"] = pd.concat(br).mean()
    out["book_market_part"] = pd.concat(mk).mean()
    return out
