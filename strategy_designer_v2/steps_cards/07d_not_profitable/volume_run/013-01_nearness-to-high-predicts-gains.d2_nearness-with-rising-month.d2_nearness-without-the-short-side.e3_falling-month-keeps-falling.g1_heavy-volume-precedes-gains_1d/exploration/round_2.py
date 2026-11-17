def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["ret3"] = b["close"].shift(-3)/b["close"]-1
            b["today"] = b["close"].pct_change()
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["win"] = w
            b["vr"] = b["volume"]/b["volume"].rolling(30, min_periods=30).mean()
            b["r30"] = b["close"]/b["close"].shift(30)-1
            b["idx"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["cm1"] = B.groupby("coin")["ret1"].transform("mean")
    G = B[B.idx % 3 == 0].dropna(subset=["ret3", "vr", "today", "r30"]).copy()
    G["ex"] = G["ret3"] - G.groupby("coin")["ret3"].transform("mean")
    G["vq"] = pd.qcut(G.vr, 5, labels=False)
    def tt(x):
        x = x.dropna()
        return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    out["ex3 by vq, down day"] = G[G.today < 0].groupby("vq")["ex"].apply(tt).unstack()
    out["ex3 by vq, up day"] = G[G.today > 0].groupby("vq")["ex"].apply(tt).unstack()
    G["sz"] = -G.today * G.vr  # graded: heavy volume on a falling day
    G["szq"] = pd.qcut(G.sz, 5, labels=False)
    out["ex3 by quintile of (-today x vr)"] = G.groupby("szq")["ex"].apply(tt).unstack()
    s = stats.linregress(G.sz, G.ex)
    out["slope ex3 on -today*vr"] = pd.Series({"slope": s.slope, "t": s.slope/s.stderr, "n": len(G)})
    hv = G[G.vq == 4]
    out["top vq: ex3 by down-day x 30d trend"] = hv.groupby([hv.today < 0, hv.r30 > 0])["ex"].apply(tt).unstack()
    out["top vq down day by year"] = G[(G.vq == 4) & (G.today < 0)].groupby("year")["ex"].apply(tt).unstack()
    # book gain split by long vs short positions
    B["gain"] = B.pos*B.ret1
    B["side"] = np.where(B.pos > 0.01, "long", np.where(B.pos < -0.01, "short", "flat"))
    out["gain by side"] = B.groupby("side").agg(gain_sum_share=("gain", "sum"), mean_gain=("gain", "mean"), coin_next=("ret1", "mean"), pos=("pos", "mean"), n=("gain", "size"))
    return out
