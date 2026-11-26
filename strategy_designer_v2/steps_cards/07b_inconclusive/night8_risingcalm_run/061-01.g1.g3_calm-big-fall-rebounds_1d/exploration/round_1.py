import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std().shift(1)
            z = r / sd
            calm = (df["regime"] == "unknown")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in H:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    if pd.isna(fwd.iloc[i]):
                        continue
                    rows.append((coin, w, h, i, yr.iloc[i], z.iloc[i], bool(calm.iloc[i]), fwd.iloc[i]))
    t = pd.DataFrame(rows, columns=["coin", "w", "h", "i", "yr", "z", "calm", "fwd"])
    t["mu"] = t.groupby(["coin", "h"])["fwd"].transform("mean")
    t["ex"] = t["fwd"] - t["mu"]
    t = t.dropna(subset=["z"])
    t["zb"] = pd.cut(t["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    out = {}
    g = t.groupby(["h", "calm", "zb"], observed=True)["ex"].agg(["mean", "count"])
    g["t"] = t.groupby(["h", "calm", "zb"], observed=True)["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
    out["excess by h, calm, z bucket"] = g.round(4)

    def slope(sub):
        if len(sub) < 10:
            return pd.Series({"slope": np.nan, "t": np.nan, "n": len(sub)})
        res = stats.linregress(sub["z"], sub["ex"])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(sub)})

    s = []
    for (h, calm), sub in t.groupby(["h", "calm"]):
        for side, ss in [("down", sub[sub.z < 0]), ("up", sub[sub.z > 0]), ("all", sub)]:
            d = slope(ss)
            d["h"] = h
            d["calm"] = calm
            d["side"] = side
            s.append(d)
    out["slope ex on z"] = pd.DataFrame(s).round(4)

    t10 = t[(t.h == 10) & t.calm & (t.z < 0)]
    out["calm down h10 by coin"] = t10.groupby("coin").apply(lambda x: pd.Series({"mean_ex": x.ex.mean(), "corr_z": x[["z", "ex"]].corr().iloc[0, 1], "n": len(x)})).round(4)
    out["calm down h10 by year"] = t10.groupby("yr").apply(lambda x: pd.Series({"mean_ex": x.ex.mean(), "corr_z": x[["z", "ex"]].corr().iloc[0, 1], "n": len(x)})).round(4)
    out["calm share"] = float(t[t.h == 1].calm.mean())
    return out
