import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    feats = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]; r = cl.pct_change()
            b["vol20"] = r.rolling(20).std()
            b["z"] = r/b["vol20"]
            b["dd60"] = cl/cl.rolling(60, min_periods=20).max()-1
            b["dd30"] = cl/cl.rolling(30, min_periods=20).max()-1
            b["r30"] = cl/cl.shift(30)-1
            b["fwd10"] = cl.shift(-10)/cl-1
            b["gain"] = b["postRebalance_current_allocation"]*(cl.shift(-1)/cl-1)
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["wn"] = int(w[1:])
            b["day"] = b["timestamp"].astype(str).str[:10]
            feats.append(b)
    F = pd.concat(feats)
    grid = F[F.pos % 10 == 0]
    drift = grid.groupby("coin")["fwd10"].mean()
    F["un10"] = F["fwd10"] - F["coin"].map(drift)
    F["cell"] = F.pos//10
    cases = F[F.forecast >= 2].groupby(["coin","wn","cell"]).head(1).dropna(subset=["un10"])
    def grp(x, col, q=5):
        x = x.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        return x.groupby("b").agg(lo=(col,"min"), hi=(col,"max"), n=("un10","size"),
                               un=("un10","mean"), tot=("fwd10","mean"),
                               t=("un10", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    out["cases by dd60 (5)"] = grp(cases, "dd60")
    out["cases by dd30 (5)"] = grp(cases, "dd30")
    near = cases[cases.dd60 > cases.dd60.quantile(0.4)]
    out["near-high cases by z"] = grp(near, "z", 3)
    far = cases[cases.dd60 <= cases.dd60.quantile(0.4)]
    out["far cases by z"] = grp(far, "z", 3)
    out["cases dd60 corr"] = pd.Series({"corr_un_dd60": cases[["un10","dd60"]].dropna().corr().iloc[0,1],
                                         "n": cases.dd60.notna().sum()})
    H = F[F.postRebalance_current_allocation.abs() > 0].dropna(subset=["dd60","gain"]).copy()
    H["b"] = pd.qcut(H["dd60"], 5, labels=False)
    out["held bar gain by dd60"] = H.groupby("b").agg(lo=("dd60","min"), hi=("dd60","max"), n=("gain","size"),
        mean_gain=("gain","mean"), sd=("gain","std"), worst=("gain","min"),
        t=("gain", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    # book fall days: book daily mean across coins; worst 5% days and dd60 of held positions
    H["absg"] = H["gain"]
    dailyb = H.groupby(["wn","day"])["gain"].mean()
    thr = dailyb.quantile(0.05)
    worst = dailyb[dailyb <= thr].index
    Hw = H.set_index(["wn","day"]).loc[lambda x: x.index.isin(worst)]
    out["dd60 on worst 5% book days vs all held"] = pd.Series({
        "worst_days_mean_dd60": Hw.dd60.mean(), "all_held_mean_dd60": H.dd60.mean(),
        "worst_share_dd60_below_-0.16": (Hw.dd60 < -0.16).mean(),
        "all_share_dd60_below_-0.16": (H.dd60 < -0.16).mean()})
    return out
