import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in (5, 10):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[h] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            f30 = df.get("debug_info.components.fall30.last_history_value")
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            lr = np.r_[np.nan, np.diff(np.log(c))]
            for i in range(0, n - 10, 10):
                if df["regime"].iloc[i] != "chop" or f30 is None or pd.isna(f30.iloc[i]):
                    continue
                if f30.iloc[i] >= 0:
                    continue
                lo = max(1, i - 29)
                v30 = np.nanstd(lr[lo:i + 1]) if i - lo >= 10 else np.nan
                r = {"coin": coin, "day": ts.iloc[i].normalize(), "f30": f30.iloc[i], "fc": fc[i],
                     "v30": v30, "z": (f30.iloc[i] / 100) / (v30 * np.sqrt(30)) if v30 and v30 > 0 else np.nan,
                     "s5": -(c[i + 5] / c[i] - 1 - drift[5]), "s10": -(c[i + 10] / c[i] - 1 - drift[10])}
                rows.append(r)
    d = pd.DataFrame(rows).dropna()
    def summ(g, col):
        dd = g[col].groupby(g["day"]).sum()
        t = dd.mean() / (dd.std() / np.sqrt(len(dd))) if len(dd) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(dd), "mean": g[col].mean(), "t_day": t})
    out = {}
    d["zq"] = pd.qcut(d.z, 4, labels=["deep_z", "q2", "q3", "mild_z"])
    out["s10 by fall/vol quartile"] = d.groupby("zq").apply(lambda g: pd.concat([summ(g, "s10"), pd.Series({"z": g.z.mean(), "f30": g.f30.mean()})]))
    d["fq"] = pd.qcut(d.f30, 4, labels=["deepest", "q2", "q3", "mildest"])
    out["s5 by depth quartile"] = d.groupby("fq").apply(lambda g: summ(g, "s5"))
    d["vq"] = pd.qcut(d.v30, 2, labels=["calm30", "agit30"])
    out["s10 by v30 half x depth half"] = d.groupby(["vq", pd.qcut(d.f30, 2, labels=["deep", "mild"])]).apply(lambda g: summ(g, "s10"))
    out["fc quartiles s10"] = d.groupby(pd.qcut(d.fc.rank(method="first"), 4, labels=["fc1_strong", "fc2", "fc3", "fc4_weak"])).apply(lambda g: pd.concat([summ(g, "s10"), pd.Series({"fc": g.fc.mean()})]))
    out["spearman z vs s10"] = float(stats.spearmanr(-d.z, d.s10)[0])
    out["spearman fc vs s10"] = float(stats.spearmanr(-d.fc, d.s10)[0])
    return out
