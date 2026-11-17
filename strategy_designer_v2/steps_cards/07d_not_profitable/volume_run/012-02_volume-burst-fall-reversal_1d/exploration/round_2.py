def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]; trades=data["trades"]
    col="debug_info.components.volratio.last_history_value"
    coinmean = {}
    for c in bars:
        for h in [1,3,5,10]:
            rs=[]
            for w,df in bars[c].items():
                cl=df["close"].values
                idx=np.arange(0,len(cl)-h,h)
                rs.extend(cl[idx+h]/cl[idx]-1)
            coinmean[(c,h)]=np.mean(rs)
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; n=len(cl)
            r1=pd.Series(cl).pct_change()
            vol20=r1.rolling(20).std().shift(1)
            ret30=pd.Series(cl).pct_change(30); ret10=pd.Series(cl).pct_change(10)
            vrc=df["volume"]/df["volume"].rolling(30,min_periods=10).mean()
            vr=df[col] if col in df.columns else pd.Series(np.nan,index=df.index)
            vr=vr.fillna(vrc)
            rng=(df["high"]-df["low"]).replace(0,np.nan)
            wick=(df["close"]-df["low"])/rng
            alloc=df["postRebalance_current_allocation"].fillna(0).values
            last=-10
            for t in range(n):
                if df.loc[t,"regime"]!="mean_reversion": continue
                if t-last<3: continue
                last=t
                d={"coin":c,"win":w,"year":pd.Timestamp(df.loc[t,"timestamp"]).year,"vr":vr.iloc[t],
                   "z":r1.iloc[t]/vol20.iloc[t] if vol20.iloc[t] else np.nan,
                   "ret30":ret30.iloc[t],"ret10":ret10.iloc[t],"wick":wick.iloc[t],"alloc":alloc[t],
                   "hold":int(np.sum(np.abs(alloc[t:min(n,t+10)])>1e-6))}
                for h in [1,3,5,10]:
                    d[f"f{h}"]=cl[t+h]/cl[t]-1-coinmean[(c,h)] if t+h<n else np.nan
                rows.append(d)
    E=pd.DataFrame(rows)
    out={"n":len(E)}
    def summ(g):
        res={}
        for h in [1,3,5,10]:
            x=g[f"f{h}"].dropna()
            res[f"m{h}"]=x.mean(); res[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        res["n"]=len(g); return pd.Series(res)
    out["all"]=summ(E)
    for k,v in [("vr","vr"),("ret30","ret30"),("ret10","ret10"),("wick","wick"),("z","z")]:
        E[k+"q"]=pd.qcut(E[v],3,labels=False,duplicates="drop")
        out["by_"+k]=E.groupby(k+"q").apply(summ)
    out["by_coin"]=E.groupby("coin").apply(summ)
    out["by_year"]=E.groupby("year").apply(summ)
    out["vr_x_ret30"]=E.groupby(["ret30q","vrq"]).apply(summ)[["m1","m3","t3","m5","t5","n"]]
    out["alloc_hold"]=E[["alloc","hold"]].describe()
    D=pd.concat([days[c][w].assign(coin=c,win=w) for c in days for w in days[c]])
    bk=D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book"]=pd.Series({"mean":bk.book_return.mean(),"sd":bk.book_return.std(),"hold_mean":bk.coin_return.mean(),
        "share_coin_days_invested":(D.book_return.abs()>1e-9).mean()})
    T=pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    out["trades"]=pd.Series({"n":len(T),"mean_gross":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean(),
        "mean_dur_days":T.duration_minutes.mean()/1440,"win_share":(T.profit_loss_percent>0).mean()})
    return out
