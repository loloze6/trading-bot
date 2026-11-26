def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    H=14
    rows=[]
    drift={}
    for c in bars:
        rr=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(df)-H,H):
                rr.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rr) if rr else np.nan
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"].values
            f=df["forecast"].fillna(0).values
            raw=df.get("debug_info.components.scaled_rise.last_history_value")
            reg=df["regime"].values
            r7=pd.Series(cl).pct_change(7).values
            r30=pd.Series(cl).pct_change(30).values
            dr=pd.Series(cl).pct_change()
            vol30=dr.rolling(30).std().values
            sc=pd.Series(r7)/ (pd.Series(cl).pct_change(7).abs().rolling(30).mean())
            for i in range(0,len(df)-H,H):
                fr=cl[i+H]/cl[i]-1
                rows.append(dict(coin=c,w=w,day=df["timestamp"].iloc[i].floor("D"),f=f[i],inprof=reg[i]=="unknown",
                    r7=r7[i],r30=r30[i],sc=sc.iloc[i],vol=vol30[i],fr=fr,un=fr-drift[c],
                    mdd=(cl[i:i+H+1].min()/cl[i]-1)))
    g=pd.DataFrame(rows)
    out={}
    def summ(s):
        s=s.dropna(); return pd.Series(dict(n=len(s),mean=s.mean(),t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan))
    pos=g[g.f>0].copy()
    pos["fb"]=pd.qcut(pos.f,4,labels=False,duplicates="drop")
    out["by_forecast_quartile_unusual"]=pos.groupby("fb").apply(lambda x: pd.concat([summ(x.un),pd.Series(dict(fmin=x.f.min(),fmax=x.f.max(),total=x.fr.mean()))]))
    ip=g[g.inprof]
    ip=ip.assign(scb=pd.cut(ip.sc,[-99,-1,0,0.5,1,1.5,2,99]))
    out["in_profile_by_rawscaled_rise"]=ip.groupby("scb").apply(lambda x: pd.concat([summ(x.un),pd.Series(dict(fpos=(x.f>0).mean(),total=x.fr.mean()))]))
    out["in_vs_out_profile_sc_gt1"]=g[g.sc>1].groupby("inprof").apply(lambda x: summ(x.un))
    out["all_bars_by_sc"]=g.assign(scb=pd.cut(g.sc,[-99,-1,0,1,2,99])).groupby("scb").apply(lambda x: summ(x.un))
    out["pos_by_window"]=pos.groupby("w").apply(lambda x: pd.Series(dict(n=len(x),un=x.un.mean(),tot=x.fr.mean())))
    out["pos_by_coin"]=pos.groupby("coin").apply(lambda x: pd.Series(dict(n=len(x),un=x.un.mean(),tot=x.fr.mean(),drift=drift[x.name])))
    # book daily
    dd=[]
    for c in days:
        for w,df in days[c].items():
            b=bars[c][w].copy(); b["day"]=b["timestamp"].dt.floor("D")
            al=b.groupby("day")["postRebalance_current_allocation"].last()
            d=df.copy(); d["coin"]=c; d["w"]=w; d["al"]=d["day"].map(al)
            dd.append(d)
    D=pd.concat(dd)
    D["al_prev"]=D.groupby(["coin","w"])["al"].shift(1)
    bk=D.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean"),inpos=("al_prev",lambda s:(s.abs()>1e-6).mean())).reset_index().sort_values(["w","day"])
    bk=bk.dropna(subset=["br"])
    out["book_by_window"]=bk.groupby("w").agg(n=("br","size"),mean=("br","mean"),hold=("cr","mean"),inpos=("inpos","mean"))
    v=(1+bk.br).cumprod().values; peak=np.maximum.accumulate(v); ddn=v/peak-1
    bk["dd"]=ddn
    # find 3 deepest troughs episodes
    eps=[]; i=0; n=len(ddn)
    while i<n:
        if ddn[i]<0:
            j=i
            while j<n and ddn[j]<0: j+=1
            k=i+np.argmin(ddn[i:j]); eps.append((ddn[k],i,k,j)); i=j
        else: i+=1
    eps=sorted(eps)[:4]
    er=[]
    for depth,s,k,e in eps:
        seg=bk.iloc[s:k+1]
        er.append(dict(depth=depth,days_to_trough=k-s+1,windows=",".join(sorted(seg.w.unique())),book_sum=seg.br.sum(),coins_mean_ret_sum=seg.cr.sum(),inpos=seg.inpos.mean()))
    out["deepest_falls"]=pd.DataFrame(er)
    # trade outcomes
    tr=[]
    for c in trades:
        for w,t in trades[c].items():
            t=t.copy(); t["coin"]=c; tr.append(t)
    T=pd.concat(tr)
    T["fb"]=pd.qcut(T.entry_forecast,4,labels=False,duplicates="drop")
    out["trades_by_entry_forecast"]=T.groupby("fb").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),gross=("profit_loss_percent","mean"),days=("duration_minutes",lambda s:(s/1440).mean()),fmin=("entry_forecast","min"))
    # positive cases split by mid-path drawdown and by r30
    pos["r30b"]=pd.qcut(pos.r30,3,labels=False)
    out["pos_by_r30_tercile"]=pos.groupby("r30b").apply(lambda x: pd.concat([summ(x.un),pd.Series(dict(r30=x.r30.mean()))]))
    ip0=ip[ip.f<=0]
    out["inprof_f0_vs_fpos"]=pd.DataFrame({"f0":summ(ip0.un),"fpos":summ(pos.un)})
    return out
