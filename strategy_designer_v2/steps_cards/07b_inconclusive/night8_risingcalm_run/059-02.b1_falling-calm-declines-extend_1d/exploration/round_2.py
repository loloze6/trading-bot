import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [3, 5]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            for i in range(len(df)):
                rec = {"coin": coin, "win": w, "pos": i,
                       "day": pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                       "inprof": df["regime"].iloc[i] == "unknown",
                       "fc": df["forecast"].iloc[i]}
                for h in H:
                    rec[f"f{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < len(df) else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    for h in H:
        g = d[d.pos % h == 0]
        d[f"u{h}"] = d[f"f{h}"] - d.coin.map(g.groupby("coin")[f"f{h}"].mean())
    def clus(sub, h):
        s = sub[["fc", f"u{h}", "day"]].dropna()
        if len(s) < 15: return {"slope": np.nan, "t_cl": np.nan, "n": len(s), "days": np.nan}
        x = s.fc.values - s.fc.mean(); y = s[f"u{h}"].values
        b = (x * y).sum() / (x * x).sum()
        e = y - y.mean() - b * x
        sc = pd.Series(x * e).groupby(s.day.values).sum()
        se = np.sqrt((sc ** 2).sum()) / (x * x).sum()
        # mean short unusual, day-clustered t
        dv = (-s[f"u{h}"]).groupby(s.day.values).sum()
        m = -s[f"u{h}"].mean()
        se_m = np.sqrt(((dv - m * s.groupby("day").size()) ** 2).sum()) / len(s)
        return {"slope": b, "t_cl": b / se, "n": len(s), "days": s.day.nunique(),
                "short_u": m, "t_short_u": m / se_m}
    out = {}
    res = []
    for h in H:
        g = d[(d.pos % h == 0) & (d.fc < 0) & d.inprof]
        r = clus(g, h); r["h"] = h; res.append(r)
    out["clustered_by_h"] = pd.DataFrame(res)
    g5 = d[(d.pos % 5 == 0) & (d.fc < 0) & d.inprof]
    out["by_window_h5"] = pd.DataFrame({k: clus(v, 5) for k, v in g5.groupby("win")}).T
    return out
