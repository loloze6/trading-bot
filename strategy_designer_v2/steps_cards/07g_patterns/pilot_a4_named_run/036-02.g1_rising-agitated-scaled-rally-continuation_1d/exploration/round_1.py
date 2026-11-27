import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (1, 3, 5):
            vals = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    vals.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(vals) if vals else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, hi, lo, op, v = b["close"], b["high"], b["low"], b["open"], b["volume"]
            rr = (hi - lo) / c
            mr = rr.rolling(30, min_periods=30).mean()
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "inprof": b["regime"].isin(["trending", "unknown"]).values,
                "regime": b["regime"].values,
                "s1": (c / c.shift(1) - 1) / mr,
                "s3": (c / c.shift(3) - 1) / mr,
                "s7": (c / c.shift(7) - 1) / mr,
                "clv": ((c - lo) / (hi - lo)).replace([np.inf, -np.inf], np.nan),
                "wide": rr / mr,
                "upwick": ((hi - np.maximum(c, op)) / (hi - lo)).replace([np.inf, -np.inf], np.nan),
                "volr": v / v.rolling(20, min_periods=20).mean(),
                "dhigh": (c / hi.rolling(20, min_periods=20).max() - 1) / mr,
                "ret60": c / c.shift(60) - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "book": b["postRebalance_current_allocation"].values,
            })
            for h in (1, 3, 5):
                fr = c.shift(-h) / c - 1
                f[f"u{h}"] = fr - drift[(coin, h)]
                f[f"g{h}"] = (f["pos"] % h == 0)
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    out = {}
    ip = df[df.inprof]
    out["counts"] = pd.Series({"bars": len(df), "inprof": len(ip),
                               "inprof_share": len(ip) / len(df)})
    out["inprof_by_coin"] = ip.groupby("coin").size()
    res = []
    for feat in ["s1", "s3", "s7", "clv", "wide", "upwick", "volr", "dhigh", "ret60"]:
        for h in (1, 3, 5):
            s = ip[ip[f"g{h}"]].dropna(subset=[feat, f"u{h}"])
            if len(s) < 40:
                continue
            q = pd.qcut(s[feat].rank(method="first"), 5, labels=False)
            m = s.groupby(q)[f"u{h}"].mean()
            top = s[q == 4][f"u{h}"]
            t = top.mean() / (top.std() / np.sqrt(len(top)))
            rho, p = stats.spearmanr(s[feat], s[f"u{h}"])
            res.append([feat, h, len(s)] + list(m.round(4)) + [round(t, 2), round(rho, 3), round(p, 3)])
    out["quintiles_inprof"] = pd.DataFrame(
        res, columns=["feat", "h", "n", "q1", "q2", "q3", "q4", "q5", "t_q5", "rho", "p"])
    s = ip[ip["g1"]].dropna(subset=["u1"])
    out["weekday_u1"] = s.groupby("wd")["u1"].agg(["mean", "count", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    s3 = ip[ip["g3"]].dropna(subset=["u3"])
    out["by_window_u3_inprof"] = s3.groupby("win")["u3"].agg(["mean", "count"])
    return out
