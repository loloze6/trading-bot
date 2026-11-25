import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            hi = df["high"].astype(float).rolling(20).max(); lo = df["low"].astype(float).rolling(20).min()
            pos = 2*(c-lo)/(hi-lo)-1
            ts = pd.to_datetime(df["timestamp"])
            # recompute profile from window prices (approx: within window only)
            r1 = c.pct_change()
            tr = c/c.shift(60)-1
            vol = r1.rolling(30).std()
            vpct = vol.rolling(365, min_periods=120).apply(lambda a: (a<=a[-1]).mean(), raw=True)
            for h in (5,10):
                fwd = c.shift(-h)/c-1
                for i in range(0, len(df), h):
                    if np.isnan(fwd.iloc[i]) or np.isnan(pos.iloc[i]): continue
                    t_ = tr.iloc[i]; v_ = vpct.iloc[i]
                    trend = np.nan if np.isnan(t_) else ("rising" if t_>0.1 else ("falling" if t_<-0.1 else "choppy"))
                    ag = np.nan if np.isnan(v_) else ("agitated" if v_>0.5 else "calm")
                    rows.append(dict(coin=coin, w=w, h=h, pos=pos.iloc[i], cc=(df["regime"].iloc[i]=="unknown"),
                                     trend=trend, ag=ag, r=fwd.iloc[i], yr=ts.iloc[i].year, day=str(ts.iloc[i])[:10]))
    d = pd.DataFrame(rows)
    d["x"] = d["r"] - d.groupby(["coin","h"])["r"].transform("mean")
    def slope(g):
        g = g.dropna(subset=["pos","x"])
        n = len(g)
        if n < 10: return pd.Series({"n":n,"days":g["day"].nunique(),"slope%":np.nan,"t_clu":np.nan})
        X = g["pos"].values - g["pos"].mean(); y = g["x"].values - g["x"].mean()
        b = (X*y).sum()/(X*X).sum(); e = y - b*X
        sc = pd.Series(X*e).groupby(g["day"].values).sum()
        G = len(sc); var = (sc**2).sum()/(X*X).sum()**2 * G/(G-1)
        return pd.Series({"n":n,"days":g["day"].nunique(),"slope%":100*b,"t_clu":b/np.sqrt(var)})
    out = {}
    d5 = d[d.h==5]
    out["slope_full_range_cc_vs_not_h5"] = d5.groupby("cc").apply(slope)
    out["slope_full_range_all_h5"] = slope(d5).to_frame().T
    out["slope_full_range_all_h10"] = slope(d[d.h==10]).to_frame().T
    out["slope_by_trend_h5"] = d5.groupby("trend").apply(slope)
    out["slope_by_ag_h5"] = d5.groupby("ag").apply(slope)
    out["slope_by_half_h5_all"] = d5.groupby(d5.pos>0).apply(slope)
    out["slope_by_half_h5_cc"] = d5[d5.cc].groupby(d5[d5.cc].pos>0).apply(slope)
    out["slope_all_by_year_h5"] = d5.groupby("yr").apply(slope)
    out["slope_all_by_coin_h5"] = d5.groupby("coin").apply(slope)
    out["slope_cc_by_year_h5"] = d5[d5.cc].groupby("yr").apply(slope)
    return out
