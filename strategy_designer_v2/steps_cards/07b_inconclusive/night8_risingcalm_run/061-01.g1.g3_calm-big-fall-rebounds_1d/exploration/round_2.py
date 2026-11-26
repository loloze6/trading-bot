import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std().shift(1)
            z = r / sd
            calm = (df["regime"] == "unknown")
            ts = pd.to_datetime(df["timestamp"])
            for h in [5, 10]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    if pd.isna(fwd.iloc[i]) or pd.isna(z.iloc[i]):
                        continue
                    rows.append((coin, w, h, ts.iloc[i].normalize(), ts.iloc[i].year, z.iloc[i], bool(calm.iloc[i]), fwd.iloc[i]))
    t = pd.DataFrame(rows, columns=["coin", "w", "h", "day", "yr", "z", "calm", "fwd"])
    t["mu"] = t.groupby(["coin", "h"])["fwd"].transform("mean")
    t["ex"] = t["fwd"] - t["mu"]
    out = {}

    def slope(sub):
        if len(sub) < 8:
            return pd.Series({"slope": np.nan, "t": np.nan, "n": len(sub)})
        res = stats.linregress(sub["z"], sub["ex"])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(sub)})

    def dayslope(sub):
        d = sub.groupby("day")[["z", "ex"]].sum()
        if len(d) < 8:
            return pd.Series({"slope": np.nan, "t": np.nan, "days": len(d)})
        res = stats.linregress(d["z"], d["ex"])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "days": len(d)})

    res = []
    for h in [5, 10]:
        for calm in [True, False]:
            for side in ["up", "down"]:
                sub = t[(t.h == h) & (t.calm == calm) & ((t.z > 0) if side == "up" else (t.z < 0))]
                d = dayslope(sub)
                d["h"] = h; d["calm"] = calm; d["side"] = side
                d["mean_ex"] = sub.ex.mean()
                res.append(d)
    out["day-summed slope"] = pd.DataFrame(res).round(4)

    u = t[(t.h == 10) & t.calm & (t.z > 0)]
    out["calm up h10 by coin"] = u.groupby("coin").apply(slope).round(4)
    out["calm up h10 by year"] = u.groupby("yr").apply(slope).round(4)
    u = u.copy()
    u["zb"] = pd.cut(u["z"], [0, 0.5, 1, 2, 99])
    out["calm up h10 buckets"] = u.groupby("zb", observed=True)["ex"].agg(["mean", "count"]).round(4)
    u5 = t[(t.h == 5) & t.calm & (t.z > 0)]
    out["calm up h5 by coin"] = u5.groupby("coin").apply(slope).round(4)
    return out
