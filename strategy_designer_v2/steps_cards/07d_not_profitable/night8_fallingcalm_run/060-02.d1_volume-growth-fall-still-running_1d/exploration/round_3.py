def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    R = []
    col = "debug_info.components.vol_growth.post_pipeline_value"
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["gain"] = b["alloc"] * b["ret1"]
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret5p"] = b["close"] / b["close"].shift(5) - 1
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            b["fwd5"] = b["close"].shift(-5) / b["close"] - 1
            b["fc"] = b[col] if col in b.columns else np.nan
            b["active"] = (b["forecast"] != 0) & b["forecast"].notna()
            b["coin"] = c; b["w"] = w
            b["pos0"] = np.arange(len(b))
            R.append(b)
    A = pd.concat(R, ignore_index=True)
    drift = A[A.pos0 % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift)
    A["side"] = np.sign(A["alloc"]).map({1: "long", -1: "short", 0: "flat"})
    # w14 worst episode
    W = A[A.w == "w14"].copy()
    W["day"] = pd.to_datetime(W["timestamp"]).dt.floor("D")
    bd = W.groupby("day")["gain"].mean().fillna(0)
    v = (1 + bd).cumprod()
    dd = v / v.cummax() - 1
    t = dd.idxmin(); s = v.loc[:t].idxmax()
    E = W[(W.day > s) & (W.day <= t)]
    out["w14_ep_by_coin_side"] = E.groupby(["coin", "side"]).agg(n=("gain", "size"), gain=("gain", "sum"),
        fcst=("forecast", "mean"), ret20=("ret20", "mean"), ret5p=("ret5p", "mean"), ret60=("ret60", "mean"), alloc=("alloc", "mean"))
    out["w14_ep_days"] = float(len(bd.loc[s:t]))
    # grid on signal cases
    G = A[(A.pos0 % 5 == 0) & A.active & A.ex5.notna()].copy()
    G["sd"] = np.where(G.forecast > 0, "long", "short")
    G["dirx"] = np.sign(G.forecast) * G.ex5
    def agg(x):
        n = len(x)
        return pd.Series({"n": n, "mean_dirx": x.dirx.mean(), "t": x.dirx.mean() / (x.dirx.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "sd_dirx": x.dirx.std(), "worst": x.dirx.min()})
    G["r5q"] = pd.qcut(G["ret5p"], 4, labels=["r5_q1crash", "r5_q2", "r5_q3", "r5_q4up"])
    G["r20q"] = pd.qcut(G["ret20"], 3, labels=["r20_deep", "r20_mid", "r20_shallow"])
    G["fq"] = pd.qcut(G.forecast.abs(), 3, labels=["weak", "mid", "strong"])
    out["grid_side_r5q"] = G.groupby(["sd", "r5q"]).apply(agg)
    out["grid_side_r20q"] = G.groupby(["sd", "r20q"]).apply(agg)
    out["grid_side_fq"] = G.groupby(["sd", "fq"]).apply(agg)
    out["grid_by_window_side"] = G.groupby(["w", "sd"])["dirx"].mean().unstack()
    # condition alone: all falling-profile grid bars (ret60<-0.1, ret20<0), by ret5p bin, ex5 (long direction)
    F = A[(A.pos0 % 5 == 0) & (A.ret60 < -0.1) & (A.ret20 < 0) & A.ex5.notna()].copy()
    qs = G.ret5p.quantile([.25, .5, .75]).values
    F["r5q"] = pd.cut(F.ret5p, [-9, qs[0], qs[1], qs[2], 9], labels=["r5_q1crash", "r5_q2", "r5_q3", "r5_q4up"])
    out["falling_all_ex5_by_r5"] = F.groupby("r5q")["ex5"].agg(["count", "mean"])
    # position-day gain by alloc size and side
    P = A[A.side != "flat"].dropna(subset=["gain"]).copy()
    P["aq"] = pd.qcut(P.alloc.abs(), 3, labels=["small", "mid", "large"])
    out["gain_by_alloc_side"] = P.groupby(["aq", "side"])["gain"].agg(["count", "mean", "std", "min"])
    P["r5q"] = pd.cut(P.ret5p, [-9, qs[0], qs[1], qs[2], 9], labels=["r5_q1crash", "r5_q2", "r5_q3", "r5_q4up"])
    out["posday_gain_by_r5_side"] = P.groupby(["r5q", "side"])["gain"].agg(["count", "mean", "std", "sum", "min"])
    return out
