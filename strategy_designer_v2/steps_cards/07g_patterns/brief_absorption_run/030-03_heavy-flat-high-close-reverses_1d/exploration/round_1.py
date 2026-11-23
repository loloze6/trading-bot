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
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "clv": (c - l) / rng,
                "volr": v / v.shift(1).rolling(20).mean(),
                "body": (c - o).abs() / o,
                "sret": (c - o) / o,
                "rngrel": (h - l) / c,
                "r1": c.pct_change(),
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            df["rngz"] = df["rngrel"] / df["rngrel"].shift(1).rolling(20).mean()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % H == 0].copy()
    drift = g.groupby("coin")["fwd"].mean(); usual = g.groupby("coin")["fwd"].std()
    for x in (d, g):
        x["ab"] = (x["fwd"] - x["coin"].map(drift)) / x["coin"].map(usual)
    g = g.dropna(subset=["ab"])
    out = {}
    feats = ["clv","volr","body","sret","rngrel","rngz","r1","r5","r20","vol20"]
    cr = []
    for f in feats:
        s = g[[f,"ab"]].dropna()
        rho, p = stats.spearmanr(s[f], s["ab"])
        cr.append({"feat": f, "n": len(s), "spearman": rho, "p": p})
    out["grid_spearman_fwd5_strength"] = pd.DataFrame(cr)
    def qtab(x, f, q=5):
        s = x[[f,"ab"]].dropna().copy()
        s["q"] = pd.qcut(s[f], q, labels=False, duplicates="drop")
        t = s.groupby("q")["ab"].agg(["count","mean","std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["fmean"] = s.groupby("q")[f].mean()
        return t
    for f in ["r1","r5","r20","vol20","rngz","clv","sret"]:
        out["q_"+f] = qtab(g, f)
    # heavy-volume days, non-overlapping greedy
    def events(mask):
        sel = []
        for (coin, w), x in d[mask].groupby(["coin","win"]):
            last = -99
            for i, r in x.iterrows():
                if r["pos"] - last >= H and not np.isnan(r["ab"]):
                    sel.append(i); last = r["pos"]
        return d.loc[sel]
    hv = events(d["volr"] >= 2)
    out["heavy_vol_clv_q"] = qtab(hv, "clv", 3)
    out["heavy_vol_sret_q"] = qtab(hv, "sret", 3)
    out["heavy_vol_r5_q"] = qtab(hv, "r5", 3)
    out["heavy_vol_by_coin"] = hv.groupby("coin")["ab"].agg(["count","mean"])
    wd = g.groupby("wd")["ab"].agg(["count","mean","std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday"] = wd
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t)
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
