import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 10
    rows = []
    drift = {}
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
                "dlo20": c / lo.rolling(20).min() - 1,
                "rng": (hi - lo) / c / ((hi - lo) / c).shift(1).rolling(20).mean(),
                "vol20": c.pct_change().rolling(20).std(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd": c.shift(-H) / c - 1,
            })
            f["coin"] = coin; f["w"] = w
            f = f.iloc[np.arange(0, len(f), H)]
            rows.append(f)
    df = pd.concat(rows)
    df["un"] = df["fwd"] - df["coin"].map(drift)
    d = df[df.inprof & df.fwd.notna()].copy()
    out = {"n in-profile grid cases": len(d), "mean unusual all in-profile": d.un.mean(),
           "t all": d.un.mean() / (d.un.std() / np.sqrt(len(d)))}
    res = []
    for col in ["r1", "r5", "r20", "vr", "clv", "dhi20", "dlo20", "rng", "vol20"]:
        x = d[[col, "un"]].dropna()
        rho, p = stats.spearmanr(x[col], x["un"])
        q = pd.qcut(x[col], 5, labels=False, duplicates="drop")
        g = x.groupby(q)["un"].mean()
        res.append({"feat": col, "n": len(x), "spearman": rho, "p": p,
                    "q0": g.iloc[0], "q1": g.iloc[1], "q2": g.iloc[2], "q3": g.iloc[3], "q4": g.iloc[-1]})
    out["features vs unusual 10d (in-profile)"] = pd.DataFrame(res)
    out["by weekday"] = d.groupby("wd")["un"].agg(["count", "mean"])
    out["by coin"] = d.groupby("coin")["un"].agg(["count", "mean"])
    up = d[d.r1 > 0]
    x = up[["vr", "un"]].dropna()
    out["up days: vr spearman"] = str(stats.spearmanr(x.vr, x.un))
    out["up vs down day unusual"] = d.groupby(d.r1 > 0)["un"].agg(["count", "mean", "std"])
    # book
    br = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            br.append(dd[["book_return", "coin_return"]].assign(coin=coin, w=w))
    B = pd.concat(br).dropna()
    out["book by window"] = B.groupby("w")["book_return"].agg(["count", "mean", "sum"])
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
