def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    R = []
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
            b["v5ratio"] = b["volume"].rolling(5).mean() / b["volume"].shift(5).rolling(30).mean()
            b["fc"] = b["debug_info.components.vol_growth.post_pipeline_value"]
            b["coin"] = c; b["w"] = w
            b["pos0"] = np.arange(len(b))
            R.append(b)
    A = pd.concat(R, ignore_index=True)
    drift = A[A.pos0 % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift)
    A["side"] = np.sign(A["alloc"]).map({1: "long", -1: "short", 0: "flat"})
    # worst episode w14: daily book gain by coin and side, last 20 days before trough
    W = A[A.w == "w14"].copy()
    W["day"] = pd.to_datetime(W["timestamp"]).dt.floor("D")
    bd = W.groupby("day")["gain"].mean()
    v = (1 + bd.fillna(0)).cumprod()
    dd = v / v.cummax() - 1
    t = dd.idxmin()
    s = v.loc[:t].idxmax()
    E = W[(W.day > s) & (W.day <= t)]
    out["w14_ep_by_coin_side"] = E.groupby(["coin", "side"]).agg(n=("gain", "size"), gain=("gain", "sum"),
        fc=("fc", "mean"), ret20=("ret20", "mean"), ret5p=("ret5p", "mean"), ret60=("ret60", "mean"), alloc=("alloc", "mean"))
    # at entry of that episode: state of the long holdings
    # grid analysis: signal cases (fc not null) on 5-bar grid
    G = A[(A.pos0 % 5 == 0) & A.fc.notna() & A.ex5.notna()].copy()
    G["sd"] = np.where(G.fc > 0, "long", "short")
    G["dirx"] = np.sign(G.fc) * G.ex5
    G["r5q"] = pd.qcut(G["ret5p"], 4, labels=["r5_q1crash", "r5_q2", "r5_q3", "r5_q4up"])
    G["r20q"] = pd.qcut(G["ret20"], 4, labels=["r20_q1deep", "q2", "q3", "q4shallow"])
    def agg(x):
        return pd.Series({"n": len(x), "mean_dirx": x.dirx.mean(), "t": x.dirx.mean() / (x.dirx.std() / np.sqrt(len(x))), "mean_ex5": x.ex5.mean()})
    out["grid_side_r5q"] = G.groupby(["sd", "r5q"]).apply(agg)
    out["grid_side_r20q"] = G.groupby(["sd", "r20q"]).apply(agg)
    G["fq"] = pd.qcut(G.fc.abs(), 3, labels=["weak", "mid", "strong"])
    out["grid_side_fq"] = G.groupby(["sd", "fq"]).apply(agg)
    # condition alone: bars in falling profile (ret60<-0.1) and ret20<0 without signal? signal exists on all such; instead
    # compare ex5 on all grid bars by ret5p quartile (no signal sign) for falling profile
    F = A[(A.pos0 % 5 == 0) & (A.ret60 < -0.1) & A.ex5.notna()].copy()
    F["r5q"] = pd.cut(F["ret5p"], [-9, G.ret5p.quantile(.25), G.ret5p.quantile(.5), G.ret5p.quantile(.75), 9])
    out["falling_all_ex5_by_r5"] = F.groupby("r5q")["ex5"].agg(["count", "mean"])
    # per-window directional gain on grid
    out["grid_by_window_side"] = G.groupby(["w", "sd"])["dirx"].agg(["count", "mean"]).unstack()
    # position days: allocation size distribution and loss by |alloc|
    P = A[A.side != "flat"].dropna(subset=["gain"]).copy()
    P["aq"] = pd.qcut(P.alloc.abs(), 3, labels=["small", "mid", "large"])
    out["gain_by_alloc_side"] = P.groupby(["aq", "side"])["gain"].agg(["count", "mean", "std", "min"])
    return out
