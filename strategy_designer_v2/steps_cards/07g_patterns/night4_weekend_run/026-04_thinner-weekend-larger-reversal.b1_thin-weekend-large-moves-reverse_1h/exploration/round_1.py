def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    # 1) weekend move vs next 48h, and weekday 48h move vs next 48h (one case per week each)
    rows = []
    hr_rows = []
    mom_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.reset_index(drop=True)
            c = d["close"].values
            n = len(d)
            wd = d["ts"].dt.weekday.values; hh = d["ts"].dt.hour.values
            # hourly returns by hour and weekday
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            hr_rows.append(pd.DataFrame({"coin":coin,"hour":hh,"wd":wd,"r":r1}))
            idx_sun = np.where((wd==6)&(hh==23))[0]
            idx_wed = np.where((wd==2)&(hh==23))[0]  # Mon-Wed 48h move ending Wed 23 -> next 48h (Thu-Fri)
            for kind, idxs in (("weekend",idx_sun),("midweek",idx_wed)):
                for i in idxs:
                    if i-48 < 0 or i+48 >= n: continue
                    past = c[i]/c[i-48]-1; fut = c[i+48]/c[i]-1
                    v = d["volume"].values
                    vr = np.nan
                    if i-167>=0:
                        vr = np.log(v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12))
                    rows.append((coin,w,kind,past,fut,vr))
            # 2) generic 24h past -> 24h future on non-overlapping grid, plus vol
            h=24
            pos = np.arange(h, n-h, h)
            past = c[pos]/c[pos-h]-1; fut = c[pos+h]/c[pos]-1
            lr = np.log(c[1:]/c[:-1])
            rv = np.array([np.std(lr[max(0,p-h):p]) for p in pos])
            mom_rows.append(pd.DataFrame({"coin":coin,"past":past,"fut":fut,"rv":rv,"wd":wd[pos]}))
    R = pd.DataFrame(rows, columns=["coin","w","kind","past","fut","vr"]).dropna(subset=["past","fut"])
    # standardise by coin per kind
    def slope_t(x,y):
        m = np.isfinite(x)&np.isfinite(y)
        res = stats.linregress(x[m],y[m]); return res.slope, res.slope/res.stderr, m.sum()
    t = []
    for kind,g in R.groupby("kind"):
        s,tt,nn = slope_t(g["past"].values,g["fut"].values); t.append((kind,"all",s,tt,nn))
        for coin,gc in g.groupby("coin"):
            s,tt,nn = slope_t(gc["past"].values,gc["fut"].values); t.append((kind,coin,s,tt,nn))
    out["past48_vs_next48_slope"] = pd.DataFrame(t,columns=["kind","coin","slope","t","n"])
    # weekend by thinness tercile and by move size quintile (directed against move)
    g = R[R.kind=="weekend"].copy()
    g["z"] = g.groupby("coin")["past"].transform(lambda x: x/x.std())
    g["fut_against"] = -np.sign(g["past"])*g["fut"]
    g["absq"] = g.groupby("coin")["z"].transform(lambda x: pd.qcut(x.abs(),5,labels=False))
    out["weekend_against_by_absmove_quintile"] = g.groupby("absq")["fut_against"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    g["vrq"] = pd.qcut(g["vr"],3,labels=False)
    out["weekend_against_by_volratio_tercile"] = g.groupby("vrq")["fut_against"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # sign split
    g["up"]=g["past"]>0
    out["weekend_next48_by_sign"] = g.groupby("up")["fut"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # 3) hour and weekday
    H = pd.concat(hr_rows).dropna()
    tf = lambda x: x.mean()/x.std()*np.sqrt(len(x))
    hagg = H.groupby("hour")["r"].agg(["mean","count",tf]); hagg.columns=["mean","n","t"]
    out["hourly_ret_by_hour"] = hagg
    wagg = H.groupby("wd")["r"].agg(["mean","count",tf]); wagg.columns=["mean","n","t"]
    out["hourly_ret_by_weekday"] = wagg
    # 4) 24h momentum/reversal by vol tercile
    M = pd.concat(mom_rows).dropna()
    M["zp"] = M.groupby("coin")["past"].transform(lambda x: x/x.std())
    M["zf"] = M.groupby("coin")["fut"].transform(lambda x: x/x.std())
    M["rvq"] = M.groupby("coin")["rv"].transform(lambda x: pd.qcut(x,3,labels=False))
    t=[]
    s,tt,nn = slope_t(M["zp"].values,M["zf"].values); t.append(("all",s,tt,nn))
    for q,gq in M.groupby("rvq"):
        s,tt,nn = slope_t(gq["zp"].values,gq["zf"].values); t.append((f"vol{q}",s,tt,nn))
    for coin,gq in M.groupby("coin"):
        s,tt,nn = slope_t(gq["zp"].values,gq["zf"].values); t.append((coin,s,tt,nn))
    out["24h_past_vs_next24h_z_slope"] = pd.DataFrame(t,columns=["group","slope","t","n"])
    vagg = M.groupby("rvq")["fut"].agg(["mean","count",tf]); vagg.columns=["mean","n","t"]
    out["next24h_ret_by_vol_tercile"] = vagg
    # 5) book: days
    D=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            x=df[["day","book_return","coin_return"]].copy(); x["coin"]=coin; D.append(x)
    D=pd.concat(D).dropna()
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book_daily_by_weekday"]=D.groupby("wd")[["book_return","coin_return"]].mean()
    q=D["book_return"].quantile([0.01,0.99])
    out["book_extreme_days_coinret"]=pd.DataFrame({"low1pct":D[D.book_return<=q.iloc[0]][["book_return","coin_return"]].mean(),
                                                  "high1pct":D[D.book_return>=q.iloc[1]][["book_return","coin_return"]].mean()})
    return out
