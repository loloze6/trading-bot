import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []; drift = {}
    H = [1, 3, 5]
    for coin, wins in data["bars"].items():
        dr = {h: [] for h in H}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float); n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h); dr[h] += list(c[idx + h] / c[idx] - 1)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            run = np.zeros(n); depth = np.zeros(n); brkrun = np.zeros(n); brkdepth = np.zeros(n)
            cur = 0; curd = 0.0
            for i in range(1, n):
                if r1[i] < 0:
                    cur += 1; curd += r1[i]; run[i] = cur; depth[i] = curd
                else:
                    if r1[i] > 0: brkrun[i] = cur; brkdepth[i] = curd
                    cur = 0; curd = 0.0
            r3 = np.r_[[np.nan]*3, c[3:] / c[:-3] - 1]
            r5 = np.r_[[np.nan]*5, c[5:] / c[:-5] - 1]
            inprof = b["regime"].astype(str).values != "chop"
            yrs = pd.to_datetime(b["timestamp"]).dt.year.values
            days = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            for i in range(n):
                s = sd30[i] if sd30[i] > 0 else np.nan
                d = {"coin": coin, "win": w, "wn": int(w[1:]), "pos": i, "inprof": inprof[i],
                     "run": run[i], "depthz": -depth[i] / s, "brkrun": brkrun[i],
                     "brkdepthz": -brkdepth[i] / s, "r1z": r1[i] / s,
                     "r3z": -r3[i] / (s * np.sqrt(3)), "r5z": -r5[i] / (s * np.sqrt(5)),
                     "year": yrs[i], "day": days[i]}
                for h in H: d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
        drift[coin] = {h: np.mean(dr[h]) for h in H}
    df = pd.DataFrame(rows)
    for h in H: df[f"u{h}"] = df[f"f{h}"] - df["coin"].map(lambda k: drift[k][h])

    def grid(sub, h):
        sub = sub.dropna(subset=[f"u{h}"]).copy(); sub["cell"] = sub["pos"] // h
        return sub.groupby(["coin", "win", "cell"]).first().reset_index()
    def summ(g, h, x=None):
        if len(g) < 8: return pd.Series({"n": len(g)})
        dd = g.groupby("day")[f"u{h}"].sum(); m = g[f"u{h}"].mean(); G = len(dd)
        se = np.sqrt((dd ** 2).sum() * G / (G - 1)) / len(g)
        r = {"n": len(g), "days": G, "mean_u%": 100 * m, "t": m / se}
        if x is not None:
            gg = g.dropna(subset=[x])
            lr = stats.linregress(gg[x], gg[f"u{h}"]); r["slope%"] = 100 * lr.slope; r["slope_t"] = lr.slope / lr.stderr
        return pd.Series(r)
    out = {}
    ip = df[df.inprof]
    tests = {
        "downday_run>=1_x_depthz": (ip[ip.run >= 1], "depthz"),
        "downday_run>=2_x_depthz": (ip[ip.run >= 2], "depthz"),
        "downday_run>=1_x_run": (ip[ip.run >= 1], "run"),
        "break_x_brkdepthz": (ip[ip.brkrun >= 2], "brkdepthz"),
        "break_x_brkrun": (ip[ip.brkrun >= 2], "brkrun"),
        "break_x_r1z": (ip[ip.brkrun >= 2], "r1z"),
        "allbars_x_r3fallz": (ip, "r3z"),
        "allbars_x_r5fallz": (ip, "r5z"),
        "r3fall_pos_x_r3z": (ip[ip.r3z > 0], "r3z"),
    }
    tab = []
    for k, (s, x) in tests.items():
        for h in H:
            r = summ(grid(s, h), h, x); r["set"] = k; r["h"] = h; tab.append(r)
    out["slopes"] = pd.DataFrame(tab).set_index(["set", "h"]).round(3)
    # deep down run (still falling) by depth tercile, coin, half
    s = ip[ip.run >= 1]
    g = grid(s, 3); g["dq"] = pd.qcut(g["depthz"], 3, labels=["shallow", "mid", "deep"])
    g["half"] = np.where(g.wn <= 9, "w1-9", "w10-18")
    t2 = []
    for col in ["dq", "coin", "half"]:
        for v, sg in g.groupby(col, observed=True):
            r = summ(sg, 3, "depthz"); r["by"] = col; r["v"] = str(v); t2.append(r)
    for v, sg in g[g.dq == "deep"].groupby("coin"):
        r = summ(sg, 3); r["by"] = "deep_coin"; r["v"] = v; t2.append(r)
    for v, sg in g[g.dq == "deep"].groupby("half"):
        r = summ(sg, 3); r["by"] = "deep_half"; r["v"] = v; t2.append(r)
    out["downday_groups_h3"] = pd.DataFrame(t2).set_index(["by", "v"]).round(3)
    # break days depth groups by half & coin
    gb = grid(ip[ip.brkrun >= 2], 3); gb["half"] = np.where(gb.wn <= 9, "w1-9", "w10-18")
    t3 = []
    for col in ["coin", "half"]:
        for v, sg in gb.groupby(col):
            r = summ(sg, 3, "brkdepthz"); r["by"] = col; r["v"] = str(v); t3.append(r)
    out["break_depth_slope_groups_h3"] = pd.DataFrame(t3).set_index(["by", "v"]).round(3)
    return out
