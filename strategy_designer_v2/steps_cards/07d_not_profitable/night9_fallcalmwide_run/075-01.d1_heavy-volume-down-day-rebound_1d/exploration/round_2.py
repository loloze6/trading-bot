def explore(data):
    import numpy as np, pandas as pd
    out = {}
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; v = b["volume"]
            r1 = cl / cl.shift(1) - 1
            vr = v / v.shift(1).rolling(20).mean()
            nxt = cl.shift(-1) / cl - 1
            nxt2 = cl.shift(-2) / cl - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=40).std()
            z = r1 / r1.shift(1).rolling(20).std()
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            t = pd.DataFrame({"r1": r1, "vr": vr, "nxt": nxt, "nxt2": nxt2, "volrel": vol20 / vol60, "z": z,
                              "alloc": b["postRebalance_current_allocation"].fillna(0), "coin": c, "wn": int(w[1:]), "day": day,
                              "pos": np.arange(len(b))})
            t["dal"] = t["alloc"].diff().abs().fillna(t["alloc"].abs())
            cs.append(t)
    A = pd.concat(cs)
    A = A.dropna(subset=["nxt", "r1", "vr"]).copy()
    drift = A.groupby("coin")["nxt"].mean()
    A["ex"] = A["nxt"] - A["coin"].map(drift)
    A["case"] = (A["r1"] < 0) & (A["vr"] > 1)
    ncoin = A.groupby(["wn", "day"])["coin"].transform("count")
    A["ncoin"] = ncoin
    C = A[A["case"]].copy()

    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(), "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    # grading by vr inside drop size halves and by z
    C["dropbin"] = pd.qcut(C["r1"], 3, labels=["big", "mid", "small"])
    C["vrbin"] = pd.qcut(C["vr"], 3, labels=["vlow", "vmid", "vhigh"])
    out["case_drop_x_vr"] = C.groupby(["dropbin", "vrbin"]).apply(summ).unstack()
    C["zbin"] = pd.qcut(C["z"], 5)
    out["case_by_z"] = C.dropna(subset=["z"]).groupby("zbin").apply(summ)
    # condition alone: z (drop measured in own swing) without heavy volume
    N = A[(A["r1"] < 0) & (A["vr"] <= 1)].dropna(subset=["z"])
    out["down_lowvr_by_z"] = N.groupby(pd.qcut(N["z"], 5)).apply(summ)
    # volrel condition alone
    N2 = A[~A["case"]].dropna(subset=["volrel"])
    out["noncase_by_volrel"] = N2.groupby(pd.qcut(N2["volrel"], 4)).apply(summ)

    # simulated books: position = alloc on chosen cases only, fee 0.0011 per side
    def book(mask):
        p = A["alloc"].where(mask, 0.0)
        g = A.assign(p=p)
        g = g.sort_values(["coin", "wn", "pos"])
        g["d"] = g.groupby(["coin", "wn"])["p"].diff().abs().fillna(g["p"].abs())
        g["r"] = g["p"] * g["nxt"] - 0.0011 * g["d"]
        Bd = g.groupby(["wn", "day"])["r"].mean().sort_index()
        val = (1 + Bd).cumprod()
        dd = (val / val.cummax() - 1).min()
        yr = val.iloc[-1] ** (365 / len(Bd)) - 1
        return pd.Series({"mean": Bd.mean(), "sharpe": Bd.mean() / Bd.std() * np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr / -dd,
                          "share_held": (p != 0).mean()})
    rows = {}
    rows["all_cases"] = book(A["case"])
    rows["r1<-1.6%"] = book(A["case"] & (A["r1"] < -0.016))
    rows["r1<-3.4%"] = book(A["case"] & (A["r1"] < -0.034))
    rows["z<-1"] = book(A["case"] & (A["z"] < -1))
    rows["z<-1.5"] = book(A["case"] & (A["z"] < -1.5))
    rows["volrel>0.74"] = book(A["case"] & (A["volrel"] > 0.741))
    rows["vr>1.3"] = book(A["case"] & (A["vr"] > 1.31))
    rows["z<-1&vr>1.3"] = book(A["case"] & (A["z"] < -1) & (A["vr"] > 1.31))
    out["sim_books"] = pd.DataFrame(rows).T
    # deepest fall w14: cases held
    W = C[C["wn"] == 14]
    W = W[W["alloc"] != 0]
    W = W.assign(pnl=W["alloc"] * W["nxt"])
    worst = W.nsmallest(15, "pnl")
    out["w14_worst_held"] = worst[["coin", "r1", "z", "vr", "volrel", "alloc", "nxt"]].reset_index(drop=True)
    # held cases: losses share by z bin
    H = C[C["alloc"] != 0].assign(pnl=lambda x: x["alloc"] * x["nxt"]).dropna(subset=["z"])
    out["held_pnl_by_z"] = H.groupby(pd.qcut(H["z"], 5)).agg(n=("pnl", "size"), pnl=("pnl", "sum"), worst=("pnl", "min"), sd=("pnl", "std"))
    # 2-day horizon for strong drop
    S = C[C["z"] < -1.5].dropna(subset=["nxt2"])
    out["z<-1.5_nxt_vs_nxt2"] = pd.Series({"n": len(S), "nxt": S["nxt"].mean(), "nxt2": S["nxt2"].mean(), "nxt2_minus_nxt": (S["nxt2"] - S["nxt"]).mean()})
    return out
