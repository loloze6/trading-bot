def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    g = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            lr = np.log(cl / cl.shift(1))
            vol20 = lr.rolling(20).std()
            z = lr / vol20.shift(1)
            ret90 = cl / cl.shift(90) - 1
            ret30 = cl / cl.shift(30) - 1
            low60 = cl / cl.rolling(60).min() - 1
            fwd20 = cl.shift(-20) / cl - 1
            x = pd.DataFrame({"gain": a * r1, "a": a, "fc": b["forecast"], "z": z, "ret90": ret90,
                              "ret30": ret30, "low60": low60, "fwd20": fwd20, "coin": c, "wn": int(w[1:]),
                              "pos": np.arange(len(b))})
            g.append(x)
    G = pd.concat(g)
    out["w17 gain by coin and side"] = G[G.wn == 17].assign(side=np.sign(G.a)).groupby(["coin", "side"])["gain"].sum().unstack()
    out["gain with fresh forecast vs stale"] = G.assign(side=np.sign(G.a), fresh=(G.fc != 0)).groupby(["side", "fresh"])["gain"].agg(["size", "sum", "mean"])
    # Cases: bounce days z>1.5, non-overlapping grid of 20 per window
    C = G[(G.pos % 20 == 0)].dropna(subset=["fwd20", "ret90"])
    allfwd = C.groupby("coin")["fwd20"].mean()
    B = G[(G.z > 1.5)].dropna(subset=["fwd20", "ret90"]).copy()
    B["cell"] = B.pos // 20
    B = B.groupby(["coin", "wn", "cell"]).head(1)
    B["ex"] = B.fwd20 - B.coin.map(allfwd)
    B["reg"] = np.where(B.ret90 < 0, "down", "up")
    B["r90q"] = pd.qcut(B.ret90, 5, labels=False)
    out["bounce cases fwd20 ex by ret90 quintile"] = B.groupby("r90q").agg(n=("ex", "size"), ret90=("ret90", "mean"), ex=("ex", "mean"), t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    D = B[B.reg == "down"].copy()
    D["r30q"] = pd.qcut(D.ret30, 3, labels=False)
    out["down-regime bounces by 30d return tercile"] = D.groupby("r30q").agg(n=("ex", "size"), ret30=("ret30", "mean"), ex=("ex", "mean"), t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    D["lowq"] = pd.qcut(D.low60, 3, labels=False)
    out["down-regime bounces by distance above 60d low"] = D.groupby("lowq").agg(n=("ex", "size"), low60=("low60", "mean"), ex=("ex", "mean"), t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    D["zq"] = pd.qcut(D.z, 3, labels=False)
    out["down-regime bounces by size"] = D.groupby("zq").agg(n=("ex", "size"), z=("z", "mean"), ex=("ex", "mean"))
    U = B[B.reg == "up"].copy(); U["zq"] = pd.qcut(U.z, 3, labels=False)
    out["up-regime bounces by size"] = U.groupby("zq").agg(n=("ex", "size"), z=("z", "mean"), ex=("ex", "mean"))
    # short losses by ret90 depth of bars held short
    S = G[G.a < 0].dropna(subset=["ret90"]).copy()
    S["q"] = pd.qcut(S.ret90, 4, labels=False)
    out["short bars gain by ret90 quartile"] = S.groupby("q").agg(n=("gain", "size"), ret90=("ret90", "mean"), mean_gain=("gain", "mean"), sum_gain=("gain", "sum"))
    return out
