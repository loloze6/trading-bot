import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon on non-overlapping grid of all windows
        drift = {}
        for h in (5, 10, 20):
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
            for i in range(0, n - 10, 10):
                if df["regime"].iloc[i] != "chop" or f30 is None or pd.isna(f30.iloc[i]):
                    continue
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "f30": f30.iloc[i], "fc": fc[i]}
                for h in (5, 10, 20):
                    r[f"u{h}"] = (c[i + h] / c[i] - 1 - drift[h]) if i + h < n else np.nan
                r["raw10"] = c[i + 10] / c[i] - 1
                # past 10d vol of daily returns
                lo = max(0, i - 20)
                r["vol20"] = np.std(np.diff(np.log(c[lo:i + 1]))) if i - lo >= 5 else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    def summ(g, col="u10", sign=1):
        x = sign * g[col].dropna()
        dd = (sign * g[col]).groupby(g["day"]).sum().dropna()
        t = dd.mean() / (dd.std() / np.sqrt(len(dd))) if len(dd) > 2 else np.nan
        return pd.Series({"n": len(x), "days": len(dd), "mean": x.mean(), "t_day": t})
    falls = d[d.f30 < 0].copy()
    rises = d[d.f30 > 0].copy()
    out["falls short gain by horizon"] = pd.DataFrame({h: summ(falls, f"u{h}", -1) for h in (5, 10, 20)}).T
    out["rises long gain by horizon"] = pd.DataFrame({h: summ(rises, f"u{h}", 1) for h in (5, 10, 20)}).T
    falls["q"] = pd.qcut(falls.f30, 4, labels=["deepest", "q2", "q3", "mildest"])
    out["falls short gain u10 by depth quartile"] = falls.groupby("q").apply(lambda g: pd.concat([summ(g, "u10", -1), pd.Series({"f30_mean": g.f30.mean()})]))
    falls["fq"] = pd.qcut(falls.fc.rank(method="first"), 2, labels=["fc_strong", "fc_weak"])
    out["falls by forecast half (fc ascending)"] = falls.groupby("fq").apply(lambda g: summ(g, "u10", -1))
    out["falls by year"] = falls.groupby("year").apply(lambda g: summ(g, "u10", -1))
    out["falls by coin"] = falls.groupby("coin").apply(lambda g: summ(g, "u10", -1))
    out["falls by window"] = falls.groupby("win").apply(lambda g: summ(g, "u10", -1))
    falls["vq"] = pd.qcut(falls.vol20, 2, labels=["calm20", "agit20"])
    out["falls by recent vol half"] = falls.groupby("vq").apply(lambda g: summ(g, "u10", -1))
    out["corr f30 vs u10 falls (spearman)"] = float(stats.spearmanr(falls.f30, falls.u10, nan_policy="omit")[0])
    out["corr f30 vs u10 all chop"] = float(stats.spearmanr(d.f30, d.u10, nan_policy="omit")[0])
    out["falls raw total 10d mean"] = float(-falls.raw10.mean())
    return out
