import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 30: continue
            o, h, l, c, v = [b[x].astype(float) for x in ["open","high","low","close","volume"]]
            rng = (h - l).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "clv": (c - l) / rng,
                "volr": v / v.shift(1).rolling(20).mean(),
                "r5": c / c.shift(5) - 1,
                "fwd": c.shift(-H) / c - 1,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % H == 0]
    drift = g.groupby("coin")["fwd"].mean(); usual = g.groupby("coin")["fwd"].std()
    d["ab"] = (d["fwd"] - d["coin"].map(drift)) / d["coin"].map(usual)
    d["abraw"] = d["fwd"] - d["coin"].map(drift)
    def tt(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    sel = []
    for (coin, w), x in d[(d["volr"] >= 2)].groupby(["coin","win"]):
        last = -99
        for i, r in x.iterrows():
            if r["pos"] - last >= H and not np.isnan(r["ab"]) and not np.isnan(r["r5"]):
                sel.append(i); last = r["pos"]
    hv = d.loc[sel].copy()
    hv["half"] = np.where(hv["wn"] <= 12, "w1-w12", "w13-w24")
    hv["score"] = (hv["clv"] - 0.5) * hv["volr"]
    out = {}
    s = hv[["score","ab"]].dropna()
    rho, p = stats.spearmanr(s["score"], s["ab"]); pr = stats.pearsonr(s["score"], s["ab"])
    out["hv_score_corr"] = pd.Series({"n": len(s), "spearman": rho, "p": p, "pearson": pr[0], "pp": pr[1]})
    hv["sq"] = pd.qcut(hv["score"], 5, labels=False)
    out["hv_score_quint"] = hv.groupby("sq").agg(n=("ab","size"), score=("score","mean"), ab=("ab","mean"), unusual=("abraw","mean"), total=("fwd","mean"))
    hv["cq"] = pd.qcut(hv["clv"], 3, labels=False)
    top = hv[hv["cq"] == 2]
    out["hiclv_by_coin"] = top.groupby("coin")["ab"].apply(tt).unstack()
    out["hiclv_by_half"] = top.groupby("half")["ab"].apply(tt).unstack()
    out["hiclv_raw"] = pd.DataFrame({"unusual": tt(top["abraw"]), "total": tt(top["fwd"])})
    up = hv[hv["r5"] > 0]
    out["up_by_coin"] = up.groupby("coin")["ab"].apply(tt).unstack()
    out["up_by_half"] = up.groupby("half")["ab"].apply(tt).unstack()
    out["up_raw"] = pd.DataFrame({"unusual": tt(up["abraw"]), "total": tt(up["fwd"])})
    up = up.copy(); up["vq"] = pd.qcut(up["volr"], 3, labels=False)
    out["up_by_volr"] = up.groupby("vq").agg(n=("ab","size"), volr=("volr","mean"), ab=("ab","mean"), unusual=("abraw","mean"))
    return out
