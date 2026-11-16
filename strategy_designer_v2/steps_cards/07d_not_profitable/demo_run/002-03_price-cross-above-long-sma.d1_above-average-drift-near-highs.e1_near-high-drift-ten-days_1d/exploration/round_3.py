def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.shift(-1) / c - 1
            pos = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            ret30p = c / c.shift(30) - 1
            fwd10 = c.shift(-10) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "i": np.arange(len(b)), "pos": pos,
                               "r1": r1, "fee": fee, "regime": b["regime"], "ret30p": ret30p, "fwd10": fwd10,
                               "fc": b["forecast"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["r1"])
    A["net"] = A["pos"] * A["r1"] - A["fee"]
    A["net_longonly"] = np.where(A["pos"] > 0, A["net"], 0.0)
    q80 = A.loc[A["regime"] == "trending", "ret30p"].quantile(0.8)
    A["net_lo_noext"] = np.where((A["pos"] > 0) & (A["ret30p"].fillna(0) < q80), A["net"], 0.0)
    def stats(col):
        B = A.groupby(["wn", "i"])[col].mean().reset_index().sort_values(["wn", "i"])
        r = B[col]
        eq = (1 + r).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(r)) - 1
        return pd.Series({"mean": r.mean(), "sharpe": r.mean() / r.std() * np.sqrt(365), "maxdd": dd,
                          "calmar": yr / -dd})
    out["approx book variants"] = pd.DataFrame({c: stats(c) for c in ["net", "net_longonly", "net_lo_noext"]}).T
    # deepest fall composition
    B = A.groupby(["wn", "i"]).agg(net=("net", "mean"), longsh=("pos", lambda x: (x > 0).mean()),
                                    shortsh=("pos", lambda x: (x < 0).mean()),
                                    r30=("ret30p", "mean"), r1=("r1", "mean")).reset_index().sort_values(["wn", "i"])
    eq = (1 + B["net"]).cumprod(); dd = eq / eq.cummax() - 1
    B["dd"] = dd.values
    B["state"] = np.where(B["dd"] < -0.15, "deep fall", "other")
    out["state of book: deep fall vs other"] = B.groupby("state").agg(n=("net", "size"), net=("net", "mean"),
        longsh=("longsh", "mean"), shortsh=("shortsh", "mean"), r30=("r30", "mean"), coin_r1=("r1", "mean"))
    # graded: trending grid fwd10 by ret30 quintile
    G = A[(A["regime"] == "trending") & (A["i"] % 10 == 0)].dropna(subset=["fwd10", "ret30p"]).copy()
    G["q"] = pd.qcut(G["ret30p"], 5)
    out["trending grid fwd10 by 30d return quintile"] = G.groupby("q").agg(n=("fwd10", "size"), m=("fwd10", "mean"),
        t=("fwd10", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    G["side"] = np.sign(G["fc"])
    out["trending grid fwd10 by forecast side"] = G.groupby("side").agg(n=("fwd10", "size"), m=("fwd10", "mean"),
        t=("fwd10", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    return out
