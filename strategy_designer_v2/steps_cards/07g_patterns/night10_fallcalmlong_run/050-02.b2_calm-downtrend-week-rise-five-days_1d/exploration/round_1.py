import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; o = df["open"]; hi = df["high"]; lo = df["low"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(df)),
                "ts": pd.to_datetime(df["timestamp"]),
                "inprof": (df["regime"] == "unknown").astype(int),
                "s7": (c / c.shift(7) - 1) / (vol30 * np.sqrt(7)),
                "s3": (c / c.shift(3) - 1) / (vol30 * np.sqrt(3)),
                "s1": r1 / vol30,
                "s20": (c / c.shift(20) - 1) / (vol30 * np.sqrt(20)),
                "clv": (c - lo) / (hi - lo),
                "rng": (hi - lo) / c / vol30,
                "dd20": (c / c.rolling(20, min_periods=10).max() - 1) / vol30,
                "vratio": df["volume"] / df["volume"].rolling(20, min_periods=10).mean(),
                "vol30": vol30,
            })
            for h in H:
                f[f"fx{h}"] = c.shift(-h) / c - 1 - drift[(coin, h)]
                f[f"g{h}"] = (f["pos"] % h == 0) & c.shift(-h).notna()
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    P = A[A["inprof"] == 1]
    out = {}

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s), 0)
        m = s[col].mean()
        d = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((d ** 2).sum()) / len(s)
        return (m, m / se if se > 0 else np.nan, len(s), s["day"].nunique())

    out["profile share bars"] = float(A["inprof"].mean())
    base = []
    for h in H:
        m, t, n, nd = ct(P[P[f"g{h}"]], f"fx{h}")
        base.append([h, m, t, n, nd])
    out["in-profile excess by horizon"] = pd.DataFrame(base, columns=["h", "mean", "t", "n", "days"])

    for feat in ["s7", "s3", "s1", "s20", "clv", "rng", "dd20", "vratio", "vol30"]:
        tab = []
        for h in [3, 5, 10]:
            s = P[P[f"g{h}"]].dropna(subset=[feat, f"fx{h}"]).copy()
            s["q"] = pd.qcut(s[feat], 5, labels=False, duplicates="drop")
            for q, g in s.groupby("q"):
                m, t, n, nd = ct(g, f"fx{h}")
                tab.append([h, q, g[feat].mean(), m, t, n])
            sp = s[[feat, f"fx{h}"]].corr(method="spearman").iloc[0, 1]
            tab.append([h, "rho", np.nan, sp, sp * np.sqrt(len(s)), len(s)])
        out[f"{feat} quintiles"] = pd.DataFrame(tab, columns=["h", "q", "feat_mean", "mean", "t", "n"])

    wd = []
    s = P[P["g1"]]
    for k, g in s.groupby(s["ts"].dt.weekday):
        m, t, n, nd = ct(g, "fx1"); wd.append([k, m, t, n])
    out["weekday fx1"] = pd.DataFrame(wd, columns=["wd", "mean", "t", "n"])
    yr = []
    s = P[P["g5"]]
    for k, g in s.groupby(s["ts"].dt.year):
        m, t, n, nd = ct(g, "fx5"); yr.append([k, m, t, n])
    out["year fx5"] = pd.DataFrame(yr, columns=["yr", "mean", "t", "n"])
    return out
