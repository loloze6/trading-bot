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
                "r1": c.pct_change(),
                "fwd": c.shift(-H) / c - 1,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % H == 0]
    drift = g.groupby("coin")["fwd"].mean(); usual = g.groupby("coin")["fwd"].std()
    d["ab"] = (d["fwd"] - d["coin"].map(drift)) / d["coin"].map(usual)
    d["abraw"] = d["fwd"] - d["coin"].map(drift)
    d["r5z"] = d["r5"] / d["coin"].map(usual)
    def events(mask):
        sel = []
        for (coin, w), x in d[mask].groupby(["coin","win"]):
            last = -99
            for i, r in x.iterrows():
                if r["pos"] - last >= H and not np.isnan(r["ab"]) and not np.isnan(r["r5"]):
                    sel.append(i); last = r["pos"]
        return d.loc[sel].copy()
    def tt(s):
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out = {}
    hv = events(d["volr"] >= 2)
    # signed: direction of r5, outcome in that direction
    hv["sgn"] = np.sign(hv["r5"])
    hv["dirab"] = hv["sgn"] * hv["ab"]
    hv["dirraw"] = hv["sgn"] * hv["fwd"]
    hv["dirunraw"] = hv["sgn"] * hv["abraw"]
    out["hv_dir_cont_all"] = pd.DataFrame({"strength": tt(hv["dirab"]), "total_move": tt(hv["dirraw"]), "unusual_move": tt(hv["dirunraw"])})
    out["hv_by_sign"] = hv.groupby("sgn")["ab"].apply(tt).unstack()
    s = hv[["r5z","ab"]].dropna()
    rho, p = stats.spearmanr(s["r5z"], s["ab"])
    out["hv_spearman_r5z_ab"] = pd.Series({"n": len(s), "rho": rho, "p": p})
    hv["q5"] = pd.qcut(hv["r5z"], 5, labels=False)
    out["hv_r5z_quintiles"] = hv.groupby("q5").agg(n=("ab","size"), r5z=("r5z","mean"), ab=("ab","mean"), raw=("fwd","mean"))
    # graded by volume within direction
    hv["vq"] = pd.qcut(hv["volr"], 3, labels=False)
    out["hv_dirab_by_volr_tercile"] = hv.groupby("vq")["dirab"].apply(tt).unstack()
    out["hv_dirab_by_coin"] = hv.groupby("coin")["dirab"].apply(tt).unstack()
    out["hv_dirab_by_year"] = hv.groupby("year")["dirab"].apply(tt).unstack()
    hv["half"] = np.where(hv["wn"] <= 12, "w1-w12", "w13-w24")
    out["hv_dirab_by_half"] = hv.groupby("half")["dirab"].apply(tt).unstack()
    # control: normal-volume days, same directional measure
    nv = events(d["volr"] < 1)
    nv["dirab"] = np.sign(nv["r5"]) * nv["ab"]
    mv = events((d["volr"] >= 1) & (d["volr"] < 2))
    mv["dirab"] = np.sign(mv["r5"]) * mv["ab"]
    out["control_dirab"] = pd.DataFrame({"volr<1": tt(nv["dirab"]), "1-2": tt(mv["dirab"]), ">=2": tt(hv["dirab"])})
    out["welch_hv_minus_nv"] = pd.Series(stats.ttest_ind(hv["dirab"].dropna(), nv["dirab"].dropna(), equal_var=False)._asdict())
    # clv within heavy volume after controlling r5 sign
    hv["cq"] = pd.qcut(hv["clv"], 3, labels=False)
    out["hv_ab_by_sign_clv"] = hv.groupby(["sgn","cq"])["ab"].apply(tt).unstack()
    return out
