def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 5
    allb = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy(); b["coin"] = c; b["win"] = w
            b["pos"] = b["postRebalance_current_allocation"]
            b["fwd1"] = b["close"].shift(-1) / b["close"] - 1
            b["fwd"] = b["close"].shift(-H) / b["close"] - 1
            b["ma50"] = b["close"] / b["close"].rolling(50, min_periods=30).mean() - 1
            lo = b["low"].values; n = len(b); cl = b["close"].values
            piv = np.full(n, np.nan)
            for i in range(2, n - 2):
                if lo[i] <= lo[i-2:i+3].min():
                    piv[i] = lo[i]
            sa = np.zeros(n); dist = np.full(n, np.nan)
            for t in range(n):
                s = max(0, t - 90)
                p = piv[s:max(s, t-1)]; p = p[~np.isnan(p)]
                if len(p):
                    sa[t] = np.sum((p > cl[t]) & (p <= cl[t] * 1.03))
                    ab = p[p >= cl[t]]
                    if len(ab): dist[t] = ab.min() / cl[t] - 1
            b["sa"] = sa; b["dist"] = dist
            b["grid"] = (np.arange(n) % H == 0)
            allb.append(b)
    B = pd.concat(allb, ignore_index=True)
    mus = B[B.grid].groupby("coin")["fwd"].mean()
    B["unus"] = B["fwd"] - B["coin"].map(mus)
    B["raw"] = B["debug_info.components.support_above.last_history_value"]
    out["raw_nonzero_share"] = float((B["raw"] > 0).mean())
    B["dq"] = pd.cut(B["dist"], [-1e-9, 0.01, 0.03, 0.07, 0.15, 10])
    out["pos_and_dist_by_dq"] = B.groupby("dq").agg(n=("pos", "size"), mean_pos=("pos", "mean"),
        gain=("fwd1", lambda x: (B.loc[x.index, "pos"] * x).mean()))
    out["share_no_level_above"] = float(B["dist"].isna().mean())
    G = B[B.grid & B.fwd.notna()].copy()
    G["sac"] = G["sa"].clip(upper=3)
    out["sa_by_coin"] = G.pivot_table(index="coin", columns="sac", values="unus", aggfunc="mean")
    G["yr"] = pd.to_datetime(G["timestamp"]).dt.year
    out["sa_by_year"] = G.pivot_table(index="yr", columns="sac", values="unus", aggfunc="mean")
    G["trend"] = np.where(G["ma50"] < 0, "below_ma50", "above_ma50")
    out["sa_x_trend"] = G.groupby(["trend", "sac"]).agg(unus=("unus", "mean"), total=("fwd", "mean"), n=("fwd", "size"),
        t=("unus", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # book's position when sa>=2 vs sa==0
    B["sac"] = B["sa"].clip(upper=3)
    out["book_pos_by_sa"] = B.groupby("sac").agg(mean_pos=("pos", "mean"), share_short=("pos", lambda x: (x < 0).mean()), n=("pos", "size"),
        gain=("fwd1", lambda x: (B.loc[x.index, "pos"] * x).mean()))
    return out
