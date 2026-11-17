def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),
                "dow":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "r":r,"z":r/vol,"vol":vol,
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f5":c.shift(-5)/c-1,
                "vr":b["volume"]/b["volume"].rolling(20,min_periods=20).mean(),
                "r7":c/c.shift(7)-1,
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin mean 1-day return
    m1=D.groupby("coin")["f1"].mean(); D["e1"]=D["f1"]-D["coin"].map(m1)
    m2=D[D.pos%2==0].groupby("coin")["f2"].mean(); D["e2"]=D["f2"]-D["coin"].map(m2)
    out={}
    g=D.dropna(subset=["e1"]).groupby("dow")["e1"]
    out["next-day excess by dow of bar"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # reversal: -sign(z)*e1 by dow
    X=D.dropna(subset=["z","e1"]).copy()
    X["rev1"]=-np.sign(X.z)*X.e1; X["slopev"]=-X.z*X.e1
    g=X.groupby("dow")
    out["fade1 by dow"]=pd.DataFrame({"rev_mean":g.rev1.mean(),"t":g.rev1.mean()/(g.rev1.std()/np.sqrt(g.rev1.count())),
        "corr_z_e1":g.apply(lambda x: x.z.corr(x.e1)),"n":g.rev1.count()})
    X["az"]=pd.qcut(X.z.abs(),5,labels=False)
    g=X.groupby("az")
    out["fade1 by |z| quint all days"]=pd.DataFrame({"rev":g.rev1.mean(),"t":g.rev1.mean()/(g.rev1.std()/np.sqrt(g.rev1.count())),"up_e1":g.apply(lambda x:x[x.z>0].e1.mean()),"dn_e1":g.apply(lambda x:x[x.z<0].e1.mean())})
    S=X[X.dow==6].dropna(subset=["e2"]).copy()
    S["rev2"]=-np.sign(S.z)*S.e2
    S["vq"]=pd.qcut(S.vr,3,labels=False)
    g=S.groupby("vq")
    out["sun fade2 by vol ratio tercile"]=pd.DataFrame({"rev2":g.rev2.mean(),"t":g.rev2.mean()/(g.rev2.std()/np.sqrt(g.rev2.count())),"n":g.rev2.count()})
    S["sgn"]=np.sign(S.z)
    g=S.groupby("sgn")
    out["sun e2 by sign of sunday move"]=pd.DataFrame({"e2":g.e2.mean(),"t":g.e2.mean()/(g.e2.std()/np.sqrt(g.e2.count())),"n":g.e2.count()})
    S["azq"]=pd.qcut(S.z.abs(),3,labels=False)
    out["sun e2 by sign x |z| tercile"]=S.groupby(["sgn","azq"]).e2.agg(["mean","count"])
    # 7-day return momentum, 5-day fwd non-overlap
    Y=D[D.pos%5==0].dropna(subset=["r7","f5"]).copy()
    m5=Y.groupby("coin").f5.mean(); Y["e5"]=Y.f5-Y.coin.map(m5)
    Y["q"]=pd.qcut(Y.r7/Y.vol,5,labels=False)
    g=Y.groupby("q").e5
    out["e5 by 7d ret/vol quint"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # vol level
    Z=X.copy(); Z["vq"]=Z.groupby("coin").vol.transform(lambda s: pd.qcut(s,3,labels=False))
    g=Z.groupby("vq")
    out["by vol tercile: e1 mean, fade1"]=pd.DataFrame({"e1":g.e1.mean(),"fade":g.rev1.mean(),"t_fade":g.rev1.mean()/(g.rev1.std()/np.sqrt(g.rev1.count()))})
    # book by dow
    bd=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            bd.append(dd.assign(coin=coin))
    B=pd.concat(bd); B["dow"]=pd.to_datetime(B["day"]).dt.dayofweek
    g=B.dropna(subset=["book_return"]).groupby("dow")
    out["book & coin daily ret by dow"]=pd.DataFrame({"book":g.book_return.mean(),"coin":g.coin_return.mean(),"coin_t":g.coin_return.mean()/(g.coin_return.std()/np.sqrt(g.coin_return.count()))})
    return out
