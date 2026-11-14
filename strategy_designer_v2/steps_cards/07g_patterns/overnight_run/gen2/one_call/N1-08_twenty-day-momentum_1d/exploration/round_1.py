def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    out = {}
    # Non-overlapping forward returns by forecast quintile at horizons 1,5,20
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].values
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            # realized vol 20
            vol = pd.Series(r1).rolling(20).std().values
            ts = pd.to_datetime(df["timestamp"])
            for h in (1,5,20):
                for i in range(0, len(df)-h, h):
                    rows.append((c, w, h, f[i], cl[i+h]/cl[i]-1, r1[i], vol[i], ts.iloc[i].weekday()))
    R = pd.DataFrame(rows, columns=["coin","win","h","f","fwd","r1","vol","wd"])
    def tstat(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    res = []
    for h in (1,5,20):
        s = R[R.h==h].copy()
        s["q"] = pd.qcut(s.f.rank(method="first"), 5, labels=False)
        g = s.groupby("q").fwd.apply(tstat).unstack()
        g["h"] = h
        res.append(g.reset_index())
    out["fwd_by_forecast_quintile"] = pd.concat(res)
    # forecast extreme bins
    s = R[R.h==5].copy()
    s["fb"] = pd.cut(s.f, [-21,-15,-5,0,5,15,21])
    out["fwd5_by_forecast_bin"] = s.groupby("fb").fwd.apply(tstat).unstack()
    # after large 1-day moves, next day return (h=1)
    s = R[R.h==1].copy()
    s["z"] = s.r1/s.vol
    s["zb"] = pd.cut(s.z, [-np.inf,-2,-1,0,1,2,np.inf])
    out["next1_by_prev_z"] = s.groupby("zb").fwd.apply(tstat).unstack()
    out["next1_by_weekday"] = s.groupby("wd").fwd.apply(tstat).unstack()
    s5 = R[R.h==5].copy()
    s5["vq"] = s5.groupby("coin").vol.transform(lambda v: pd.qcut(v.rank(method="first"),3,labels=False))
    out["fwd5_by_volterc"] = s5.groupby("vq").fwd.apply(tstat).unstack()
    # trades
    T = pd.concat([trades[c][w].assign(coin=c, win=w) for c in trades for w in trades[c] if len(trades[c][w])])
    T["dur_d"] = T.duration_minutes/1440
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"), mean=("net_profit_loss_percent","mean"), win=("net_profit_loss_percent", lambda x:(x>0).mean()), dur=("dur_d","median"))
    out["trades_by_coin_side"] = T.groupby(["coin","side"]).net_profit_loss_percent.agg(["size","mean","sum"])
    return out
