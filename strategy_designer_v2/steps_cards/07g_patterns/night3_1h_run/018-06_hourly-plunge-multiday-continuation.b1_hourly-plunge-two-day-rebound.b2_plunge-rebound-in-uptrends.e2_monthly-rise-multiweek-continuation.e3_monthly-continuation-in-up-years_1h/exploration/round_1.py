def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    hr = []
    big = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            if n < 1000: continue
            ts = pd.to_datetime(b["timestamp"])
            reg = b["regime"].values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r1":r1}))
            s = pd.Series(r1)
            vol = s.rolling(168, min_periods=100).std().values
            vol_med = np.nanmedian(vol)
            # large hourly moves: z vs past 168h vol, next 24h return
            z = r1/np.r_[np.nan, vol[:-1]]
            f24 = np.r_[c[24:]/c[:-24]-1, [np.nan]*24]
            for i in range(0, n-24, 24):
                pass
            idx = np.where(np.abs(z) > 4)[0]
            last = -100
            for i in idx:
                if i - last < 24 or i+24 >= n: continue
                last = i
                big.append({"coin":coin,"sign":np.sign(z[i]),"f24":f24[i],"f168":(c[i+168]/c[i]-1) if i+168<n else np.nan,"reg":reg[i]})
            for i in range(0, n-168, 168):
                rows.append({"coin":coin,"w":w,"reg":reg[i],
                    "f168":c[i+168]/c[i]-1,
                    "r30": c[i]/c[i-720]-1 if i>=720 else np.nan,
                    "r7": c[i]/c[i-168]-1 if i>=168 else np.nan,
                    "r1d": c[i]/c[i-24]-1 if i>=24 else np.nan,
                    "volrel": vol[i]/vol_med,
                    "dd": c[i]/np.max(c[max(0,i-720):i+1])-1,
                    "fc": float(b["forecast"].iloc[i])})
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["f168"].transform("mean")
    g["un"] = g["f168"]-g["drift"]
    def summ(df, key):
        a = df.groupby(key, observed=True)["un"].agg(["mean","std","count"])
        a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a.round(4)
    out = {}
    g["trend"] = (g["reg"]=="trending")
    gg = g.dropna(subset=["r30"]).copy()
    gg["q30"] = gg.groupby("coin")["r30"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["r30 quintile x trending"] = summ(gg, ["trend","q30"])
    g2 = g.dropna(subset=["r7"]).copy()
    g2["q7"] = g2.groupby("coin")["r7"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["r7 quintile x trending"] = summ(g2, ["trend","q7"])
    g3 = g.dropna(subset=["volrel"]).copy()
    g3["qv"] = g3.groupby("coin")["volrel"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    out["vol tercile x trending"] = summ(g3, ["trend","qv"])
    g4 = g.dropna(subset=["dd"]).copy()
    g4["qd"] = g4.groupby("coin")["dd"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["30d drawdown quintile x trending"] = summ(g4, ["trend","qd"])
    out["by coin x trending"] = summ(g, ["coin","trend"])
    H = pd.concat(hr).dropna()
    a = H.groupby("hour")["r1"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["hour mean 1h ret bps"] = (a.assign(mean=a["mean"]*1e4)[["mean","t"]]).round(2)
    a = H.groupby("wd")["r1"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["weekday mean 1h ret bps"] = (a.assign(mean=a["mean"]*1e4)[["mean","t"]]).round(2)
    B = pd.DataFrame(big)
    if len(B):
        bb = B.groupby(["sign"])[["f24","f168"]].agg(["mean","count"])
        out["after |z|>4 hour moves"] = bb.round(4)
        out["after big moves t f24"] = B.groupby("sign")["f24"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).round(2)
    D = []
    for coin, wins in days.items():
        for w, d in wins.items():
            D.append(d[["book_return","coin_return"]].assign(coin=coin))
    D = pd.concat(D).dropna()
    D["inpos"] = D["book_return"].abs() > 1e-9
    out["book days in/out"] = D.groupby("inpos")[["book_return","coin_return"]].agg(["mean","count"]).round(5)
    return out
