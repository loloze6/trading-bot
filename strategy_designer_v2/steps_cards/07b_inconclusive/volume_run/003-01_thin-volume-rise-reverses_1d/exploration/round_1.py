import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    rows = []
    base = {}
    for coin, wins in bars.items():
        for h in H:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            base[(coin, h)] = np.nanmean(vals)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; v = df["volume"]
            r1 = c.pct_change()
            vr = v / v.rolling(30, min_periods=10).mean()
            vs = r1 / r1.rolling(20, min_periods=10).std()
            z = (vs - vs.rolling(60, min_periods=20).mean()) / vs.rolling(60, min_periods=20).std()
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in H:
                fwd = c.shift(-h) / c - 1
                d = pd.DataFrame({"coin": coin, "w": w, "h": h, "i": np.arange(len(df)), "r1": r1, "vr": vr, "vs": vs, "z": z,
                                  "fc": df["forecast"], "fwd": fwd - base[(coin, h)], "yr": yr})
                rows.append(d)
    A = pd.concat(rows)
    A = A.dropna(subset=["vr", "vs", "fwd"])

    def deover(d, h):
        keep = []
        for (cn, w), g in d.groupby(["coin", "w"]):
            last = -10**9
            for i, r in zip(g["i"], g.index):
                if i - last >= h:
                    keep.append((cn, w, i)); last = i
        k = pd.MultiIndex.from_tuples(keep, names=["coin", "w", "i"]) if keep else None
        return d.set_index(["coin", "w", "i"]).loc[k].reset_index() if keep else d.iloc[:0]

    def summ(x):
        x = x.dropna()
        n = len(x)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})

    out = {}
    # tested events across horizons
    hz = []
    for h in H:
        e = deover(A[(A.h == h) & (A.fc <= -2)].copy(), h)
        hz.append(summ(e["fwd"]).rename(f"h{h}"))
    out["tested_events_by_horizon"] = pd.DataFrame(hz)

    e5 = deover(A[(A.h == 5) & (A.fc <= -2)].copy(), 5)
    out["tested_by_coin"] = e5.groupby("coin")["fwd"].apply(summ).unstack()
    out["tested_by_year"] = e5.groupby("yr")["fwd"].apply(summ).unstack()
    e5["vband"] = pd.cut(e5.vr, [0, 0.5, 0.75])
    out["tested_by_vband"] = e5.groupby("vband")["fwd"].apply(summ).unstack()
    e5["zq"] = pd.qcut(e5.z, 4, duplicates="drop")
    out["tested_by_z_quart"] = e5.groupby("zq")["fwd"].apply(summ).unstack()

    # contrast: rises (vs>1) by volume band, horizon 5 and 1
    for h in [1, 5]:
        r = A[(A.h == h) & (A.vs > 1)].copy()
        r["vband"] = pd.cut(r.vr, [0, 0.5, 0.75, 1.0, 1.5, 2.5, 100])
        res = []
        for b, g in r.groupby("vband"):
            e = deover(g, h)
            res.append(summ(e["fwd"]).rename(str(b)))
        out[f"rise_vs>1_by_vband_h{h}"] = pd.DataFrame(res)
        # falls
        r = A[(A.h == h) & (A.vs < -1)].copy()
        r["vband"] = pd.cut(r.vr, [0, 0.5, 0.75, 1.0, 1.5, 2.5, 100])
        res = []
        for b, g in r.groupby("vband"):
            e = deover(g, h)
            res.append(summ(e["fwd"]).rename(str(b)))
        out[f"fall_vs<-1_by_vband_h{h}"] = pd.DataFrame(res)
    return out
