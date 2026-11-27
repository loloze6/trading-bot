def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r = c.pct_change()
            sd20 = r.rolling(20).std()
            sd30 = r.rolling(30).std()
            hh = b["high"].rolling(20).max()
            depth = (c - hh) / hh / sd20
            ret5 = c / c.shift(5) - 1
            z5 = ret5 / (sd20 * np.sqrt(5))
            ret60 = c / c.shift(60) - 1
            volrel = sd30 / r.rolling(90).std()
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            pos = np.arange(len(b))
            rows.append(pd.DataFrame({"coin": coin, "win": w, "depth": depth, "z5": z5, "r1": r,
                "volrel": volrel, "ret60": ret60, "f3": f3, "f1": f1, "g3": pos % 3 == 0,
                "chop": (b["regime"] == "unknown").values,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D")}))
    D = pd.concat(rows, ignore_index=True)
    d3 = D[D.g3].groupby("coin")["f3"].mean()
    D["x3"] = D["f3"] - D["coin"].map(d3)
    G = D[D.g3].dropna(subset=["depth", "x3"]).copy()
    G["dq"] = G.groupby("chop")["depth"].transform(lambda s: pd.qcut(s, 5, labels=False))
    G["deep"] = G["dq"] == 0
    out = {}
    def summ(g):
        return pd.Series({"mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan, "n": len(g)})
    C = G[G.chop]
    out["chop_deep_by_coin"] = C[C.deep].groupby("coin")["x3"].apply(summ).unstack().round(3)
    out["chop_deep_by_year"] = C[C.deep].groupby("yr")["x3"].apply(summ).unstack().round(3)
    out["chop_deep_by_updown"] = C[C.deep].groupby(C[C.deep]["r1"] > 0)["x3"].apply(summ).unstack().round(3)
    out["chop_deep_by_volrel"] = C[C.deep].groupby(C[C.deep]["volrel"] > C["volrel"].median())["x3"].apply(summ).unstack().round(3)
    # deepest decile and slope in chop
    C2 = C.copy(); C2["dd"] = pd.qcut(C2["depth"], 10, labels=False)
    out["chop_depth_decile"] = C2.groupby("dd")["x3"].apply(summ).unstack().round(3)
    # all bars depth deciles, day-clustered t for deepest decile
    A = G.copy(); A["dd"] = pd.qcut(A["depth"], 10, labels=False)
    out["all_depth_decile"] = A.groupby("dd")["x3"].apply(summ).unstack().round(3)
    dp = A[A.dd == 0].groupby("day")["x3"].sum()
    out["all_deepdecile_dayclustered_t"] = float(A[A.dd == 0]["x3"].mean() / (np.sqrt((dp - dp.mean()*0).pow(2).sum()) / len(A[A.dd == 0])) )
    out["all_deepdecile_days"] = int(dp.shape[0])
    # z5 momentum by trend group (ret60) and volrel
    G["tr"] = np.where(G.ret60 > 0.10, "rising", np.where(G.ret60 < -0.10, "falling", "choppy"))
    G["ag"] = np.where(G.volrel > 1, "agit", "calm")
    G["zq"] = pd.qcut(G["z5"], 5, labels=False)
    tt = G.dropna(subset=["ret60", "z5"])
    out["z5_top_by_profile"] = tt[tt.zq == 4].groupby(["tr", "ag"])["x3"].apply(summ).unstack().round(3)
    out["z5_bot_by_profile"] = tt[tt.zq == 0].groupby(["tr", "ag"])["x3"].apply(summ).unstack().round(3)
    out["deep_by_profile"] = A.assign(tr=G.tr, ag=G.ag)[A.dd <= 1].dropna(subset=["ret60"]).groupby(["tr", "ag"])["x3"].apply(summ).unstack().round(3)
    # book: forecast vs depth in chop, position share
    out["chop_fc_by_depthq"] = C.groupby("dq")[["fc", "alloc"]].mean().round(3)
    return out
