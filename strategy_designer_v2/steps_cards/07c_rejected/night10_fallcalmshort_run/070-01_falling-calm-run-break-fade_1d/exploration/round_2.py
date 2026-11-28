import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            reg = b["regime"].astype(str).values
            cur = 0; start = None
            for i in range(1, n):
                if r[i] < 0:
                    if cur == 0: start = i - 1
                    cur += 1
                else:
                    if r[i] > 0 and cur >= 1 and reg[i] != "chop":
                        d = {"coin": coin, "w": w, "run": cur,
                             "depth": c[i - 1] / c[start] - 1, "r0": r[i],
                             "retr": r[i] / max(1e-9, -(c[i - 1] / c[start] - 1)),
                             "pos": i}
                        for h in (1, 2, 3, 5):
                            d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                        rows.append(d)
                    cur = 0
    df = pd.DataFrame(rows)
    # coin drift over all its explore windows, all days
    mus = {}
    for coin, wins in data["bars"].items():
        rr = []
        for w, b in wins.items():
            cc = b["close"].astype(float).values
            rr.append(cc[1:] / cc[:-1] - 1)
        mus[coin] = np.concatenate(rr).mean()
    for h in (1, 2, 3, 5):
        df[f"x{h}"] = df[f"f{h}"] - h * df["coin"].map(mus)
    out = {}
    g2 = df[df.run >= 2].copy()
    res = {}
    for h in (1, 2, 3, 5):
        s = g2.dropna(subset=[f"x{h}"])
        res[f"h{h}"] = {
            "n": len(s), "mean_x": s[f"x{h}"].mean(),
            "t": s[f"x{h}"].mean() / (s[f"x{h}"].std() / np.sqrt(len(s))),
            "spear_run": stats.spearmanr(s["run"], s[f"x{h}"])[0],
            "spear_depth": stats.spearmanr(s["depth"], s[f"x{h}"])[0],
            "spear_retr": stats.spearmanr(s["retr"], s[f"x{h}"])[0],
            "spear_depth_p": stats.spearmanr(s["depth"], s[f"x{h}"])[1],
            "spear_run_p": stats.spearmanr(s["run"], s[f"x{h}"])[1]}
    out["run2+_grading"] = pd.DataFrame(res).T
    g1 = df.copy()
    g1["dq"] = pd.qcut(g1["depth"], 3, labels=["deep", "mid", "shallow"])
    def summ(g):
        o = {"n": len(g)}
        for h in (1, 2, 3):
            x = g[f"x{h}"].dropna()
            o[f"x{h}"] = x.mean(); o[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(o)
    out["all_runs_by_depth_tercile"] = g1.groupby("dq").apply(summ)
    g1["rq"] = pd.qcut(g1["retr"].rank(method="first"), 3, labels=["small_retr", "mid_retr", "big_retr"])
    out["all_runs_by_retracement"] = g1.groupby("rq").apply(summ)
    out["run2+_by_window"] = g2.groupby("w").apply(summ)
    out["drift"] = pd.Series(mus)
    return out
