import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            rng = (hi - lo) / cl
            rr = rng.rolling(6).mean() / rng.rolling(180, min_periods=90).mean()
            lr = np.log(cl).diff()
            vol = lr.rolling(42).std() / lr.rolling(360, min_periods=180).std()
            r1d = cl / cl.shift(6) - 1
            mad = r1d.abs().rolling(180, min_periods=90).mean()
            depth = (-r1d / mad).clip(lower=0)
            fwd = cl.shift(-84) / cl - 1
            r1 = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            recs.append(pd.DataFrame({"c": c, "w": w, "i": np.arange(len(b)), "a": a, "f": b["forecast"],
                                      "rr": rr, "vol": vol, "depth": depth, "fwd": fwd, "g": a * r1, "r1": r1}))
    R = pd.concat(recs, ignore_index=True)
    out["alloc_vs_forecast"] = pd.Series({"share_alloc_pos_when_f0": (R.loc[R.f == 0, "a"] > 0).mean(),
                                          "mean_alloc_f0": R.loc[R.f == 0, "a"].mean(),
                                          "mean_alloc_fpos": R.loc[R.f > 0, "a"].mean(),
                                          "gain_bp_f0": R.loc[R.f == 0, "g"].mean() * 1e4,
                                          "gain_bp_fpos": R.loc[R.f > 0, "g"].mean() * 1e4})
    G = R[R.i % 84 == 0].dropna(subset=["fwd", "rr", "depth"]).copy()
    drift = R[R.i % 84 == 0].dropna(subset=["fwd"]).groupby("c")["fwd"].mean()
    G["ex"] = G["fwd"] - G["c"].map(drift)
    S = G[G.depth > 0].copy()
    S["rrq"] = pd.qcut(S["rr"], 4, labels=False)
    out["fallcases_by_range_ratio"] = S.groupby("rrq").agg(rr=("rr", "mean"), n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))), depth=("depth", "mean"))
    # graded: slope of ex on depth*rr (panic score) vs on depth
    S["panic"] = S["depth"] * S["rr"]
    for k in ["depth", "panic", "rr"]:
        sl = stats.linregress(S[k], S["ex"])
        out[f"slope_{k}"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(S)})
    hi = S[S.rr >= S.rr.median()]
    sl = stats.linregress(hi["depth"], hi["ex"])
    out["slope_depth_in_high_range_half"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(hi)})
    # book fall: deepest falls of daily book chain and conditions
    rows = []
    for w in sorted({w for c in coins for w in days[c]}, key=lambda s: int(s[1:])):
        B = pd.concat([days[c][w].set_index("day")["book_return"].rename(c) for c in coins if w in days[c]], axis=1).mean(axis=1)
        H = pd.concat([days[c][w].set_index("day")["coin_return"].rename(c) for c in coins if w in days[c]], axis=1).mean(axis=1)
        rows.append(pd.DataFrame({"b": B.values, "h": H.values, "w": w}).dropna())
    D = pd.concat(rows, ignore_index=True)
    D["b30"] = D.groupby("w")["b"].transform(lambda x: (1 + x).rolling(30).apply(np.prod, raw=True) - 1)
    D["h30"] = D.groupby("w")["h"].transform(lambda x: (1 + x).rolling(30).apply(np.prod, raw=True) - 1)
    worst = D.dropna().nsmallest(200, "b30")
    out["worst30d_spells"] = pd.Series({"book_30d_mean": worst.b30.mean(), "hold_30d_mean": worst.h30.mean(),
                                        "corr_b_h_daily": D[["b", "h"]].corr().iloc[0, 1],
                                        "beta_b_on_h": stats.linregress(D.h, D.b).slope})
    return out
