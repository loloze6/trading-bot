def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r = cl.pct_change()
            sd = r.rolling(30).std()
            z = r / sd
            alloc = b["postRebalance_current_allocation"].astype(float)
            r1 = cl.shift(-1) / cl - 1
            df = pd.DataFrame({"coin": c, "win": w, "pos": np.arange(len(b)), "z": z,
                               "f": b["forecast"].astype(float), "inprof": (b["regime"] == "unknown"),
                               "alloc": alloc, "r1": r1, "gain": alloc * r1,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            df["fr5"] = cl.shift(-5) / cl - 1
            df["fr3"] = cl.shift(-3) / cl - 1
            # was the coin in profile at any of the last 5 bars (position carried)
            df["prof_recent"] = df["inprof"].astype(int).rolling(5, min_periods=1).max().astype(bool)
            rows.append(df)
    B = pd.concat(rows, ignore_index=True)
    B["aside"] = np.sign(B["alloc"]).map({1.0: "long", -1.0: "short", 0.0: "flat"})
    # book gain by in-profile bar or not, by side
    out["gain_by_inprof_side"] = B[B["aside"] != "flat"].groupby(["inprof", "aside"])["gain"].agg(["size", "mean", "sum"]).round(5)
    # position sign vs the sign of the last in-profile big day? -> position agreement with today's z, by |z|
    P = B[(B["aside"] != "flat")].dropna(subset=["z"]).copy()
    P["agree"] = np.sign(P["alloc"]) == np.sign(P["z"])
    P["zb"] = pd.cut(P["z"].abs(), [0, 0.5, 1, 2, 100])
    out["pos_agree_by_zbucket"] = P.groupby("zb", observed=True).agg(n=("agree", "size"), agree=("agree", "mean"), gain=("gain", "mean")).round(4)
    # grid h5, in profile: signed excess and raw by side and z buckets
    G = B[B["pos"] % 5 == 0].dropna(subset=["z", "fr5"]).copy()
    mu = G.groupby("coin")["fr5"].mean()
    G["ex"] = G["fr5"] - G["coin"].map(mu)
    G["zb"] = pd.cut(G["z"], [-100, -1.5, -0.75, 0, 0.75, 1.5, 100])
    out["h5_inprof_by_signed_z"] = G[G["inprof"]].groupby("zb", observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), raw=("fr5", "mean")).round(4)
    out["h5_outprof_by_signed_z"] = G[~G["inprof"]].groupby("zb", observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), raw=("fr5", "mean")).round(4)
    # all bars (overlap ok for descriptive) in profile: raw fr5 mean, z>0 slope on up days only
    A = B[B["inprof"]].dropna(subset=["z", "fr5"])
    up = A[A["z"] > 0]
    out["inprof_allbars_mean_fr5"] = float(A["fr5"].mean())
    out["inprof_up_corr_z_fr5"] = float(np.corrcoef(up["z"], up["fr5"])[0, 1])
    dn = A[A["z"] < 0]
    out["inprof_down_corr_z_fr5"] = float(np.corrcoef(dn["z"], dn["fr5"])[0, 1])
    # up days by window in profile (grid), z>0.75
    Gu = G[G["inprof"] & (G["z"] > 0.75)]
    out["inprof_up_by_window"] = Gu.groupby("win").agg(n=("ex", "size"), ex=("ex", "mean")).round(4)
    Gd = G[G["inprof"] & (G["z"] < -0.75)]
    out["inprof_down_by_window"] = Gd.groupby("win").agg(n=("ex", "size"), ex=("ex", "mean")).round(4)
    # simulate long-only, held 5 bars from each in-profile up day, size z (capped 2), daily mean gain, cost 0.19% per entry
    sims = {}
    for name, cond in [("long_up", lambda d: d["inprof"] & (d["z"] > 0)),
                       ("short_down", lambda d: d["inprof"] & (d["z"] < 0))]:
        gains = []
        for (c, w), d in B.groupby(["coin", "win"]):
            d = d.reset_index(drop=True)
            sig = cond(d).values
            zz = d["z"].fillna(0).abs().clip(upper=2).values
            pos = np.zeros(len(d)); i = 0; ent = 0
            while i < len(d):
                if sig[i]:
                    sgn = 1 if name == "long_up" else -1
                    pos[i:i + 5] = sgn * zz[i] / 2; ent += zz[i] / 2 * 2; i += 5
                else:
                    i += 1
            g = pos * d["r1"].fillna(0).values
            gains.append((g.sum() - ent * 0.0019 / 2, len(d), (pos != 0).sum()))
        tot = sum(x[0] for x in gains); n = sum(x[1] for x in gains); np_ = sum(x[2] for x in gains)
        sims[name] = {"sum_net": round(tot, 4), "per_bar": tot / n, "per_bar_in_pos": tot / max(np_, 1), "share_in_pos": np_ / n}
    out["sim"] = pd.DataFrame(sims).T
    return out
