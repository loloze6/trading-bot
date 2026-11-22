import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            hh = h.rolling(30).max(); ll = l.rolling(30).min()
            ratio = (c - c.shift(29)).abs() / (hh - ll)
            pos = (c - ll) / (hh - ll)
            ret10 = c.pct_change(10)
            year = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for H in (3, 5, 10):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, H=H, year=year.iloc[i], regime=df["regime"].iloc[i],
                                     ratio=ratio.iloc[i], pos=pos.iloc[i], ret10=ret10.iloc[i],
                                     fwd=c.iloc[i+H]/c.iloc[i]-1))
    g = pd.DataFrame(rows)
    g = g.join(g.groupby(["coin","H"])["fwd"].mean().rename("drift"), on=["coin","H"])
    g["ex"] = g.fwd - g.drift
    g = g.dropna(subset=["ratio","pos","ret10","ex"])
    out = {}
    def sl(x, col="pos"):
        if len(x) < 15: return pd.Series(dict(slope=np.nan, t=np.nan, n=len(x)))
        r = stats.linregress(x[col], x.ex); return pd.Series(dict(slope=r.slope, t=r.slope/r.stderr, n=len(x)))
    sit = g[(g.ratio<=0.5)&(g.pos<0.5)]
    out["pos_slope_by_H_flat_below"] = sit.groupby("H").apply(sl)
    out["pos_slope_by_H_trend_below"] = g[(g.ratio>0.5)&(g.pos<0.5)].groupby("H").apply(sl)
    s5 = sit[sit.H==5]
    out["pos_slope_by_coin_5d"] = s5.groupby("coin").apply(sl)
    out["pos_slope_by_year_5d"] = s5.groupby("year").apply(sl)
    # both drivers together
    X = np.column_stack([np.ones(len(s5)), s5.pos, s5.ret10]); y = s5.ex.values
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X@b
    cov = np.linalg.inv(X.T@X) * (res@res)/(len(y)-3)
    out["multi_5d"] = pd.Series({"b_pos": b[1], "t_pos": b[1]/np.sqrt(cov[1,1]), "b_ret10": b[2], "t_ret10": b[2]/np.sqrt(cov[2,2]), "n": len(y)})
    s5b = s5.copy(); s5b["pb"] = pd.cut(s5b.pos, [0,0.1,0.2,0.3,0.4,0.5])
    out["pos_bins_5d"] = s5b.groupby("pb").ex.agg(["mean","count","std"]).assign(t=lambda x: x["mean"]/(x["std"]/np.sqrt(x["count"])))
    return out
