def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            lc = np.log(b["close"].astype(float))
            b["r1"] = lc.diff()
            b["f12"] = lc.shift(-12) - lc
            b["raw"] = b["debug_info.components.rsi_high.last_history_value"].astype(float)
            b["rsi"] = 50 - b["raw"]
            b["vol24"] = b["r1"].rolling(24).std()
            b["vol24rank"] = b["vol24"].rolling(24*30, min_periods=24*5).rank(pct=True)
            b["p24"] = lc - lc.shift(24)
            b["pos"] = b["postRebalance_current_allocation"].astype(float)
            v = b["postRebalance_total_value"].astype(float)
            b["bookr"] = np.log(v).shift(-1) - np.log(v)
            b["grid"] = (np.arange(len(b)) % 12 == 0)
            b["coin"] = coin; b["win"] = w
            # drift-demeaned forward return
            b["xf12"] = b["f12"] - b["f12"].mean()
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    out["raw_describe"] = d["raw"].describe()
    out["rsi_quantiles"] = d["rsi"].quantile([0.01,0.05,0.1,0.5,0.9,0.95,0.99])
    g = d[d["grid"]].copy()
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean_bp": 1e4*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # RSI decile per coin (non-overlap grid), excess over window drift
    g["rsid"] = g.groupby("coin")["rsi"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["xf12_by_rsi_decile_grid"] = g.groupby("rsid")["xf12"].apply(summ).unstack()
    out["xf12_rsi_top_decile_by_coin"] = g[g["rsid"]==9].groupby("coin")["xf12"].apply(summ).unstack()
    out["xf12_rsi_bot_decile_by_coin"] = g[g["rsid"]==0].groupby("coin")["xf12"].apply(summ).unstack()
    # top-minus-bottom decile by window
    tb = g[g["rsid"].isin([0,9])].groupby(["win","rsid"])["xf12"].mean().unstack()*1e4
    out["top_bot_decile_by_window_bp"] = tb
    # vol rank tercile, excess over window drift, grid, per window
    g["vb"] = pd.cut(g["vol24rank"], [0,1/3,2/3,1.0001], labels=["lo","mid","hi"])
    out["xf12_by_vol_grid"] = g.groupby("vb")["xf12"].apply(summ).unstack()
    out["xf12_vol_by_window_bp"] = g.groupby(["win","vb"])["xf12"].mean().unstack()*1e4
    out["xf12_vol_by_coin"] = g.groupby(["coin","vb"])["xf12"].apply(summ).unstack()
    # vol x RSI top decile
    out["xf12_rsitop_by_vol"] = g[g["rsid"]>=8].groupby("vb")["xf12"].apply(summ).unstack()
    # prior 24h move tercile -> forward
    g["pb"] = g.groupby("coin")["p24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["xf12_by_p24_quintile"] = g.groupby("pb")["xf12"].apply(summ).unstack()
    # book: pnl by position size bucket
    d["pb_"] = pd.cut(d["pos"].abs(), [-0.001,0.0001,0.25,0.5,0.75,1.01,100])
    out["book_by_pos"] = d.groupby("pb_")["bookr"].agg(["size","sum","mean"])
    out["pos_describe"] = d["pos"].describe()
    return out
