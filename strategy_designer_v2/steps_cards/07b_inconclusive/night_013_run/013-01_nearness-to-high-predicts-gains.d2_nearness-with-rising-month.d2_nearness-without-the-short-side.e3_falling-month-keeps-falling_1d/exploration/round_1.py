import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    def grid(h):
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values; f = df["forecast"].values
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                n = len(df)
                for i in range(0, n - h, h):
                    r30 = c[i]/c[i-30]-1 if i >= 30 else np.nan
                    r90 = c[i]/c[i-60]-1 if i >= 60 else np.nan
                    rows.append((coin, w, yr[i], f[i], c[i+h]/c[i]-1, r30, r90))
        g = pd.DataFrame(rows, columns=["coin","w","year","f","r","r30","r60"])
        g["ex"] = g["r"] - g.groupby("coin")["r"].transform("mean")
        g["gain"] = g["f"]/10*g["ex"]
        return g
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    hz = {}
    for h in [1,3,5,10,20]:
        g = grid(h); a = g[g.f<0]
        s = tt(a["gain"]); s["ex_neg"] = a["ex"].mean(); s["t_ex_neg"]=tt(a["ex"])["t"]
        s["ex_zero"] = g[g.f==0]["ex"].mean()
        s["t_neg_minus_zero"] = stats.ttest_ind(a["ex"], g[g.f==0]["ex"], equal_var=False).statistic
        hz[h] = s
    out["by horizon (gain=f/10*excess, f<0)"] = pd.DataFrame(hz).T
    g = grid(3); a = g[g.f<0].copy()
    out["h3 by coin"] = a.groupby("coin")["gain"].apply(tt).unstack()
    out["h3 by year"] = a.groupby("year")["gain"].apply(tt).unstack()
    a["q"] = pd.qcut(a["f"], 5, labels=["deepest","q2","q3","q4","shallow"])
    qq = a.groupby("q")["ex"].apply(tt).unstack(); qq["f_mean"]=a.groupby("q")["f"].mean()
    out["h3 excess by forecast quintile"] = qq
    a["trend"] = np.where(a["r60"].isna(), "na", np.where(a["r60"]>0, "60d up", "60d down"))
    out["h3 gain by 60d trend"] = a.groupby("trend")["gain"].apply(tt).unstack()
    out["corr f vs ex (f<0) spearman"] = stats.spearmanr(a["f"], a["ex"]).correlation
    out["corr gain on g all f<0 pearson"] = stats.pearsonr(a["f"], a["ex"])[0]
    out["h3 by window"] = a.groupby("w")["gain"].apply(tt).unstack()
    return out
