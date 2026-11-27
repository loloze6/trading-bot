def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","regime","forecast","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            c = d["close"]
            d["r1"] = c.pct_change()
            d["ret30"] = c / c.shift(30) - 1
            d["ret60"] = c / c.shift(60) - 1
            d["vol30"] = d["r1"].rolling(30, min_periods=20).std()
            d["z1"] = d["r1"] / d["vol30"].shift(1)
            for h in (1, 3, 7, 14, 21):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            ts = pd.to_datetime(d["timestamp"])
            d["day"] = ts.dt.floor("D"); d["wd"] = ts.dt.weekday; d["year"] = ts.dt.year
            d["choppy"] = d["regime"] == "mean_reversion"
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    medv = A.groupby("coin")["vol30"].median()
    A["agit"] = A["vol30"] > A["coin"].map(medv)
    A["trend"] = np.where(A["choppy"], "choppy", np.where(A["ret60"] > 0.10, "rising", np.where(A["ret60"] < -0.10, "falling", "na")))
    def ctt(g):
        g = g.dropna(subset=["ex"])
        N = len(g)
        if N < 3: return (N, np.nan, np.nan, 0)
        m = g["ex"].mean()
        S = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((S**2).sum()) / N
        return (N, round(m,4), round(m/se,2) if se>0 else np.nan, g["day"].nunique())
    def grid(h):
        g = A[A["pos"] % h == 0].dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift)
        return g
    out = {}
    # choppy ret30 continuation, clustered, by horizon
    res = []
    for h in (3, 7, 14, 21):
        g = grid(h); s = g[g.choppy].dropna(subset=["ret30"]).copy()
        s["q"] = pd.qcut(s["ret30"].rank(method="first"), 5, labels=False)
        for q, sub in s.groupby("q"):
            res.append((h, q) + ctt(sub))
        sub = s.copy(); sub["ex"] = sub["ex"] * np.sign(sub["ret30"])
        res.append((h, "signed") + ctt(sub))
    out["choppy ret30 q -> ex, clustered"] = pd.DataFrame(res, columns=["h","q","n","ex","t_day","days"])
    # choppy ret30 7d by agitation, by sign, by window halves
    g = grid(7); s = g[g.choppy].dropna(subset=["ret30","vol30"]).copy()
    s["ex_s"] = s["ex"] * np.sign(s["ret30"])
    res = []
    for k, sub in s.groupby(["agit", s["ret30"] > 0]):
        x = sub.copy(); x["ex"] = x["ex_s"]; res.append(k + ctt(x))
    out["choppy 7d signed by agit, up"] = pd.DataFrame(res, columns=["agit","up","n","ex","t_day","days"])
    res = []
    for k, sub in s.groupby("win"):
        x = sub.copy(); x["ex"] = x["ex_s"]; res.append((k,) + ctt(x))
    out["choppy 7d signed by window"] = pd.DataFrame(res, columns=["win","n","ex","t_day","days"])
    # z-scaled ret30 (graded) correlation inside choppy
    s["z30"] = s["ret30"] / (s["vol30"] * np.sqrt(30))
    out["choppy 7d corr ret30,ex ; z30,ex"] = f"{s['ret30'].corr(s['ex']):.3f} ; {s['z30'].corr(s['ex']):.3f} ; n {len(s)}"
    # other profiles: ret30 at 7d signed
    res = []
    for k, sub in g.dropna(subset=["ret30","vol30"]).groupby(["trend","agit"]):
        x = sub.copy(); x["ex"] = x["ex"] * np.sign(x["ret30"]); res.append(k + ctt(x))
    out["7d ret30-signed by profile"] = pd.DataFrame(res, columns=["trend","agit","n","ex","t_day","days"])
    # weekday clustered by day (one day = all coins)
    g1 = A.dropna(subset=["f1"]).copy(); g1["ex"] = g1["f1"] - g1["coin"].map(g1.groupby("coin")["f1"].mean())
    res = []
    for k, sub in g1.groupby("wd"): res.append((k,) + ctt(sub))
    out["next-day ex by weekday of bar, clustered"] = pd.DataFrame(res, columns=["wd_of_bar","n","ex","t_day","days"])
    res = []
    for k, sub in g1.groupby(["wd","year"]):
        if k[0] in (4,): res.append(k + ctt(sub))
    out["fri bar->sat ex by year"] = pd.DataFrame(res, columns=["wd","year","n","ex","t_day","days"])
    # z1 rebound by profile, clustered
    g1 = g1.dropna(subset=["z1","vol30"])
    g1["zd"] = pd.qcut(g1["z1"].rank(method="first"), 10, labels=False)
    res = []
    for k, sub in g1[g1.zd == 0].groupby(["trend","agit"]): res.append(k + ctt(sub))
    out["largest down day -> next day ex by profile"] = pd.DataFrame(res, columns=["trend","agit","n","ex","t_day","days"])
    return out
