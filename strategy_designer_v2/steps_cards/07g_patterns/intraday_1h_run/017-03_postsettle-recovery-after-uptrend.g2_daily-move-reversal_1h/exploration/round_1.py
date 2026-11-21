def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    gross_d, fee_d, book_d = [], [], []
    hr_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            if n < 200: continue
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            pos = b["postRebalance_current_allocation"].values
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            gross_d.append(np.nansum(pos*r1)); fee_d.append(np.nansum(fee)); book_d.append(n)
            lr = np.log(c)
            ret1 = pd.Series(np.r_[np.nan, np.diff(lr)])
            vol = ret1.rolling(168).std()*np.sqrt(24)
            past24 = pd.Series(lr).diff(24)
            z = past24/vol
            past1 = ret1/ (ret1.rolling(168).std())
            ts = pd.to_datetime(b["timestamp"])
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values
            for h in (1,4,8,24):
                fwd = np.r_[lr[h:]-lr[:-h], [np.nan]*h]
                idx = np.arange(0, n, h)
                for i in idx:
                    rows.append((coin,w,h,z.iloc[i],past1.iloc[i],fwd[i],vol.iloc[i],hr[i],wd[i],b["forecast"].iloc[i]))
    df = pd.DataFrame(rows, columns=["coin","w","h","z","p1","fwd","vol","hr","wd","fc"]).dropna()
    out["gross_vs_fee_per_bar"] = pd.Series({"gross_mean_per_bar": np.sum(gross_d)/np.sum(book_d), "fee_mean_per_bar": np.sum(fee_d)/np.sum(book_d)})
    res = []
    for h, g in df.groupby("h"):
        g = g.copy(); g["fwd"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        s = -np.sign(g["z"])*g["fwd"]
        s1 = -np.sign(g["p1"])*g["fwd"]
        res.append({"h":h,"n":len(g),"rev24_mean":s.mean(),"rev24_t":s.mean()/s.std()*np.sqrt(len(g)),
                    "rev1h_mean":s1.mean(),"rev1h_t":s1.mean()/s1.std()*np.sqrt(len(g)),
                    "corr_z":np.corrcoef(g["z"],g["fwd"])[0,1]})
    out["reversal_by_horizon"] = pd.DataFrame(res)
    g = df[df.h==24].copy(); g["fwd"] -= g.groupby("coin")["fwd"].transform("mean")
    g["zq"] = pd.qcut(g["z"],5,labels=False)
    out["z_quintile_next24"] = g.groupby("zq").agg(n=("fwd","size"),z=("z","mean"),fwd=("fwd","mean"),sd=("fwd","std"))
    g["vq"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False))
    g["s"] = -np.sign(g["z"])*g["fwd"]
    out["rev24_by_voltercile"] = g.groupby("vq")["s"].agg(["size","mean",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["rev24_by_coin"] = g.groupby("coin")["s"].agg(["size","mean",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    g1 = df[df.h==1].copy(); g1["fwd"] -= g1.groupby("coin")["fwd"].transform("mean")
    g1["s"] = -np.sign(g1["z"])*g1["fwd"]
    out["hour_ret_and_rev24"] = g1.groupby("hr").agg(n=("fwd","size"),ret=("fwd","mean"),
        ret_t=("fwd",lambda x: x.mean()/x.std()*np.sqrt(len(x))),rev=("s","mean"),
        rev_t=("s",lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    g4 = df[df.h==4].copy(); g4["fwd"] -= g4.groupby("coin")["fwd"].transform("mean")
    g4["s"]= -np.sign(g4["p1"])*g4["fwd"]
    out["wd_ret24"] = g.groupby("wd")["fwd"].agg(["size","mean",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
