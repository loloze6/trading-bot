def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    F='forecast'; RAW='debug_info.components.above_ma.last_history_value'; AL='postRebalance_current_allocation'
    bars=data['bars']
    mu={}
    for c in bars:
        mu[c]=pd.concat([df['close'].pct_change().dropna() for df in bars[c].values()]).mean()
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            cl=df['close'].values; fc=df[F].values; al=df[AL].values
            raw=df[RAW].values if RAW in df else np.full(len(df),np.nan)
            n=len(df)
            above=(raw>0)
            age=np.full(n,np.nan); cnt=np.nan
            for i in range(n):
                if np.isnan(raw[i]): cnt=np.nan
                elif above[i]:
                    cnt = (cnt+1) if (i>0 and not np.isnan(cnt) and above[i-1]) else 0
                else: cnt=np.nan
                age[i]=cnt
            # implied sma and its 20-bar slope
            sma=cl/(1+raw) if np.nanmax(np.abs(raw))<5 else cl/(1+raw/100)
            lr=np.log(cl); 
            vol=pd.Series(lr).diff().rolling(30).std().values
            mom=np.full(n,np.nan); mom[60:]=cl[60:]/cl[:-60]-1
            for h in (20,60):
                for i in range(0,n-h,h):
                    r=cl[i+h]/cl[i]-1
                    sl=sma[i]/sma[i-20]-1 if i>=20 else np.nan
                    rows.append(dict(coin=c,h=h,fc=fc[i],raw=raw[i],age=age[i],ex=r-h*mu[c],al=al[i],sl=sl,vol=vol[i],mom=mom[i]))
    d=pd.DataFrame(rows)
    def summ(g):
        e=g.ex.dropna()
        tr=stats.trim_mean(e,0.05) if len(e)>5 else np.nan
        return pd.Series(dict(n=len(e),mean_ex=e.mean(),trim5=tr,med=e.median(),t=e.mean()/(e.std()/np.sqrt(len(e))) if len(e)>2 else np.nan,beat=(e>0).mean()))
    out={}
    out['raw_scale']=pd.Series(dict(rawmax=d.raw.max(),rawmed=d.raw.median()))
    on=d[d.fc>0].copy()
    on['ageb']=pd.cut(on.age,[-1,20,60,150,10000],labels=['<=20','21-60','61-150','>150'])
    out['age_h']=on.groupby(['h','ageb']).apply(summ)
    for h in (20,):
        x=d[d.h==h].copy()
        x['slb']=pd.cut(x.sl,[-10,0,10],labels=['sma_down','sma_up'])
        x['on']=x.fc>0
        out['slope_on_h20']=x.groupby(['slb','on']).apply(summ)
        x['vt']=pd.qcut(x.vol,3,labels=['lowvol','midvol','hivol'])
        out['vol_on_h20']=x.groupby(['vt','on']).apply(summ)
        o=x[x.on]
        out['skew_on_h20']=pd.Series(dict(skew=stats.skew(o.ex),top10share_of_sum=o.ex.nlargest(10).sum()/o.ex.sum(),sum=o.ex.sum()))
        out['diff_on_minus_off']=pd.Series(dict(diff=x[x.on].ex.mean()-x[~x.on].ex.mean(),t=stats.ttest_ind(x[x.on].ex,x[~x.on].ex,equal_var=False).statistic))
        # raw distance continuous corr with ex, all bars incl below
        cc=x.dropna(subset=['raw'])
        out['spearman_raw_ex_h20_allbars']=pd.Series(dict(rho=stats.spearmanr(cc.raw,cc.ex).correlation,p=stats.spearmanr(cc.raw,cc.ex).pvalue,n=len(cc)))
        x['rq']=pd.qcut(x.raw,5,labels=['d1','d2','d3','d4','d5'])
        out['raw_quint_allbars_h20']=x.groupby('rq').apply(summ)
        x['mq']=pd.qcut(x.mom,3,labels=['mom_lo','mom_mid','mom_hi'])
        out['mom_on_h20']=x.groupby(['mq','on']).apply(summ)
    return out
