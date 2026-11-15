def explore(data):
    import pandas as pd, numpy as np
    bars=data["bars"]; days=data["days"]
    mu={}
    for c in bars:
        mu[c]=pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean()
    rows=[]; blocks=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True); cl=df["close"].values; n=len(df)
            dist=df["debug_info.components.above_ma.last_history_value"].values
            fc=df["forecast"].values; al=df["postRebalance_current_allocation"].values
            ts=pd.to_datetime(df["timestamp"])
            sma=cl/(1+dist/100.0)
            r=pd.Series(cl).pct_change()
            vol=r.rolling(20).std().values
            above=(dist>0).astype(float)
            # bars since state last changed
            since=np.full(n,np.nan); cnt=0
            for i in range(n):
                if i>0 and not np.isnan(dist[i-1]) and above[i]==above[i-1]: cnt+=1
                else: cnt=0
                since[i]=cnt
            slope=np.full(n,np.nan)
            slope[20:]=sma[20:]/sma[:-20]-1
            mom=np.full(n,np.nan); mom[20:]=cl[20:]/cl[:-20]-1
            h=20
            for i in range(0,n-h,h):
                rows.append(dict(coin=c,w=w,year=ts.iloc[i].year,fc=fc[i],dist=dist[i],al=al[i],since=since[i],
                    slope=slope[i],vol=vol[i],mom=mom[i],ex=cl[i+h]/cl[i]-1-h*mu[c]))
            # block contribution like the plan
            for b in range(0,n,h):
                s=0;k=0
                for i in range(b,min(b+h,n)):
                    if i+h<n:
                        s+=al[i]*(cl[i+h]/cl[i]-1-h*mu[c]);k+=1
                if k>0: blocks.append(dict(coin=c,year=ts.iloc[b].year,v=s,act=(al[b:b+h]!=0).any()))
    d=pd.DataFrame(rows); B=pd.DataFrame(blocks)
    def summ(g):
        return pd.Series(dict(n=len(g),mean=g.ex.mean(),t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))),win=(g.ex>0).mean()))
    def bs(g):
        return pd.Series(dict(n=len(g),mean=g.v.mean(),t=g.v.mean()/(g.v.std()/np.sqrt(len(g))),share_pos=(g.v>0).mean()))
    out={}
    out["blocks_by_coin"]=B.groupby("coin").apply(bs)
    out["blocks_by_year"]=B.groupby("year").apply(bs)
    vb=B.v.sort_values(ascending=False)
    out["blocks_total_and_top10_sum"]=pd.Series(dict(total=B.v.sum(),top10=vb.head(10).sum(),bottom10=vb.tail(10).sum(),n=len(B)))
    pos=d[d.fc>0].copy()
    pos["since_b"]=pd.cut(pos.since,[-1,20,60,150,10000])
    out["pos_by_since"]=pos.groupby("since_b").apply(summ)
    pos["slope_q"]=pd.qcut(pos.slope,3,labels=False)
    out["pos_by_smaslope_t"]=pos.groupby("slope_q").apply(summ)
    pos["vol_q"]=pd.qcut(pos.vol,3,labels=False)
    out["pos_by_vol_t"]=pos.groupby("vol_q").apply(summ)
    pos["mom_q"]=pd.qcut(pos.mom,3,labels=False)
    out["pos_by_mom_t"]=pos.groupby("mom_q").apply(summ)
    allb=d.dropna(subset=["slope"]).copy(); allb["sl_q"]=pd.qcut(allb.slope,5,labels=False)
    out["all_by_smaslope_q"]=allb.groupby("sl_q").apply(summ)
    # book decomposition
    br=[];
    for c in days:
        cr=pd.concat([x["coin_return"].dropna() for x in days[c].values()]).mean()
        for w,x in days[c].items():
            x=x.copy(); x["mu"]=cr; br.append(x)
    D=pd.concat(br)
    out["coin_ret_mean_all"]=D.coin_return.mean()
    return out
