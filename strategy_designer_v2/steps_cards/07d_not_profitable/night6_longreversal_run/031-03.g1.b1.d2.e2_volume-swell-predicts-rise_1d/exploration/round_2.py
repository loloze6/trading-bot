def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]
    out={}
    # coin-day panel with previous-day allocation and conditions known at previous close
    dl=[]
    for c in days:
        for w,d in days[c].items():
            b=bars[c][w].copy().reset_index(drop=True)
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            cl=b["close"]
            b["r14"]=cl/cl.shift(14)-1
            b["r60"]=cl/cl.shift(60)-1
            b["ma50"]=cl/cl.rolling(50).mean()-1
            g=b.groupby("day").agg(alloc=("postRebalance_current_allocation","last"),f=("forecast","last"),
                                   r14=("r14","last"),r60=("r60","last"),ma50=("ma50","last")).shift(1)
            dd=d.copy(); dd["day"]=pd.to_datetime(dd["day"]).dt.floor("D")
            dd=dd.merge(g.reset_index(),on="day",how="left")
            dd["coin"]=c; dd["w"]=w; dl.append(dd)
    D=pd.concat(dl).dropna(subset=["book_return","alloc"])
    D["wn"]=D["w"].str[1:].astype(int)
    def book(series_df,col):
        bk=series_df.groupby(["wn","day"])[col].mean().reset_index().sort_values(["wn","day"])
        r=bk[col]
        sh=r.mean()/r.std()*np.sqrt(365)
        v=(1+r).cumprod().values; pk=np.maximum.accumulate(v); mdd=(v/pk-1).min()
        yr=v[-1]**(365/len(v))-1
        return pd.Series(dict(sharpe=sh,yearly=yr,mdd=mdd,calmar=yr/abs(mdd),mean=r.mean()))
    D["full"]=D["book_return"]
    D["longonly"]=np.where(D["alloc"]>0,D["book_return"],0.0)
    D["shortonly"]=np.where(D["alloc"]<0,D["book_return"],0.0)
    D["long_r14up"]=np.where((D["alloc"]>0)&(D["r14"]>0),D["book_return"],0.0)
    D["long_ma50up"]=np.where((D["alloc"]>0)&(D["ma50"]>0),D["book_return"],0.0)
    D["full_noshort_up"]=np.where((D["alloc"]<0)&(D["ma50"]>0),0.0,D["book_return"])
    D["hold"]=D["coin_return"]
    res={k:book(D,k) for k in ["full","longonly","shortonly","long_r14up","long_ma50up","full_noshort_up","hold"]}
    out["books"]=pd.DataFrame(res).T
    out["share_in_pos"]=pd.Series({k:(D[k]!=0).mean() for k in ["longonly","long_r14up","long_ma50up","full_noshort_up"]})
    # grid at 14 and 28 days: signal side x ma50 state, plus condition alone
    rows=[]
    for c in bars:
        for H in (14,28):
            allr=[]
            for w,df in bars[c].items():
                cl=df["close"].values
                allr+= [cl[i+H]/cl[i]-1 for i in range(0,len(cl)-H,H)]
            drift=np.mean(allr)
            for w,df in bars[c].items():
                df=df.reset_index(drop=True); cl=df["close"]
                ma50=cl/cl.rolling(50).mean()-1; r14=cl/cl.shift(14)-1
                for i in range(0,len(df)-H,H):
                    fr=cl.iloc[i+H]/cl.iloc[i]-1
                    rows.append(dict(H=H,f=df["forecast"].iloc[i],fr=fr,un=fr-drift,ma50=ma50.iloc[i],r14=r14.iloc[i]))
    G=pd.DataFrame(rows).dropna()
    G["side"]=np.sign(G["f"]); G["up"]=(G["ma50"]>0).astype(int)
    def s(x):
        n=len(x); return pd.Series(dict(n=n,tot=x["fr"].mean(),un=x["un"].mean(),t_un=x["un"].mean()/(x["un"].std()/np.sqrt(n))))
    out["grid_H_side_trend"]=G.groupby(["H","side","up"]).apply(s)
    out["grid_trend_alone"]=G.groupby(["H","up"]).apply(s)
    G["fq"]=G.groupby("H")["f"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["grid_H28_fq_up"]=G[(G.H==28)].groupby(["up","fq"]).apply(s)
    out["grid_H14_fq_up"]=G[(G.H==14)].groupby(["up","fq"]).apply(s)
    # trades cost
    T=pd.concat([t for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"]=T.groupby("side").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),days=("duration_minutes",lambda x:(x/1440).mean()))
    return out
