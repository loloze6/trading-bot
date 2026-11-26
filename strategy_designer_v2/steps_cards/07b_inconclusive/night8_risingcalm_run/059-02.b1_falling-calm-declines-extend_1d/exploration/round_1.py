import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            hi = c.rolling(14, min_periods=14).max()
            sd = c.pct_change().rolling(30, min_periods=30).std()
            depth = (c - hi) / hi / sd
            r60 = c / c.shift(60) - 1
            for i in range(len(df)):
                rec = {"coin": coin, "win": w, "pos": i,
                       "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "inprof": df["regime"].iloc[i] == "unknown",
                       "fc": df["forecast"].iloc[i], "depth": depth.iloc[i], "r60": r60.iloc[i]}
                for h in H:
                    rec[f"f{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < len(df) else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    # drift per coin per horizon on non-overlapping grid
    drift = {}
    for h in H:
        g = d[d.pos % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    for h in H:
        d[f"u{h}"] = d[f"f{h}"] - d.coin.map(drift[h])
    def slope(sub, h, x="depth"):
        s = sub[[x, f"u{h}"]].dropna()
        if len(s) < 15: return (np.nan, np.nan, len(s), np.nan)
        lr = stats.linregress(s[x], s[f"u{h}"])
        # positive = deeper (more negative depth) followed by fall -> slope of u on depth positive
        return (lr.slope, lr.slope / lr.stderr, len(s), -s[f"u{h}"].mean())
    out = {}
    res = []
    for h in H:
        g = d[(d.pos % h == 0) & (d.fc < 0) & d.inprof]
        sl, t, n, um = slope(g, h, "fc")
        res.append({"h": h, "slope_fc": sl, "t": t, "n": n, "short_unusual": um})
    out["in_profile_by_horizon"] = pd.DataFrame(res)
    g5 = d[(d.pos % 5 == 0) & (d.fc < 0) & d.inprof]
    out["by_coin_h5"] = pd.DataFrame({k: slope(v, 5, "fc") for k, v in g5.groupby("coin")}, index=["slope", "t", "n", "short_u"]).T
    out["by_year_h5"] = pd.DataFrame({k: slope(v, 5, "fc") for k, v in g5.groupby("year")}, index=["slope", "t", "n", "short_u"]).T
    g5 = g5.copy()
    g5["q"] = pd.qcut(g5.fc, 4, labels=False, duplicates="drop")
    out["fc_quartile_h5"] = g5.groupby("q").agg(fc=("fc", "mean"), n=("u5", "size"), u5=("u5", "mean"), u10=("u10", "mean"))
    # outside profile, depth recomputed, by trend bucket, grid 5
    o = d[(d.pos % 5 == 0) & (d.depth < 0)].copy()
    o["trend"] = pd.cut(o.r60, [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    res = []
    for (ip, tr), v in o.groupby(["inprof", "trend"]):
        for h in [5, 10]:
            sl, t, n, um = slope(v, h, "depth")
            res.append({"inprof": ip, "trend": tr, "h": h, "slope_depth": sl, "t": t, "n": n, "short_u": um})
    out["depth_by_trend_profile"] = pd.DataFrame(res)
    return out
