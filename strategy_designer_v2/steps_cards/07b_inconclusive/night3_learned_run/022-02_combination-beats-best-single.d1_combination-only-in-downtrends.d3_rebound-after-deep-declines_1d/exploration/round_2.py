import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            hi = pd.Series(c).rolling(90, min_periods=90).max().values
            rawd = c / hi - 1
            r90 = pd.Series(c).pct_change(90).values
            ts = pd.to_datetime(df["timestamp"])
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, year=ts.iloc[i].year,
                        fwd=c[i+h]/c[i]-1, regime=df["regime"].iloc[i],
                        r90=r90[i], deep=-rawd[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin","h"])["fwd"].transform("mean")
    R["sd"] = R.groupby(["coin","h"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"]/R["sd"]
    R = R.dropna(subset=["deep","r90"])
    def slope(d, x="deep", y="ex"):
        d = d.dropna(subset=[x,y])
        if len(d) < 10: return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        r = stats.linregress(d[x], d[y])
        return pd.Series(dict(n=len(d), slope=r.slope, t=r.slope/r.stderr, mean_ex=d[y].mean(), mean_str=d["str"].mean(), mean_fwd=d["fwd"].mean()))
    D = R[R.r90 < 0].copy()
    U = R[R.r90 >= 0].copy()
    out = {}
    out["down_by_h"] = D.groupby("h").apply(slope)
    out["up_by_h"] = U.groupby("h").apply(slope)
    out["down_h5_by_coin"] = D[D.h==5].groupby("coin").apply(slope)
    out["down_h10_by_coin"] = D[D.h==10].groupby("coin").apply(slope)
    out["down_h5_by_year"] = D[D.h==5].groupby("year").apply(slope)
    D["q"] = D.groupby("h")["deep"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["down_quint"] = D.groupby(["h","q"]).agg(n=("ex","size"), deep=("deep","mean"), ex=("ex","mean"), fwd=("fwd","mean"), strn=("str","mean")).reset_index()
    # depth relative to the coin's usual move: normalise deep by 90d vol proxy? use r90 interaction
    D["deep_x"] = D["deep"]
    out["down_h5_r90_split"] = D[D.h==5].assign(r90q=lambda d: pd.qcut(d.r90, 3, labels=False)).groupby("r90q").apply(slope)
    return out
