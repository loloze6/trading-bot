import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 6, 12, 24]
    # drift per coin per horizon, non-overlapping grid pooled over windows
    drift = {}
    usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs)
            drift[(c, h)] = rs.mean(); usual[(c, h)] = rs.std()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.pct_change()
            mabs = r1.abs().rolling(720, min_periods=120).mean()
            sc = r1 / mabs
            vr = b["volume"] / b["volume"].rolling(720, min_periods=120).mean()
            f = b["forecast"].fillna(0)
            sig = (f.diff() <= -2) & (f < 0)
            n = len(b)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in H:
                fwd = cl.shift(-h) / cl - 1
                cell = np.arange(n) // h
                d = pd.DataFrame({"sc": sc, "vr": vr, "fwd": fwd, "cell": cell, "sig": sig,
                                  "f": f, "yr": yr, "hour": pd.to_datetime(b["timestamp"]).dt.hour})
                d = d.dropna(subset=["sc", "vr", "fwd"])
                d["coin"] = c; d["w"] = w; d["h"] = h
                d["un"] = (d["fwd"] - drift[(c, h)]) / usual[(c, h)]
                d["unraw"] = d["fwd"] - drift[(c, h)]
                rows.append(d)
    D = pd.concat(rows)
    out = {}
    # 1) signals: by horizon, short-signed
    S = D[D.sig].groupby(["coin", "w", "h", "cell"]).head(1).copy()
    S["s"] = -S["unraw"]
    def summ(g):
        return pd.Series({"n": len(g), "mean_pct": g.s.mean() * 100, "t": g.s.mean() / (g.s.std() / np.sqrt(len(g)))})
    out["signal_by_h"] = S.groupby("h").apply(summ)
    S6 = S[S.h == 6]
    out["signal6_by_coin"] = S6.groupby("coin").apply(summ)
    out["signal6_by_year"] = S6.groupby("yr").apply(summ)
    S6 = S6.assign(scb=pd.cut(S6.sc, [0, 1, 2, 3, 5, 100]))
    out["signal6_by_scaled"] = S6.groupby("scb").apply(summ)
    # 2) all bars: scaled move bins x volume bins, h=6, direction-signed continuation (sign of r1)
    A = D[D.sc.abs() >= 2].copy()
    A["dir"] = np.sign(A.sc)
    A["s"] = A["dir"] * A["unraw"]
    A = A.groupby(["coin", "w", "h", "cell"]).head(1)
    A["vb"] = pd.cut(A.vr, [0, 0.5, 1.5, 3, 1000], labels=["<0.5", "0.5-1.5", "1.5-3", ">3"])
    A["mb"] = pd.cut(A.sc.abs(), [2, 3, 5, 1000], labels=["2-3", "3-5", ">5"])
    A["side"] = np.where(A.dir > 0, "up", "down")
    for h in [1, 3, 6, 12]:
        g = A[A.h == h].groupby(["side", "vb", "mb"]).apply(summ)
        out[f"cont_h{h}_side_vol_mag"] = g
    return out
