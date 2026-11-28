import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [1, 2, 3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        dr = {h: [] for h in H}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                dr[h] += list(c[idx + h] / c[idx] - 1)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # prior down run length broken by today's up close
            run = np.zeros(n); downrun = np.zeros(n); cur = 0
            depth = np.zeros(n); curd = 0.0
            for i in range(1, n):
                if r1[i] < 0:
                    cur += 1; curd += r1[i]; downrun[i] = cur
                else:
                    if r1[i] > 0:
                        run[i] = cur; depth[i] = curd
                    cur = 0; curd = 0.0
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().shift(0).values
            reg = b["regime"].astype(str).values
            inprof = reg != "chop"
            for i in range(n):
                d = {"coin": coin, "win": w, "pos": i, "inprof": inprof[i], "run": run[i],
                     "downrun": downrun[i], "r1": r1[i], "z": r1[i] / sd30[i] if sd30[i] > 0 else np.nan,
                     "depthz": depth[i] / sd30[i] if sd30[i] > 0 else np.nan,
                     "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(b["timestamp"].iloc[i]).floor("D")}
                for h in H:
                    d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
        drift[coin] = {h: np.mean(dr[h]) for h in H}
    df = pd.DataFrame(rows)
    for h in H:
        df[f"u{h}"] = df[f"f{h}"] - df["coin"].map(lambda k: drift[k][h])

    def grid(sub, h):
        sub = sub.dropna(subset=[f"u{h}"]).copy()
        sub["cell"] = sub["pos"] // h
        return sub.groupby(["coin", "win", "cell"]).first().reset_index()

    def summ(sub, h):
        g = grid(sub, h)
        if len(g) < 5: return pd.Series({"n": len(g)})
        dd = g.groupby("day")[f"u{h}"].sum()
        m = g[f"u{h}"].mean(); G = len(dd)
        se = np.sqrt((dd ** 2).sum() * G / (G - 1)) / len(g)
        return pd.Series({"n": len(g), "days": G, "mean_u%": 100 * m, "t": m / se,
                          "mean_tot%": 100 * g[f"f{h}"].mean()})

    out = {}
    brk = df[(df.run >= 2)]
    sets = {"break_inprof": brk[brk.inprof], "break_outprof": brk[~brk.inprof],
            "inprof_all": df[df.inprof], "inprof_downday2plus": df[df.inprof & (df.downrun >= 2)],
            "inprof_downday3plus": df[df.inprof & (df.downrun >= 3)],
            "inprof_bigdown_z<-1.5": df[df.inprof & (df.z < -1.5)],
            "inprof_bigup_z>1.5": df[df.inprof & (df.z > 1.5)],
            "inprof_upday_any": df[df.inprof & (df.r1 > 0)]}
    tab = []
    for k, s in sets.items():
        for h in H:
            r = summ(s, h); r["set"] = k; r["h"] = h; tab.append(r)
    out["sets_by_h"] = pd.DataFrame(tab).set_index(["set", "h"]).round(3)

    bi = brk[brk.inprof].copy()
    bi["zq"] = pd.qcut(bi["z"], 3, labels=["low", "mid", "high"])
    bi["runc"] = bi["run"].clip(upper=4)
    bi["dq"] = pd.qcut(bi["depthz"], 3, labels=["shallow", "mid", "deep"])
    t2 = []
    for col in ["zq", "runc", "dq", "coin", "year"]:
        for v, s in bi.groupby(col, observed=True):
            for h in [3, 5, 10]:
                r = summ(s, h); r["by"] = col; r["v"] = str(v); r["h"] = h; t2.append(r)
    out["break_inprof_groups"] = pd.DataFrame(t2).set_index(["by", "v", "h"]).round(3)
    return out
