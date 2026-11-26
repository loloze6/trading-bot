import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    # momentum / reversal by past lookback, forward horizon h, non-overlapping grid
    rows = []
    for H, L in [(30, 30), (30, 60), (14, 14), (14, 30), (7, 7), (7, 30), (3, 3)]:
        recs = []
        for c, ws in bars.items():
            # coin drift over horizon on the grid, all windows
            allf = []
            per = []
            for w, df in ws.items():
                cl = df["close"].values.astype(float); n = len(cl)
                lr = np.diff(np.log(cl))
                for i in range(0, n - H, H):
                    f = cl[i + H] / cl[i] - 1
                    allf.append(f)
                    if i >= L and i >= 30:
                        p = cl[i] / cl[i - L] - 1
                        vol = np.std(lr[max(0, i - 30):i], ddof=1) * np.sqrt(L)
                        per.append((c, w, p, p / vol if vol > 0 else np.nan, f))
            d = np.mean(allf)
            for r in per:
                recs.append((r[0], r[1], r[2], r[3], r[4] - d))
        df = pd.DataFrame(recs, columns=["coin", "w", "past", "z", "fwd_ex"]).dropna()
        df["q"] = pd.qcut(df["z"].rank(method="first"), 5, labels=False)
        g = df.groupby("q")["fwd_ex"]
        for q, s in g:
            rows.append({"H": H, "L": L, "q": q, "n": len(s), "z_mean": df.loc[df.q == q, "z"].mean(), "fwd_ex": s.mean(), "t": tstat(s)})
        r, pv = stats.spearmanr(df["z"], df["fwd_ex"])
        rows.append({"H": H, "L": L, "q": "rho", "n": len(df), "z_mean": r, "fwd_ex": pv, "t": np.nan})
    out["mom_rev_by_quintile"] = pd.DataFrame(rows)
    # forecast size vs forward 30
    recs = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].values.astype(float); fc = df["forecast"].values; n = len(cl)
            for i in range(0, n - 30, 30):
                if fc[i] < 0:
                    recs.append((fc[i], cl[i + 30] / cl[i] - 1, cl[min(i+7,n-1)]/cl[i]-1))
    f = pd.DataFrame(recs, columns=["fc", "f30", "f7"])
    if len(f) > 10:
        f["bin"] = pd.qcut(f["fc"].rank(method="first"), 3, labels=False)
        out["forecast_tercile_fwd"] = f.groupby("bin").agg(n=("f30", "size"), fc=("fc", "mean"), f30=("f30", "mean"), f7=("f7", "mean"))
    # daily: weekday and vol-level
    recs = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].astype(float); r = cl.pct_change()
            vol = r.rolling(30).std()
            ts = pd.to_datetime(df["timestamp"])
            nxt = r.shift(-1)
            recs.append(pd.DataFrame({"wd": ts.dt.weekday.values, "r": r.values, "nxt": nxt.values, "vol": vol.values, "c": c, "yr": ts.dt.year.values}))
    D = pd.concat(recs).dropna()
    out["weekday"] = D.groupby("wd")["r"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    D["volq"] = pd.qcut(D["vol"].rank(method="first"), 5, labels=False)
    out["nextday_by_volq"] = D.groupby("volq")["nxt"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    D["z1"] = D["r"] / D["vol"]
    D["zq"] = pd.qcut(D["z1"].rank(method="first"), 10, labels=False)
    out["nextday_by_today_decile"] = D.groupby("zq")["nxt"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    # book by coin and year
    recs = []
    for c, ws in data["days"].items():
        for w, df in ws.items():
            recs.append(pd.DataFrame({"c": c, "yr": pd.to_datetime(df["day"]).dt.year, "br": df["book_return"], "cr": df["coin_return"]}))
    B = pd.concat(recs).dropna()
    out["book_by_coin"] = B.groupby("c")[["br", "cr"]].mean()
    out["book_by_year"] = B.groupby("yr")[["br", "cr"]].mean()
    return out
