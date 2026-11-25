import numpy as np, pandas as pd
from scipy import stats

def clustered_slope(x, y, days):
    d = pd.DataFrame({"x": x, "y": y, "day": days}).dropna()
    if len(d) < 10: return {"slope": np.nan, "t_cl": np.nan, "n": len(d), "days": 0}
    xm = d.x - d.x.mean()
    b = (xm * (d.y - d.y.mean())).sum() / (xm ** 2).sum()
    a = d.y.mean() - b * d.x.mean()
    e = d.y - a - b * d.x
    s = (xm * e).groupby(d.day).sum()
    se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
    return {"slope": b, "t_cl": b / se, "n": len(d), "days": d.day.nunique()}

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values.astype(float))
            n = len(c)
            ret1 = c.pct_change()
            vol20 = ret1.rolling(20).std()
            hi20 = c.shift(1).rolling(20).max()
            raw = ((c - hi20) / hi20 / vol20).values
            r20 = c.pct_change(20).values
            r5p = c.pct_change(5).values
            for i in range(0, n, 5):
                d = {"coin": coin, "w": w, "reg": b["regime"].iloc[i], "fc": b["forecast"].iloc[i],
                     "raw": raw[i], "r20": r20[i], "r5p": r5p[i], "day": str(b["timestamp"].iloc[i])[:10],
                     "f5": c[i + 5] / c[i] - 1 if i + 5 < n else np.nan,
                     "f10": c[i + 10] / c[i] - 1 if i + 10 < n else np.nan}
                rows.append(d)
    df = pd.DataFrame(rows)
    for h in [5, 10]:
        df[f"a{h}"] = df[f"f{h}"] - df.groupby("coin")[f"f{h}"].transform("mean")
    ch = df[df.reg == "unknown"]
    below = ch[ch.raw < 0].copy()
    out = {}
    out["clustered"] = pd.DataFrame({
        "raw_a5_below": clustered_slope(below.raw, below.a5, below.day),
        "raw_a10_below": clustered_slope(below.raw, below.a10, below.day),
        "fc_a5_fcneg": clustered_slope(below.fc.where(below.fc < 0), below.a5, below.day),
        "rawclip_a5_allchoppy": clustered_slope(ch.raw.clip(upper=0), ch.a5, ch.day),
        "raw_a5_r20down": clustered_slope(below.raw.where(below.r20 < 0), below.a5, below.day),
        "raw_a5_r20up": clustered_slope(below.raw.where(below.r20 >= 0), below.a5, below.day),
    }).T
    out["fc_status_below"] = pd.Series({"fc<0": int((below.fc < 0).sum()), "fc==0": int((below.fc == 0).sum()),
                                        "corr_raw_fc": below.raw.corr(below.fc)})
    below["half"] = np.where(below.raw < below.raw.median(), "deep_half", "shallow_half")
    below["tr"] = np.where(below.r20 < 0, "r20down", "r20up")
    g = below.groupby(["half", "tr"])
    def t(x):
        x = x.dropna(); return x.mean() / (x.std() / np.sqrt(len(x)))
    out["half_by_r20"] = pd.DataFrame({"n": g.size(), "a5": g.a5.mean(), "t5": g.a5.apply(t), "a10": g.a10.mean()})
    below["fcq"] = pd.qcut(below.fc.where(below.fc < 0), 3, labels=["deepest", "mid", "least"])
    g2 = below.groupby("fcq", observed=True)
    out["fc_thirds"] = pd.DataFrame({"n": g2.size(), "a5": g2.a5.mean(), "raw_mean": g2.raw.mean(), "fc_mean": g2.fc.mean()})
    g3 = below.groupby(pd.cut(below.raw, [-50, -4, -2, -1, 0]), observed=True)
    out["raw_bins"] = pd.DataFrame({"n": g3.size(), "a5": g3.a5.mean(), "t5": g3.a5.apply(t), "a10": g3.a10.mean()})
    return out
