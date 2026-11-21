def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    # 1-day unusual returns by weekday, on non-overlapping 1-bar grid (every bar), split by year parity and coin group
    rows = []
    for c, ws in bars.items():
        allr = np.concatenate([b["close"].pct_change().dropna().values for b in ws.values()])
        d1 = allr.mean(); s1 = allr.std()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            r = cl[1:] / cl[:-1] - 1
            for i in range(len(r)):
                rows.append((c, w, ts.dt.year.values[i+1], ts.dt.weekday.values[i+1], (r[i]-d1)/s1))
    D = pd.DataFrame(rows, columns=["coin","win","yr","wd","u"])
    D["half"] = np.where(D.yr <= 2021, "early", "late")
    D["big"] = np.where(D.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]), "old6", "new13")
    def t(g):
        return pd.Series({"n": len(g), "mean": g.mean(), "t": g.mean()/(g.std()/np.sqrt(len(g)))})
    out["wd_1d_by_half"] = D.groupby(["half","wd"])["u"].apply(t).unstack()
    out["wd_1d_by_group"] = D.groupby(["big","wd"])["u"].apply(t).unstack()
    # weekday per year: mean only, count of years with positive sign per weekday
    py = D.groupby(["yr","wd"])["u"].mean().unstack()
    out["wd_years_positive"] = (py > 0).sum()
    # cases: signal bar size vs continuation, and horizon by forecast quartile
    cases = []
    for c, ws in bars.items():
        dr = {}
        for h in [5,10,20]:
            r=[]
            for b in ws.values():
                cl=b["close"].values; idx=np.arange(0,len(cl)-h,h); r.extend(cl[idx+h]/cl[idx]-1)
            dr[h]=(np.mean(r), np.std(r))
        for w, b in ws.items():
            b=b.reset_index(drop=True); cl=b["close"].values; n=len(cl)
            f=b["forecast"].fillna(0).values; df_=np.diff(np.r_[0,f])
            sig=np.where((df_>=2)&(f>0))[0]; seen=set()
            hi=b["high"].values; lo=b["low"].values
            for i in sig:
                if i//5 in seen or i+5>=n or i==0: continue
                seen.add(i//5)
                d=dict(coin=c,f=f[i],bar=cl[i]/cl[i-1]-1, rng=(hi[i]-lo[i])/cl[i],
                       closepos=(cl[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan)
                for h in [5,10,20]:
                    if i+h<n: d[f"s{h}"]=(cl[i+h]/cl[i]-1-dr[h][0])/dr[h][1]
                cases.append(d)
    C=pd.DataFrame(cases)
    for col in ["bar","closepos","f","rng"]:
        C[col+"_q"]=pd.qcut(C[col].rank(method="first"),4,labels=False)
        out[f"strength_by_{col}_q"]=C.groupby(col+"_q")[["s5","s10","s20"]].agg(["mean","count"]).round(4)
    # book: daily returns around largest gains/losses; book return by weekday
    rows=[]
    for c, ws in days.items():
        for w, d in ws.items():
            d=d.reset_index(drop=True)
            br=d["book_return"].values; cr=d["coin_return"].values
            wd=pd.to_datetime(d["day"]).dt.weekday.values
            for i in range(len(d)): rows.append((c,wd[i],br[i],cr[i]))
    B=pd.DataFrame(rows,columns=["coin","wd","br","cr"]).dropna()
    out["book_by_weekday"]=B.groupby("wd")["br"].apply(t).unstack()
    return out
