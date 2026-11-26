import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            L30 = l.shift(1).rolling(30, min_periods=30).min()
            vol30 = r1.rolling(30, min_periods=20).std()
            vol_rel = vol30 / r1.rolling(90, min_periods=60).std()
            rng = (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "day": ts.dt.floor("D").astype("int64"),
                "year": ts.dt.year,
                "ret60": c / c.shift(60) - 1, "ret30": c / c.shift(30) - 1,
                "vol_rel": vol_rel,
                "z5": (c / c.shift(5) - 1) / (vol30 * np.sqrt(5)),
                "z1": r1 / vol30.shift(1),
                "pr": (l < L30) & (c > L30),
                "reclaim": (c - L30) / rng,
                "f5": c.shift(-5) / c - 1,
                "f3": c.shift(-3) / c - 1,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 5 == 0) & A["f5"].notna()].copy()
    drift = G["f5"].mean()
    G["ex"] = G["f5"] - drift
    G["trend"] = np.where(G["ret60"] < -0.1, "fall", np.where(G["ret60"] > 0.1, "rise", "chop"))
    G.loc[G["ret60"].isna(), "trend"] = "na"
    G["agit"] = np.where(G["vol_rel"].isna(), "na", np.where(G["vol_rel"] > 1, "ag", "calm"))

    def ct(x, days):
        d = pd.DataFrame({"x": x.values, "d": days.values}).groupby("d")["x"].sum()
        nd = len(d); n = len(x)
        if nd < 3: return np.nan, nd
        se = np.sqrt(((d - d.index.map(lambda k: 0)) ** 2).sum()) if False else None
        m = x.mean()
        dd = pd.DataFrame({"x": x.values - m, "d": days.values}).groupby("d")["x"].sum()
        se = np.sqrt((dd ** 2).sum()) / n
        return m / se, nd

    out = {}
    res = {}
    for tr in ["chop", "fall", "rise"]:
        for ag in ["ag", "calm"]:
            s = G[(G["trend"] == tr) & (G["agit"] == ag) & G["z5"].notna()]
            if len(s) < 10: continue
            rho, p = stats.spearmanr(s["z5"], s["ex"])
            neg = s[s["z5"] < 0]
            rho2, p2 = stats.spearmanr(neg["z5"], neg["ex"]) if len(neg) > 5 else (np.nan, np.nan)
            low = s[s["z5"] <= s["z5"].quantile(0.25)]
            t, nd = ct(low["ex"], low["day"])
            res[(tr, ag)] = pd.Series({"n": len(s), "rho_z5_ex": rho, "p": p, "n_neg": len(neg), "rho_neg": rho2, "p_neg": p2,
                                       "low25_mean": low["ex"].mean(), "low25_t_day": t, "low25_days": nd})
    out["z5 grading by trend x agitation"] = pd.DataFrame(res).T

    ch = G[(G["trend"] == "chop") & G["z5"].notna()].copy()
    ch["neg"] = ch["z5"] < -0.5
    out["chop, z5<-0.5 by year"] = ch[ch["neg"]].groupby("year")["ex"].agg(["count", "mean"])
    out["chop, z5<-0.5 by window"] = ch[ch["neg"]].groupby("win")["ex"].agg(["count", "mean"])
    out["chop all by z5 sign x agit"] = ch.groupby([ch["z5"] < 0, "agit"])["ex"].agg(["count", "mean"])

    # reclaim grading in falling market, all event bars (non-overlap per coin-window: keep first per 5 bars)
    P = A[A["pr"] & A["f5"].notna() & (A["ret60"] < -0.1)].copy()
    P = P.sort_values(["coin", "win", "pos"])
    keep = []; last = {}
    for i, r in P.iterrows():
        k = (r["coin"], r["win"])
        if k not in last or r["pos"] - last[k] >= 5:
            keep.append(i); last[k] = r["pos"]
    P = P.loc[keep]
    P["ex"] = P["f5"] - drift
    rho, p = stats.spearmanr(P["reclaim"], P["ex"])
    out["falling pierce-reclaim: reclaim vs ex"] = pd.Series({"n": len(P), "rho": rho, "p": p, "days": P["day"].nunique()})
    P["rq"] = pd.qcut(P["reclaim"], 3, labels=False, duplicates="drop")
    out["falling pr by reclaim tercile"] = P.groupby("rq")["ex"].agg(["count", "mean", "median"])
    P["ag"] = P["vol_rel"] > 1
    out["falling pr by reclaim tercile x agit"] = P.groupby(["ag", "rq"])["ex"].agg(["count", "mean"])
    out["falling pr by year, high-reclaim"] = P[P["rq"] == 2].groupby("year")["ex"].agg(["count", "mean"])

    # big up day continuation by trend
    G["z1q"] = pd.qcut(G["z1"], 5, labels=False, duplicates="drop")
    top = G[G["z1q"] == 4]
    r2 = {}
    for tr in ["chop", "fall", "rise", "na"]:
        s = top[top["trend"] == tr]
        t, nd = ct(s["ex"], s["day"]) if len(s) > 3 else (np.nan, 0)
        r2[tr] = pd.Series({"n": len(s), "mean": s["ex"].mean(), "t_day": t, "days": nd})
    out["top day-z quintile by trend"] = pd.DataFrame(r2).T
    return out
