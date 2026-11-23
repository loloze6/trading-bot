import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["hour"] = d["ts"].dt.hour
            d["wd"] = d["ts"].dt.weekday
            d["year"] = d["ts"].dt.year
            d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(len(d))
            c = d["close"]
            r1 = c.pct_change()
            d["vol24"] = r1.rolling(24).std()
            for k in [1,4,8,24,72]:
                d[f"past{k}"] = c / c.shift(k) - 1
            for h in [1,4,8,24,72]:
                d[f"fwd{h}"] = c.shift(-h) / c - 1
            d["vrel"] = d["volume"] / d["volume"].rolling(168).median()
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # demean fwd by coin drift (all windows)
    out = {}
    for h in [1,4,8,24,72]:
        A[f"x{h}"] = A[f"fwd{h}"] - A.groupby("coin")[f"fwd{h}"].transform("mean")
    # 1. hour of day, next-1h excess return
    g = A.dropna(subset=["x1"]).groupby("hour")["x1"]
    hod = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())),
                        "vol_rel": A.groupby("hour")["vrel"].median()})
    out["next1h_by_hour"] = hod.round(3)
    # 2. reversal grid: scaled past k vs fwd h, non-overlapping grid of h
    res = []
    for k in [1,4,24,72]:
        for h in [1,4,24,72]:
            s = A[(A["pos"] % h == 0)].copy()
            s["z"] = s[f"past{k}"] / (s["vol24"]*np.sqrt(k))
            s = s.dropna(subset=["z", f"x{h}"])
            s = s[np.isfinite(s["z"])]
            sl, ic, rr, p, se = stats.linregress(s["z"], s[f"x{h}"])
            # top decile |z| cases: move in reversal direction
            q = s["z"].abs().quantile(0.9)
            big = s[s["z"].abs() >= q]
            rev = -np.sign(big["z"]) * big[f"fwd{h}"]
            res.append({"k_h": f"{k}->{h}", "n": len(s), "slope_bp": sl*1e4, "t": sl/se,
                        "top10_rev_total_bp": rev.mean()*1e4,
                        "top10_t": rev.mean()/(rev.std()/np.sqrt(len(rev)))})
    out["reversal_grid"] = pd.DataFrame(res).round(3)
    # 3. 24h->24h by vol tercile and by coin
    s = A[A["pos"] % 24 == 0].copy()
    s["z"] = s["past24"]/(s["vol24"]*np.sqrt(24))
    s = s.dropna(subset=["z","x24"])
    s["vt"] = s.groupby("coin")["vol24"].transform(lambda v: pd.qcut(v, 3, labels=False))
    def tt(g, col="x24"):
        sl, ic, rr, p, se = stats.linregress(g["z"], g[col]); return pd.Series({"n":len(g),"slope_bp":sl*1e4,"t":sl/se})
    out["24to24_by_voltercile"] = s.groupby("vt").apply(tt).round(3)
    out["24to24_by_coin"] = s.groupby("coin").apply(tt).round(3)
    # 4. settlement: pre hours (5,6,7 / 13,14,15 / 21,22,23) return vs 24h trend sign
    A["tr"] = np.sign(A["past24"])
    A["signed_x1"] = A["x1"] * A["tr"]
    A["settle_rel"] = A["hour"] % 8
    g = A.dropna(subset=["signed_x1"]).groupby("settle_rel")["signed_x1"]
    out["trend_signed_next1h_by_hour_mod8"] = pd.DataFrame({"mean_bp": g.mean()*1e4,
        "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()}).round(3)
    # 5. weekday
    g = A.dropna(subset=["x1"]).groupby("wd")["x1"]
    out["next1h_by_weekday"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count()))}).round(3)
    return out
