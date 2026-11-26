def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"]
            lr=np.log(c).diff()
            vol=lr.rolling(20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"year":ts.dt.year,
                "day":ts.dt.floor("D"),
                "r1":c.shift(-1)/c-1,"r1b":c.shift(-2)/c.shift(-1)-1,"r2":c.shift(-2)/c-1,
                "fc":b["forecast"],"pos":np.arange(len(b))})
            for L in [3,7,14,28,56]:
                d[f"s{L}"]=(np.log(c)-np.log(c.shift(L)))/(vol*np.sqrt(L))
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    out={}
    g=A.dropna(subset=["r1"]).groupby("wd")["r1"]
    out["r1_by_weekday_of_bar"]=pd.DataFrame({"mean":g.mean(),"n":g.size(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    fri=A[A.wd==4].dropna(subset=["r2","s14"]).copy()
    fri["top"]=fri.s14>0
    # Saturday vs Sunday leg split by s14 sign
    g=fri.groupby("top")
    out["fri_legs_by_s14_sign"]=pd.DataFrame({"sat":g.r1.mean(),"sun":g.r1b.mean(),"r2":g.r2.mean(),"n":g.size()})
    # other weekdays: next-day r1 by s14 sign, per weekday
    o=A.dropna(subset=["r1","s14"]).copy()
    o["up"]=o.s14>0
    out["r1_up_minus_down_by_wd"]=o.groupby("wd").apply(lambda x: pd.Series({
        "up":x[x.up].r1.mean(),"down":x[~x.up].r1.mean(),
        "t":stats.ttest_ind(x[x.up].r1,x[~x.up].r1,equal_var=False).statistic}))
    # Friday: lookback comparison, correlation of s_L with r2 and top-minus-bottom tercile
    res={}
    for L in [3,7,14,28,56]:
        f=A[A.wd==4].dropna(subset=["r2",f"s{L}"])
        q=pd.qcut(f[f"s{L}"],3,labels=False)
        top=f[q==2].r2; bot=f[q==0].r2
        res[L]={"corr":f[f"s{L}"].corr(f.r2),"top":top.mean(),"bot":bot.mean(),
                "t":stats.ttest_ind(top,bot,equal_var=False).statistic,"n":len(f)}
    out["fri_lookback"]=pd.DataFrame(res).T
    # Friday s14>0 minus s14<=0 by year and by coin
    def diff(x):
        a=x[x.s14>0].r2; b_=x[x.s14<=0].r2
        return pd.Series({"up":a.mean(),"down":b_.mean(),"n_up":len(a),"t":stats.ttest_ind(a,b_,equal_var=False).statistic})
    out["fri_by_year"]=fri.groupby("year").apply(diff)
    out["fri_by_coin"]=fri.groupby("coin").apply(diff)
    # day-clustered: mean over days of up-cases excess vs mean
    mu2=A[A.pos%2==0].groupby("coin").r2.mean()
    fri["ex"]=fri.r2-fri.coin.map(mu2)
    up=fri[fri.top].groupby("day").ex.sum()
    out["fri_up_excess_daysum"]=pd.Series({"mean_per_case":fri[fri.top].ex.mean(),
        "t_days":up.mean()/(up.std()/np.sqrt(len(up))),"days":len(up)})
    # Thursday-opening bar r2 (Fri+Sat) by s14 sign
    th=A[A.wd==3].dropna(subset=["r2","s14"])
    out["thu_r2_by_s14_sign"]=th.groupby(th.s14>0).agg(r1=("r1","mean"),r1b=("r1b","mean"),r2=("r2","mean"),n=("r2","size"))
    # book by window
    D=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    bw=D.groupby("w").book_return.mean()
    out["book_by_window_summary"]=pd.Series({"n_windows":len(bw),"pos_windows":(bw>0).sum(),
        "top3_share":bw.sort_values(ascending=False).head(3).sum()/bw.sum()})
    return out
