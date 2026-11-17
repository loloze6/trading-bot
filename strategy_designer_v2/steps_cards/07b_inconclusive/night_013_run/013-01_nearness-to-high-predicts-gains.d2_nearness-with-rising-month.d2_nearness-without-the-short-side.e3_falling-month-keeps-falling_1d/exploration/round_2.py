import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    h = 3
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values
            n = len(df)
            for i in range(0, n - h, h):
                r30 = c[i]/c[i-30]-1 if i >= 30 else np.nan
                r60 = c[i]/c[i-60]-1 if i >= 60 else np.nan
                rows.append((coin, w, f[i], c[i+h]/c[i]-1, r30, r60))
    g = pd.DataFrame(rows, columns=["coin","w","f","r","r30","r60"])
    g["ex"] = g["r"] - g.groupby("coin")["r"].transform("mean")
    g["gain"] = g["f"]/10*g["ex"]
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    a = g[g.f<0].copy()
    a["trend"] = np.where(a["r60"].isna(), "na", np.where(a["r60"]>0, "60d up", "60d down"))
    a["half"] = np.where(a["f"] < a["f"].median(), "deep", "shallow")
    out["excess by trend x half"] = a.groupby(["trend","half"])["ex"].apply(tt).unstack()
    up = a[a.trend=="60d up"].copy()
    up["q"] = pd.qcut(up["f"], 3, labels=["deep","mid","shallow"])
    out["60d up: excess by f tercile"] = up.groupby("q")["ex"].apply(tt).unstack()
    out["60d up spearman f vs ex"] = stats.spearmanr(up["f"], up["ex"]).correlation
    out["60d up by coin gain"] = up.groupby("coin")["gain"].apply(tt).unstack()
    # graded on raw r30 among all cases with r30<0
    b = g[g.r30<0].copy()
    b["q"] = pd.qcut(b["r30"], 5, labels=["deepest","q2","q3","q4","shallow"])
    qq = b.groupby("q")["ex"].apply(tt).unstack(); qq["r30_mean"] = b.groupby("q")["r30"].mean()
    out["excess by raw r30 quintile (r30<0)"] = qq
    out["spearman r30 vs ex (r30<0)"] = stats.spearmanr(b["r30"], b["ex"]).correlation
    # all cases: raw r30 quintiles
    c_ = g.dropna(subset=["r30"]).copy()
    c_["q"] = pd.qcut(c_["r30"], 5, labels=["q1","q2","q3","q4","q5"])
    q2 = c_.groupby("q")["ex"].apply(tt).unstack(); q2["r30_mean"]=c_.groupby("q")["r30"].mean()
    out["excess by raw r30 quintile (all)"] = q2
    # 60d up: raw r60 position: down month in up 60d -> pullback depth = r30 graded
    up2 = g[(g.r60>0)&(g.r30<0)]
    out["pullback (r60>0,r30<0) spearman r30 vs ex"] = stats.spearmanr(up2["r30"], up2["ex"]).correlation
    out["pullback n, mean ex, t"] = tt(up2["ex"])
    return out
