def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    # coin mean returns for h horizons on grids
    coinmean = {}
    for c in bars:
        for h in [1,3,5,10]:
            rs=[]
            for w,df in bars[c].items():
                cl=df["close"].values
                idx=np.arange(0,len(cl)-h,h)
                rs.extend(cl[idx+h]/cl[idx]-1)
            coinmean[(c,h)]=np.mean(rs)
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; n=len(cl)
            r1=pd.Series(cl).pct_change()
            vol20=r1.rolling(20).std().shift(1)
            ret30=pd.Series(cl).pct_change(30)
            ret10=pd.Series(cl).pct_change(10)
            vr=df["debug_info.components.volratio.last_history_value"]
            rng=(df["high"]-df["low"]).replace(0,np.nan)
            wick=(df["close"]-df["low"])/rng
            last=-10
            for t in range(n):
                if df.loc[t,"regime"]!="mean_reversion": continue
                if t-last<3: continue
                last=t
                d={"coin":c,"win":w,"vr":vr.iloc[t],"z":r1.iloc[t]/vol20.iloc[t] if vol20.iloc[t] else np.nan,
                   "ret30":ret30.iloc[t],"ret10":ret10.iloc[t],"wick":wick.iloc[t],"alloc":df.loc[t,"postRebalance_current_allocation"]}
                for h in [1,3,5,10]:
                    d[f"f{h}"]=cl[t+h]/cl[t]-1-coinmean[(c,h)] if t+h<n else np.nan
                rows.append(d)
    E=pd.DataFrame(rows)
    out={}
    out["n"]=len(E)
    def summ(g):
        res={}
        for h in [1,3,5,10]:
            x=g[f"f{h}"].dropna()
            res[f"m{h}"]=x.mean(); res[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        res["n"]=len(g)
        return pd.Series(res)
    out["all"]=summ(E)
    E["vrq"]=pd.qcut(E["vr"],3,labels=False,duplicates="drop")
    out["by_vr"]=E.groupby("vrq").apply(summ)
    E["r30q"]=pd.qcut(E["ret30"],3,labels=False)
    out["by_ret30"]=E.groupby("r30q").apply(summ)
    E["r10q"]=pd.qcut(E["ret10"],3,labels=False)
    out["by_ret10"]=E.groupby("r10q").apply(summ)
    E["wq"]=pd.qcut(E["wick"],3,labels=False)
    out["by_wick"]=E.groupby("wq").apply(summ)
    E["zq"]=pd.qcut(E["z"],3,labels=False)
    out["by_z"]=E.groupby("zq").apply(summ)
    out["by_coin"]=E.groupby("coin").apply(summ)
    out["vr_x_ret30"]=E.groupby(["r30q","vrq"]).apply(summ)[["m3","t3","m5","n"]]
    # book stats
    D=pd.concat([days[c][w].assign(coin=c,win=w) for c in days for w in days[c]])
    bk=D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book"]=pd.Series({"mean":bk.book_return.mean(),"sd":bk.book_return.std(),"hold_mean":bk.coin_return.mean(),"hold_sd":bk.coin_return.std(),"share_days_invested":(D.book_return.abs()>1e-9).mean()})
    out["mean_alloc_active"]=E["alloc"].describe()
    return out
