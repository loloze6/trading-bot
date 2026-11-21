def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    comps = ["mom28","rev1","high90","vol30"]
    def grid(h):
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                n = len(df)
                idx = np.arange(0, n - h, h)
                if len(idx) == 0: continue
                r = c[idx + h] / c[idx] - 1
                d = pd.DataFrame({"coin": coin, "win": w, "r": r,
                                  "f": df["forecast"].values[idx],
                                  "year": pd.to_datetime(df["timestamp"].values[idx]).year})
                for k in comps:
                    col = f"debug_info.components.{k}.post_pipeline_value"
                    d[k] = df[col].values[idx] if col in df else np.nan
                rows.append(d)
        g = pd.concat(rows, ignore_index=True)
        g["ex"] = g["r"] - g.groupby("coin")["r"].transform("mean")
        g["p"] = g["f"] * g["ex"]
        return g
    def tstat(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # horizons
    hz = {}
    for h in [1, 3, 5, 10, 20]:
        g = grid(h)
        hz[h] = tstat(g["p"])
        if h == 5: g5 = g
    out["by_horizon"] = pd.DataFrame(hz).T
    g = g5
    out["by_coin"] = g.groupby("coin")["p"].apply(tstat).unstack()
    out["by_year"] = g.groupby("year")["p"].apply(tstat).unstack()
    out["by_window"] = g.groupby("win")["p"].apply(tstat).unstack()
    # components alone (in their known direction, post pipeline)
    cr = {}
    for k in comps:
        cr[k] = tstat(g[k] * g["ex"])
    out["components_5d"] = pd.DataFrame(cr).T
    # side
    g["side"] = np.where(g["f"] > 0, "long", np.where(g["f"] < 0, "short", "flat"))
    out["by_side_excess_ret"] = g.groupby("side")["ex"].apply(tstat).unstack()
    # forecast quintiles
    g["q"] = pd.qcut(g["f"].rank(method="first"), 5, labels=False)
    out["by_forecast_quintile"] = g.groupby("q").agg(f_mean=("f", "mean"), ex_mean=("ex", "mean"), n=("ex", "size"))
    # vol regime: coin's 30d vol component sign
    g["lowvol"] = np.where(g["vol30"] > 0, "lowvol", "highvol")
    out["by_vol_state"] = g.groupby("lowvol")["p"].apply(tstat).unstack()
    # market drift sign (coin's own 5d return excess big) - abs move bucket
    g["bigmove"] = pd.qcut(g["r"].abs().rank(method="first"), 3, labels=["small", "mid", "large"])
    out["by_abs_move"] = g.groupby("bigmove")["p"].apply(tstat).unstack()
    return out
