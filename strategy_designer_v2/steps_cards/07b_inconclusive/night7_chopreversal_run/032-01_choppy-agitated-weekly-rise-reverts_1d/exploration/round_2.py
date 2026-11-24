import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values.astype(float)
            s = pd.Series(c)
            p7 = s / s.shift(7) - 1
            zp7 = (p7 - p7.rolling(60, min_periods=20).mean()) / p7.rolling(60, min_periods=20).std()
            n = len(c)
            for h in (3, 5, 7, 10, 14):
                for t in range(0, n, h):
                    if t + h >= n or t < 7:
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, t=t, fut=c[t + h] / c[t] - 1,
                                     past7=p7.iloc[t], zp7=zp7.iloc[t],
                                     inprof=(reg[t] == "unknown"), fc=fc[t]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fut"].transform("mean")
    d["unus"] = d["fut"] - d["drift"]
    d["sd"] = d.groupby(["coin", "h"])["fut"].transform("std")
    d["z"] = d["unus"] / d["sd"]

    def summ(g, x="past7"):
        g = g.dropna(subset=[x, "unus"])
        if len(g) < 8:
            return pd.Series(dict(n=len(g)))
        r, _ = stats.pearsonr(g[x], g["unus"])
        tt = r * np.sqrt((len(g) - 2) / max(1e-12, 1 - r * r))
        fall = -g["z"]
        return pd.Series(dict(n=len(g), corr=round(r, 3), t=round(tt, 2),
                              fall_strength=round(fall.mean(), 3),
                              fall_t=round(fall.mean() / (fall.std() / np.sqrt(len(g))), 2),
                              mean_unus=round(g["unus"].mean(), 4)))

    out = {}
    rin = d[d.inprof & (d.past7 > 0)]
    rout = d[~d.inprof & (d.past7 > 0)]
    out["rises in profile, past7, by horizon"] = rin.groupby("h").apply(summ)
    out["rises in profile, zp7, by horizon"] = rin.groupby("h").apply(lambda g: summ(g, "zp7"))
    out["rises out of profile, past7, by horizon"] = rout.groupby("h").apply(summ)
    out["falls in profile, past7, by horizon"] = d[d.inprof & (d.past7 < 0)].groupby("h").apply(summ)
    # forecast-based, as step 5 (h7 grid, forecast<0)
    f = d[(d.h == 7) & (d.fc < 0)].dropna(subset=["unus"])
    r, _ = stats.pearsonr(-f.fc, -f.unus) if len(f) > 3 else (np.nan, None)
    out["step5-like, BC: n, corr(-fc, fall)"] = pd.Series(dict(n=len(f), corr=round(r, 3),
                                                              mean_fall=round(-f.unus.mean(), 4)))
    # rises in profile h7/h14 by coin
    out["rises in profile h14 by coin"] = rin[rin.h == 14].groupby("coin").apply(summ)
    out["rises in profile h7 by year-window"] = rin[rin.h == 7].groupby("w").agg(
        n=("z", "size"), fall=("z", lambda x: -x.mean()))
    return out
