def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        g5 = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            for i in range(0, n - 5, 5):
                g5.append(c[i+5]/c[i]-1)
            rng = (b["high"]-b["low"])
            rr = rng / rng.rolling(20).mean()
            fl = 1 - (b["close"]-b["open"]).abs()/rng.replace(0, np.nan)
            pe5 = b["close"]/b["close"].shift(5)-1
            pe60 = b["close"]/b["close"].shift(60)-1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in range(n):
                cell = i // 5
                d = dict(coin=coin, w=w, i=i, cell=cell, rr=rr.iat[i], fl=fl.iat[i], pe5=pe5.iat[i],
                         pe60=pe60.iat[i], yr=yr.iat[i], day=str(b["timestamp"].iat[i])[:10],
                         act=b["regime"].iat[i]=="mean_reversion")
                for h in (1,2,3,5,10):
                    d[f"r{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(d)
        drift[coin] = np.mean(g5)
    df = pd.DataFrame(rows)
    df["u5"] = df["r5"] - df["coin"].map(drift)
    out = {}
    def summ(sub, col="u5", sign=1):
        sub = sub.dropna(subset=[col])
        sub = sub.groupby(["coin","w","cell"]).head(1)
        v = sign*sub[col]
        dd = v.groupby(sub["day"]).sum()
        t = dd.mean()/ (dd.std(ddof=1)/np.sqrt(len(dd))) * 1 if len(dd)>2 else np.nan
        return pd.Series(dict(n=len(sub), days=len(dd), mean=v.mean(), t_daysum=t, med=v.median(), share_pos=(v>0).mean()))
    up = df["pe5"]>0; dn = df["pe5"]<0
    wide = df["rr"]>=1.5; flat = df["fl"]>=0.9
    sit = up & wide & flat
    t = {}
    t["regime_active_short"] = summ(df[df.act], sign=-1)
    t["sit_up_short"] = summ(df[sit], sign=-1)
    t["other_up_days_short"] = summ(df[up & ~(wide&flat)], sign=-1)
    t["up_narrowflat_short"] = summ(df[up & flat & (df.rr<1.0)], sign=-1)
    t["up_wide_nonflat_short"] = summ(df[up & wide & (df.fl<0.5)], sign=-1)
    t["mirror_dn_long"] = summ(df[dn & wide & flat], sign=1)
    t["loose_up_rr1.2_fl0.7_short"] = summ(df[up & (df.rr>=1.2) & (df.fl>=0.7)], sign=-1)
    t["loose_dn_rr1.2_fl0.7_long"] = summ(df[dn & (df.rr>=1.2) & (df.fl>=0.7)], sign=1)
    out["groups (u5, signed)"] = pd.DataFrame(t).T
    # horizons, situation, raw returns short direction
    hz = {}
    for h in (1,2,3,5,10):
        hz[f"up_short_r{h}"] = summ(df[sit], col=f"r{h}", sign=-1)
        hz[f"dn_long_r{h}"] = summ(df[dn & wide & flat], col=f"r{h}", sign=1)
    out["horizons raw"] = pd.DataFrame(hz).T
    s = df[sit].dropna(subset=["u5"]).groupby(["coin","w","cell"]).head(1).copy()
    s["us"] = -s["u5"]
    out["sit by coin"] = s.groupby("coin")["us"].agg(["count","mean"])
    out["sit by window"] = s.groupby("w")["us"].agg(["count","mean"])
    s["trend"] = pd.cut(s["pe60"], [-9,-0.1,0.1,99], labels=["falling","choppy","rising"])
    out["sit by trend"] = s.groupby("trend")["us"].agg(["count","mean","median"])
    s["pe5q"] = pd.qcut(s["pe5"], 3, labels=False)
    out["sit by pe5 tercile"] = s.groupby("pe5q").agg(n=("us","count"), mean=("us","mean"), pe5=("pe5","mean"))
    s["rrq"] = pd.qcut(s["rr"], 3, labels=False)
    out["sit by rr tercile"] = s.groupby("rrq").agg(n=("us","count"), mean=("us","mean"), rr=("rr","mean"))
    # gradient over all up days: corr of rr*fl with -u5
    a = df[up].dropna(subset=["u5","rr","fl"]).groupby(["coin","w","cell"]).head(1)
    out["up days spearman(rr,-u5)"] = stats.spearmanr(a["rr"], -a["u5"])[0]
    out["up days spearman(fl,-u5)"] = stats.spearmanr(a["fl"], -a["u5"])[0]
    out["n up grid"] = len(a)
    return out
