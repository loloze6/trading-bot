import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    H = 3
    for coin, wins in data["bars"].items():
        # coin drift: mean 3-bar return on grid over all windows
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr)
        usual = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; o = b["open"]; hi = b["high"]; lo = b["low"]
            r1 = c.pct_change()
            vol10 = r1.rolling(10).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "inprof": b["regime"] != "chop",
                "regime": b["regime"],
                "r1z": r1 / vol10,
                "r3z": (c / c.shift(3) - 1) / (vol10 * np.sqrt(3)),
                "r7z": (c / c.shift(7) - 1) / (vol10 * np.sqrt(7)),
                "r20z": (c / c.shift(20) - 1) / (vol10 * np.sqrt(20)),
                "clv": (c - lo) / (hi - lo).replace(0, np.nan),
                "upwick": (hi - np.maximum(o, c)) / (hi - lo).replace(0, np.nan),
                "rangez": (hi - lo) / c / vol10,
                "volz": np.log(b["volume"] / b["volume"].rolling(20).mean()),
                "dist_hi": (c / c.rolling(20).max() - 1) / vol10,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd": c.shift(-H) / c - 1,
            })
            df["short_unusual"] = -(df["fwd"] - drift)
            df["short_strength"] = df["short_unusual"] / usual
            df["grid"] = (np.arange(len(df)) % H == 0)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d.grid & d.inprof & d.fwd.notna()]
    out = {}
    out["counts"] = pd.Series({"grid in-profile": len(g), "grid all": int((d.grid & d.fwd.notna()).sum()),
                               "mean short unusual inprof": g.short_unusual.mean(),
                               "t": stats.ttest_1samp(g.short_unusual, 0).statistic})
    def bucket(col, q=5):
        x = g[[col, "short_unusual", "short_strength"]].dropna()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        r = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("short_unusual", "size"),
                               mean=("short_unusual", "mean"), strength=("short_strength", "mean"),
                               sd=("short_unusual", "std"))
        r["t"] = r["mean"] / (r["sd"] / np.sqrt(r["n"]))
        rho = stats.spearmanr(x[col], x["short_unusual"])
        r.loc["rho"] = [rho.correlation, rho.pvalue, len(x), np.nan, np.nan, np.nan, np.nan]
        return r.drop(columns="sd")
    for col in ["r1z", "r3z", "r7z", "r20z", "clv", "upwick", "rangez", "volz", "dist_hi"]:
        out[col] = bucket(col)
    wd = g.groupby("wd").short_unusual.agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday"] = wd
    bc = g.groupby("coin").short_unusual.agg(["size", "mean"])
    out["by_coin"] = bc
    return out
