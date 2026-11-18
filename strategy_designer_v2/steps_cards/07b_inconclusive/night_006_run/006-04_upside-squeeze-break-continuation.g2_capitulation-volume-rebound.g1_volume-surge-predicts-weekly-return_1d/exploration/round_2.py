import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for h in [1, 2, 3, 5, 7]:
                for i in range(0, n - h, h):
                    r5 = c[i] / c[i-5] - 1 if i >= 5 else np.nan
                    rows.append((coin, w, yr[i], h, f[i], c[i+h]/c[i]-1, r5))
    d = pd.DataFrame(rows, columns=["coin","w","year","h","f","r","r5"]).dropna(subset=["f","r"])
    d["ex"] = d["r"] - d.groupby(["coin","h"])["r"].transform("mean")

    def slope(g):
        if len(g) < 20 or g["f"].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        res = stats.linregress(g["f"], g["ex"])
        return pd.Series({"n": len(g), "slope": res.slope, "t": res.slope / res.stderr})

    out = {}
    d3 = d[d.h == 3]
    out["h3_by_coin"] = d3.groupby("coin").apply(slope)
    out["h3_by_year"] = d3.groupby("year").apply(slope)
    d1 = d[d.h == 1]
    out["h1_by_coin"] = d1.groupby("coin").apply(slope)
    out["h1_by_year"] = d1.groupby("year").apply(slope)
    d3 = d3.copy(); d3["fq"] = pd.qcut(d3["f"], 5, labels=False)
    out["h3_quintile"] = d3.groupby("fq").agg(n=("ex","size"), f=("f","mean"), ex=("ex","mean"))
    out["by_h_all"] = d.groupby("h").apply(slope)
    # abs-move check (brief): forecast vs abs excess return at h7
    d7 = d[d.h == 7].copy()
    d7["absr"] = d7["r"].abs()
    res = stats.linregress(d7["f"], d7["absr"])
    out["h7_absret_slope_t"] = float(res.slope / res.stderr)
    # dispersion of 7d ex vs top-bottom diff
    out["h7_ex_sd"] = float(d7["ex"].std())
    return out
