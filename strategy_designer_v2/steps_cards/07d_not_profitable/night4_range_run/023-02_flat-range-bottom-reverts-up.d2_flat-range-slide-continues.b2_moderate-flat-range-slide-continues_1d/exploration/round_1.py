def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    out={}
    # coin mean daily return over all windows
    rows=[]; caserows=[]
    for c in bars:
        cr=pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu=cr.mean()
        br_all=[];mk_all=[]
        # 5-bar grid returns per coin
        g5=[]
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            for i in range(0,len(b)-5,5):
                g5.append(cl[i+5]/cl[i]-1)
        mu5=np.mean(g5); sd5=np.std(g5)
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; f=b["forecast"].values
            hi=b["high"].rolling(30).max(); lo=b["low"].rolling(30).min()
            nmr=(b["close"]-b["close"].shift(30)).abs()/(hi-lo)
            ret10=b["close"]/b["close"].shift(10)-1
            ret30=b["close"]/b["close"].shift(30)-1
            ret60=b["close"]/b["close"].shift(60)-1
            pos=((b["close"]-(hi+lo)/2)/(hi-lo))
            for i in range(0,len(b)-5,5):
                if f[i]<0:
                    r=cl[i+5]/cl[i]-1
                    caserows.append(dict(coin=c,w=w,f=f[i],tot=-r,unu=-(r-mu5),nmr=nmr[i],ret10=ret10[i],ret30=ret30[i],ret60=ret60[i],pos=pos[i],year=pd.Timestamp(b["timestamp"][i]).year))
            d=days[c][w].dropna()
            a=b["postRebalance_current_allocation"]
            rows.append(dict(coin=c,w=w,book=d["book_return"].sum(),n=len(d),mkt=0))
        rows_c=pd.DataFrame([r for r in rows if r["coin"]==c])
    cs=pd.DataFrame(caserows)
    def summ(g):
        return pd.Series(dict(n=len(g),tot=g.tot.mean(),unu=g.unu.mean(),t=g.unu.mean()/(g.unu.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out["cases_by_coin"]=cs.groupby("coin").apply(summ)
    out["cases_by_year"]=cs.groupby("year").apply(summ)
    cs["fq"]=pd.qcut(cs.f.rank(method="first"),4,labels=["most_neg","q2","q3","least_neg"])
    out["cases_by_forecast_q"]=cs.groupby("fq").apply(summ)
    for col in ["ret30","ret60","ret10","pos","nmr"]:
        cs[col+"_q"]=pd.qcut(cs[col].rank(method="first"),4,labels=["q1low","q2","q3","q4high"])
        out["cases_by_"+col]=cs.groupby(col+"_q").apply(summ)
    # book daily: by coin, timing vs market
    bk=[]
    for c in days:
        allcr=pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna(); mu=allcr.mean()
        for w,d in days[c].items():
            b=bars[c][w].copy(); b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            a=b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd=d.set_index(pd.to_datetime(d["day"]))
            dd["alloc"]=a.reindex(dd.index).values
            for _,r in dd.dropna(subset=["book_return"]).iterrows():
                bk.append(dict(coin=c,w=w,br=r.book_return,cr=r.coin_return,al=r.alloc,mkt=(r.alloc if pd.notna(r.alloc) else 0)*mu))
    bk=pd.DataFrame(bk)
    out["book_by_coin"]=bk.groupby("coin").agg(mean=("br","mean"),mkt=("mkt","mean"),exposure=("al",lambda x:x.abs().mean()))
    tr=pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    out["trades"]=tr.groupby("coin").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),days=("duration_minutes",lambda x:x.mean()/1440))
    out["trades_all"]=pd.Series(dict(n=len(tr),gross=tr.profit_loss_percent.mean(),net=tr.net_profit_loss_percent.mean(),win=(tr.net_profit_loss_percent>0).mean()))
    return out
