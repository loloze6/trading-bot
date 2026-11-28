import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    feats = ["r1", "r5", "r20", "vr", "clv", "dhi20", "rng", "vol20", "body"]
    for H in [1, 3, 5]:
        rows = []; drift = {}
        for coin, ws in data["bars"].items():
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr += list(c[idx + H] / c[idx] - 1)
            drift[coin] = np.mean(allr)
            for w, b in ws.items():
                b = b.reset_index(drop=True)
                c = b["close"]; v = b["volume"]; o = b["open"]; hi = b["high"]; lo = b["low"]
                f = pd.DataFrame({
                    "inprof": b["regime"] != "chop",
                    "r1": c.pct_change(),
                    "r5": c / c.shift(5) - 1,
                    "r20": c / c.shift(20) - 1,
                    "vr": v / v.shift(1).rolling(20).mean(),
                    "clv": (c - lo) / (hi - lo).replace(0, np.nan),
                    "dhi20": c / hi.rolling(20).max() - 1,
                    "rng": (hi - lo) / c / ((hi - lo) / c).shift(1).rolling(20).mean(),
                    "vol20": c.pct_change().rolling(20).std(),
                    "body": (c - o) / (hi - lo).replace(0, np.nan),
                    "fwd": c.shift(-H) / c - 1,
                })
                f["coin"] = coin; f["w"] = w
                f = f.iloc[np.arange(0, len(f), H)]
                rows.append(f)
        df = pd.concat(rows)
        df["un"] = df["fwd"] - df["coin"].map(drift)
        d = df[df.inprof & df.fwd.notna()].copy()
        res = []
        for col in feats:
            x = d[[col, "un"]].dropna()
            rho, p = stats.spearmanr(x[col], x["un"])
            q = pd.qcut(x[col], 5, labels=False, duplicates="drop")
            g = x.groupby(q)["un"].mean()
            hi_ = x[q == q.max()]["un"]; lo_ = x[q == 0]["un"]
            tt = stats.ttest_ind(hi_, lo_, equal_var=False).statistic
            res.append({"feat": col, "n": len(x), "spearman": rho, "p": p,
                        "q0": g.iloc[0], "q2": g.iloc[2], "q4": g.iloc[-1], "t q4-q0": tt})
        out[f"H{H} n, mean, t"] = f"{len(d)} {d.un.mean():.5f} {d.un.mean()/(d.un.std()/np.sqrt(len(d))):.2f}"
        out[f"H{H} features"] = pd.DataFrame(res)
        # interaction: up day x volume
        x = d.dropna(subset=["r1", "vr"])
        x["upday"] = x.r1 > 0; x["heavy"] = x.vr >= x.vr.median()
        out[f"H{H} up x heavy"] = x.groupby(["upday", "heavy"])["un"].agg(["count", "mean"])
        # by window
        out[f"H{H} by window"] = d.groupby("w")["un"].agg(["count", "mean"]) if H == 3 else "skip"
    return out
