def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    fc = 'debug_info.components.low_close_wide_day.post_pipeline_value'
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b['ret1'] = b['close'].shift(-1)/b['close']-1
            b['ret3'] = b['close'].shift(-3)/b['close']-1
            b['tr60'] = b['close']/b['close'].shift(60)-1
            r = b['close'].pct_change()
            v30 = r.rolling(30).std()
            b['agit'] = v30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            b['past5'] = b['close']/b['close'].shift(5)-1
            b['cl'] = (b['close']-b['low'])/(b['high']-b['low']).replace(0,np.nan)
            b['coin'] = coin; b['w'] = w
            b['year'] = pd.to_datetime(b['timestamp']).dt.year
            b['f'] = b[fc] if fc in b else b['forecast']
            rows.append(b[['coin','w','year','f','forecast','postRebalance_current_allocation','ret1','ret3','tr60','agit','past5','cl','timestamp']])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby('coin')['ret1'].mean()
    B['ex1'] = B['ret1'] - B['coin'].map(mu)
    B['trend'] = np.where(B['tr60']>0.10,'rising',np.where(B['tr60']<-0.10,'falling',np.where(B['tr60'].notna(),'choppy',None)))
    B['ag'] = np.where(B['agit'].isna(), None, np.where(B['agit']>0.5,'agitated','calm'))
    B['fq'] = B.groupby('coin')['f'].transform(lambda x: pd.qcut(x.rank(method='first'),5,labels=False))
    out['alloc_by_fq'] = B.groupby('fq').agg(alloc=('postRebalance_current_allocation','mean'), ret1=('ret1','mean'), ex1=('ex1','mean'), n=('ret1','count'))
    def summ(g):
        top = g[g.fq==4]['ret1'].dropna(); rest = g[g.fq<4]['ret1'].dropna()
        t = stats.ttest_ind(top, rest, equal_var=False).statistic if len(top)>5 else np.nan
        return pd.Series({'n':len(g),'alloc':g['postRebalance_current_allocation'].mean(),'ret_all':g['ret1'].mean(),'ret_top':top.mean(),'ret_rest':rest.mean(),'t_top_rest':t,'n_top':len(top),
                          'pnl_proxy':(g['postRebalance_current_allocation']*g['ret1']).mean()})
    out['by_trend'] = B.groupby('trend').apply(summ)
    out['by_ag'] = B.groupby('ag').apply(summ)
    B['prof'] = B['trend'].astype(str)+' '+B['ag'].astype(str)
    out['by_prof'] = B.groupby('prof').apply(summ)
    out['by_year'] = B.groupby('year').apply(summ)
    # book daily
    D=[]
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d=d.copy(); d['coin']=coin; d['w']=w; D.append(d)
    D=pd.concat(D)
    bk = D.groupby(['w','day']).agg(br=('book_return','mean'), cr=('coin_return','mean')).reset_index()
    order = sorted(bk['w'].unique(), key=lambda s:int(s[1:]))
    bk['wo']=bk['w'].map({w:i for i,w in enumerate(order)})
    bk=bk.sort_values(['wo','day']).dropna(subset=['br']).reset_index(drop=True)
    v=(1+bk['br']).cumprod(); h=(1+bk['cr']).cumprod()
    dd=v/v.cummax()-1; bk['dd']=dd
    out['book_maxdd']=float(dd.min()); out['hold_maxdd']=float((h/h.cummax()-1).min())
    out['book_mean_sd']=pd.Series({'book_mean':bk.br.mean(),'book_sd':bk.br.std(),'hold_mean':bk.cr.mean(),'hold_sd':bk.cr.std(),'corr':bk.br.corr(bk.cr)})
    # worst 30-day stretches
    bk['b30']=bk.groupby('w')['br'].transform(lambda x:(1+x).rolling(30).apply(np.prod,raw=True)-1)
    bk['c30']=bk.groupby('w')['cr'].transform(lambda x:(1+x).rolling(30).apply(np.prod,raw=True)-1)
    out['b30_vs_c30']=pd.Series({'corr':bk.b30.corr(bk.c30),'worst_b30':bk.b30.min(),'c30_at_worst':bk.loc[bk.b30.idxmin(),'c30']})
    # book daily by coin-avg trend state
    B['day']=pd.to_datetime(B['timestamp']).dt.floor('D')
    st=B.groupby(['w','day']).agg(tr=('tr60','mean'),al=('postRebalance_current_allocation','mean')).reset_index()
    bk['day']=pd.to_datetime(bk['day']).dt.floor('D') if not np.issubdtype(bk['day'].dtype,np.datetime64) else bk['day']
    m=bk.merge(st,on=['w','day'],how='left')
    m['tb']=pd.cut(m['tr'],[-9,-0.1,0.1,99],labels=['falling','choppy','rising'])
    out['book_by_avg_trend']=m.groupby('tb').agg(n=('br','count'),book=('br','mean'),hold=('cr','mean'),alloc=('al','mean'),book_sd=('br','std'))
    # dd episodes: days in dd< -15%
    out['in_deep_dd']=m.assign(deep=m.dd<-0.15).groupby('deep').agg(n=('br','count'),tr=('tr','mean'),alloc=('al','mean'),book=('br','mean'),hold=('cr','mean'))
    out['by_window_book']=m.groupby('w').agg(book=('br','mean'),hold=('cr','mean'),mindd=('dd','min'),tr=('tr','mean'))
    # past5 interaction
    B['p5q']=B.groupby('coin')['past5'].transform(lambda x: pd.qcut(x.rank(method='first'),3,labels=['down','mid','up']))
    out['by_past5']=B.groupby('p5q').apply(summ)
    return out
