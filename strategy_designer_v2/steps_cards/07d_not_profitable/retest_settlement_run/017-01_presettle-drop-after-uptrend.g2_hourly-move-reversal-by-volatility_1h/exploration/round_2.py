import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [6, 12, 24, 48]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = b["close"].astype(float).reset_index(drop=True)
            r1 = c.pct_change()
            vol = r1.rolling(24, min_periods=20).std()
            z1 = r1 / vol
            z1s6 = z1.rolling(6).sum() / np.sqrt(6)
            zfc = -pd.to_numeric(b["forecast"], errors="coerce").reset_index(drop=True)
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                fwd = (c.shift(-h) / c - 1).iloc[idx]
                usual = fwd.std()
                rows.append(pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "h": h,
                    "fwd": fwd.values, "z1": z1.iloc[idx].values, "z1s6": z1s6.iloc[idx].values,
                    "fc": -zfc.iloc[idx].values}))
    d = pd.concat(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["usual"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["ex"] = d.fwd - d.drift
    out = {}
    res = []
    for sig in ["z1", "z1s6", "fc"]:
        for h in H:
            s = d[d.h == h].dropna(subset=[sig, "ex"])
            sl = np.polyfit(-s[sig], s.ex, 1)[0]
            x = -s[sig]; e = s.ex - sl * x
            se = np.sqrt((e ** 2).sum() / (len(s) - 2) / ((x - x.mean()) ** 2).sum())
            for lo, hi in [(0, 1), (1, 2), (2, 3), (1, 3)]:
                g = s[(s[sig].abs() > lo) & (s[sig].abs() <= hi)]
                mv = -np.sign(g[sig]) * g.ex
                res.append({"sig": sig, "h": h, "absz": f"{lo}-{hi}", "n": len(g),
                            "unusual_%": 100 * mv.mean(), "total_%": 100 * (-np.sign(g[sig]) * g.fwd).mean(),
                            "strength": (mv / g.usual).mean(),
                            "t": mv.mean() / (mv.std() / np.sqrt(len(g))), "slope_t": sl / se})
    out["horizons"] = pd.DataFrame(res)
    s = d[(d.h == 24)].dropna(subset=["z1", "ex"])
    s = s[s.z1.abs() > 1].copy()
    s["mv"] = -np.sign(s.z1) * s.ex * 100
    out["z1_h24_by_coin"] = s.groupby("coin").mv.agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    s["wgrp"] = pd.cut(s.wn, [0, 6, 12, 18, 24])
    out["z1_h24_by_wgroup"] = s.groupby("wgrp", observed=True).mv.agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    s["side"] = np.where(s.z1 > 0, "short_after_up", "long_after_down")
    out["z1_h24_by_side"] = s.groupby("side").mv.agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    return out
