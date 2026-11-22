import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    def summ(g):
        m = g.s.mean(); return pd.Series({"n": len(g), "mean_pct": m * 100,
                                          "t": m / (g.s.std() / np.sqrt(len(g)))})
    for h in [2, 6, 12]:
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
                sc = r1 / r1.abs().rolling(720, min_periods=120).mean()
                vr = b["volume"] / b["volume"].rolling(720, min_periods=120).mean()
                fwd = cl.shift(-h) / cl - 1
                n = len(b)
                d = pd.DataFrame({"sc": sc, "vr": vr, "fwd": fwd, "cell": np.arange(n) // h,
                                  "yr": pd.to_datetime(b["timestamp"]).dt.year})
                d = d.dropna(); d["coin"] = c; d["w"] = w
                d["un"] = d["fwd"] - drift[c]
                rows.append(d)
        D = pd.concat(rows)
        # first qualifying bar in cell (no look-ahead selection)
        Q = D[(D.sc >= 1.5) & (D.vr >= 0.5) & (D.vr <= 1.5)].groupby(["coin", "w", "cell"]).head(1).copy()
        Q["s"] = -Q["un"]
        Q["scb"] = pd.cut(Q.sc, [1.5, 2, 3, 4, 6, 100])
        out[f"quietup_first_h{h}_by_sc"] = Q.groupby("scb").apply(summ)
        lr = stats.linregress(np.log(Q.sc), Q.s)
        out[f"quietup_first_h{h}_slope_logsc"] = pd.Series({"slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(Q)})
        if h == 6:
            Q2 = Q[Q.sc >= 2]
            out["quietup_first_h6_sc2_by_year"] = Q2.groupby("yr").apply(summ)
            out["quietup_first_h6_sc2_by_coin"] = Q2.groupby("coin").apply(summ)
            Dn = D[(D.sc <= -2) & (D.vr >= 0.5) & (D.vr <= 1.5)].groupby(["coin", "w", "cell"]).head(1).copy()
            Dn["s"] = Dn["un"]  # bounce after quiet fall, long-signed
            out["quietdown_first_h6_bounce"] = summ(Dn)
    return out
