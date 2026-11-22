def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    hs = {"1d": 6, "3d": 18, "7d": 42, "14d": 84}
    col = "debug_info.components.panic.last_history_value"
    drift = {}
    for c in bars:
        for k, h in hs.items():
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, k)] = np.mean(rs)
    # clean grid: for each horizon, bars at positions 0,h,2h of each window; situation = raw component value
    res = {}
    out = []
    G = {}
    for k, h in hs.items():
        rows = []
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                v = df[col].values if col in df else np.full(len(df), np.nan)
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                fall = (pd.Series(cl) / pd.Series(cl).shift(6) - 1).values
                for t in range(0, len(cl) - h, h):
                    rows.append(dict(coin=c, year=yr[t], v=v[t], fall=fall[t],
                                     ex=cl[t + h] / cl[t] - 1 - drift[(c, k)]))
        G[k] = pd.DataFrame(rows)
    def st(x):
        x = x.dropna()
        return pd.Series({"mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "n": len(x)})
    tab = []
    for k in hs:
        g = G[k]
        a = g[(g["v"] > 0) & g["v"].notna()].copy()
        z = g[(g["v"] == 0)]
        a["q"] = pd.qcut(a["v"].rank(method="first"), 5, labels=False)
        for q, s in a.groupby("q"):
            r = st(s["ex"]); r["h"] = k; r["grp"] = "pos_q" + str(q); tab.append(r)
        r = st(z["ex"]); r["h"] = k; r["grp"] = "zero(nofall)"; tab.append(r)
        r = st(a["ex"]); r["h"] = k; r["grp"] = "all_pos"; tab.append(r)
        if len(a) > 3:
            r = pd.Series({"mean": np.corrcoef(a["v"].rank(), a["ex"])[0, 1], "t": np.nan, "n": len(a), "h": k, "grp": "rankcorr_v_ex"}); tab.append(r)
        top = a[a["q"] >= 3]
        r = st(top[top["year"] != 2018]["ex"]); r["h"] = k; r["grp"] = "top2q_ex2018"; tab.append(r)
    res["grid_by_component_quintile"] = pd.DataFrame(tab)[["h", "grp", "mean", "t", "n"]]
    # top 2 quintiles at 14d and 3d by year
    for k in ["3d", "14d"]:
        g = G[k]; a = g[(g["v"] > 0) & g["v"].notna()].copy()
        a["q"] = pd.qcut(a["v"].rank(method="first"), 5, labels=False)
        res["top2q_by_year_" + k] = a[a["q"] >= 3].groupby("year")["ex"].apply(st).unstack()
        res["top2q_by_coin_" + k] = a[a["q"] >= 3].groupby("coin")["ex"].apply(st).unstack()
    return res
