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
            for h in [1, 3, 7, 14, 21]:
                for i in range(0, n - h, h):
                    r5 = c[i] / c[i-5] - 1 if i >= 5 else np.nan
                    rows.append((coin, w, int(w[1:]), yr[i], h, f[i], c[i+h]/c[i]-1, r5))
    d = pd.DataFrame(rows, columns=["coin","w","wn","year","h","f","r","r5"])
    d = d.dropna(subset=["f","r"])
    d["ex"] = d["r"] - d.groupby(["coin","h"])["r"].transform("mean")

    def slope(g):
        if len(g) < 20 or g["f"].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        res = stats.linregress(g["f"], g["ex"])
        return pd.Series({"n": len(g), "slope": res.slope, "t": res.slope / res.stderr})

    out = {}
    out["by_horizon"] = d.groupby("h").apply(slope)
    d7 = d[d.h == 7].copy()
    out["h7_by_coin"] = d7.groupby("coin").apply(slope)
    out["h7_by_year"] = d7.groupby("year").apply(slope)
    d7["dir5"] = np.where(d7["r5"] > 0, "up5", np.where(d7["r5"] <= 0, "down5", "na"))
    out["h7_by_dir5"] = d7.groupby("dir5").apply(slope)
    d7["fside"] = np.where(d7["f"] > 0, "pos", "neg")
    out["h7_by_fside"] = d7.groupby("fside").apply(slope)
    d7["fq"] = pd.qcut(d7["f"], 5, labels=False)
    out["h7_quintile_meanex"] = d7.groupby("fq").agg(n=("ex","size"), f=("f","mean"), ex=("ex","mean"), r=("r","mean"))
    d7["dq"] = d7["dir5"] + "_" + d7["fside"]
    out["h7_dir_x_side_meanex"] = d7.groupby("dq").agg(n=("ex","size"), ex=("ex","mean"), sd=("ex","std"))
    d14 = d[d.h == 14].copy(); d14["dir5"] = np.where(d14["r5"] > 0, "up5", "down5")
    out["h14_by_dir5"] = d14.groupby("dir5").apply(slope)
    d3 = d[d.h == 3].copy(); d3["dir5"] = np.where(d3["r5"] > 0, "up5", "down5")
    out["h3_by_dir5"] = d3.groupby("dir5").apply(slope)
    return out
