import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    col = "debug_info.components.rsi_above_age.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lhv = df[col].values if col in df else np.full(len(df), np.nan)
            n = len(df)
            for h in (14, 21, 28, 42, 56):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, wi=int(w[1:]), year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     h=h, lhv=lhv[i], r=c[i+h]/c[i]-1))
    g = pd.DataFrame(rows)
    g["ex"] = g["r"] - g.groupby(["coin","h"])["r"].transform("mean")
    g["half"] = np.where(g.year <= 2021, "2018-2021", "2022-2025")
    def slope(s):
        s = s.dropna(subset=["lhv","ex"])
        if len(s) < 8: return pd.Series(dict(slope=np.nan, t=np.nan, n=len(s)))
        r = stats.linregress(s["lhv"], s["ex"])
        return pd.Series(dict(slope=r.slope, t=r.slope/r.stderr, n=len(s)))
    res = []
    for side, cond in (("above", lambda s: s.lhv > 0), ("below", lambda s: s.lhv < 0)):
        for h in (14, 21, 28, 42, 56):
            s = g[(g.h==h)]
            s = s[cond(s)]
            res.append(dict(side=side, h=h, grp="all", **slope(s)))
            for k, x in s.groupby("coin"):
                res.append(dict(side=side, h=h, grp=k, **slope(x)))
            for k, x in s.groupby("half"):
                res.append(dict(side=side, h=h, grp=k, **slope(x)))
    out["slopes"] = pd.DataFrame(res)
    s = g[(g.h==28)].dropna(subset=["lhv"]).copy()
    s["bin"] = pd.cut(s.lhv, [-61,-30,-10,0,10,30,61])
    out["ex_by_bin_h28"] = s.groupby("bin")["ex"].agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    return out
