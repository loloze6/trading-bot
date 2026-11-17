def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 7
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float)
            n = len(cl)
            r14 = pd.Series(cl).pct_change(14).values
            r60 = pd.Series(cl).pct_change(60).values
            r1 = pd.Series(cl).pct_change(1).values
            vol20 = pd.Series(r1).rolling(20).std().values
            hi60 = pd.Series(cl).rolling(60, min_periods=20).max().values
            vol = df["volume"].values.astype(float)
            vrel = vol / pd.Series(vol).rolling(20).mean().values
            for i in range(0, n - H, H):
                rows.append(dict(coin=c, w=w, fwd=cl[i+H]/cl[i]-1, r14=r14[i], r60=r60[i], r1=r1[i],
                                 vol20=vol20[i], near=cl[i]/hi60[i]-1, vrel=vrel[i],
                                 fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                 wd=pd.Timestamp(df["timestamp"].iloc[i]).dayofweek,
                                 yr=pd.Timestamp(df["timestamp"].iloc[i]).year))
    s = pd.DataFrame(rows)
    s["dm"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
    out = {}
    def tab(g, col):
        a = g.groupby(col)["dm"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    tr = s[s.reg == "trending"].copy(); un = s[s.reg != "trending"].copy()
    tr["q14"] = pd.qcut(tr["r14"], 5, labels=False); out["trend r14 quint"] = tab(tr, "q14")
    un["q14"] = pd.qcut(un["r14"], 5, labels=False); out["untrend r14 quint"] = tab(un, "q14")
    s["qv"] = pd.qcut(s["vol20"], 5, labels=False); out["vol quint all"] = tab(s, "qv")
    s["qn"] = pd.qcut(s["near"], 5, labels=False); out["near60high quint all"] = tab(s, "qn")
    s["q1"] = pd.qcut(s["r1"], 5, labels=False); out["1d ret quint all"] = tab(s, "q1")
    s["qvr"] = pd.qcut(s["vrel"], 5, labels=False); out["rel volume quint all"] = tab(s, "qvr")
    out["by coin"] = tab(s.assign(g=s.coin + "_" + s.reg), "g")
    out["year"] = tab(s, "yr")
    # correlations per regime
    cr = {}
    for nm, g in [("trend", tr), ("untrend", un)]:
        for v in ["r14", "r60", "near", "vol20", "vrel", "r1"]:
            gg = g[[v, "dm"]].dropna()
            r, p = stats.pearsonr(gg[v], gg["dm"]); cr[nm + "_" + v] = (round(r, 4), round(p, 4), len(gg))
    out["corr"] = pd.DataFrame(cr, index=["r", "p", "n"]).T
    # book daily
    d = []
    for c in days:
        for w, df in days[c].items():
            x = df.copy(); x["coin"] = c; x["w"] = w; d.append(x)
    d = pd.concat(d)
    d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek; d["yr"] = pd.to_datetime(d["day"]).dt.year
    out["book by year"] = d.groupby("yr")[["book_return", "coin_return"]].mean()
    out["book by coin"] = d.groupby("coin")[["book_return", "coin_return"]].agg(["mean"])
    out["coin ret by weekday"] = d.groupby("wd")["coin_return"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
