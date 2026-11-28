import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [1, 2, 3, 5, 10]
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
            for t in range(3, len(c)):
                if not inprof[t] or not np.isfinite(r[t]):
                    continue
                k = 0; dep = 0.0; j = t - 1
                while j >= 1 and r[j] < 0 and k < 30:
                    k += 1; dep += r[j]; j -= 1
                v = vol[t]
                d = dict(coin=coin, win=w, yr=yr[t], up=r[t] > 0, run=k,
                         dep=(dep / v) if v and v > 0 else np.nan,
                         force=(r[t] / v) if v and v > 0 else np.nan,
                         turn=(r[t] > 0 and k >= 2))
                for h in H:
                    d["u%d" % h] = (c[t + h] / c[t] - 1 - drift[(coin, h)]) if t + h < len(c) else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)

    def summ(g):
        res = {}
        for h in H:
            x = g["u%d" % h].dropna()
            res["m%d" % h] = x.mean()
            res["t%d" % h] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 and x.std() > 0 else np.nan
        res["n"] = len(g)
        return pd.Series(res)

    df["grp"] = np.where(df.turn, "turn",
                np.where(df.up & (df.run == 1), "up_after_1down",
                np.where(df.up, "up_after_up",
                np.where(df.run >= 1, "down_in_run", "down_after_up"))))
    out = {}
    out["by_group_inprofile"] = df.groupby("grp").apply(summ)
    tu = df[df.turn].copy()
    tu["runb"] = tu.run.clip(upper=5)
    out["turn_by_runlen"] = tu.groupby("runb").apply(summ)
    tu["depq"] = pd.qcut(tu.dep, 3, labels=["deep", "mid", "shallow"])
    out["turn_by_depth"] = tu.groupby("depq").apply(summ)
    tu["fq"] = pd.qcut(tu.force, 3, labels=["weak", "mid", "strong"])
    out["turn_by_force"] = tu.groupby("fq").apply(summ)
    out["turn_by_coin"] = tu.groupby("coin").apply(summ)
    out["turn_by_year"] = tu.groupby("yr").apply(summ)
    dn = df[~df.up].copy()
    dn["k_incl_today"] = (dn.run + 1).clip(upper=5)
    out["down_day_by_runlen"] = dn.groupby("k_incl_today").apply(summ)
    out["rank_corr_turn"] = pd.DataFrame(
        {h: [stats.spearmanr(tu.dep, tu["u%d" % h], nan_policy="omit")[0],
             stats.spearmanr(tu.force, tu["u%d" % h], nan_policy="omit")[0],
             stats.spearmanr(tu.run, tu["u%d" % h], nan_policy="omit")[0]] for h in H},
        index=["rho_depth", "rho_force", "rho_runlen"])
    return out
