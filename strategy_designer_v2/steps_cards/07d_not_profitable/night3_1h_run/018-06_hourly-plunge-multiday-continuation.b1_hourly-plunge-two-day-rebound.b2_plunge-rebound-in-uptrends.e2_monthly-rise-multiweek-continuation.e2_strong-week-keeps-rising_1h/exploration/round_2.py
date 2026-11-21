def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]
            b["r30"] = cl.pct_change(720)
            b["dhi"] = cl / cl.rolling(720).max() - 1
            b["al"] = b["postRebalance_current_allocation"]
            b["g"] = b["al"] * (cl.shift(-1) / cl - 1)
            b["c"] = c; b["w"] = w
            rows.append(b[["c","w","al","g","r30","dhi","forecast"]])
    X = pd.concat(rows).dropna(subset=["g"])
    L = X[X["al"].abs() > 1e-6].copy()
    out["n_long_bars"] = len(L)
    out["total_gain_sum"] = L["g"].sum()
    L["r30s"] = np.where(L["r30"] < 0, "r30<0", "r30>=0")
    out["gain_by_r30sign"] = L.groupby("r30s").agg(
        bars=("g","size"), gain_sum=("g","sum"), gain_mean=("g","mean"),
        gain_std=("g","std"), mean_alloc=("al","mean"))
    L["dq"] = pd.qcut(L["dhi"], 4, labels=False, duplicates="drop")
    out["gain_by_dhi_q"] = L.groupby("dq").agg(
        lo=("dhi","min"), hi=("dhi","max"), bars=("g","size"),
        gain_sum=("g","sum"), gain_mean=("g","mean"), gain_std=("g","std"))
    # graded: near-high x strong forecast
    L["strong"] = L["forecast"] >= 18.9
    out["gain_by_strong_x_r30"] = L.groupby(["strong","r30s"]).agg(
        bars=("g","size"), gain_sum=("g","sum"), gain_mean=("g","mean"))
    # simulated deepest fall of hourly gain chain, all vs excluding r30<0 positions, per coin then mean
    res = {}
    for c in X["c"].unique():
        Xc = X[X["c"] == c]
        for lab, mask in [("all", np.ones(len(Xc), bool)), ("only_r30>=0", (Xc["r30"] >= 0).values)]:
            parts = []
            for w in sorted(Xc["w"].unique(), key=lambda x: int(x[1:])):
                sel = (Xc["w"] == w).values
                g = np.where(mask[sel], Xc["g"].values[sel], 0.0)
                parts.append(g)
            g = np.concatenate(parts)
            e = np.cumprod(1 + np.nan_to_num(g))
            mdd = (e / np.maximum.accumulate(e) - 1).min()
            yr = e[-1] ** (8760 / len(g)) - 1
            res[(c, lab)] = (yr, mdd, yr / -mdd)
    out["sim_calmar_gross"] = pd.DataFrame(res, index=["yr","mdd","calmar"]).T
    return out
