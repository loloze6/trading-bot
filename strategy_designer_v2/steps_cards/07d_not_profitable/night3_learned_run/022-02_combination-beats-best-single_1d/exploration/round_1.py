import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=5
    cases=[]; daily=[]; barrows=[]
    for coin in data["bars"]:
        # drift of coin over all windows (5-bar grid)
        g_all=[]
        for w,b in data["bars"][coin].items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            g_all+=list(c[idx+H]/c[idx]-1)
        drift=np.mean(g_all)
        dd=[]
        for w,d in data["days"][coin].items():
            dd+=list(d["coin_return"].dropna())
        dmean=np.mean(dd)
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"]
            comb=b.get("debug_info.components.combined.post_pipeline_value")
            best=b.get("debug_info.components.best.post_pipeline_value")
            r28=c/c.shift(28)-1; r1=c/c.shift(1)-1
            vol30=np.log(c).diff().rolling(30).std()
            hi90=c/c.rolling(90,min_periods=30).max()-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            alloc=b["postRebalance_current_allocation"]
            idx=np.arange(0,len(c)-H,H)
            for i in idx:
                cases.append(dict(coin=coin,win=w,year=yr[i],y=c[i+H]/c[i]-1-drift,
                    comb=comb[i] if comb is not None else np.nan,best=best[i] if best is not None else np.nan,
                    r28=r28[i],r1=r1[i],vol30=vol30[i],hi90=hi90[i],alloc=alloc[i]))
            nxt=c.shift(-1)/c-1
            barrows.append(pd.DataFrame(dict(coin=coin,year=yr,alloc=alloc,gain=alloc*nxt,
                    chg=b["allocation_change"].abs() if "allocation_change" in b else np.nan,dmean=dmean)))
            d=data["days"][coin][w]
            daily.append(pd.DataFrame(dict(coin=coin,br=d["book_return"],cr=d["coin_return"],
                    year=pd.to_datetime(d["day"]).dt.year)))
    C=pd.DataFrame(cases); B=pd.concat(barrows); D=pd.concat(daily).dropna()
    out={}
    def cor(df,col):
        x=df[[col,"y"]].dropna()
        if len(x)<20: return np.nan,len(x)
        return stats.pearsonr(x[col],x["y"])[0],len(x)
    rows=[]
    for col in ["comb","best","r28","r1","vol30","hi90","alloc"]:
        r,n=cor(C,col); rows.append(dict(signal=col,corr=r,n=n))
    out["corr_with_y_pooled"]=pd.DataFrame(rows)
    yrows=[]
    for y,g in C.groupby("year"):
        dct=dict(year=y,n=len(g))
        for col in ["comb","best","r28","r1","vol30","hi90"]:
            dct[col]=cor(g,col)[0]
        yrows.append(dct)
    out["corr_by_year"]=pd.DataFrame(yrows)
    crow=[]
    for co,g in C.groupby("coin"):
        dct=dict(coin=co)
        for col in ["comb","best","r28","r1","vol30"]:
            dct[col]=cor(g,col)[0]
        crow.append(dct)
    out["corr_by_coin"]=pd.DataFrame(crow)
    # long vs short gain
    B=B.dropna(subset=["gain"])
    B["side"]=np.sign(B["alloc"])
    out["gain_by_side"]=B.groupby("side").agg(n=("gain","size"),mean_gain=("gain","mean"),
        mean_alloc=("alloc","mean"),drift_part=("dmean","mean")).assign(
        drift_gain=lambda x: x.mean_alloc*x.drift_part)
    out["book_vs_hold_by_year"]=D.groupby("year").agg(book=("br","mean"),hold=("cr","mean"),n=("br","size"))
    out["book_vs_hold_by_coin"]=D.groupby("coin").agg(book=("br","mean"),hold=("cr","mean"))
    out["mean_abs_alloc_change_per_bar"]=float(B["chg"].mean())
    out["mean_abs_alloc"]=float(B["alloc"].abs().mean())
    out["gross_gain_per_bar"]=float(B["gain"].mean())
    out["book_daily_mean"]=float(D["br"].mean())
    # quintiles of comb vs y
    q=C.dropna(subset=["comb"]).copy(); q["qb"]=pd.qcut(q["comb"],5,labels=False)
    out["y_by_comb_quintile"]=q.groupby("qb")["y"].agg(["mean","count"])
    return out
