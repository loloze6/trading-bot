import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            L30 = l.shift(1).rolling(30, min_periods=30).min()
            H30 = h.shift(1).rolling(30, min_periods=30).max()
            ret60 = c / c.shift(60) - 1
            ret5p = c / c.shift(5) - 1
            vol30 = r1.rolling(30, min_periods=20).std()
            vol_rel = vol30 / r1.rolling(90, min_periods=60).std()
            rng = (h - l)
            clpos = (c - l) / rng.replace(0, np.nan)
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "r1": r1, "z1": r1 / vol30.shift(1), "ret60": ret60, "ret5p": ret5p,
                "vol_rel": vol_rel, "clpos": clpos,
                "pierce_reclaim": (l < L30) & (c > L30),
                "break_close": (c < L30),
                "pierce_hi_fail": (h > H30) & (c < H30),
                "break_hi": (c > H30),
                "reclaim": (c - L30) / rng.replace(0, np.nan),
                "f5": f5, "f1": f1,
                "z5": ret5p / (vol30 * np.sqrt(5)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 5 == 0) & A["f5"].notna()].copy()
    drift = G["f5"].mean()
    G["ex"] = G["f5"] - drift
    out = {"grid n, drift5, sd5": pd.Series({"n": len(G), "drift5": drift, "sd5": G["f5"].std()})}

    def summ(mask_name, m, col="ex"):
        x = G.loc[m, col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    G["trend"] = np.where(G["ret60"] < -0.1, "fall", np.where(G["ret60"] > 0.1, "rise", "chop"))
    G.loc[G["ret60"].isna(), "trend"] = "na"
    G["agit"] = np.where(G["vol_rel"] > 1, "ag", "calm")
    ev = {}
    for name in ["pierce_reclaim", "break_close", "pierce_hi_fail", "break_hi"]:
        for tr in ["fall", "chop", "rise", "na"]:
            ev[(name, tr)] = summ(name, G[name] & (G["trend"] == tr))
        ev[(name, "all")] = summ(name, G[name])
    out["events by trend (excess f5)"] = pd.DataFrame(ev).T
    # past 5d return z deciles
    G["z5q"] = pd.qcut(G["z5"], 5, labels=False, duplicates="drop")
    out["by past 5d z quintile"] = G.groupby("z5q")["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["by past 5d z quintile x trend"] = G.groupby(["trend", "z5q"])["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    G["z1q"] = pd.qcut(G["z1"], 5, labels=False, duplicates="drop")
    out["by day z quintile"] = G.groupby("z1q")["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    G["clq"] = pd.qcut(G["clpos"], 5, labels=False, duplicates="drop")
    out["by close position quintile"] = G.groupby("clq")["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    G["vq"] = pd.qcut(G["vol_rel"], 4, labels=False, duplicates="drop")
    out["by vol_rel quartile x trend"] = G.groupby(["vq", "trend"])["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # weekday on daily returns (all bars)
    A1 = A[A["f1"].notna()]
    m1 = A1["f1"].mean()
    out["next-day return by weekday of signal day"] = A1.groupby("wd")["f1"].agg(["count", "mean", lambda x: (x.mean()-m1)/(x.std()/np.sqrt(len(x)))])
    # reclaim grading among pierce-reclaim events in all bars (not grid), falling
    pr = A[A["pierce_reclaim"] & A["f5"].notna()].copy()
    pr["ex"] = pr["f5"] - drift
    pr["rq"] = pd.qcut(pr["reclaim"], 3, labels=False, duplicates="drop")
    out["pierce_reclaim all bars by reclaim tercile x trend"] = pr.groupby(["trend" if False else pd.cut(pr["ret60"], [-9, -0.1, 0.1, 9]), "rq"])["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # book: trades
    T = pd.concat([t.assign(coin=c_) for c_, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
    out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(), "win": (T["net_profit_loss_percent"] > 0).mean(), "med": T["net_profit_loss_percent"].median()})
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
