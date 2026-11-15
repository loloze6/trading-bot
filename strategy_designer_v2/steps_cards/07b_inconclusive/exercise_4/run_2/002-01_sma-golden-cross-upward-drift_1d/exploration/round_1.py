import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df["debug_info.components.sma_cross.last_history_value"].values if "debug_info.components.sma_cross.last_history_value" in df else np.full(len(df), np.nan)
            # age of current positive state
            pos = (f > 0).astype(int)
            age = np.zeros(len(df))
            for i in range(1, len(df)):
                age[i] = age[i-1] + 1 if pos[i] == pos[i-1] else 0
            r20 = np.full(len(df), np.nan)
            r20[20:] = c[20:] / c[:-20] - 1
            n = len(df)
            for h in (5, 10, 20, 40):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], raw=raw[i], age=age[i], r20=r20[i],
                                     ret=c[i+h]/c[i]-1, year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin","h"])["ret"].transform("mean")
    out = {}
    # slope by horizon
    hs = []
    for h, g in d.groupby("h"):
        s = stats.linregress(g["f"], g["ex"])
        a = g[g.f > 0]; b = g[g.f == 0]
        t = stats.ttest_ind(a["ex"], b["ex"], equal_var=False)
        hs.append(dict(h=h, n=len(g), slope=s.slope, t=s.slope/s.stderr, on_mean=a["ex"].mean(), off_mean=b["ex"].mean(), t_on_off=t.statistic, n_on=len(a)))
    out["by_horizon"] = pd.DataFrame(hs)
    g = d[d.h == 10].copy()
    gp = g[g.f > 0].copy()
    gp["fq"] = pd.qcut(gp["f"].rank(method="first"), 4, labels=False)
    out["h10_fbucket"] = gp.groupby("fq").agg(n=("ex","size"), fmean=("f","mean"), ex=("ex","mean"), hit=("ret", lambda x:(x>0).mean()))
    out["h10_off"] = pd.Series(dict(n=(g.f==0).sum(), ex=g[g.f==0]["ex"].mean(), hit=(g[g.f==0]["ret"]>0).mean()))
    def cs(x):
        if len(x) < 5: return pd.Series(dict(n=len(x)))
        s = stats.linregress(x["f"], x["ex"])
        return pd.Series(dict(n=len(x), slope=s.slope, t=s.slope/s.stderr, on_ex=x[x.f>0]["ex"].mean(), off_ex=x[x.f==0]["ex"].mean()))
    out["h10_by_coin"] = g.groupby("coin").apply(cs)
    out["h10_by_year"] = g.groupby("year").apply(cs)
    gp["agebin"] = pd.cut(gp["age"], [-1, 20, 60, 150, 10000])
    out["h10_on_by_age"] = gp.groupby("agebin").agg(n=("ex","size"), ex=("ex","mean"), sd=("ex","std"))
    gp["r20s"] = np.sign(gp["r20"])
    out["h10_on_by_r20sign"] = gp.groupby("r20s").agg(n=("ex","size"), ex=("ex","mean"), sd=("ex","std"))
    g["rawbin"] = pd.qcut(g["raw"], 6, duplicates="drop")
    out["h10_by_rawspread"] = g.groupby("rawbin").agg(n=("ex","size"), ex=("ex","mean"), hit=("ret", lambda x:(x>0).mean()))
    g20 = d[d.h == 20]
    g20 = g20.assign(age_bin=pd.cut(g20["age"], [-1, 20, 60, 150, 10000]))
    out["h20_on_by_age"] = g20[g20.f>0].groupby("age_bin").agg(n=("ex","size"), ex=("ex","mean"))
    return out
