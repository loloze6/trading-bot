def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=8
    rows=[]; book=[]; drift={}
    for coin,ws in data["bars"].items():
        # coin normal drift over 8 bars
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            allr+=list(c[idx+H]/c[idx]-1)
        drift[coin]=(np.mean(allr),np.std(allr))
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            n=len(c)
            r1=np.r_[np.nan,c[1:]/c[:-1]-1]
            seen=set()
            for t in range(1,n-H):
                if f[t]<=-2 and f[t-1]-f[t]>=2:
                    cell=t//H
                    if cell in seen: continue
                    seen.add(cell)
                    fwd=c[t+H]/c[t]-1
                    vol=np.nanstd(r1[max(1,t-19):t+1])
                    rows.append(dict(coin=coin,w=w,absf=-f[t],fwd=fwd,
                        exc=-(fwd-drift[coin][0]),tot=-fwd,
                        ret30=c[t]/c[t-30]-1 if t>=30 else np.nan,
                        ret10=c[t]/c[t-10]-1 if t>=10 else np.nan,
                        ret2=c[t]/c[t-2]-1 if t>=2 else np.nan,
                        vol20=vol,year=pd.Timestamp(b["timestamp"].iloc[t]).year))
        for w,d in data["days"][coin].items():
            bb=ws[w]
            a=bb["postRebalance_current_allocation"].values
            book.append(dict(coin=coin,w=w,br=d["book_return"].mean(),cr=d["coin_return"].mean(),
                expo=np.mean(a!=0),meanpos=np.mean(a)))
    R=pd.DataFrame(rows)
    out={}
    out["cases"]=len(R)
    def summ(g):
        return pd.Series(dict(n=len(g),tot=g.tot.mean(),exc=g.exc.mean(),
            t_tot=g.tot.mean()/(g.tot.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out["by_coin"]=R.groupby("coin").apply(summ)
    out["by_year"]=R.groupby("year").apply(summ)
    for k in ["ret30","ret10","ret2","vol20","absf"]:
        q=R.dropna(subset=[k]).copy()
        q["q"]=pd.qcut(q[k],4,labels=False,duplicates="drop")
        g=q.groupby("q").apply(summ); g["mid"]=q.groupby("q")[k].median()
        out["by_"+k]=g
    # correlations
    out["spearman"]=pd.Series({k:stats.spearmanr(R[k],R["tot"],nan_policy="omit")[0] for k in ["ret30","ret10","ret2","vol20","absf"]})
    # book daily
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            bb=data["bars"][coin][w]
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w
            dd["pos"]=bb["postRebalance_current_allocation"].values[:len(dd)] if len(bb)==len(dd) else np.nan
            D.append(dd)
    D=pd.concat(D)
    daily=D.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    out["book_mean_daily"]=daily.br.mean(); out["hold_mean_daily"]=daily.cr.mean()
    out["exposure_share_bars"]=float((D["pos"]!=0).mean())
    out["mean_pos"]=float(D["pos"].mean())
    cm=D.groupby("coin")["coin_return"].mean()
    D["mkt"]=D["pos"].shift(0)*D["coin"].map(cm)
    out["mkt_part_daily"]=float(D.groupby(["w","day"])["mkt"].mean().mean())
    bw=daily.groupby("w").br.agg(["mean","count"]); bw["sum"]=bw["mean"]*bw["count"]
    out["book_by_window"]=bw
    # deepest fall
    chain=(1+daily.br).cumprod().values
    dd=chain/np.maximum.accumulate(chain)-1
    out["maxdd"]=float(dd.min())
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items(): tr.append(t)
    T=pd.concat(tr)
    out["trades"]=pd.Series(dict(n=len(T),gross=T.profit_loss_percent.mean(),net=T.net_profit_loss_percent.mean(),
        win=(T.net_profit_loss_percent>0).mean(),dur_days=T.duration_minutes.mean()/1440))
    return out
