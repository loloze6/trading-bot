def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    col='debug_info.components.grind_residual.last_history_value'
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b['close'].values; n=len(c)
            g=b[col].values if col in b else np.full(n,np.nan)
            yr=pd.to_datetime(b['timestamp']).dt.year.values
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            for t in range(0,n,72):
                if t<72: past=np.nan
                else: past=c[t]/c[t-72]-1
                row={'coin':coin,'w':int(w[1:]),'yr':yr[t],'g':g[t],'past':past}
                for h in (24,72,144,240):
                    row['f%d'%h]=c[t+h]/c[t]-1 if t+h<n else np.nan
                rows.append(row)
    d=pd.DataFrame(rows)
    s=d[(d.g>0)&d.f72.notna()].copy()
    s['med']=s.groupby('coin').g.transform('median')
    s['grind']=s.g>s.med
    def wt(x,col='f72'):
        a=x[x.grind][col].dropna(); b=x[~x.grind][col].dropna()
        t=stats.ttest_ind(a,b,equal_var=False).statistic
        return pd.Series({'diff':a.mean()-b.mean(),'t':t,'nA':len(a),'nB':len(b),'mA':a.mean(),'mB':b.mean()})
    out={}
    out['all_check']=wt(s)
    out['by_coin']=s.groupby('coin').apply(wt)
    out['by_year']=s.groupby('yr').apply(wt)
    out['by_horizon']=pd.DataFrame({h:wt(s,'f%d'%h) for h in (24,72,144,240)})
    s['gq']=s.groupby('coin').g.transform(lambda x: pd.qcut(x,5,labels=False,duplicates='drop'))
    out['quintile_f72']=s.groupby('gq').f72.agg(['mean','std','count'])
    out['quintile_past']=s.groupby('gq').past.agg(['mean','median'])
    s['pq']=s.groupby('coin').past.transform(lambda x: pd.qcut(x,3,labels=False,duplicates='drop'))
    out['by_pastsize_tercile']=s.groupby('pq').apply(wt)
    out['spearman_g_f72']=stats.spearmanr(s.g,s.f72).correlation
    out['spearman_g_past']=stats.spearmanr(s.g,s.past,nan_policy='omit').correlation
    # residual on past size
    ss=s.dropna(subset=['past'])
    X=np.c_[np.ones(len(ss)),ss.past,ss.g]
    beta,res,_,_=np.linalg.lstsq(X,ss.f72.values,rcond=None)
    e=ss.f72.values-X@beta; s2=e@e/(len(ss)-3); cov=s2*np.linalg.inv(X.T@X)
    out['ols_f72_on_past_g']=pd.Series({'b_past':beta[1],'t_past':beta[1]/np.sqrt(cov[1,1]),'b_g':beta[2],'t_g':beta[2]/np.sqrt(cov[2,2]),'n':len(ss)})
    # falls: down moves (g==0) forward
    dn=d[(d.g==0)&d.f72.notna()]
    out['notrisen_f72']=pd.Series({'mean':dn.f72.mean(),'n':len(dn),'risen_mean':s.f72.mean()})
    return out
