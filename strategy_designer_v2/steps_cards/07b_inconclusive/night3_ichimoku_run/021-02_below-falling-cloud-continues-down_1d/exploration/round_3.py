import numpy as np, pandas as pd
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    bars = data["bars"]
    out = {}
    col = "debug_info.components.cloud_slope.last_history_value"
    for H in (10, 26):
        rows = []
        for coin, wins in bars.items():
            allret = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    allret.append(c[i + H] / c[i] - 1)
            mu = np.mean(allret); sd = np.std(allret)
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values; f = b["forecast"].values
                s = b[col].values if col in b else np.full(len(c), np.nan)
                yr = pd.to_datetime(b["timestamp"].iloc[0]).year
                for i in range(0, len(c) - H, H):
                    if not (f[i] < 0):
                        continue
                    r = c[i + H] / c[i] - 1
                    rows.append(dict(coin=coin, year=yr, slope=s[i], absf=abs(f[i]),
                                     longex=r - mu, strength=(r - mu) / sd))
        d = pd.DataFrame(rows).dropna(subset=["slope"])
        q = pd.qcut(d["slope"], 4, labels=False, duplicates="drop")
        def summ(g):
            return pd.Series(dict(n=len(g), long_ex=g["longex"].mean(), t=tstat(g["longex"]),
                                  strength=g["strength"].mean(), hit=(g["longex"] > 0).mean()))
        out[f"H{H}_by_slope_q"] = d.groupby(q).apply(summ)
        out[f"H{H}_all"] = summ(d)
        lr = stats.linregress(-d["slope"], d["longex"])
        out[f"H{H}_reg_longex_on_fallspeed"] = pd.Series(dict(slope=lr.slope, t=lr.slope / lr.stderr, n=len(d),
                                                              spearman=stats.spearmanr(-d["slope"], d["longex"]).correlation))
        steep = d[q <= 1]
        out[f"H{H}_steep_half_by_year"] = steep.groupby("year").apply(summ)
        out[f"H{H}_steep_half_by_coin"] = steep.groupby("coin").apply(summ)
    return out
