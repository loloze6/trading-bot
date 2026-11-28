import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                if len(idx):
                    rr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr) if rr else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(r).rolling(30, min_periods=20).std().values
            inprof = b["regime"].isin(["trending", "unknown"]).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            for t in range(3, len(c)):
                if not inprof[t] or not np.isfinite(r[t]) or r[t] <= 0:
                    continue
                k = 0; dep = 0.0; j = t - 1
                while j >= 1 and r[j] < 0 and k < 30:
                    k += 1; dep += r[j]; j -= 1
                if k < 1:
                    continue
                v = vol[t]
                if not (v and v > 0):
                    continue
                d = dict(coin=coin, win=w, yr=yr[t], run=k, dep=dep / v, force=r[t] / v,
                         rawdep=dep, day=day[t], half="early" if yr[t] <= 2019 else "late")
                for h in H:
                    d["u%d" % h] = (c[t + h] / c[t] - 1 - drift[(coin, h)]) if t + h < len(c) else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    df["shallow_score"] = df.dep  # higher = shallower

    def summ(g):
        res = {}
        for h in H:
            x = g["u%d" % h].dropna()
            res["m%d" % h] = x.mean()
            res["t%d" % h] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 and x.std() > 0 else np.nan
        res["n"] = len(g)
        return pd.Series(res)

    out = {}
    for name, sub in [("run>=2", df[df.run >= 2]), ("run>=1", df)]:
        s = sub.copy()
        s["depq"] = pd.qcut(s.dep, 3, labels=["deep", "mid", "shallow"])
        out["depth_terc_" + name] = s.groupby("depq").apply(summ)
        out["depth_terc_by_half_" + name] = s.groupby(["half", "depq"]).apply(summ)
        out["depth_terc_by_coin_" + name] = s.groupby(["coin", "depq"])["u5"].agg(["mean", "count"]).unstack()
        # day-clustered slope of u5 on dep
        x = s.dropna(subset=["u5"])
        X = x.dep.values; Y = x.u5.values
        Xc = X - X.mean()
        beta = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = Y - Y.mean() - beta * Xc
        sc = pd.Series(Xc * e).groupby(x.day.values).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (Xc ** 2).sum()
        out["slope_u5_on_depth_" + name] = pd.DataFrame(
            {"beta": [beta], "t_day_clustered": [beta / se], "days": [G], "n": [len(x)],
             "spearman": [stats.spearmanr(X, Y)[0]]})
        # raw depth (not vol scaled)
        out["rawdepth_spearman_" + name] = pd.DataFrame(
            {h: [stats.spearmanr(x.rawdep, x["u%d" % h], nan_policy="omit")[0]] for h in H})
    return out
