def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["loc"] = (c - b["low"]) / rng
            b["ret5"] = c / c.shift(5) - 1
            b["ret20"] = c / c.shift(20) - 1
            b["rng"] = rng / c
            b["ret1"] = c / c.shift(1) - 1
            b["fwd5"] = c.shift(-5) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["fwd1"]
            held = b["pos"].abs() > 1e-9
            entry = held & ~held.shift(1, fill_value=False)
            tid = entry.cumsum().where(held)
            b["tid"] = tid
            b["age"] = b.groupby("tid").cumcount().where(held)
            b["cumgain"] = b.groupby("tid")["gain"].cumsum().where(held) - b["gain"].where(held)
            b["coin"] = coin; b["w"] = w
            b["entry"] = entry
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    H = B[B.pos.abs() > 1e-9].copy()
    out["held gain by age"] = H.groupby(H["age"].clip(upper=7)).agg(n=("gain","size"), gain=("gain","mean"), pos=("pos","mean"))
    H["cgq"] = pd.cut(H["cumgain"], [-1, -0.02, -0.005, 0.005, 0.02, 1])
    out["held gain by trade gain so far"] = H.groupby("cgq").agg(n=("gain","size"), gain=("gain","mean"))
    H["r1b"] = pd.cut(H["ret1"], [-1, -0.05, 0, 0.05, 0.10, 2])
    out["held gain by today's ret1"] = H.groupby("r1b").agg(n=("gain","size"), gain=("gain","mean"))
    out["held gain sum by regime x coin"] = H.groupby(["coin","regime"])["gain"].sum().unstack()
    # worst held bars: what was the situation
    W = H.nsmallest(15, "gain")[["coin","w","regime","age","pos","ret1","ret5","ret20","loc","rng","fwd1"]].reset_index(drop=True)
    out["worst 15 held bars"] = W
    # Entries: trade outcome by entry characteristics
    E = B[B.entry].copy()
    tr = H.groupby(["coin","w","tid"])["gain"].sum().rename("tgain").reset_index()
    E = E.merge(tr, on=["coin","w","tid"])
    E["r5q"] = pd.qcut(E["ret5"], 3, labels=False)
    out["trade gain by entry ret5 tercile"] = E.groupby("r5q").agg(n=("tgain","size"), tgain=("tgain","mean"), r5=("ret5","mean"), fwd5=("fwd5","mean"))
    E["r20q"] = pd.qcut(E["ret20"], 3, labels=False)
    out["trade gain by entry ret20 tercile"] = E.groupby("r20q").agg(n=("tgain","size"), tgain=("tgain","mean"), r20=("ret20","mean"), fwd5=("fwd5","mean"))
    E["rq"] = pd.qcut(E["rng"], 3, labels=False)
    out["trade gain by entry range tercile"] = E.groupby("rq").agg(n=("tgain","size"), tgain=("tgain","mean"), rng=("rng","mean"), fwd5=("fwd5","mean"))
    # all-bar situation (overlapping, informative) in mean_reversion regime by ret5 bins, fwd5 short
    M = B[B.regime=="mean_reversion"].copy()
    M["r5b"] = pd.cut(M["ret5"], [-1, -0.15, -0.08, -0.04, 0])
    out["mr bars short fwd5 by ret5 bin"] = M.groupby("r5b").agg(n=("fwd5","size"), short=("fwd5", lambda x: -x.mean()))
    # condition alone: in profile (mr+unknown) with deep ret5 but loc<=0.5 (all bars)
    P = B[B.regime.isin(["mean_reversion","unknown"])].copy()
    P["deep"] = P["ret5"] < -0.08
    P["locU"] = P["loc"] > 0.5
    out["profile bars short fwd5 deep x locU"] = P.groupby(["deep","locU"]).agg(n=("fwd5","size"), short=("fwd5", lambda x: -x.mean()))
    # exposure
    out["mean |pos| when held"] = float(H.pos.abs().mean())
    return out
