def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            pos = b["postRebalance_current_allocation"]
            nxt = c.shift(-1) / c - 1
            ret30 = c / c.shift(30) - 1
            lhv = b["debug_info.components.hpm.last_history_value"]
            W = lhv / ret30
            depth = 1 / np.sqrt(W.where(W > 0)) - 1
            vol30 = nxt.shift(1).rolling(30).std()
            vol_ratio = vol30 / nxt.shift(1).rolling(90).std()
            df = pd.DataFrame({"coin": coin, "wn": int(w[1:]), "i": np.arange(len(b)), "pos": pos, "nxt": nxt,
                               "gain": pos * nxt, "ret30": ret30, "W": W, "depth": depth,
                               "ts": pd.to_datetime(b["timestamp"]), "vr": vol_ratio,
                               "ret90": c / c.shift(90) - 1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["gain"])
    A["side"] = np.sign(A["pos"]).map({1: "long", -1: "short", 0: "flat"})
    A["era"] = np.where(A["wn"] <= 10, "w2_10fall" if True else "", "w11_24")
    A.loc[A["wn"] == 1, "era"] = "w1"
    out["era_side"] = A.groupby(["era", "side"]).agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                                                     sum_gain=("gain", "sum"), mean_nxt=("nxt", "mean")).unstack()
    A["dq"] = pd.qcut(A["depth"], 5, labels=False, duplicates="drop")
    out["depth_side"] = A.groupby(["dq", "side"]).agg(n=("gain", "size"), mg=("gain", "mean"),
                                                     dep=("depth", "mean")).unstack()
    A["r90s"] = np.where(A["ret90"] > 0, "r90up", "r90dn")
    out["r90_side"] = A.groupby(["r90s", "side"]).agg(n=("gain", "size"), mg=("gain", "mean"),
                                                     sg=("gain", "sum")).unstack()
    A["vq"] = pd.qcut(A["vr"], 4, labels=False)
    out["volratio_side"] = A.groupby(["vq", "side"]).agg(n=("gain", "size"), mg=("gain", "mean")).unstack()
    # long-only variants daily book approx
    A["day"] = A["ts"].dt.floor("D")
    def bookstats(g):
        d = A.assign(g=g).groupby(["wn", "day"])["g"].mean().sort_index()
        eq = (1 + d).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(d)) - 1
        return pd.Series({"mean": d.mean(), "sharpe": d.mean() / d.std() * np.sqrt(365), "maxdd": dd, "calmar": yr / -dd})
    out["variants"] = pd.DataFrame({
        "actual": bookstats(A["gain"]),
        "long_only": bookstats(A["gain"].where(A["pos"] > 0, 0)),
        "short_only_r90dn": bookstats(A["gain"].where((A["pos"] > 0) | (A["ret90"] < 0), 0)),
        "long_r90up_only": bookstats(A["gain"].where((A["pos"] > 0) & (A["ret90"] > 0), 0)),
        "hold": bookstats(A["nxt"] * 0.4),
    })
    return out
