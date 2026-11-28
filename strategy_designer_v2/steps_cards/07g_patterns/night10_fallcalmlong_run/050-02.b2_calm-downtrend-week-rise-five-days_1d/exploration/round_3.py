import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [3, 5]
    rows = []; drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            f = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                "ts": pd.to_datetime(df["timestamp"]),
                "inprof": (df["regime"] == "unknown").astype(int),
                "s7": (c / c.shift(7) - 1) / (vol30 * np.sqrt(7)),
                "up20": (c / c.rolling(20, min_periods=10).min() - 1) / vol30,
                "up10": (c / c.rolling(10, min_periods=7).min() - 1) / vol30,
                "dd20": (c / c.rolling(20, min_periods=10).max() - 1) / vol30})
            for h in H:
                f[f"fx{h}"] = c.shift(-h) / c - 1 - drift[(coin, h)]
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    P = A[A["inprof"] == 1]
    out = {}
    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s))
        m = s[col].mean(); d = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((d ** 2).sum()) / len(s)
        return (m, m / se, len(s))
    tab = []
    for feat in ["up20", "up10"]:
        for h in H:
            for off in range(h):
                s = P[((P["pos"] - off) % h == 0)].dropna(subset=[feat, f"fx{h}", "s7"])
                rho = s[[feat, f"fx{h}"]].corr(method="spearman").iloc[0, 1]
                X = np.column_stack([np.ones(len(s)), s[feat], s["s7"]])
                b = np.linalg.lstsq(X, s[f"fx{h}"].values, rcond=None)[0]
                med = s[feat].median()
                mt, tt, nt = ct(s[s[feat] > med], f"fx{h}")
                tab.append([feat, h, off, rho, rho*np.sqrt(len(s)), b[1], b[2], mt, tt, nt])
    out["up by offset"] = pd.DataFrame(tab, columns=["feat","h","off","rho","t_rho","b_feat","b_s7","m_top_half","t_top","n_top"])
    s = P[P["pos"] % 3 == 0].dropna(subset=["up20", "fx3"]).copy()
    s["q"] = pd.qcut(s["up20"], 3, labels=False)
    out["up20 terciles h3 by coin"] = pd.DataFrame([[c, q, *ct(g, "fx3")] for (c, q), g in s.groupby(["coin","q"])], columns=["coin","q","mean","t","n"])
    out["up20 terciles h3 by year"] = pd.DataFrame([[y, q, *ct(g, "fx3")] for (y, q), g in s.groupby([s["ts"].dt.year, "q"])], columns=["yr","q","mean","t","n"])
    return out
