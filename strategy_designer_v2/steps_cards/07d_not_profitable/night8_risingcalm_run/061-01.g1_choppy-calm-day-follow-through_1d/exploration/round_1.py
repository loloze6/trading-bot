def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w; tr.append(t)
    tr = pd.concat(tr, ignore_index=True)
    tr["absf"] = tr["entry_forecast"].abs()
    tr["fb"] = pd.cut(tr["absf"], [0, 5, 10, 15, 20.01])
    tr["days"] = tr["duration_minutes"] / 1440
    g = tr.groupby(["side", "fb"], observed=True)
    out["trades_by_side_fbucket"] = g.agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        days=("days", "mean")).round(3)
    out["trades_by_side"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        win=("net_profit_loss_percent", lambda x: (x > 0).mean()), days=("days", "median")).round(3)
    out["trade_duration_q"] = tr["days"].describe().round(2)

    # bar-level: z, profile, forward returns
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r = cl.pct_change()
            sd = r.rolling(30).std()
            z = r / sd
            inprof = (b["regime"] == "unknown")
            alloc = b["postRebalance_current_allocation"].astype(float)
            r1 = cl.shift(-1) / cl - 1
            df = pd.DataFrame({"coin": c, "win": w, "pos": np.arange(len(b)), "z": z,
                               "f": b["forecast"].astype(float), "inprof": inprof,
                               "alloc": alloc, "gain": alloc * r1,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            for h in [1, 2, 3, 5, 10]:
                df[f"fr{h}"] = cl.shift(-h) / cl - 1
            rows.append(df)
    B = pd.concat(rows, ignore_index=True)
    # coin mean 5-bar return over grid
    def grid(h):
        G = B[B["pos"] % h == 0].copy()
        mu = G.groupby("coin")[f"fr{h}"].mean()
        G["ex"] = G[f"fr{h}"] - G["coin"].map(mu)
        G["sx"] = np.sign(G["z"]) * G["ex"]
        return G
    res = []
    for h in [1, 2, 3, 5, 10]:
        G = grid(h).dropna(subset=["z", "ex"])
        G["zb"] = pd.cut(G["z"].abs(), [0, 0.5, 1, 1.5, 2, 100])
        for (ip, zb), s in G.groupby(["inprof", "zb"], observed=True):
            res.append({"h": h, "inprof": ip, "zb": str(zb), "n": len(s),
                        "signed_ex_mean": s["sx"].mean(),
                        "t": s["sx"].mean() / (s["sx"].std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    R = pd.DataFrame(res)
    out["signed_ex_by_h_prof_zbucket"] = R[R["h"].isin([5, 10])].round(4)
    out["signed_ex_h1_3"] = R[R["h"].isin([1, 3])].round(4)
    # by side of z in profile, h5
    G = grid(5).dropna(subset=["z", "ex"])
    G["side"] = np.where(G["z"] > 0, "up", "down")
    G["big"] = G["z"].abs() > 1
    out["h5_prof_side_big"] = G.groupby(["inprof", "side", "big"]).agg(
        n=("sx", "size"), sx=("sx", "mean"), raw=("fr5", "mean")).round(4)
    # book: gain by alloc side, by year in profile
    B["aside"] = np.sign(B["alloc"]).map({1: "long", -1: "short", 0: "flat"})
    out["gain_by_alloc_side"] = B.groupby("aside").agg(n=("gain", "size"), mean=("gain", "mean"),
                                                         sum=("gain", "sum")).round(5)
    out["gain_by_year_side"] = B[B["aside"] != "flat"].groupby(["year", "aside"])["gain"].agg(["size", "mean", "sum"]).round(4)
    # forecast vs z correlation, and position-holding: z on entry bars
    s = B[B["inprof"]].dropna(subset=["z"])
    out["corr_f_z_inprof"] = float(np.corrcoef(s["f"], s["z"])[0, 1])
    out["share_alloc_sign_eq_z"] = float((np.sign(s["alloc"]) == np.sign(s["z"]))[s["alloc"] != 0].mean())
    out["inprof_share"] = float(B["inprof"].mean())
    return out
