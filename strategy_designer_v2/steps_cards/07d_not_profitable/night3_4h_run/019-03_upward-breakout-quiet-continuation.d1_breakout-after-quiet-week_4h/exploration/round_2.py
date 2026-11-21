def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    wins = sorted(set(w for c in coins for w in bars[c].keys()), key=lambda s: int(s[1:]))
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b.timestamp)
            b["r30"] = b.close / b.close.shift(180) - 1
            b["r60"] = b.close / b.close.shift(360) - 1
            b["r14"] = b.close / b.close.shift(84) - 1
            b["fwd"] = b.close.shift(-1) / b.close - 1
            b["alloc"] = b.postRebalance_current_allocation
            b["gain"] = b.alloc * b.fwd
            b["day"] = b.ts.dt.floor("D")
            b["coin"] = c; b["w"] = w
            b["wi"] = int(w[1:])
            rows.append(b[["coin", "w", "wi", "day", "r14", "r30", "r60", "fwd", "alloc", "gain", "forecast"]])
    B = pd.concat(rows)
    B["fall"] = B.wi.between(5, 10)
    inp = B[B.alloc.abs() > 1e-6]
    # gain by r30 sign inside and outside the deepest-fall windows
    g = inp.dropna(subset=["r30"]).assign(up=lambda x: x.r30 > 0).groupby(["fall", "up"]).agg(
        bps=("gain", lambda x: x.mean() * 1e4), n=("gain", "size"), sd=("gain", "std"), alloc=("alloc", "mean"))
    g["t"] = g.bps / 1e4 / (g.sd / np.sqrt(g.n)); out["gain_fall_by_r30sign"] = g.drop(columns="sd").round(3)
    for f in ["r14", "r60"]:
        x = inp.dropna(subset=[f]).copy()
        x["qt"] = pd.qcut(x[f], 5, labels=False)
        g = x.groupby("qt").agg(bps=("gain", lambda s: s.mean() * 1e4), n=("gain", "size"), sd=("gain", "std"), fmed=(f, "median"))
        g["t"] = g.bps / 1e4 / (g.sd / np.sqrt(g.n)); out["gain_by_" + f] = g.drop(columns="sd").round(4)
    # graded: gain per unit alloc vs r30 deciles, per-unit move
    x = inp.dropna(subset=["r30"]).copy()
    x["qt"] = pd.qcut(x.r30, 10, labels=False)
    out["fwd_per_unit_by_r30_decile_bps"] = x.groupby("qt").agg(bps=("fwd", lambda s: s.mean() * 1e4), fmed=("r30", "median"), n=("fwd", "size")).round(4)
    # counterfactual chains (before extra costs): base, flat when r30<0, scaled by clip(r30 rank)
    def chain(col):
        d = B.dropna(subset=["r30"]).groupby(["wi", "coin", "day"])[col].apply(lambda s: (1 + s).prod() - 1).groupby(["wi", "day"]).mean()
        eq = (1 + d).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(d)) - 1
        sh = d.mean() / d.std() * np.sqrt(365)
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": sh})
    B["g_base"] = B.gain.where(B.r30.notna())
    B["g_r30pos"] = np.where(B.r30 > 0, B.gain, 0.0)
    B["g_r60pos"] = np.where(B.r60.fillna(B.r30) > 0, B.gain, 0.0)
    out["cf_base"] = chain("g_base"); out["cf_flat_r30neg"] = chain("g_r30pos"); out["cf_flat_r60neg"] = chain("g_r60pos")
    out["share_inpos_r30neg"] = float((inp.r30 < 0).mean())
    return out
