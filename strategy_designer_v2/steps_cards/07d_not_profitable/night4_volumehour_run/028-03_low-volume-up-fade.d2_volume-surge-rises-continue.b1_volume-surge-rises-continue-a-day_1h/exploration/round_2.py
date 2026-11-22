import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    rows = []; caseRows = []
    for c in coins:
        g = {h: [] for h in (3, 6, 12, 24)}
        for w, b in bars[c].items():
            cl = b.close.values
            for h in g:
                idx = np.arange(0, len(cl) - h, h)
                g[h].append(cl[idx + h] / cl[idx] - 1)
        drift = {h: np.concatenate(v).mean() for h, v in g.items()}
        usd = {h: np.concatenate(v).std() for h, v in g.items()}
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close
            a = b.postRebalance_current_allocation.fillna(0)
            r = cl.pct_change().shift(-1)
            r30 = cl / cl.shift(720) - 1
            ma = cl.rolling(720, min_periods=200).mean()
            rows.append(pd.DataFrame({"a": a, "r": r, "r30": r30,
                                      "above": (cl > ma).astype(float).where(ma.notna()),
                                      "w": w, "coin": c}))
            f = b.forecast.fillna(0).values
            low = 0.0; cells = set()
            for k in range(len(b)):
                if f[k] <= 0:
                    low = 0.0; continue
                if f[k] - low >= 2:
                    cell = k // 24
                    if cell not in cells and k + 24 < len(b):
                        cells.add(cell)
                        d = {"coin": c, "r30": r30.iloc[k]}
                        for h in (3, 6, 12, 24):
                            d["s%d" % h] = (cl.iloc[k + h] / cl.iloc[k] - 1 - drift[h]) / usd[h]
                        caseRows.append(d)
                    low = f[k]
                low = min(low, f[k])
    B = pd.concat(rows).dropna()
    B["state"] = np.where(B.r30 > 0, "30d up", "30d down")
    G = B.groupby("state").apply(lambda x: pd.Series({
        "share_bars": len(x) / len(B), "mean_alloc": x.a.mean(),
        "share_in": (x.a.abs() > 1e-6).mean(),
        "coin_mean_hourly": x.r.mean(), "book_mean_hourly": (x.a * x.r).mean()}))
    out["book by 30d state"] = G
    C = pd.DataFrame(caseRows).dropna()
    C["state"] = np.where(C.r30 > 0, "30d up", "30d down")
    res = []
    for st, x in C.groupby("state"):
        for h in (3, 6, 12, 24):
            s = x["s%d" % h]
            res.append({"state": st, "h": h, "n": len(s), "strength": s.mean(),
                        "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    for h in (3, 6, 12, 24):
        s = C["s%d" % h]
        res.append({"state": "all", "h": h, "n": len(s), "strength": s.mean(),
                    "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out["strength by horizon and state"] = pd.DataFrame(res)
    # correlation of strength with r30 within cases
    out["corr strength24 vs r30"] = float(np.corrcoef(C.r30, C.s24)[0, 1])
    return out
