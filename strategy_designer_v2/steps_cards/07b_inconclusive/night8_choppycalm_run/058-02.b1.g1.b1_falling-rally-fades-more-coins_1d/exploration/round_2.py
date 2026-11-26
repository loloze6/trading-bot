import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    coin_mean = {}
    for coin, wins in data["bars"].items():
        rs = [pd.Series(b["close"].astype(float).values).pct_change().dropna() for b in wins.values()]
        coin_mean[coin] = pd.concat(rs).mean()
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            r = pd.Series(c).pct_change()
            sd20 = r.rolling(20).std()
            sd30 = r.rolling(30).std()
            ret60 = pd.Series(c) / pd.Series(c).shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(1, n-1):
                d = {"coin": coin, "w": w, "day": ts[i].normalize(), "fall": b.loc[i, "regime"] == "unknown",
                     "r": r[i], "z": r[i]/sd20[i] if sd20[i] > 0 else np.nan, "ret60": ret60[i],
                     "sd30": sd30[i], "x1": c[i+1]/c[i]-1-coin_mean[coin]}
                d["x2"] = c[i+2]/c[i]-1-2*coin_mean[coin] if i+2 < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    df["agit"] = df.groupby("coin")["sd30"].transform(lambda s: s > s.median())
    def tday(col, sub):
        sub = sub.dropna(subset=[col])
        m = sub[col].mean(); dev = sub[col]-m
        gs = dev.groupby(sub["day"]).sum()
        se = np.sqrt((gs**2).sum())/len(sub)
        return len(sub), sub["day"].nunique(), m, m/se if se > 0 else np.nan
    out = {}
    g = {}
    for fall in (True, False):
        for side, cond in (("up", df.r > 0), ("down", df.r <= 0), ("all", df.r.notna())):
            s = df[(df.fall == fall) & cond]
            n, nd, m, t = tday("x1", s)
            n2, _, m2, t2 = tday("x2", s)
            g[f"fall={fall}_{side}"] = {"n": n, "days": nd, "x1": m, "t1": t, "x2": m2, "t2": t2}
    out["next_day_by_profile_and_side"] = pd.DataFrame(g).T
    f = df[df.fall & df.z.notna()].copy()
    f["zq"] = pd.qcut(f["z"], 6, labels=False)
    g = {}
    for k, s in f.groupby("zq"):
        n, nd, m, t = tday("x1", s)
        g[k] = {"n": n, "z_mean": s.z.mean(), "x1": m, "t1": t}
    out["falling_by_z_sextile"] = pd.DataFrame(g).T
    ff = f.dropna(subset=["ret60"]).copy()
    ff["tq"] = pd.qcut(ff["ret60"], 3, labels=False)
    g = {}
    for (k, up), s in ff.groupby(["tq", ff.r > 0]):
        n, nd, m, t = tday("x1", s)
        g[f"trend_t{k}_up={up}"] = {"n": n, "ret60_mean": s.ret60.mean(), "x1": m, "t1": t}
    out["falling_by_trend_depth"] = pd.DataFrame(g).T
    g = {}
    for (a, up), s in f.groupby(["agit", f.r > 0]):
        n, nd, m, t = tday("x1", s)
        g[f"agit={a}_up={up}"] = {"n": n, "x1": m, "t1": t}
    out["falling_by_agitation"] = pd.DataFrame(g).T
    s = f.dropna(subset=["ret60", "x1"])
    out["spearman_ret60_x1_falling"] = stats.spearmanr(s.ret60, s.x1)[0]
    out["spearman_z_x1_falling_all"] = stats.spearmanr(f.z, f.x1)[0]
    return out
