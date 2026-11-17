def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    comp = "debug_info.components.rsi_below_age.last_history_value"
    recs = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["fwd1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["fwd1"]
            b["run"] = -b[comp]
            b["ret30"] = b["close"] / b["close"].shift(30) - 1
            b["ret14"] = b["close"] / b["close"].shift(14) - 1
            b["fwd7"] = b["close"].shift(-7) / b["close"] - 1
            dlt = b["close"].diff()
            up = dlt.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
            dn = (-dlt.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
            b["rsi"] = 100 - 100 / (1 + up / dn)
            b["rsich7"] = b["rsi"] - b["rsi"].shift(7)
            b["coin"] = coin; b["w"] = w; b["pos"] = np.arange(len(b))
            recs.append(b[["coin","w","pos","fwd1","fwd7","gain","run","ret30","ret14","rsi","rsich7","forecast","postRebalance_current_allocation"]])
    B = pd.concat(recs)
    mean7 = B[B.pos % 7 == 0].groupby("coin")["fwd7"].mean()
    B["ex7"] = B["fwd7"] - B["coin"].map(mean7)
    act = B[B.forecast < 0].copy()
    act["long"] = act["run"] > 30
    out["gain_long_vs_short_runs"] = act.groupby("long")["gain"].agg(["size","mean","sum","std"])
    a, c = act.loc[act.long,"gain"].dropna(), act.loc[~act.long,"gain"].dropna()
    out["t_long_minus_rest"] = stats.ttest_ind(a, c, equal_var=False).statistic
    out["gain_sum_excl_w2_by_long"] = act[act.w != "w2"].groupby("long")["gain"].sum()
    g = act[(act.pos % 7 == 0)].dropna(subset=["ex7"])
    g["rsich_q"] = pd.qcut(g["rsich7"], 4)
    out["ex7_by_rsi_change7"] = g.groupby("rsich_q")["ex7"].agg(["size","mean","std"])
    g["r14q"] = pd.qcut(g["ret14"], 4)
    out["ex7_by_ret14"] = g.groupby("r14q")["ex7"].agg(["size","mean","std"])
    # within long runs: rsi change
    gl = g[g.run > 14].copy()
    gl["rsich_q"] = pd.qcut(gl["rsich7"], 3)
    out["ex7_run>14_by_rsich7"] = gl.groupby("rsich_q")["ex7"].agg(["size","mean","std"])
    # daily gain by rsi change sign among active bars
    act["rsi_rising"] = act["rsich7"] > 0
    out["gain_by_rsi_rising"] = act.groupby("rsi_rising")["gain"].agg(["size","mean","sum"])
    out["gain_by_rsi_rising_excl_w2"] = act[act.w!="w2"].groupby("rsi_rising")["gain"].agg(["size","mean","sum"])
    out["w2_alloc_run"] = act[act.w=="w2"][["run","postRebalance_current_allocation"]].mean()
    return out
