import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    H = [2, 6, 12, 24]
    # drift per coin per horizon: non-overlapping grid
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs)
            drift[(c, h)] = rs.mean(); usual[(c, h)] = rs.std()
    # recorded cases: first bar per 24-cell with forecast >= 2
    rows = []
    rawrows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            f = b["forecast"].fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            cell = np.arange(n) // 24
            df = pd.DataFrame({"f": f, "cell": cell})
            cand = df[df.f >= 2]
            first = cand.groupby("cell").head(1).index.values
            for i in first:
                r = {"coin": c, "win": w, "year": ts.iloc[i].year, "hour": ts.iloc[i].hour, "f": f[i]}
                ok = True
                for h in H:
                    if i + h < n:
                        r[f"u{h}"] = (cl[i + h] / cl[i] - 1 - drift[(c, h)])
                    else:
                        r[f"u{h}"] = np.nan
                r["r1"] = cl[i] / cl[i - 1] - 1 if i > 0 else np.nan
                rows.append(r)
            # raw score both sides, recomputed
            ret = pd.Series(cl).pct_change()
            sd = ret.rolling(720, min_periods=240).std()
            v = b["volume"].astype(float)
            vr = v / v.rolling(720, min_periods=240).mean()
            z = ret / sd
            for h in [6, 24]:
                cellh = np.arange(n) // h
                d = pd.DataFrame({"z": z.values, "vr": vr.values, "cell": cellh})
                d = d[(d.z.abs() >= 3)]
                fi = d.groupby("cell").head(1)
                for i, rr in fi.iterrows():
                    if i + h < n:
                        rawrows.append({"coin": c, "h": h, "side": np.sign(rr.z), "zabs": abs(rr.z), "vr": rr.vr,
                                        "m": np.sign(rr.z) * (cl[i + h] / cl[i] - 1 - drift[(c, h)])})
    R = pd.DataFrame(rows)
    def summ(g):
        res = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            res[f"mean{h}"] = x.mean(); res[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        res["n"] = len(g)
        return pd.Series(res)
    out["cases_all"] = summ(R)
    out["by_coin"] = R.groupby("coin").apply(summ)
    out["by_year"] = R.groupby("year").apply(summ)
    R["fq"] = pd.qcut(R.f.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_fquart"] = R.groupby("fq").apply(summ)
    out["f_quart_range"] = R.groupby("fq").f.agg(["min", "max", "mean"])
    w = R.groupby("win").u24.mean()
    out["windows_pos_share_u24"] = float((w > 0).mean())
    out["window_mean_u24_std"] = float(w.std())
    Q = pd.DataFrame(rawrows)
    Q["vb"] = pd.cut(Q.vr, [0, 1.5, 3, 6, np.inf], labels=["<1.5", "1.5-3", "3-6", ">6"])
    def s2(g):
        x = g.m.dropna()
        return pd.Series({"mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "n": len(x)})
    out["raw_abs_z3_by_h_side_vol"] = Q.groupby(["h", "side", "vb"]).apply(s2)
    return out
