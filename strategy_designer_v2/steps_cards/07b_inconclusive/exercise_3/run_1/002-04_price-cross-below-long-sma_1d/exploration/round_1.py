def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            allr.append(df["close"].pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            a = df["postRebalance_current_allocation"].values
            f = df["forecast"].values
            d = df.get("debug_info.components.below_ma.last_history_value")
            d = d.values if d is not None else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for h in [1, 5, 10, 20, 40]:
                for i in range(0, n - h, h):
                    past20 = c[i] / c[i-20] - 1 if i >= 20 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, yr=yr[i], a=a[i], f=f[i], d=d[i],
                                     r=c[i+h]/c[i]-1, ex=c[i+h]/c[i]-1-h*mu, past20=past20))
    R = pd.DataFrame(rows)
    R["g"] = R["a"] * R["ex"]
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    act = R[R["a"] != 0]
    out["by_h_gain_all"] = R.groupby("h")["g"].apply(tt).unstack()
    out["by_h_active_excess_ret"] = act.groupby("h")["ex"].apply(tt).unstack()
    out["by_h_flat_excess_ret"] = R[R["a"]==0].groupby("h")["ex"].apply(tt).unstack()
    A = act[act.h == 10].copy()
    out["h10_by_coin_excess"] = A.groupby("coin")["ex"].apply(tt).unstack()
    out["h10_by_year_excess"] = A.groupby("yr")["ex"].apply(tt).unstack()
    A["fq"] = pd.qcut(A["f"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["h10_by_forecast_q"] = A.groupby("fq")["ex"].apply(tt).unstack()
    A["dq"] = pd.qcut(A["d"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["h10_by_rawdist_q"] = A.groupby("dq")["ex"].apply(tt).unstack()
    A["pq"] = pd.qcut(A["past20"], 3, labels=["fell_most", "mid", "fell_least_or_rose"])
    out["h10_by_past20"] = A.groupby("pq")["ex"].apply(tt).unstack()
    A40 = act[act.h == 40].copy()
    A40["dq"] = pd.qcut(A40["d"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["h40_by_rawdist_q"] = A40.groupby("dq")["ex"].apply(tt).unstack()
    A40["pq"] = pd.qcut(A40["past20"], 3, labels=["fell_most", "mid", "fell_least_or_rose"])
    out["h40_by_past20"] = A40.groupby("pq")["ex"].apply(tt).unstack()
    out["h10_raw_ret_active"] = tt(A["r"]).to_frame().T
    out["h10_sd_excess_active"] = A["ex"].std()
    return out
