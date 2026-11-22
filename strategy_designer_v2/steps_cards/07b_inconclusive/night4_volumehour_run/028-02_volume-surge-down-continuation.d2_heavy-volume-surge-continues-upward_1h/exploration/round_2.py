import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    ev = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values; v = b["volume"].astype(float)
            r = pd.Series(c).pct_change()
            sd = r.rolling(720, min_periods=240).std()
            mv = v.rolling(720, min_periods=240).mean()
            z = (r / sd).values; vr = (v / mv).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(b)
            for h in (2, 4, 6):
                # drift grid
                pos = np.arange(0, n - h, h)
                gr = c[pos + h] / c[pos] - 1
                ev.append(pd.DataFrame({"coin": coin, "h": h, "kind": "grid", "fr": gr,
                                        "z": np.nan, "vr": np.nan, "yr": yr[pos]}))
                cell = np.arange(n) // h
                for kind, m in [("up_heavy", (z > 2) & (vr > 3)),
                                ("down_heavy", (z < -2) & (vr > 3)),
                                ("up_thin", (z > 2) & (vr < 1.5)),
                                ("down_thin", (z < -2) & (vr < 1.5))]:
                    idx = np.where(m & (np.arange(n) < n - h))[0]
                    if len(idx) == 0: continue
                    _, first = np.unique(cell[idx], return_index=True)
                    idx = idx[first]
                    ev.append(pd.DataFrame({"coin": coin, "h": h, "kind": kind,
                                            "fr": c[idx + h] / c[idx] - 1,
                                            "z": z[idx], "vr": vr[idx], "yr": yr[idx]}))
    d = pd.concat(ev)
    drift = d[d.kind == "grid"].groupby(["coin", "h"])["fr"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["u"] = d["fr"] - d["drift"]
    e = d[d.kind != "grid"].copy()

    def summ(g):
        n = len(g); m = g["u"].mean(); s = g["u"].std()
        return pd.Series({"n": n, "mean_u_%": 100 * m,
                          "t": m / (s / np.sqrt(n)) if n > 1 else np.nan,
                          "share_pos": (g["u"] > 0).mean()})
    out["by_kind_h"] = e.groupby(["kind", "h"]).apply(summ)
    out["by_kind_coin_h2"] = e[e.h == 2].groupby(["kind", "coin"]).apply(summ)
    out["by_kind_coin_h6"] = e[e.h == 6].groupby(["kind", "coin"]).apply(summ)
    dh = e[(e.kind == "down_heavy") & (e.h == 2)]
    out["down_heavy_h2_by_year"] = dh.groupby("yr").apply(summ)
    ut = e[(e.kind == "up_thin") & (e.h == 6)]
    out["up_thin_h6_by_year"] = ut.groupby("yr").apply(summ)
    # graded: u vs |z|*vr, in signal direction sign kept raw
    res = []
    for (k, h), g in e.groupby(["kind", "h"]):
        g = g.dropna(subset=["z", "vr", "u"])
        x = np.abs(g["z"]) * g["vr"]
        sl = stats.linregress(x, g["u"])
        q = pd.qcut(x, 3, labels=False, duplicates="drop")
        top = g["u"][q == q.max()].mean(); bot = g["u"][q == 0].mean()
        res.append({"kind": k, "h": h, "slope_t": sl.slope / sl.stderr,
                    "top3rd_u_%": 100 * top, "bot3rd_u_%": 100 * bot})
    out["graded"] = pd.DataFrame(res).set_index(["kind", "h"])
    return out
