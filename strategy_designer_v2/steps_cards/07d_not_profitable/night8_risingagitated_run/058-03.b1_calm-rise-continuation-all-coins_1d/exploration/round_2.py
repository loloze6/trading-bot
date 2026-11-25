def explore(data):
    import numpy as np, pandas as pd
    out = {}
    wn = lambda w: int(w[1:])
    feats = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            v30 = r1.rolling(30).std()
            vpct = v30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            f = pd.DataFrame({
                "coin": c, "window": w, "ts": b["timestamp"],
                "pos": b["postRebalance_current_allocation"].fillna(0),
                "fc": b["forecast"].fillna(0),
                "dist": cl / cl.rolling(20).mean() - 1,
                "ret60": cl / cl.shift(60) - 1,
                "ret20": cl / cl.shift(20) - 1,
                "vpct": vpct,
                "vr": r1.rolling(10).std() / r1.rolling(60).std(),
                "nxt": cl.shift(-1) / cl - 1,
                "fwd5": cl.shift(-5) / cl - 1,
                "fwd10": cl.shift(-10) / cl - 1,
                "grid": (np.arange(len(b)) % 5 == 0),
                "grid10": (np.arange(len(b)) % 10 == 0),
                "regime": b["regime"],
            })
            f["gain"] = f["pos"] * f["nxt"]
            f["day"] = pd.to_datetime(f["ts"]).dt.floor("D")
            f["cum_from_entry"] = np.nan
            # running return since entry of current held stretch
            held = f["pos"] > 0
            grp = (held != held.shift()).cumsum()
            f["run"] = f.groupby(grp)["nxt"].transform(lambda x: (1 + x).cumprod().shift().fillna(1) - 1)
            f.loc[~held, "run"] = np.nan
            f["inprof"] = f["regime"] == "unknown"
            feats.append(f)
    F = pd.concat(feats, ignore_index=True)
    drift5 = F[F.grid].groupby("coin")["fwd5"].mean()
    drift10 = F[F.grid10].groupby("coin")["fwd10"].mean()
    F["ex5"] = F["fwd5"] - F["coin"].map(drift5)
    F["ex10"] = F["fwd10"] - F["coin"].map(drift10)
    H = F[F.pos > 0]
    # held bars: losing days by profile state
    out["held_gain_by_inprof"] = H.groupby("inprof")["gain"].agg(["size", "mean", "sum"])
    def tab(df, col, bins, val):
        df = df.dropna(subset=[col, val])
        g = df.groupby(pd.cut(df[col], bins), observed=True)[val]
        return pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size())), "neg_sum": g.apply(lambda x: x[x < 0].sum()), "sum": g.sum()})
    out["held_gain_by_ret60"] = tab(H, "ret60", [-1, 0.1, 0.3, 0.6, 1.0, 20], "gain")
    out["held_gain_by_vpct"] = tab(H, "vpct", [0, 0.25, 0.5, 0.75, 1.0], "gain")
    out["held_gain_by_run"] = tab(H, "run", [-1, -0.1, -0.05, 0, 0.05, 0.15, 10], "gain")
    out["held_gain_by_dist_fine"] = tab(H, "dist", [-1, 0, 0.05, 0.1, 0.15, 0.25, 5], "gain")
    # grid: signal cases in profile, graded by ret60; and profile without signal
    G = F[F.grid & F.ex5.notna()]
    sig = G[(G.fc > 0) & G.inprof]
    nos = G[(G.fc == 0) & G.inprof]
    out["sig_ex5_by_ret60"] = tab(sig, "ret60", [0.1, 0.3, 0.6, 20], "ex5")
    out["nosig_inprof_ex5_by_ret60"] = tab(nos, "ret60", [0.1, 0.3, 0.6, 20], "ex5")
    out["sig_ex5_by_dist"] = tab(sig, "dist", [0, 0.05, 0.1, 0.15, 0.25, 5], "ex5")
    G10 = F[F.grid10 & F.ex10.notna()]
    s10 = G10[(G10.fc > 0) & G10.inprof]
    out["sig_ex10_by_dist"] = tab(s10, "dist", [0, 0.05, 0.1, 0.2, 5], "ex10")
    # bars just after profile ends while held
    out["held_outprof_by_dist"] = tab(H[~H.inprof], "dist", [-1, 0, 0.05, 0.15, 5], "gain")
    # deepest fall w11: what held
    W11 = H[H.window == "w11"]
    out["w11_held"] = W11.groupby("coin")[["gain", "dist", "ret60", "vpct"]].agg(["size", "mean"] if False else "mean").assign(n=W11.groupby("coin").size(), sumgain=W11.groupby("coin")["gain"].sum())
    W12 = H[H.window == "w12"]
    out["w12_held"] = W12.groupby("coin")[["gain", "dist", "ret60", "vpct"]].mean().assign(n=W12.groupby("coin").size(), sumgain=W12.groupby("coin")["gain"].sum())
    return out
