def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["bars"].keys())
    wins = sorted(set(w for c in coins for w in data["bars"][c].keys()), key=lambda s:int(s[1:]))
    # exposure
    alloc = []; fc=[]
    for c in coins:
        for w,b in data["bars"][c].items():
            alloc.append(b["postRebalance_current_allocation"].values); fc.append(b["forecast"].values)
    A = np.concatenate(alloc); F = np.concatenate(fc)
    out["exposure"] = pd.Series({"share_bars_long":np.mean(A>0.01),"mean_alloc":np.nanmean(A),"share_forecast_pos":np.mean(F>0),"share_forecast_20":np.mean(F>=19.9),"median_alloc_when_long":np.nanmedian(A[A>0.01])})
    # cases: grid of 78 bars, first bar in cell where forecast rises >=2 from min since flat
    H=78; rows=[]; drifts={}
    for c in coins:
        rs=[]
        for w,b in data["bars"][c].items():
            cl=b["close"].values
            for s in range(0,len(cl)-H,H): rs.append(cl[s+H]/cl[s]-1)
        drifts[c]=(np.mean(rs),np.std(rs))
    for c in coins:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True); cl=b["close"].values; f=b["forecast"].values
            lr=np.log(pd.Series(cl)).diff()
            r30=pd.Series(cl).pct_change(180).values
            r90=pd.Series(cl).pct_change(540).values
            v7=lr.rolling(42).std().values; v60=lr.rolling(360,min_periods=180).std().values
            ma=pd.Series(cl).rolling(300,min_periods=150).mean().values
            n=len(cl)
            for s in range(0,n-H,H):
                for i in range(s,min(s+H,n-H)):
                    if f[i]>=2 and (i==0 or f[i-1]<f[i]):
                        u=cl[i+H]/cl[i]-1-drifts[c][0]
                        rows.append(dict(coin=c,win=w,u=u,tot=cl[i+H]/cl[i]-1,r30=r30[i],r90=r90[i],vr=v7[i]/v60[i] if v60[i] else np.nan,
                                         abovema=cl[i]/ma[i]-1 if ma[i]==ma[i] else np.nan,f=f[i])); break
    C=pd.DataFrame(rows)
    out["cases"]=pd.Series({"n":len(C),"u_mean":C.u.mean(),"t":C.u.mean()/C.u.std()*np.sqrt(len(C)),"tot_mean":C.tot.mean()})
    for col in ["r30","r90","vr","abovema","f"]:
        d=C.dropna(subset=[col]); q=pd.qcut(d[col],4,labels=False,duplicates="drop")
        g=d.groupby(q).agg(n=("u","size"),x=(col,"mean"),u_mean=("u","mean"),u_sd=("u","std"),tot=("tot","mean"))
        g["t"]=g.u_mean/g.u_sd*np.sqrt(g.n)
        out["cases_by_"+col]=g.round(4)
    # book drawdowns per window: book vs coin in worst 30-day stretch
    rr=[]
    for w in wins:
        fr=[]
        for c in coins:
            if w in data["days"][c]:
                d=data["days"][c][w][["day","book_return","coin_return"]]; fr.append(d)
        g=pd.concat(fr).groupby("day").mean().dropna()
        b30=(1+g.book_return).rolling(30).apply(np.prod,raw=True)-1
        h30=(1+g.coin_return).rolling(30).apply(np.prod,raw=True)-1
        i=b30.idxmin()
        rr.append(dict(win=w,book_worst30=b30.min(),hold_same=h30.loc[i]))
    out["worst30_per_window"]=pd.DataFrame(rr).set_index("win").round(3)
    # book daily returns in down-trend vs up-trend days (coin below 50d MA) per coin
    rs=[]
    for c in coins:
        for w,d in data["days"][c].items():
            d=d.copy(); ma=d["close"].rolling(50,min_periods=25).mean()
            d["below"]=(d["close"].shift(1)<ma.shift(1))
            rs.append(d.dropna(subset=["book_return"]))
    D=pd.concat(rs)
    out["book_by_trend"]=D.groupby("below").agg(n=("book_return","size"),book=("book_return","mean"),book_sd=("book_return","std"),coin=("coin_return","mean")).round(5)
    return out
