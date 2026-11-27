import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    coin_mean = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            coin_mean[(coin, h)] = np.mean(rs) if rs else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            reg = df["regime"].values
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(30).std().values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(0, n - 5, 5):
                if reg[i] != "unknown" or not np.isfinite(f[i]) or f[i] == 0:
                    continue
                d = {"coin": coin, "win": w, "f": f[i], "day": ts.iloc[i].floor("D"),
                     "year": ts.iloc[i].year, "vol30": vol[i]}
                for h in H:
                    if i + h < n:
                        d[f"x{h}"] = c[i + h] / c[i] - 1 - coin_mean[(coin, h)]
                    else:
                        d[f"x{h}"] = np.nan
                rows.append(d)
    X = pd.DataFrame(rows)
    X["side"] = np.where(X.f > 0, "long", "short")
    X["absf"] = X.f.abs()
    for h in H:
        X[f"s{h}"] = X.f / 10 * X[f"x{h}"]
        X[f"d{h}"] = np.sign(X.f) * X[f"x{h}"]

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5:
            return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan})
        g = s.groupby("day")[col]
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev**2).sum() * D / (D - 1)) / len(s)
        return pd.Series({"n": len(s), "days": D, "mean": m, "t": m / se})

    out = {}
    out["by_horizon_score"] = pd.DataFrame({h: ct(X, f"s{h}") for h in H}).T
    out["by_horizon_dir"] = pd.DataFrame({h: ct(X, f"d{h}") for h in H}).T
    out["side_s5"] = X.groupby("side").apply(lambda s: ct(s, "s5"))
    out["side_s10"] = X.groupby("side").apply(lambda s: ct(s, "s10"))
    X["fq"] = pd.qcut(X.absf, 4, labels=["q1", "q2", "q3", "q4"])
    out["absf_q_d5"] = X.groupby("fq").apply(lambda s: ct(s, "d5"))
    out["absf_q_d10"] = X.groupby("fq").apply(lambda s: ct(s, "d10"))
    out["coin_s5"] = X.groupby("coin").apply(lambda s: ct(s, "s5"))
    out["win_s5"] = X.groupby("win").apply(lambda s: ct(s, "s5"))
    out["year_s5"] = X.groupby("year").apply(lambda s: ct(s, "s5"))
    X["vq"] = X.groupby("coin")["vol30"].transform(lambda v: pd.qcut(v, 2, labels=["calmer", "wilder"]) if v.notna().sum() > 4 else np.nan)
    out["vol_s5"] = X.groupby("vq").apply(lambda s: ct(s, "s5"))
    out["vol_s10"] = X.groupby("vq").apply(lambda s: ct(s, "s10"))
    return out
