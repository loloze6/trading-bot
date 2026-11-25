def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    fc = 'debug_info.components.low_close_wide_day.post_pipeline_value'
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b['ts'] = pd.to_datetime(b['timestamp'], utc=True).dt.tz_localize(None)
            b['ret1'] = b['close'].shift(-1)/b['close']-1
            b['tr60'] = b['close']/b['close'].shift(60)-1
            b['tr30'] = b['close']/b['close'].shift(30)-1
            r = b['close'].pct_change()
            b['v20'] = r.rolling(20).std()
            b['past3'] = b['close']/b['close'].shift(3)-1
            b['cl'] = (b['close']-b['low'])/(b['high']-b['low']).replace(0,np.nan)
            b['coin'] = coin; b['w'] = w
            b['year'] = b['ts'].dt.year
            b['f'] = b[fc] if fc in b else b['forecast']
            b['al'] = b['postRebalance_current_allocation']
            b['dal'] = b['al'].diff().abs().fillna(b['al'].abs())
            rows.append(b[['coin','w','year','f','al','dal','ret1','tr60','tr30','v20','past3','cl','ts']])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby('coin')['ret1'].mean()
    B['ex1'] = B['ret1'] - B['coin'].map(mu)
    B['fq'] = B.groupby('coin')['f'].transform(lambda x: pd.qcut(x.rank(method='first'),5,labels=False))
    B['trend'] = np.where(B['tr60'].isna(),'na',np.where(B['tr60']>0.10,'rising',np.where(B['tr60']<-0.10,'falling','choppy')))
    B['tr30b'] = np.where(B['tr30'].isna(),'na',np.where(B['tr30']>0.07,'up30',np.where(B['tr30']<-0.07,'down30','flat30')))
    vmed = B.groupby('coin')['v20'].transform('median')
    B['ag'] = np.where(B['v20'].isna(),'na',np.where(B['v20']>vmed,'agitated','calm'))
    out['alloc_by_fq'] = B.groupby('fq').agg(alloc=('al','mean'), f=('f','mean'), ret1=('ret1','mean'), ex1=('ex1','mean'), n=('ret1','count'))
    def summ(g):
        top = g[g.fq==4]['ret1'].dropna(); rest = g[g.fq<4]['ret1'].dropna()
        t = stats.ttest_ind(top, rest, equal_var=False).statistic if len(top)>5 else np.nan
        return pd.Series({'n':len(g),'alloc':g['al'].mean(),'ret_all':g['ret1'].mean(),'ret_top':top.mean(),'ret_rest':rest.mean(),'top_minus_rest_t':t,'n_top':len(top),'pnl':(g['al']*g['ret1']).mean()})
    out['by_trend60'] = B.groupby('trend').apply(summ)
    out['by_trend30'] = B.groupby('tr30b').apply(summ)
    out['by_ag'] = B.groupby('ag').apply(summ)
    out['by_year'] = B.groupby('year').apply(summ)
    B['p3q']=B.groupby('coin')['past3'].transform(lambda x: pd.qcut(x.rank(method='first'),3,labels=['down','mid','up']))
    out['by_past3'] = B.groupby('p3q').apply(summ)
    # proxy books
    B['day']=B['ts'].dt.floor('D')
    cost=0.00095
    def book(mask_alloc, name):
        a = mask_alloc
        pnl = a*B['ret1'] - cost*(a.diff().abs().fillna(0))
        tmp = B[['w','day']].assign(p=pnl.values).dropna()
        d = tmp.groupby(['w','day'])['p'].mean().reset_index()
        d['wo']=d['w'].str[1:].astype(int); d=d.sort_values(['wo','day'])
        v=(1+d['p']).cumprod(); dd=(v/v.cummax()-1).min()
        yrs=len(d)/365; yr=v.iloc[-1]**(1/yrs)-1
        return pd.Series({'mean':d.p.mean(),'sd':d.p.std(),'sharpe':d.p.mean()/d.p.std()*np.sqrt(365),'yearly':yr,'maxdd':dd,'calmar':yr/abs(dd),'inpos':(a.abs()>0).mean()})
    hold_al = B.groupby('coin')['al'].transform('mean')
    res = {}
    res['actual'] = book(B['al'], 'a')
    res['hold_const'] = book(pd.Series(1.0,index=B.index),'h')
    res['top_fifth_only'] = book(B['al'].where(B.fq==4,0)*1.0,'t')
    res['top2_fifths'] = book(B['al'].where(B.fq>=3,0)*1.0,'t2')
    res['excl_falling60'] = book(B['al'].where(B.trend!='falling',0),'nf')
    res['excl_down30'] = book(B['al'].where(B.tr30b!='down30',0),'nd')
    res['excl_agitated'] = book(B['al'].where(B.ag!='agitated',0),'na')
    res['top_fifth_excl_down30'] = book(B['al'].where((B.fq==4)&(B.tr30b!='down30'),0),'x')
    res['forecast_minus_mean'] = book((B['al']*(B['f']-B.groupby('coin')['f'].transform('median'))/B.groupby('coin')['f'].transform('std')).clip(-2,2),'fm')
    out['proxy_books'] = pd.DataFrame(res).T
    # book drawdowns from days table
    D=[]
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d=d.copy(); d['coin']=coin; d['w']=w; D.append(d)
    D=pd.concat(D)
    D['day']=pd.to_datetime(D['day'],utc=True).dt.tz_localize(None).dt.floor('D')
    bk=D.groupby(['w','day']).agg(br=('book_return','mean'),cr=('coin_return','mean')).reset_index().dropna()
    bk['wo']=bk['w'].str[1:].astype(int); bk=bk.sort_values(['wo','day']).reset_index(drop=True)
    v=(1+bk.br).cumprod(); bk['dd']=v/v.cummax()-1
    h=(1+bk.cr).cumprod()
    out['dd'] = pd.Series({'book_maxdd':bk.dd.min(),'hold_maxdd':(h/h.cummax()-1).min(),'corr_book_hold':bk.br.corr(bk.cr),'beta':np.polyfit(bk.cr,bk.br,1)[0]})
    st=B.groupby(['w','day']).agg(tr30=('tr30','mean'),al=('al','mean'),fq=('fq','mean')).reset_index()
    m=bk.merge(st,on=['w','day'],how='left')
    m['deep']=m.dd<-0.15
    out['deep_dd_days']=m.groupby('deep').agg(n=('br','count'),tr30=('tr30','mean'),alloc=('al','mean'),fq=('fq','mean'),book=('br','mean'),hold=('cr','mean'))
    out['by_window']=m.groupby('wo').agg(book=('br','mean'),hold=('cr','mean'),mindd=('dd','min'),alloc=('al','mean'))
    return out
