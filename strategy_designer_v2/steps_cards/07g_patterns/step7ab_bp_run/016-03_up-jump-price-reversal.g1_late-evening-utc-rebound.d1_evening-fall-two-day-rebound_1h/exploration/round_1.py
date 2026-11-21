def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            v = d["volume"].astype(float).values
            ts = pd.to_datetime(d["timestamp"])
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            n = len(c)
            for H in (48, 120):
                for t in range(0, n, H):
                    if t < 168 or t+H >= n: continue
                    rr = r[t-71:t+1]
                    past72 = c[t]/c[t-72]-1
                    past24 = c[t]/c[t-24]-1
                    eff = abs(np.log(c[t]/c[t-72]))/np.nansum(np.abs(np.log1p(rr)))
                    absr = np.abs(rr)
                    top3 = np.sort(absr)[-3:].sum()/absr.sum()
                    vv = v[t-71:t+1]
                    vshare = np.sort(vv)[-3:].sum()/max(vv.sum(),1e-12)
                    vol24 = np.nanstd(r[t-23:t+1])
                    vol168 = np.nanstd(r[t-167:t+1])
                    rows.append(dict(coin=coin, w=w, H=H, fwd=c[t+H]/c[t]-1,
                        past72=past72, past24=past24, eff=eff, top3=top3, vshare=vshare,
                        volratio=vol24/vol168 if vol168>0 else np.nan,
                        vol168=vol168, hour=ts[t].hour, wd=ts[t].weekday(), yr=ts[t].year))
    X = pd.DataFrame(rows)
    # excess vs coin mean per H, and z by coin usual move
    X["mu"] = X.groupby(["coin","H"])["fwd"].transform("mean")
    X["sd"] = X.groupby(["coin","H"])["fwd"].transform("std")
    X["ex"] = (X["fwd"]-X["mu"])/X["sd"]
    X["p72z"] = X["past72"]/X.groupby(["coin","H"])["past72"].transform("std")
    X["p24z"] = X["past24"]/X.groupby(["coin","H"])["past24"].transform("std")
    out = {}
    def reg(df, cols):
        import numpy.linalg as la
        D = df[cols+["ex"]].dropna()
        A = np.c_[np.ones(len(D)), D[cols].values]
        b, res, *_ = la.lstsq(A, D["ex"].values, rcond=None)
        e = D["ex"].values - A@b
        s2 = e@e/(len(D)-A.shape[1])
        se = np.sqrt(np.diag(s2*la.inv(A.T@A)))
        return pd.Series(np.r_[b/se, len(D)], index=["t_const"]+["t_"+x for x in cols]+["n"])
    for H in (48,120):
        S = X[X.H==H].copy()
        S["eff_c"] = S["eff"]-S["eff"].mean()
        S["p72_x_eff"] = S["p72z"]*S["eff_c"]
        S["top3_c"] = S["top3"]-S["top3"].mean()
        S["p72_x_top3"] = S["p72z"]*S["top3_c"]
        S["vsh_c"]=S["vshare"]-S["vshare"].mean()
        S["p72_x_vsh"]=S["p72z"]*S["vsh_c"]
        out[f"reg_H{H}"] = pd.DataFrame({
            "size":reg(S,["p72z"]),
            "eff":reg(S,["p72z","eff_c","p72_x_eff"]),
            "top3":reg(S,["p72z","top3_c","p72_x_top3"]),
            "vshare":reg(S,["p72z","vsh_c","p72_x_vsh"]),
            "p24":reg(S,["p24z"]),
        })
        S["vq"]=S.groupby("coin")["vol168"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
        out[f"byvolq_H{H}"]=S.groupby("vq")["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
        S["vrq"]=S.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
        out[f"byvolratioq_H{H}"]=S.groupby("vrq")["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
        S["pq"]=S.groupby("coin")["past72"].transform(lambda s: pd.qcut(s,5,labels=False))
        S["eq"]=S.groupby("coin")["eff"].transform(lambda s: pd.qcut(s,3,labels=False))
        out[f"p72q_by_effq_H{H}"]=S.pivot_table(index="pq",columns="eq",values="ex",aggfunc="mean")
        out[f"bycoin_p72_H{H}"]=S.groupby("coin").apply(lambda g: pd.Series({"corr":g["p72z"].corr(g["ex"]),"n":len(g)}))
    # book days
    dd=[]
    for coin in data["days"]:
        for w,df in data["days"][coin].items():
            x=df.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    out["book_by_year"]=D.assign(yr=pd.to_datetime(D["day"]).dt.year).groupby("yr")[["book_return","coin_return"]].agg(["mean","count"])
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    return out
