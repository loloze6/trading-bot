import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 5]
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
            r30 = c / c.shift(30) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in H:
                fwd = c.shift(-h) / c - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "i": np.arange(len(df)), "vr": vr, "vs": vs,
                                          "r30": r30, "fc": df["forecast"], "fwd": fwd - base[(coin, h)], "yr": yr}))
    A = pd.concat(rows).dropna(subset=["vr", "vs", "fwd"])

    def deover(d, h):
        d = d.sort_values(["coin", "w", "i"])
        keep = []
        for (cn, w), g in d.groupby(["coin", "w"]):
            last = -10**9
            for ix, i in zip(g.index, g["i"]):
                if i - last >= h:
                    keep.append(True); last = i
                else:
                    keep.append(False)
        return d[np.array(keep)] if len(keep) else d

    def summ(x):
        x = x.dropna(); n = len(x)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})

    out = {}
    e5 = deover(A[(A.h == 5) & (A.fc <= -2)].reset_index(drop=True), 5)
    e5["trend"] = np.where(e5.r30 > 0, "r30>0", "r30<=0")
    out["tested_by_30d_trend"] = e5.groupby("trend")["fwd"].apply(summ).unstack()
    e5["vb"] = pd.cut(e5.vr, [0, 0.5, 0.75])
    out["tested_by_trend_vband"] = e5.groupby(["trend", "vb"])["fwd"].apply(summ).unstack()

    # heavy-volume rises h5: graded and by year
    r = A[(A.h == 5) & (A.vs > 1) & (A.vr > 1.5)].reset_index(drop=True)
    r = deover(r, 5)
    r["vq"] = pd.qcut(r.vr, 3)
    out["heavyrise_h5_by_vr_tercile"] = r.groupby("vq")["fwd"].apply(summ).unstack()
    out["heavyrise_h5_by_year"] = r.groupby("yr")["fwd"].apply(summ).unstack()
    out["heavyrise_h5_by_trend"] = r.assign(tr=np.where(r.r30 > 0, "up", "down")).groupby("tr")["fwd"].apply(summ).unstack()
    out["heavyrise_h5_by_coin"] = r.groupby("coin")["fwd"].apply(summ).unstack()
    # all rises, graded: corr of fwd5 with vr*vs among vs>1
    rr = deover(A[(A.h == 5) & (A.vs > 1)].reset_index(drop=True), 5)
    rr["lv"] = np.log(rr.vr)
    rr["lvq"] = pd.qcut(rr.lv, 5)
    out["allrise_h5_by_vr_quint"] = rr.groupby("lvq")["fwd"].apply(summ).unstack()
    out["allrise_h5_corr_logvr"] = float(rr[["lv", "fwd"]].corr().iloc[0, 1])
    out["allrise_h5_n"] = len(rr)
    return out
