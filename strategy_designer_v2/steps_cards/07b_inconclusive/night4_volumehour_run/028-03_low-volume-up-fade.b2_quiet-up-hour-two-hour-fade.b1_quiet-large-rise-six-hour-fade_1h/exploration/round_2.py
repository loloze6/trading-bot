import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    h = 6
    drift = {}
    for c in bars:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - h, h)
            rs.append(cl[idx + h] / cl[idx] - 1)
        drift[c] = np.concatenate(rs).mean()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.pct_change()
            mabs = r1.abs().rolling(720, min_periods=120).mean()
            sc = r1 / mabs
            vr = b["volume"] / b["volume"].rolling(720, min_periods=120).mean()
            fwd = cl.shift(-h) / cl - 1
            n = len(b)
            d = pd.DataFrame({"sc": sc, "vr": vr, "fwd": fwd, "cell": np.arange(n) // h,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year})
            d = d.dropna()
            d["coin"] = c; d["w"] = w
            d["un"] = d["fwd"] - drift[c]
            rows.append(d)
    D = pd.concat(rows)
    A = D[D.sc.abs() >= 2].copy()
    A = A.sort_values("sc", key=lambda s: -s.abs())  # largest move in cell first
    A = A.groupby(["coin", "w", "cell"]).head(1)
    A["dir"] = np.sign(A.sc)
    A["s"] = A["dir"] * A["un"]  # continuation-signed
    def summ(g):
        m = g.s.mean(); return pd.Series({"n": len(g), "mean_pct": m * 100,
                                          "t": m / (g.s.std() / np.sqrt(len(g)))})
    out = {}
    A["vb"] = pd.cut(A.vr, [0, 0.5, 1.5, 3, 1e6], labels=["<0.5", "0.5-1.5", "1.5-3", ">3"])
    A["side"] = np.where(A.dir > 0, "up", "down")
    out["cont6_side_vol"] = A.groupby(["side", "vb"]).apply(summ)
    out["cont6_vol_bothsides"] = A.groupby("vb").apply(summ)
    hv = A[A.vr > 3]
    out["highvol_cont6_by_coin"] = hv.groupby("coin").apply(summ)
    out["highvol_cont6_by_year"] = hv.groupby("yr").apply(summ)
    hv = hv.assign(lvr=np.log(hv.vr))
    out["highvol_slope_s_on_logvr"] = pd.Series(stats.linregress(hv.lvr, hv.s)._asdict())
    out["highvol_slope_s_on_absc"] = pd.Series(stats.linregress(hv.sc.abs(), hv.s)._asdict())
    allv = A.assign(lvr=np.log(A.vr))
    out["all_slope_s_on_logvr"] = pd.Series(stats.linregress(allv.lvr, allv.s)._asdict())
    q = A[(A.vb == "0.5-1.5") & (A.dir > 0)]
    out["quietup_slope_fade_on_sc"] = pd.Series(stats.linregress(q.sc, -q.s)._asdict())
    out["quietup_fade_by_coin"] = q.assign(s=-q.s).groupby("coin").apply(summ)
    return out
