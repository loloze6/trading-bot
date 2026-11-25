def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        cmean = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            cmean.append(r.dropna())
        mu = pd.concat(cmean).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30).std()
            rng = (h-l)/c.shift(1)
            mrng = rng.rolling(30).mean()
            d = pd.DataFrame({
                "coin":coin,"win":w,"pos":np.arange(len(b)),
                "r":r,"z":r/sd,"rr":rng/mrng,
                "clv":(c-l)/(h-l).replace(0,np.nan),
                "agit":(b["regime"]!="chop"),
                "fc":b["forecast"].astype(float),
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r60":c/c.shift(60)-1,
                "n1":c.shift(-1)/c-1-mu,
                "n2":c.shift(-2)/c.shift(-1)-1-mu,
                "n3":c.shift(-3)/c-1-3*mu,
                "mu":mu,
            })
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["z","rr","n1"])
    out = {}
    def tday(s, dayser):
        g = s.groupby(dayser).sum(); n=s.groupby(dayser).size()
        m = s.mean()
        # day-clustered t
        dev = (s-m).groupby(dayser).sum()
        se = np.sqrt((dev**2).sum())/len(s)
        return m, m/se if se>0 else np.nan, len(g)
    def summ(df, col="n1"):
        res=[]
        return None
    # 1: fall size x range buckets, agitated vs calm
    F = D[D.r<0].copy()
    F["zq"]=pd.qcut(-F.z,3,labels=["smallfall","midfall","bigfall"])
    F["rq"]=pd.qcut(F.rr,3,labels=["narrow","mid","wide"])
    tab=[]
    for (a,zq,rq),g in F.groupby(["agit","zq","rq"],observed=True):
        m,t,nd=tday(g.n1,g.day)
        tab.append(dict(agit=a,zq=zq,rq=rq,n=len(g),mean_pct=m*100,t=t))
    out["fall_x_range_next1"]=pd.DataFrame(tab)
    # 2: up days by z and range (next day)
    U = D[D.r>0].copy()
    U["zq"]=pd.qcut(U.z,3,labels=["small","mid","big"]); U["rq"]=pd.qcut(U.rr,3,labels=["narrow","mid","wide"])
    tab=[]
    for (a,zq,rq),g in U.groupby(["agit","zq","rq"],observed=True):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(agit=a,zq=zq,rq=rq,n=len(g),mean_pct=m*100,t=t))
    out["up_x_range_next1"]=pd.DataFrame(tab)
    # 3: close location on all days, agitated vs calm
    D["cq"]=pd.qcut(D.clv,5,labels=False,duplicates="drop")
    tab=[]
    for (a,cq),g in D.groupby(["agit","cq"]):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(agit=a,clv_q=cq,n=len(g),mean_pct=m*100,t=t))
    out["clv_next1"]=pd.DataFrame(tab)
    # 4: trend profile among agitated falls (bigfall*wide)
    F["trend"]=np.where(F.r60>0.1,"rising",np.where(F.r60<-0.1,"falling","choppy"))
    tab=[]
    for (a,tr),g in F[F.zq=="bigfall"].groupby(["agit","trend"]):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(agit=a,trend=tr,n=len(g),mean_pct=m*100,t=t))
    out["bigfall_by_trend"]=pd.DataFrame(tab)
    # 5: day2 after big agitated falls
    g=F[(F.agit)&(F.zq=="bigfall")].dropna(subset=["n2"])
    m,t,nd=tday(g.n2,g.day); out["bigfall_agit_day2"]=f"mean {m*100:.3f}% t {t:.2f} n {len(g)}"
    # 6: weekday of agitated falls
    tab=[]
    for wd,g in F[F.agit].groupby("wd"):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(wd=wd,n=len(g),mean_pct=m*100,t=t))
    out["agitfall_by_weekday"]=pd.DataFrame(tab)
    # 7: weekday all days
    tab=[]
    for wd,g in D.groupby("wd"):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(wd=wd,n=len(g),mean_pct=m*100,t=t))
    out["all_by_weekday"]=pd.DataFrame(tab)
    # 8: by coin, agitated falls forecast>0
    tab=[]
    for co,g in D[D.fc>0].groupby("coin"):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(coin=co,n=len(g),mean_pct=m*100,t=t,corr=np.corrcoef(g.fc,g.n1)[0,1]))
    out["active_by_coin"]=pd.DataFrame(tab)
    # 9: by year active
    tab=[]
    for y,g in D[D.fc>0].groupby("yr"):
        m,t,nd=tday(g.n1,g.day); tab.append(dict(yr=y,n=len(g),mean_pct=m*100,t=t))
    out["active_by_year"]=pd.DataFrame(tab)
    # 10: book days: largest gains/losses: what prior coin return
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["prev_coin"]=d.coin_return.shift(1); dd.append(d)
    DD=pd.concat(dd).dropna(subset=["book_return"])
    act=DD[DD.book_return!=0]
    q=act.book_return.quantile([0.05,0.95])
    out["book_extremes"]=pd.DataFrame({
        "worst5_prevcoin_mean":[act[act.book_return<=q.iloc[0]].prev_coin.mean()],
        "best5_prevcoin_mean":[act[act.book_return>=q.iloc[1]].prev_coin.mean()],
        "worst5_n":[ (act.book_return<=q.iloc[0]).sum()],
        "share_gain_top5pct":[act[act.book_return>=q.iloc[1]].book_return.sum()/act.book_return.sum()]})
    return out
