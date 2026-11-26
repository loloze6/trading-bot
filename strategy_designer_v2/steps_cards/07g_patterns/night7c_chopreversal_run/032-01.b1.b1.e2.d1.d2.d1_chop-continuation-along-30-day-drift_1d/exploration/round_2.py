import numpy as np, pandas as pd
from scipy import stats

def clt(vals, keys):
    d = pd.DataFrame({"v": vals.values, "k": keys.values}).dropna()
    m = d["v"].mean()
    s = (d["v"] - m).groupby(d["k"]).sum()
    se = np.sqrt((s ** 2).sum()) / len(d)
    return len(d), d["k"].nunique(), m, m / se if se > 0 else np.nan

def explore(data):
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r1 = cl.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": c, "w": w, "pos": np.arange(len(b)),
                              "r1": r1, "r7": cl / cl.shift(7) - 1, "r30": cl / cl.shift(30) - 1,
                              "er": (cl - cl.shift(30)).abs() / cl.diff().abs().rolling(30).sum(),
                              "vol": r1.rolling(30).std(), "f7": cl.shift(-7) / cl - 1,
                              "f1": cl.shift(-1) / cl - 1, "wd": ts.dt.weekday, "yr": ts.dt.year,
                              "day": ts.dt.floor("D").astype(np.int64) // 86400_000_000_000})
            d["sc"] = d["r7"] / (d["vol"] * np.sqrt(7))
            d["sc30"] = d["r30"] / (d["vol"] * np.sqrt(30))
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # weekday, day-clustered, by year
    D = A.dropna(subset=["f1"])
    D = D.assign(u1=D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean()))
    wk = []
    for wd, g in D.groupby("wd"):
        n, nd, m, t = clt(g["u1"], g["day"])
        wk.append({"wd": wd, "n": n, "days": nd, "mean_u1": m, "t_cl": t,
                   "share_years_pos": (g.groupby("yr")["u1"].mean() > 0).mean()})
    out["weekday_clustered"] = pd.DataFrame(wk)
    out["weekday_by_year"] = D.groupby(["yr", "wd"])["u1"].mean().unstack()
    G = A[A["pos"] % 7 == 0].copy()
    G["u7"] = G["f7"] - G["coin"].map(G.groupby("coin")["f7"].mean())
    G = G.dropna(subset=["sc", "er", "u7", "r30"])
    G["agree"] = np.sign(G["r7"]) == np.sign(G["r30"])
    # signed by 30-day direction: trend-resumption in high ER, against-the-week
    G["s30u"] = np.sign(G["r30"]) * G["u7"]
    res = []
    for name, m in [("ER>=.3 disagree", (G["er"] >= .3) & ~G["agree"]),
                    ("ER>=.3 agree", (G["er"] >= .3) & G["agree"]),
                    ("ER<.3 disagree", (G["er"] < .3) & ~G["agree"]),
                    ("ER<.3 agree", (G["er"] < .3) & G["agree"]),
                    ("all", G["er"] >= 0)]:
        g = G[m]
        n, nd, mm, t = clt(g["s30u"], g["day"])
        sl = stats.linregress(g["sc30"], g["u7"])
        res.append({"set": name, "n": n, "days": nd, "mean_u7_along_30d": mm, "t_cl": t,
                    "slope_on_sc30": sl.slope, "t_slope": sl.slope / sl.stderr})
    out["along_30d"] = pd.DataFrame(res)
    # graded 30-day scaled move, by tercile of |sc30|, all bars
    G["s30b"] = pd.qcut(G["sc30"].abs(), 4, labels=["q1", "q2", "q3", "q4"])
    rr = []
    for q, g in G.groupby("s30b", observed=True):
        n, nd, mm, t = clt(g["s30u"], g["day"])
        rr.append({"q": q, "n": n, "mean_u7_along_30d": mm, "t_cl": t,
                   "up_mean": g[g["r30"] > 0]["s30u"].mean(), "down_mean": g[g["r30"] < 0]["s30u"].mean()})
    out["sc30_quartiles"] = pd.DataFrame(rr)
    # agree chop: up vs down side; vol level
    C = G[(G["er"] < .3) & G["agree"]].copy()
    C["s_u"] = np.sign(C["sc"]) * C["u7"]
    C["side"] = np.where(C["r7"] > 0, "up", "down")
    C["volb"] = pd.qcut(C.groupby("coin")["vol"].rank(pct=True), 3, labels=["lo", "mid", "hi"])
    rr = []
    for k, g in C.groupby(["side", "volb"], observed=True):
        n, nd, mm, t = clt(g["s_u"], g["day"])
        rr.append({"side": k[0], "vol": k[1], "n": n, "mean": mm, "t_cl": t})
    out["chop_side_vol"] = pd.DataFrame(rr)
    # vol as grade across all bars: continuation of 7d scaled by inverse vol?
    G["volr"] = G.groupby("coin")["vol"].rank(pct=True)
    G["s7u"] = np.sign(G["r7"]) * G["u7"]
    G["volb"] = pd.qcut(G["volr"], 4, labels=["v1", "v2", "v3", "v4"])
    rr = []
    for k, g in G.groupby("volb", observed=True):
        n, nd, mm, t = clt(g["s7u"], g["day"])
        n2, _, m2, t2 = clt(g["s30u"], g["day"])
        rr.append({"vol": k, "n": n, "mean_along_7d": mm, "t7": t, "mean_along_30d": m2, "t30": t2})
    out["vol_quartiles_all"] = pd.DataFrame(rr)
    return out
